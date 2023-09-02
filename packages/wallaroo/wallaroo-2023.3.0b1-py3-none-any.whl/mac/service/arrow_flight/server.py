"""This module features the ArrowFlightServer class, that
implements a flight.FlightServerBase that runs inferences
on an Inference object."""

import logging
import threading
from typing import List, Tuple

import numpy.typing as npt
import pyarrow as pa
import pyarrow.flight as flight

from mac.config.service import ServerConfig
from mac.exceptions import ArrowRecordBatchConversionError
from mac.inference import Inference
from mac.types import InferenceData
from mac.utils.helpers import (
    convert_multi_dim_chunked_array_to_numpy_array,
    convert_numpy_array_to_nested_list_array,
    get_shape_of_nested_pa_list_scalar,
    is_numpy_array_multi_dim,
    log_error,
    pa_type_is_fixed_shape_tensor,
    pa_type_is_list,
)

logger = logging.getLogger(__name__)


class ArrowFlightServer(flight.FlightServerBase):
    """This class implements the Arrow Flight server, that can be used to
    serve an Inference via the Arrow Flight RPC protocol.

    Attributes:
    - inference: An Inference object to serve.
    - server_config: A ServerConfig object.
    - lock: A threading.Lock object.
    """

    def __init__(self, inference: Inference, server_config: ServerConfig):
        self._inference = inference
        self._server_config = server_config
        self._lock = threading.Lock()
        super().__init__(location=self.location)

    @property
    def location(self):
        """This property returns the location of the server."""
        return f"grpc://{self._server_config.host}:{self._server_config.port}"

    def do_exchange(
        self,
        context: flight.ServerCallContext,
        descriptor: flight.FlightDescriptor,
        reader: flight.FlightStreamReader,
        writer: flight.FlightStreamWriter,
    ):
        """This method implements the do_exchange method of the FlightServerBase
        class.

        :param context: A ServerCallContext object.
        :param descriptor: A FlightDescriptor object.
        :param reader: A FlightStreamReader object.
        :param writer: A FlightStreamWriter object.
        """
        is_first_batch = True
        while True:
            logger.info("Processing data...")
            (
                writer,
                reader,
                is_first_batch,
            ) = self._run_inference_and_write_to_stream(
                writer, reader, is_first_batch
            )
            logger.info("Output data ready to be consumed.")

    def _run_inference_and_write_to_stream(
        self,
        writer: flight.FlightStreamWriter,
        reader: flight.FlightStreamReader,
        is_first_batch: bool,
    ) -> Tuple[flight.FlightStreamWriter, flight.FlightStreamReader, bool]:
        logger.debug("Starting batch processing...")
        for batch in reader.read_chunk():
            if batch is None:
                break
            writer, is_first_batch = self._process_batch(  # type: ignore[no-redef]
                batch, writer, is_first_batch
            )
        logger.debug("Batch processing finished.")

        writer.close()

        return (writer, reader, is_first_batch)

    def _process_batch(
        self,
        batch: pa.RecordBatch,
        writer: flight.MetadataRecordBatchWriter,
        is_first_batch: bool,
    ) -> Tuple[flight.FlightStreamWriter, bool]:
        result = self._run_inference_for_batch(batch)
        return self._write_result(writer, result, is_first_batch)  # type: ignore

    def _run_inference_for_batch(
        self, batch: pa.RecordBatch
    ) -> List[pa.RecordBatch]:
        logger.info("Converting pa.RecordBatch to InferenceData...")
        inference_data = self._convert_record_batch_to_inference_data(batch)

        logger.info("Parsing InferenceData to Inference...")
        self._lock.acquire()
        inference_data = self._inference.predict(  # type: ignore
            input_data=inference_data
        )
        self._lock.release()

        logger.info("Converting InferenceData to pa.RecordBatch...")
        return self._convert_inference_data_to_table_batches(inference_data)

    @log_error(
        ArrowRecordBatchConversionError,
        "Failed to convert pa.RecordBatch to InferenceData.",
    )
    def _convert_record_batch_to_inference_data(
        self,
        batch: pa.RecordBatch,
    ) -> InferenceData:
        table = pa.Table.from_batches([batch])
        return {
            column_name: self._convert_column_to_numpy_array(
                column, column_type
            )
            for column, column_name, column_type in zip(
                table, table.column_names, table.schema.types
            )
        }

    def _convert_column_to_numpy_array(
        self,
        column: pa.ChunkedArray,
        column_type: pa.DataType,
    ) -> npt.NDArray:
        if pa_type_is_fixed_shape_tensor(column_type):
            return convert_multi_dim_chunked_array_to_numpy_array(
                array=column,
                shape=tuple(column_type.shape),
            )
        elif pa_type_is_list(column_type):
            return convert_multi_dim_chunked_array_to_numpy_array(
                array=column,
                shape=get_shape_of_nested_pa_list_scalar(column[0]),
            )
        else:
            return column.to_numpy().astype(column_type.to_pandas_dtype())

    @log_error(
        ArrowRecordBatchConversionError,
        "Failed to convert InferenceData to pa.RecordBatch.",
    )
    def _convert_inference_data_to_table_batches(
        self,
        inference_data: InferenceData,
    ) -> List[pa.RecordBatch]:
        data: List[pa.Array] = []
        data_info: List[Tuple[str, pa.DataType]] = []

        for key, value in inference_data.items():
            if is_numpy_array_multi_dim(value):
                (
                    tensor_type,
                    tensor_array,
                ) = convert_numpy_array_to_nested_list_array(value)
                data.append(tensor_array)
                data_info.append((key, tensor_type))
                del tensor_array
                continue
            data.append(pa.array(value))
            data_info.append((key, pa.from_numpy_dtype(value.dtype)))

        return pa.Table.from_arrays(
            data, schema=pa.schema(data_info)
        ).to_batches()

    def _write_result(
        self,
        writer: flight.FlightStreamWriter,
        result: List[pa.RecordBatch],
        is_first_batch: bool,
    ) -> Tuple[flight.FlightStreamWriter, bool]:
        if is_first_batch is True:
            is_first_batch = False
            logger.debug("Writing schema to stream...")
            writer.begin(result[0].schema)

        for batch in result:
            writer.write_batch(batch)

        return (writer, is_first_batch)

"""This module defines custom types for the Model Auto Conversion (MAC) package.

Currently, the following types are available:
- InferenceData: This type is used to define the data that is used for inference.
- SupportedFrameworks: This type is used to define the supported frameworks.
- SupportedServices: This type is used to define the supported services.
"""

from enum import Enum
from typing import Dict

import numpy.typing as npt
from typing_extensions import TypeAlias

# Define the type for inference data.
InferenceData: TypeAlias = Dict[str, npt.NDArray]


class SupportedFrameworks(str, Enum):
    """This class defines an Enum for supported frameworks. The frameworks are used
    to load models. The frameworks can be keras, sklearn, etc.
    """

    KERAS = "keras"
    SKLEARN = "sklearn"
    PYTORCH = "pytorch"
    XGBOOST = "xgboost"
    HUGGING_FACE = "hugging-face"
    CUSTOM = "custom"


class SupportedServices(str, Enum):
    """This class defines an Enum for supported services such as MLflow, etc.
    These services are used to convert models and run inference on them.
    """

    MLFLOW = "mlflow"
    ARROW_FLIGHT = "arrow-flight"

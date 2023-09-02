from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="PipelinePublishHelm")


@attr.s(auto_attribs=True)
class PipelinePublishHelm:
    """ 
        Attributes:
            reference (str):
            chart (Union[Unset, None, str]):
            version (Union[Unset, None, str]):
     """

    reference: str
    chart: Union[Unset, None, str] = UNSET
    version: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        reference = self.reference
        chart = self.chart
        version = self.version

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "reference": reference,
        })
        if chart is not UNSET:
            field_dict["chart"] = chart
        if version is not UNSET:
            field_dict["version"] = version

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        reference = d.pop("reference")

        chart = d.pop("chart", UNSET)

        version = d.pop("version", UNSET)

        pipeline_publish_helm = cls(
            reference=reference,
            chart=chart,
            version=version,
        )

        pipeline_publish_helm.additional_properties = d
        return pipeline_publish_helm

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties

from typing import Any, Dict, List, Type, TypeVar

import attr

T = TypeVar("T", bound="AssaysRunInteractiveBaselineJsonBodyBaselineType0CalculatedType1FixedWindow")


@attr.s(auto_attribs=True)
class AssaysRunInteractiveBaselineJsonBodyBaselineType0CalculatedType1FixedWindow:
    """ 
        Attributes:
            pipeline (str):
            model (str):
            start_at (str):
            end_at (str):
     """

    pipeline: str
    model: str
    start_at: str
    end_at: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)


    def to_dict(self) -> Dict[str, Any]:
        pipeline = self.pipeline
        model = self.model
        start_at = self.start_at
        end_at = self.end_at

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "pipeline": pipeline,
            "model": model,
            "start_at": start_at,
            "end_at": end_at,
        })

        return field_dict



    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        pipeline = d.pop("pipeline")

        model = d.pop("model")

        start_at = d.pop("start_at")

        end_at = d.pop("end_at")

        assays_run_interactive_baseline_json_body_baseline_type_0_calculated_type_1_fixed_window = cls(
            pipeline=pipeline,
            model=model,
            start_at=start_at,
            end_at=end_at,
        )

        assays_run_interactive_baseline_json_body_baseline_type_0_calculated_type_1_fixed_window.additional_properties = d
        return assays_run_interactive_baseline_json_body_baseline_type_0_calculated_type_1_fixed_window

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

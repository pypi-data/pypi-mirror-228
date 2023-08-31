from typing import Any, Dict, List, Type, TypeVar

import attr

from ..models.get_flow_by_path_with_draft_response_200_draft_value_modules_item_sleep_type_1_type import (
    GetFlowByPathWithDraftResponse200DraftValueModulesItemSleepType1Type,
)

T = TypeVar("T", bound="GetFlowByPathWithDraftResponse200DraftValueModulesItemSleepType1")


@attr.s(auto_attribs=True)
class GetFlowByPathWithDraftResponse200DraftValueModulesItemSleepType1:
    """
    Attributes:
        expr (str):
        type (GetFlowByPathWithDraftResponse200DraftValueModulesItemSleepType1Type):
    """

    expr: str
    type: GetFlowByPathWithDraftResponse200DraftValueModulesItemSleepType1Type
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        expr = self.expr
        type = self.type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "expr": expr,
                "type": type,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        expr = d.pop("expr")

        type = GetFlowByPathWithDraftResponse200DraftValueModulesItemSleepType1Type(d.pop("type"))

        get_flow_by_path_with_draft_response_200_draft_value_modules_item_sleep_type_1 = cls(
            expr=expr,
            type=type,
        )

        get_flow_by_path_with_draft_response_200_draft_value_modules_item_sleep_type_1.additional_properties = d
        return get_flow_by_path_with_draft_response_200_draft_value_modules_item_sleep_type_1

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

from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.create_app_json_body_policy import CreateAppJsonBodyPolicy
from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateAppJsonBody")


@attr.s(auto_attribs=True)
class CreateAppJsonBody:
    """
    Attributes:
        path (str):
        value (Any):
        summary (str):
        policy (CreateAppJsonBodyPolicy):
        draft_only (Union[Unset, bool]):
    """

    path: str
    value: Any
    summary: str
    policy: CreateAppJsonBodyPolicy
    draft_only: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        path = self.path
        value = self.value
        summary = self.summary
        policy = self.policy.to_dict()

        draft_only = self.draft_only

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "path": path,
                "value": value,
                "summary": summary,
                "policy": policy,
            }
        )
        if draft_only is not UNSET:
            field_dict["draft_only"] = draft_only

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        path = d.pop("path")

        value = d.pop("value")

        summary = d.pop("summary")

        policy = CreateAppJsonBodyPolicy.from_dict(d.pop("policy"))

        draft_only = d.pop("draft_only", UNSET)

        create_app_json_body = cls(
            path=path,
            value=value,
            summary=summary,
            policy=policy,
            draft_only=draft_only,
        )

        create_app_json_body.additional_properties = d
        return create_app_json_body

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

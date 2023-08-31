import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.get_input_history_response_200_item_args import GetInputHistoryResponse200ItemArgs
from ..types import UNSET, Unset

T = TypeVar("T", bound="GetInputHistoryResponse200Item")


@attr.s(auto_attribs=True)
class GetInputHistoryResponse200Item:
    """
    Attributes:
        id (str):
        name (str):
        args (GetInputHistoryResponse200ItemArgs):
        created_by (str):
        created_at (datetime.datetime):
        is_public (bool):
        success (Union[Unset, bool]):
    """

    id: str
    name: str
    args: GetInputHistoryResponse200ItemArgs
    created_by: str
    created_at: datetime.datetime
    is_public: bool
    success: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        args = self.args.to_dict()

        created_by = self.created_by
        created_at = self.created_at.isoformat()

        is_public = self.is_public
        success = self.success

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "args": args,
                "created_by": created_by,
                "created_at": created_at,
                "is_public": is_public,
            }
        )
        if success is not UNSET:
            field_dict["success"] = success

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        name = d.pop("name")

        args = GetInputHistoryResponse200ItemArgs.from_dict(d.pop("args"))

        created_by = d.pop("created_by")

        created_at = isoparse(d.pop("created_at"))

        is_public = d.pop("is_public")

        success = d.pop("success", UNSET)

        get_input_history_response_200_item = cls(
            id=id,
            name=name,
            args=args,
            created_by=created_by,
            created_at=created_at,
            is_public=is_public,
            success=success,
        )

        get_input_history_response_200_item.additional_properties = d
        return get_input_history_response_200_item

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

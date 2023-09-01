from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.flow_module_value_2_type_4_branches_item_modules_item_suspend_resume_form import (
    FlowModuleValue2Type4BranchesItemModulesItemSuspendResumeForm,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="FlowModuleValue2Type4BranchesItemModulesItemSuspend")


@attr.s(auto_attribs=True)
class FlowModuleValue2Type4BranchesItemModulesItemSuspend:
    """
    Attributes:
        required_events (Union[Unset, int]):
        timeout (Union[Unset, int]):
        resume_form (Union[Unset, FlowModuleValue2Type4BranchesItemModulesItemSuspendResumeForm]):
    """

    required_events: Union[Unset, int] = UNSET
    timeout: Union[Unset, int] = UNSET
    resume_form: Union[Unset, FlowModuleValue2Type4BranchesItemModulesItemSuspendResumeForm] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        required_events = self.required_events
        timeout = self.timeout
        resume_form: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.resume_form, Unset):
            resume_form = self.resume_form.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if required_events is not UNSET:
            field_dict["required_events"] = required_events
        if timeout is not UNSET:
            field_dict["timeout"] = timeout
        if resume_form is not UNSET:
            field_dict["resume_form"] = resume_form

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        required_events = d.pop("required_events", UNSET)

        timeout = d.pop("timeout", UNSET)

        _resume_form = d.pop("resume_form", UNSET)
        resume_form: Union[Unset, FlowModuleValue2Type4BranchesItemModulesItemSuspendResumeForm]
        if isinstance(_resume_form, Unset):
            resume_form = UNSET
        else:
            resume_form = FlowModuleValue2Type4BranchesItemModulesItemSuspendResumeForm.from_dict(_resume_form)

        flow_module_value_2_type_4_branches_item_modules_item_suspend = cls(
            required_events=required_events,
            timeout=timeout,
            resume_form=resume_form,
        )

        flow_module_value_2_type_4_branches_item_modules_item_suspend.additional_properties = d
        return flow_module_value_2_type_4_branches_item_modules_item_suspend

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

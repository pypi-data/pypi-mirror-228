from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.flow_module_value_2_type_3_modules_item_mock import FlowModuleValue2Type3ModulesItemMock
from ..models.flow_module_value_2_type_3_modules_item_retry import FlowModuleValue2Type3ModulesItemRetry
from ..models.flow_module_value_2_type_3_modules_item_sleep_type_0 import FlowModuleValue2Type3ModulesItemSleepType0
from ..models.flow_module_value_2_type_3_modules_item_sleep_type_1 import FlowModuleValue2Type3ModulesItemSleepType1
from ..models.flow_module_value_2_type_3_modules_item_stop_after_if import FlowModuleValue2Type3ModulesItemStopAfterIf
from ..models.flow_module_value_2_type_3_modules_item_suspend import FlowModuleValue2Type3ModulesItemSuspend
from ..types import UNSET, Unset

T = TypeVar("T", bound="FlowModuleValue2Type3ModulesItem")


@attr.s(auto_attribs=True)
class FlowModuleValue2Type3ModulesItem:
    """
    Attributes:
        id (str):
        value (Any):
        stop_after_if (Union[Unset, FlowModuleValue2Type3ModulesItemStopAfterIf]):
        sleep (Union[FlowModuleValue2Type3ModulesItemSleepType0, FlowModuleValue2Type3ModulesItemSleepType1, Unset]):
        cache_ttl (Union[Unset, float]):
        timeout (Union[Unset, float]):
        summary (Union[Unset, str]):
        mock (Union[Unset, FlowModuleValue2Type3ModulesItemMock]):
        suspend (Union[Unset, FlowModuleValue2Type3ModulesItemSuspend]):
        retry (Union[Unset, FlowModuleValue2Type3ModulesItemRetry]):
    """

    id: str
    value: Any
    stop_after_if: Union[Unset, FlowModuleValue2Type3ModulesItemStopAfterIf] = UNSET
    sleep: Union[FlowModuleValue2Type3ModulesItemSleepType0, FlowModuleValue2Type3ModulesItemSleepType1, Unset] = UNSET
    cache_ttl: Union[Unset, float] = UNSET
    timeout: Union[Unset, float] = UNSET
    summary: Union[Unset, str] = UNSET
    mock: Union[Unset, FlowModuleValue2Type3ModulesItemMock] = UNSET
    suspend: Union[Unset, FlowModuleValue2Type3ModulesItemSuspend] = UNSET
    retry: Union[Unset, FlowModuleValue2Type3ModulesItemRetry] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        value = self.value
        stop_after_if: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.stop_after_if, Unset):
            stop_after_if = self.stop_after_if.to_dict()

        sleep: Union[Dict[str, Any], Unset]
        if isinstance(self.sleep, Unset):
            sleep = UNSET

        elif isinstance(self.sleep, FlowModuleValue2Type3ModulesItemSleepType0):
            sleep = UNSET
            if not isinstance(self.sleep, Unset):
                sleep = self.sleep.to_dict()

        else:
            sleep = UNSET
            if not isinstance(self.sleep, Unset):
                sleep = self.sleep.to_dict()

        cache_ttl = self.cache_ttl
        timeout = self.timeout
        summary = self.summary
        mock: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.mock, Unset):
            mock = self.mock.to_dict()

        suspend: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.suspend, Unset):
            suspend = self.suspend.to_dict()

        retry: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.retry, Unset):
            retry = self.retry.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "value": value,
            }
        )
        if stop_after_if is not UNSET:
            field_dict["stop_after_if"] = stop_after_if
        if sleep is not UNSET:
            field_dict["sleep"] = sleep
        if cache_ttl is not UNSET:
            field_dict["cache_ttl"] = cache_ttl
        if timeout is not UNSET:
            field_dict["timeout"] = timeout
        if summary is not UNSET:
            field_dict["summary"] = summary
        if mock is not UNSET:
            field_dict["mock"] = mock
        if suspend is not UNSET:
            field_dict["suspend"] = suspend
        if retry is not UNSET:
            field_dict["retry"] = retry

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id")

        value = d.pop("value")

        _stop_after_if = d.pop("stop_after_if", UNSET)
        stop_after_if: Union[Unset, FlowModuleValue2Type3ModulesItemStopAfterIf]
        if isinstance(_stop_after_if, Unset):
            stop_after_if = UNSET
        else:
            stop_after_if = FlowModuleValue2Type3ModulesItemStopAfterIf.from_dict(_stop_after_if)

        def _parse_sleep(
            data: object,
        ) -> Union[FlowModuleValue2Type3ModulesItemSleepType0, FlowModuleValue2Type3ModulesItemSleepType1, Unset]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                _sleep_type_0 = data
                sleep_type_0: Union[Unset, FlowModuleValue2Type3ModulesItemSleepType0]
                if isinstance(_sleep_type_0, Unset):
                    sleep_type_0 = UNSET
                else:
                    sleep_type_0 = FlowModuleValue2Type3ModulesItemSleepType0.from_dict(_sleep_type_0)

                return sleep_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            _sleep_type_1 = data
            sleep_type_1: Union[Unset, FlowModuleValue2Type3ModulesItemSleepType1]
            if isinstance(_sleep_type_1, Unset):
                sleep_type_1 = UNSET
            else:
                sleep_type_1 = FlowModuleValue2Type3ModulesItemSleepType1.from_dict(_sleep_type_1)

            return sleep_type_1

        sleep = _parse_sleep(d.pop("sleep", UNSET))

        cache_ttl = d.pop("cache_ttl", UNSET)

        timeout = d.pop("timeout", UNSET)

        summary = d.pop("summary", UNSET)

        _mock = d.pop("mock", UNSET)
        mock: Union[Unset, FlowModuleValue2Type3ModulesItemMock]
        if isinstance(_mock, Unset):
            mock = UNSET
        else:
            mock = FlowModuleValue2Type3ModulesItemMock.from_dict(_mock)

        _suspend = d.pop("suspend", UNSET)
        suspend: Union[Unset, FlowModuleValue2Type3ModulesItemSuspend]
        if isinstance(_suspend, Unset):
            suspend = UNSET
        else:
            suspend = FlowModuleValue2Type3ModulesItemSuspend.from_dict(_suspend)

        _retry = d.pop("retry", UNSET)
        retry: Union[Unset, FlowModuleValue2Type3ModulesItemRetry]
        if isinstance(_retry, Unset):
            retry = UNSET
        else:
            retry = FlowModuleValue2Type3ModulesItemRetry.from_dict(_retry)

        flow_module_value_2_type_3_modules_item = cls(
            id=id,
            value=value,
            stop_after_if=stop_after_if,
            sleep=sleep,
            cache_ttl=cache_ttl,
            timeout=timeout,
            summary=summary,
            mock=mock,
            suspend=suspend,
            retry=retry,
        )

        flow_module_value_2_type_3_modules_item.additional_properties = d
        return flow_module_value_2_type_3_modules_item

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

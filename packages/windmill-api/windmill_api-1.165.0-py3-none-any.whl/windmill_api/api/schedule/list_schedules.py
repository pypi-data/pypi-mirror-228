from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import Client
from ...models.list_schedules_response_200_item import ListSchedulesResponse200Item
from ...types import UNSET, Response, Unset


def _get_kwargs(
    workspace: str,
    *,
    client: Client,
    page: Union[Unset, None, int] = UNSET,
    per_page: Union[Unset, None, int] = UNSET,
    path: Union[Unset, None, str] = UNSET,
    is_flow: Union[Unset, None, bool] = UNSET,
) -> Dict[str, Any]:
    url = "{}/w/{workspace}/schedules/list".format(client.base_url, workspace=workspace)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["page"] = page

    params["per_page"] = per_page

    params["path"] = path

    params["is_flow"] = is_flow

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[List[ListSchedulesResponse200Item]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ListSchedulesResponse200Item.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[List[ListSchedulesResponse200Item]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    workspace: str,
    *,
    client: Client,
    page: Union[Unset, None, int] = UNSET,
    per_page: Union[Unset, None, int] = UNSET,
    path: Union[Unset, None, str] = UNSET,
    is_flow: Union[Unset, None, bool] = UNSET,
) -> Response[List[ListSchedulesResponse200Item]]:
    """list schedules

    Args:
        workspace (str):
        page (Union[Unset, None, int]):
        per_page (Union[Unset, None, int]):
        path (Union[Unset, None, str]):
        is_flow (Union[Unset, None, bool]):

    Returns:
        Response[List[ListSchedulesResponse200Item]]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        client=client,
        page=page,
        per_page=per_page,
        path=path,
        is_flow=is_flow,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    workspace: str,
    *,
    client: Client,
    page: Union[Unset, None, int] = UNSET,
    per_page: Union[Unset, None, int] = UNSET,
    path: Union[Unset, None, str] = UNSET,
    is_flow: Union[Unset, None, bool] = UNSET,
) -> Optional[List[ListSchedulesResponse200Item]]:
    """list schedules

    Args:
        workspace (str):
        page (Union[Unset, None, int]):
        per_page (Union[Unset, None, int]):
        path (Union[Unset, None, str]):
        is_flow (Union[Unset, None, bool]):

    Returns:
        Response[List[ListSchedulesResponse200Item]]
    """

    return sync_detailed(
        workspace=workspace,
        client=client,
        page=page,
        per_page=per_page,
        path=path,
        is_flow=is_flow,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    *,
    client: Client,
    page: Union[Unset, None, int] = UNSET,
    per_page: Union[Unset, None, int] = UNSET,
    path: Union[Unset, None, str] = UNSET,
    is_flow: Union[Unset, None, bool] = UNSET,
) -> Response[List[ListSchedulesResponse200Item]]:
    """list schedules

    Args:
        workspace (str):
        page (Union[Unset, None, int]):
        per_page (Union[Unset, None, int]):
        path (Union[Unset, None, str]):
        is_flow (Union[Unset, None, bool]):

    Returns:
        Response[List[ListSchedulesResponse200Item]]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        client=client,
        page=page,
        per_page=per_page,
        path=path,
        is_flow=is_flow,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    workspace: str,
    *,
    client: Client,
    page: Union[Unset, None, int] = UNSET,
    per_page: Union[Unset, None, int] = UNSET,
    path: Union[Unset, None, str] = UNSET,
    is_flow: Union[Unset, None, bool] = UNSET,
) -> Optional[List[ListSchedulesResponse200Item]]:
    """list schedules

    Args:
        workspace (str):
        page (Union[Unset, None, int]):
        per_page (Union[Unset, None, int]):
        path (Union[Unset, None, str]):
        is_flow (Union[Unset, None, bool]):

    Returns:
        Response[List[ListSchedulesResponse200Item]]
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            client=client,
            page=page,
            per_page=per_page,
            path=path,
            is_flow=is_flow,
        )
    ).parsed

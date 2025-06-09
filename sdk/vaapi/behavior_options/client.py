import typing
from json.decoder import JSONDecodeError

from ..core.api_error import ApiError
from ..core.client_wrapper import SyncClientWrapper
from ..core.jsonable_encoder import jsonable_encoder
from ..core.pydantic_utilities import pydantic_v1
from ..core.request_options import RequestOptions
from ..types.behavior_option import BehaviorOptions

# this is used as the default value for optional parameters
OMIT = typing.cast(typing.Any, ...)


class BehaviorOptionClient:
    def __init__(self, *, client_wrapper: SyncClientWrapper):
        self._client_wrapper = client_wrapper

    def get(
        self, id: int, *, request_options: typing.Optional[RequestOptions] = None
    ) -> BehaviorOptions:
        """ """
        _response = self._client_wrapper.httpx_client.request(
            f"api/behavior-option/{jsonable_encoder(id)}/",
            method="GET",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return pydantic_v1.parse_obj_as(BehaviorOptions, _response.json())  # type: ignore
            _response_json = _response.json()

        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def delete(
        self, id: int, *, request_options: typing.Optional[RequestOptions] = None
    ) -> None:
        _response = self._client_wrapper.httpx_client.request(
            f"api/behavior-option/{jsonable_encoder(id)}/",
            method="DELETE",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def update(
        self,
        id: int,
        *,
        log: typing.Optional[int] = OMIT,
        xabsl_internal_option_id: typing.Optional[int] = OMIT,
        option_name: typing.Optional[str] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> BehaviorOptions:
        _response = self._client_wrapper.httpx_client.request(
            f"api/behavior-option/{jsonable_encoder(id)}/",
            method="PATCH",
            json={
                "log": log,
                "xabsl_internal_option_id": xabsl_internal_option_id,
                "option_name": option_name,
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return pydantic_v1.parse_obj_as(BehaviorOptions, _response.json())  # type: ignore
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def list(
        self,
        request_options: typing.Optional[RequestOptions] = None,
        **filters: typing.Any,
    ) -> typing.List[BehaviorOptions]:
        query_params = {k: v for k, v in filters.items() if v is not None}
        _response = self._client_wrapper.httpx_client.request(
            "api/behavior-option/",
            method="GET",
            request_options=request_options,
            params=query_params,
        )
        # _response = self._client_wrapper.httpx_client.request(
        #    f"api/cognitionrepr/?log={jsonable_encoder(log_id)}", method="GET", request_options=request_options
        # )
        try:
            if 200 <= _response.status_code < 300:
                return pydantic_v1.parse_obj_as(
                    typing.List[BehaviorOptions], _response.json()
                )  # type: ignore
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def create(
        self,
        *,
        log: typing.Optional[int] = OMIT,
        option_name: typing.Optional[str] = OMIT,
        xabsl_internal_option_id: typing.Optional[int] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> BehaviorOptions:
        """
        Examples
        --------
        from vaapi.client import Vaapi

        client = Vaapi(
            base_url='https://vat.berlin-united.com/',
            api_key="YOUR_API_KEY",
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            "api/behavior-option/",
            method="POST",
            json={
                "log": log,
                "xabsl_internal_option_id": xabsl_internal_option_id,
                "option_name": option_name,
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return pydantic_v1.parse_obj_as(BehaviorOptions, _response.json())  # type: ignore
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def bulk_create(
        self,
        *,
        repr_list: typing.List[BehaviorOptions] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> BehaviorOptions:
        """
        Examples
        --------
        from vaapi.client import Vaapi

        client = Vaapi(
            base_url='https://vat.berlin-united.com/',
            api_key="YOUR_API_KEY",
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            "api/behavior-option/",
            method="POST",
            json=repr_list,
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return pydantic_v1.parse_obj_as(BehaviorOptions, _response.json())  # type: ignore
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

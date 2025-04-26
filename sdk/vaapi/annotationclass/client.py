import typing
from json.decoder import JSONDecodeError

from ..core.api_error import ApiError
from ..core.client_wrapper import SyncClientWrapper
from ..core.jsonable_encoder import jsonable_encoder
from ..core.pydantic_utilities import pydantic_v1
from ..core.request_options import RequestOptions
from ..types.annotationclass import AnnotationClass

# this is used as the default value for optional parameters
OMIT = typing.cast(typing.Any, ...)


class AnnotationClassClient:
    def __init__(self, *, client_wrapper: SyncClientWrapper):
        self._client_wrapper = client_wrapper

    def get(
        self, id: int, *, request_options: typing.Optional[RequestOptions] = None
    ) -> AnnotationClass:
        _response = self._client_wrapper.httpx_client.request(
            f"api/annotationclass/{jsonable_encoder(id)}/",
            method="GET",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return pydantic_v1.parse_obj_as(AnnotationClass, _response.json())  # type: ignore
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def delete(
        self, id: int, *, request_options: typing.Optional[RequestOptions] = None
    ) -> None:
        _response = self._client_wrapper.httpx_client.request(
            f"api/annotationclass/{jsonable_encoder(id)}/",
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
        name: typing.Optional[str] = OMIT,
        color: typing.Optional[str] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> AnnotationClass:
        """ """
        _response = self._client_wrapper.httpx_client.request(
            f"api/annotationclass/{jsonable_encoder(id)}/",
            method="PATCH",
            json={
                "name": name,
                "color": color,
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return pydantic_v1.parse_obj_as(AnnotationClass, _response.json())  # type: ignore
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def list(
        self,
        id: int,
        *,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> typing.List[AnnotationClass]:
        """
        TODO: think about when it makes sense to use list for annotations:
        - kind of only makes sense for statistics on annotations.
        """
        query_params = {"id":id}
        _response = self._client_wrapper.httpx_client.request(
            "api/annotationclass/",
            method="GET",
            request_options=request_options,
            params=query_params,
        )
        try:
            if 200 <= _response.status_code < 300:
                return pydantic_v1.parse_obj_as(
                    typing.List[AnnotationClass], _response.json()
                )  # type: ignore
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def create(
        self,
        name,
        color,
        *,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> AnnotationClass:
        """ """
        _response = self._client_wrapper.httpx_client.request(
            "api/annotationclass/",
            method="POST",
            json={
                "name": name,
                "color": color,
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return pydantic_v1.parse_obj_as(AnnotationClass, _response.json())  # type: ignore
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

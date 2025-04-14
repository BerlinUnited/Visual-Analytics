import typing
from json.decoder import JSONDecodeError

from ..core.api_error import ApiError
from ..core.client_wrapper import SyncClientWrapper
from ..core.jsonable_encoder import jsonable_encoder
from ..core.pydantic_utilities import pydantic_v1
from ..core.request_options import RequestOptions
from ..types.xabsl_symbol_sparse import XabslSymbolSparse

# this is used as the default value for optional parameters
OMIT = typing.cast(typing.Any, ...)


class XabslSymbolClientSparse:
    """Wrapper for interacting with the XabslSymbolSparse Table of the database.

    This class provides methods to interact with XabslSymbolSparse entries
    in the database through the API.

    Parameters
    ----------
    client_wrapper : SyncClientWrapper
        The client wrapper instance used for making HTTP requests.

    Attributes
    ----------
    _client_wrapper : SyncClientWrapper
        Internal reference to the client wrapper.
    """

    def __init__(self, *, client_wrapper: SyncClientWrapper):
        """Initialize the XabslSymbolClientSparse.

        Parameters
        ----------
        client_wrapper : SyncClientWrapper
            The client wrapper instance for making HTTP requests.
        """
        self._client_wrapper = client_wrapper

    def get(
        self, id: int, *, request_options: typing.Optional[RequestOptions] = None
    ) -> XabslSymbolSparse:
        """Retrieve an XabslSymbolSparse entry by its ID.

        Parameters
        ----------
        id : int
            The unique identifier of the XabslSymbolSparse entry.
        request_options : RequestOptions, optional
            Additional options for the HTTP request.

        Returns
        -------
        XabslSymbolSparse
            The retrieved XabslSymbolSparse object.

        Raises
        ------
        ApiError
            If the API request fails or returns an error status code.

        Examples
        --------
        ```python
        from vaapi.client import Vaapi

        client = Vaapi(
            base_url='https://vat.berlin-united.com/',
            api_key="YOUR_API_KEY",
        )

        symbol = client.behavior.symbol.sparse.get(id=123)
        ```
        """
        _response = self._client_wrapper.httpx_client.request(
            f"api/behavior/symbol/sparse/{jsonable_encoder(id)}/",
            method="GET",
            request_options=request_options,
        )

        try:
            if 200 <= _response.status_code < 300:
                return pydantic_v1.parse_obj_as(XabslSymbolSparse, _response.json())  # type: ignore
            _response_json = _response.json()

        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def delete(
        self, id: int, *, request_options: typing.Optional[RequestOptions] = None
    ) -> None:
        """
        Delete a Xabsl Symbol from the XabslSymbolSparse Table.

        <Warning>This action can't be undone!</Warning>

        Parameters
        ----------
        id : int
            A unique integer value identifying this Xabsl Symbol.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        None

        Examples
        --------
        ```python
        from vaapi.client import Vaapi

        client = Vaapi(
            base_url='https://vat.berlin-united.com/',
            api_key="YOUR_API_KEY",
        )
        client.xabsl_symbol_sparse.delete(
            id=1,
        )
        ```
        """
        _response = self._client_wrapper.httpx_client.request(
            f"api/behavior/symbol/sparse/{jsonable_encoder(id)}/",
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
        log_id: typing.Optional[int] = OMIT,
        frame: typing.Optional[int] = OMIT,
        symbol_type: typing.Optional[str] = OMIT,
        symbol_name: typing.Optional[str] = OMIT,
        symbol_value: typing.Optional[str] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> XabslSymbolSparse:
        """
         Update attributes for an existing annotation.

         You will need to supply the annotation's unique ID. You can find the ID in the Label Studio UI listed at the top of the annotation in its tab. It is also listed in the History panel when viewing the annotation. Or you can use [Get all task annotations](list) to find all annotation IDs.

         For information about the JSON format used in the result, see [Label Studio JSON format of annotated tasks](https://labelstud.io/guide/export#Label-Studio-JSON-format-of-annotated-tasks).

         Parameters
         ----------
         id : int
             A unique integer value identifying this annotation.

         result : typing.Optional[typing.Sequence[typing.Dict[str, typing.Any]]]
             Labeling result in JSON format. Read more about the format in [the Label Studio documentation.](https://labelstud.io/guide/task_format)

         task : typing.Optional[int]
             Corresponding task for this annotation

         project : typing.Optional[int]
             Project ID for this annotation

         completed_by : typing.Optional[int]
             User ID of the person who created this annotation

         updated_by : typing.Optional[int]
             Last user who updated this annotation

         was_cancelled : typing.Optional[bool]
             User skipped the task

         ground_truth : typing.Optional[bool]
             This annotation is a Ground Truth

         lead_time : typing.Optional[float]
             How much time it took to annotate the task (in seconds)

         request_options : typing.Optional[RequestOptions]
             Request-specific configuration.

         Returns
         -------
         Annotation
             Updated annotation

        Examples
         --------
         ```python
         from vaapi.client import Vaapi

         client = Vaapi(
             base_url='https://vat.berlin-united.com/',
             api_key="YOUR_API_KEY",
         )
         client.xabsl_symbol_sparse.update(
             id=1,
         )
         ```
        """
        _response = self._client_wrapper.httpx_client.request(
            f"api/behavior/symbol/sparse/{jsonable_encoder(id)}/",
            method="PATCH",
            json={
                "log_id": log_id,
                "frame": frame,
                "symbol_type": symbol_type,
                "symbol_name": symbol_name,
                "symbol_value": symbol_value,
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return pydantic_v1.parse_obj_as(XabslSymbolSparse, _response.json())  # type: ignore
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def list(
        self,
        # log_id: int, *,
        request_options: typing.Optional[RequestOptions] = None,
        **filters: typing.Any,
    ) -> typing.List[XabslSymbolSparse]:
        """
        List XabslSymbolSparse with or without filters.

        You should always use at least filter by log_id, otherwise the response will be too large.

        Parameters
        ----------
        log_id : int
            Game ID

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        typing.List[XabslSymbol]
            XabslSymbol

        Examples
        --------
        ```python
        from vaapi.client import Vaapi

        client = Vaapi(
            base_url='https://vat.berlin-united.com/',
            api_key="YOUR_API_KEY",
        )
        client.xabsl_symbol_sparse.list(
            id=1,
        )
        ```
        """
        query_params = {k: v for k, v in filters.items() if v is not None}
        _response = self._client_wrapper.httpx_client.request(
            "api/xabsl-symbol/",
            method="GET",
            request_options=request_options,
            params=query_params,
        )

        try:
            if 200 <= _response.status_code < 300:
                return pydantic_v1.parse_obj_as(
                    typing.List[XabslSymbolSparse], _response.json()
                )  # type: ignore
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def create(
        self,
        *,
        log_id: typing.Optional[int] = OMIT,
        frame: typing.Optional[int] = OMIT,
        data: typing.Optional[typing.Dict[str, typing.Any]] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> XabslSymbolSparse:
        """
        Parameters
        ----------
        id : int
            A unique integer value identifying this Xabsl Symbol.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        None

        Examples
        --------
        ```python
        from vaapi.client import Vaapi

        client = Vaapi(
            base_url='https://vat.berlin-united.com/',
            api_key="YOUR_API_KEY",
        )
        client.xabsl_symbol_sparse.create(
            id=1,
        )
        ```
        """
        _response = self._client_wrapper.httpx_client.request(
            "api/behavior/symbol/sparse/",
            method="POST",
            json={
                "log_id": log_id,
                "frame": frame,
                "data": data,
                "request_options": request_options,
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return pydantic_v1.parse_obj_as(XabslSymbolSparse, _response.json())  # type: ignore
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def bulk_create(
        self,
        *,
        data: typing.List[XabslSymbolSparse] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> XabslSymbolSparse:
        """
        Parameters
        ----------
        id : int
            A unique integer value identifying this Xabsl Symbol.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        None

        Examples
        --------
        ```python
        from vaapi.client import Vaapi

        client = Vaapi(
            base_url='https://vat.berlin-united.com/',
            api_key="YOUR_API_KEY",
        )
        client.xabsl_symbol_sparse.bulk_create(
            id=1,
        )
        ```
        """
        _response = self._client_wrapper.httpx_client.request(
            "api/behavior/symbol/sparse/",
            method="POST",
            json=data,
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return pydantic_v1.parse_obj_as(XabslSymbolSparse, _response.json())  # type: ignore
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def get_behavior_count(
        self,
        request_options: typing.Optional[RequestOptions] = None,
        **filters: typing.Any,
    ) -> typing.Optional[int]:
        """
        Parameters
        ----------
        id : int
            A unique integer value identifying this Xabsl Symbol.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        None

        Examples
        --------
        ```python
        from vaapi.client import Vaapi

        client = Vaapi(
            base_url='https://vat.berlin-united.com/',
            api_key="YOUR_API_KEY",
        )
        client.xabsl_symbol_sparse.get_behavior_count(
            id=1,
        )
        ```
        """
        query_params = {k: v for k, v in filters.items() if v is not None}
        _response = self._client_wrapper.httpx_client.request(
            "api/behavior/symbol/count/",
            method="GET",
            request_options=request_options,
            params=query_params,
        )
        try:
            if 200 <= _response.status_code < 300:
                return pydantic_v1.parse_obj_as(
                    typing.Dict[str, typing.Any], _response.json()
                )  # type: ignore
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

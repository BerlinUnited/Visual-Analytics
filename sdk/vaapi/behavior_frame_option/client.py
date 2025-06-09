import typing
from json.decoder import JSONDecodeError

from ..core.api_error import ApiError
from ..core.client_wrapper import SyncClientWrapper
from ..core.jsonable_encoder import jsonable_encoder
from ..core.pydantic_utilities import pydantic_v1
from ..core.request_options import RequestOptions
from ..types.behaviorframe_options import BehaviorFrameOption
from ..types.cognition_frame import CognitionFrame

# this is used as the default value for optional parameters
OMIT = typing.cast(typing.Any, ...)


class BehaviorFrameOptionClient:
    def __init__(self, *, client_wrapper: SyncClientWrapper):
        self._client_wrapper = client_wrapper

    def get(
        self, id: int, *, request_options: typing.Optional[RequestOptions] = None
    ) -> BehaviorFrameOption:
        """ """
        _response = self._client_wrapper.httpx_client.request(
            f"api/behavior-frame-option/{jsonable_encoder(id)}/",
            method="GET",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return pydantic_v1.parse_obj_as(BehaviorFrameOption, _response.json())  # type: ignore
            _response_json = _response.json()

        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def delete(
        self, id: int, *, request_options: typing.Optional[RequestOptions] = None
    ) -> None:
        """
        Delete a BehaviorFrameOption.

        <Warning>This action can't be undone!</Warning>

        Parameters
        ----------
        id : int
            A unique integer value identifying this BehaviorFrameOption.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        None

        Examples
        --------
        from vaapi.client import Vaapi

        client = Vaapi(
            base_url='https://vat.berlin-united.com/',
            api_key="YOUR_API_KEY",
        )
        client.behavior_frame_option.delete(
            id=1,
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            f"api/behavior-frame-option/{jsonable_encoder(id)}/",
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
        options_id: typing.Optional[int] = OMIT,
        activeState: typing.Optional[int] = OMIT,
        frame: typing.Optional[int] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> BehaviorFrameOption:
        """
        Update attributes for an existing annotation.

        You will need to supply the annotation's unique ID. You can find the ID in the Label Studio UI listed at the top of the annotation in its tab. It is also listed in the History panel when viewing the annotation. Or you can use [Get all task annotations](list) to find all annotation IDs.

        For information about the JSON format used in the result, see [Label Studio JSON format of annotated tasks](https://labelstud.io/guide/export#Label-Studio-JSON-format-of-annotated-tasks).

        Parameters
        ----------
        id : int
            A unique integer value identifying this annotation.

        log_id : typing.Optional[typing.Sequence[typing.Dict[str, typing.Any]]]
            Labeling result in JSON format. Read more about the format in [the Label Studio documentation.](https://labelstud.io/guide/task_format)

        options_id : typing.Optional[int]
            Corresponding task for this annotation

        activeState : typing.Optional[int]
            Project ID for this annotation

        frame : typing.Optional[int]
            User ID of the person who created this annotation

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        BehaviorFrameOption
            Updated BehaviorFrameOption

        Examples
        --------
        from vaapi.client import Vaapi

        client = Vaapi(
            base_url='https://vat.berlin-united.com/',
            api_key="YOUR_API_KEY",
        )
        client.behavior_frame_option.update(

        )
        """
        _response = self._client_wrapper.httpx_client.request(
            f"api/behavior-frame-option/{jsonable_encoder(id)}/",
            method="PATCH",
            json={
                "log": log,
                "options_id": options_id,
                "activeState": activeState,
                # "parent": parent,
                "frame": frame,
                # "time": time,
                # "timeOfExecution": timeOfExecution,
                # "stateTime": stateTime,
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return pydantic_v1.parse_obj_as(BehaviorFrameOption, _response.json())  # type: ignore
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def list(
        self,
        request_options: typing.Optional[RequestOptions] = None,
        **filters: typing.Any,
    ) -> typing.List[BehaviorFrameOption]:
        """
        List all BehaviorFrameOptions. This endpoint requires to give id's for options_id and active_state if set. You can't put the names here. If you want that you have to use the filter endpoint.

        Parameters
        ----------
        log_id : int
            Game ID

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        typing.List[BehaviorFrameOption]
            BehaviorFrameOption

        Examples
        --------
        from vaapi.client import Vaapi

        client = Vaapi(
            base_url='https://vat.berlin-united.com/',
            api_key="YOUR_API_KEY",
        )

        client.behavior_frame_option.list(
            log_id=1,
            options_id
            active_state
            frame
        )
        """
        query_params = {k: v for k, v in filters.items() if v is not None}
        _response = self._client_wrapper.httpx_client.request(
            "api/behavior-frame-option/",
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
                    typing.List[BehaviorFrameOption], _response.json()
                )  # type: ignore
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def create(
        self,
        *,
        log: typing.Optional[int] = OMIT,
        options_id: typing.Optional[int] = OMIT,
        activeState: typing.Optional[int] = OMIT,
        parent: typing.Optional[int] = OMIT,
        frame: typing.Optional[int] = OMIT,
        time: typing.Optional[int] = OMIT,
        timeOfExecution: typing.Optional[int] = OMIT,
        stateTime: typing.Optional[int] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> BehaviorFrameOption:
        """
        from vaapi.client import Vaapi

        client = Vaapi(
            base_url='https://vat.berlin-united.com/',
            api_key="YOUR_API_KEY",
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            "api/behavior-frame-option/",
            method="POST",
            json={
                "log": log,
                "options_id": options_id,
                "activeState": activeState,
                "parent": parent,
                "frame": frame,
                "time": time,
                "timeOfExecution": timeOfExecution,
                "stateTime": stateTime,
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return pydantic_v1.parse_obj_as(BehaviorFrameOption, _response.json())  # type: ignore
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def bulk_create(
        self,
        *,
        data_list: typing.List[BehaviorFrameOption] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> BehaviorFrameOption:
        """
        from vaapi.client import Vaapi

        client = Vaapi(
            base_url='https://vat.berlin-united.com/',
            api_key="YOUR_API_KEY",
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            "api/behavior-frame-option/",
            method="POST",
            json=data_list,
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return pydantic_v1.parse_obj_as(BehaviorFrameOption, _response.json())  # type: ignore
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def filter(
        self,
        request_options: typing.Optional[RequestOptions] = None,
        **filters: typing.Any,
    ) -> typing.List[CognitionFrame]:
        """
        Returns frame numbers where the given option and states are active for one log

        Parameters
        ----------
        log_id : int
            ID of the log

        option_name : str
            Name of the option e.g. decide_game_state

        state_name : str
            Name of state inside a given option e.g. for option decide_game_state it could be set

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        typing.List[int]
            Frame Number

        Examples
        --------
        from vaapi.client import Vaapi

        client = Vaapi(
            base_url='https://vat.berlin-united.com/',
            api_key="YOUR_API_KEY",
        )
        client.behavior_frame_option.filter(
            id=7,
            option_name=arms_control,
            state_name=arms_synchronised_with_walk
        )
        """
        url = "api/behavior/filter/"
        query_params = {k: v for k, v in filters.items()}
        _response = self._client_wrapper.httpx_client.request(
            url, method="GET", request_options=request_options, params=query_params
        )
        # print(_response.text)
        try:
            if 200 <= _response.status_code < 300:
                return pydantic_v1.parse_obj_as(
                    typing.List[CognitionFrame], _response.json()
                )  # type: ignore
                # return _response.json()
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def get_behavior_count(
        self,
        request_options: typing.Optional[RequestOptions] = None,
        **filters: typing.Any,
    ) -> typing.Optional[int]:
        """ """
        query_params = {k: v for k, v in filters.items() if v is not None}
        _response = self._client_wrapper.httpx_client.request(
            "api/behavior/count/",
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

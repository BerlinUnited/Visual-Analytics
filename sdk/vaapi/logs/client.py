import typing
import datetime as dt
from json.decoder import JSONDecodeError

from ..core.api_error import ApiError
from ..core.client_wrapper import SyncClientWrapper
from ..core.jsonable_encoder import jsonable_encoder
from ..core.pydantic_utilities import pydantic_v1
from ..core.request_options import RequestOptions
from ..types.log import Log

# this is used as the default value for optional parameters
OMIT = typing.cast(typing.Any, ...)


class LogClient:
    def __init__(self, *, client_wrapper: SyncClientWrapper):
        self._client_wrapper = client_wrapper

    def get(
        self, id: int, *, request_options: typing.Optional[RequestOptions] = None
    ) -> Log:
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
            f"api/logs/{jsonable_encoder(id)}/",
            method="GET",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return pydantic_v1.parse_obj_as(Log, _response.json())  # type: ignore
            _response_json = _response.json()

        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def delete(
        self, id: int, *, request_options: typing.Optional[RequestOptions] = None
    ) -> None:
        """
        Delete a Log., this will also delete all images and representations

        <Warning>This action can't be undone!</Warning>

        You will need to supply the logs's unique ID. You can find the ID in
        the django admin panel or in the log settings in the UI.
        Parameters
        ----------
        id : int
            A unique integer value identifying this annotation.

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
        client.annotations.delete(
            id=1,
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            f"api/logs/{jsonable_encoder(id)}/",
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
        game: typing.Optional[str] = OMIT,
        experiment: typing.Optional[str] = OMIT,
        robot_version: typing.Optional[str] = OMIT,
        player_number: typing.Optional[dt.date] = OMIT,
        head_number: typing.Optional[str] = OMIT,
        body_serial: typing.Optional[str] = OMIT,
        head_serial: typing.Optional[str] = OMIT,
        representation_list: typing.Optional[typing.Dict[str, typing.Any]] = OMIT,
        sensor_log_path: typing.Optional[str] = OMIT,
        log_path: typing.Optional[str] = OMIT,
        combined_log_path: typing.Optional[str] = OMIT,
        git_commit: typing.Optional[str] = OMIT,
        is_favourite: typing.Optional[bool] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> Log:
        """ """
        _response = self._client_wrapper.httpx_client.request(
            f"api/logs/{jsonable_encoder(id)}/",
            method="PATCH",
            json={
                "game": game,
                "experiment": experiment,
                "robot_version": robot_version,
                "player_number": player_number,
                "head_number": head_number,
                "body_serial": body_serial,
                "head_serial": head_serial,
                "representation_list": representation_list,
                "sensor_log_path": sensor_log_path,
                "log_path": log_path,
                "combined_log_path": combined_log_path,
                "git_commit": git_commit,
                "is_favourite": is_favourite,
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return pydantic_v1.parse_obj_as(Log, _response.json())  # type: ignore
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def list(
        self,
        *,
        # game_id: typing.Optional[int] = None,
        request_options: typing.Optional[RequestOptions] = None,
        **filters: typing.Any,
    ) -> typing.List[Log]:
        # TODO: maybe we should not allow filtering for arbitrary fields - makes validation hard and also filtering for json fields is not useful/possible
        """
        List all logs.

        You will need to supply the event ID. You can find this in ...

        Parameters
        ----------
        game_id : int
            Game ID

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        typing.List[Log]
            Log

        Examples
        --------
        from vaapi.client import Vaapi

        client = Vaapi(
            base_url='https://vat.berlin-united.com/',
            api_key="YOUR_API_KEY",
        )
        client.annotations.list(
            id=1,
        )
        """
        query_params = {k: v for k, v in filters.items() if v is not None}
        # if game_id:
        #    _response = self._client_wrapper.httpx_client.request(
        #        f"api/logs/?game={jsonable_encoder(game_id)}", method="GET", request_options=request_options
        #    )
        # else:
        #    _response = self._client_wrapper.httpx_client.request(
        #        f"api/logs/", method="GET", request_options=request_options
        #    )
        _response = self._client_wrapper.httpx_client.request(
            "api/logs/",
            method="GET",
            request_options=request_options,
            params=query_params,
        )
        try:
            if 200 <= _response.status_code < 300:
                return pydantic_v1.parse_obj_as(typing.List[Log], _response.json())  # type: ignore
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def create(
        self,
        *,
        game: typing.Optional[str] = OMIT,
        experiment: typing.Optional[str] = OMIT,
        robot_version: typing.Optional[str] = OMIT,
        player_number: typing.Optional[dt.date] = OMIT,
        head_number: typing.Optional[str] = OMIT,
        body_serial: typing.Optional[str] = OMIT,
        head_serial: typing.Optional[str] = OMIT,
        representation_list: typing.Optional[typing.Dict[str, typing.Any]] = OMIT,
        sensor_log_path: typing.Optional[str] = OMIT,
        log_path: typing.Optional[str] = OMIT,
        combined_log_path: typing.Optional[str] = OMIT,
        git_commit: typing.Optional[str] = OMIT,
        is_favourite: typing.Optional[bool] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> Log:
        """ """
        _response = self._client_wrapper.httpx_client.request(
            "api/logs/",
            method="POST",
            json={
                "game": game,
                "experiment": experiment,
                "robot_version": robot_version,
                "player_number": player_number,
                "head_number": head_number,
                "body_serial": body_serial,
                "head_serial": head_serial,
                "representation_list": representation_list,
                "sensor_log_path": sensor_log_path,
                "log_path": log_path,
                "combined_log_path": combined_log_path,
                "git_commit": git_commit,
                "is_favourite": is_favourite,
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return pydantic_v1.parse_obj_as(Log, _response.json())  # type: ignore
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

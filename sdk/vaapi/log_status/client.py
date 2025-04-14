import typing
from json.decoder import JSONDecodeError

from ..core.api_error import ApiError
from ..core.client_wrapper import SyncClientWrapper
from ..core.jsonable_encoder import jsonable_encoder
from ..core.pydantic_utilities import pydantic_v1
from ..core.request_options import RequestOptions
from ..types.log_status import LogStatus

# this is used as the default value for optional parameters
OMIT = typing.cast(typing.Any, ...)


class LogStatusClient:
    def __init__(self, *, client_wrapper: SyncClientWrapper):
        self._client_wrapper = client_wrapper

    def get(
        self, id: int, *, request_options: typing.Optional[RequestOptions] = None
    ) -> LogStatus:
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
            f"api/log-status/{jsonable_encoder(id)}/",
            method="GET",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return pydantic_v1.parse_obj_as(LogStatus, _response.json())  # type: ignore
            _response_json = _response.json()

        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def delete(
        self, id: int, *, request_options: typing.Optional[RequestOptions] = None
    ) -> None:
        """
        Delete the log status for one log.

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
            f"api/log-status/{jsonable_encoder(id)}/",
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
        log: int,
        *,
        FrameInfo: typing.Optional[int] = OMIT,
        RobotInfo: typing.Optional[int] = OMIT,
        AudioData: typing.Optional[int] = OMIT,
        BallModel: typing.Optional[int] = OMIT,
        BallCandidates: typing.Optional[int] = OMIT,
        BallCandidatesTop: typing.Optional[int] = OMIT,
        BehaviorStateComplete: typing.Optional[int] = OMIT,
        BehaviorStateSparse: typing.Optional[int] = OMIT,
        CameraMatrix: typing.Optional[int] = OMIT,
        CameraMatrixTop: typing.Optional[int] = OMIT,
        FieldPercept: typing.Optional[int] = OMIT,
        FieldPerceptTop: typing.Optional[int] = OMIT,
        GoalPercept: typing.Optional[int] = OMIT,
        GoalPerceptTop: typing.Optional[int] = OMIT,
        MultiBallPercept: typing.Optional[int] = OMIT,
        RansacLinePercept: typing.Optional[int] = OMIT,
        RansacCirclePercept2018: typing.Optional[int] = OMIT,
        ShortLinePercept: typing.Optional[int] = OMIT,
        ScanLineEdgelPercept: typing.Optional[int] = OMIT,
        ScanLineEdgelPerceptTop: typing.Optional[int] = OMIT,
        TeamMessageDecision: typing.Optional[int] = OMIT,
        TeamState: typing.Optional[int] = OMIT,
        OdometryData: typing.Optional[int] = OMIT,
        Image: typing.Optional[int] = OMIT,
        ImageTop: typing.Optional[int] = OMIT,
        ImageJPEG: typing.Optional[int] = OMIT,
        ImageJPEGTop: typing.Optional[int] = OMIT,
        WhistlePercept: typing.Optional[int] = OMIT,
        IMUData: typing.Optional[int] = OMIT,
        FSRData: typing.Optional[int] = OMIT,
        ButtonData: typing.Optional[int] = OMIT,
        SensorJointData: typing.Optional[int] = OMIT,
        AccelerometerData: typing.Optional[int] = OMIT,
        InertialSensorData: typing.Optional[int] = OMIT,
        MotionStatus: typing.Optional[int] = OMIT,
        MotorJointData: typing.Optional[int] = OMIT,
        GyrometerData: typing.Optional[int] = OMIT,
        num_motion_frames: typing.Optional[int] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> LogStatus:
        """ """
        _response = self._client_wrapper.httpx_client.request(
            f"api/log-status/{jsonable_encoder(log)}/",
            method="PATCH",
            json={
                "FrameInfo": FrameInfo,
                "RobotInfo": RobotInfo,
                "AudioData": AudioData,
                "BallModel": BallModel,
                "BallCandidates": BallCandidates,
                "BallCandidatesTop": BallCandidatesTop,
                "BehaviorStateComplete": BehaviorStateComplete,
                "BehaviorStateSparse": BehaviorStateSparse,
                "CameraMatrix": CameraMatrix,
                "CameraMatrixTop": CameraMatrixTop,
                "FieldPercept": FieldPercept,
                "FieldPerceptTop": FieldPerceptTop,
                "GoalPercept": GoalPercept,
                "GoalPerceptTop": GoalPerceptTop,
                "MultiBallPercept": MultiBallPercept,
                "RansacLinePercept": RansacLinePercept,
                "RansacCirclePercept2018": RansacCirclePercept2018,
                "ShortLinePercept": ShortLinePercept,
                "ScanLineEdgelPercept": ScanLineEdgelPercept,
                "ScanLineEdgelPerceptTop": ScanLineEdgelPerceptTop,
                "TeamMessageDecision": TeamMessageDecision,
                "TeamState": TeamState,
                "OdometryData": OdometryData,
                "Image": Image,
                "ImageTop": ImageTop,
                "ImageJPEG": ImageJPEG,
                "ImageJPEGTop": ImageJPEGTop,
                "WhistlePercept": WhistlePercept,
                "IMUData": IMUData,
                "FSRData": FSRData,
                "ButtonData": ButtonData,
                "SensorJointData": SensorJointData,
                "AccelerometerData": AccelerometerData,
                "InertialSensorData": InertialSensorData,
                "MotionStatus": MotionStatus,
                "MotorJointData": MotorJointData,
                "GyrometerData": GyrometerData,
                "num_motion_frames": num_motion_frames,
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return pydantic_v1.parse_obj_as(LogStatus, _response.json())  # type: ignore
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def list(
        self,
        # log_id: int, *,
        request_options: typing.Optional[RequestOptions] = None,
        **filters: typing.Any,
    ) -> typing.List[LogStatus]:
        """
        List all logs.

        You will need to supply the event ID. You can find this in ...

        Parameters
        ----------
        log_id : int
            Game ID

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        typing.List[LogStatus]
            LogStatus

        Examples
        --------
        ```python
        from vaapi.client import Vaapi

        client = Vaapi(
            base_url='https://vat.berlin-united.com/',
            api_key="YOUR_API_KEY",
        )
        client.log_status.list(log_id=1)
        ```
        """
        query_params = {k: v for k, v in filters.items() if v is not None}
        _response = self._client_wrapper.httpx_client.request(
            "api/log-status/",
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
                    typing.List[LogStatus], _response.json()
                )  # type: ignore
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def create(
        self,
        *,
        log: typing.Optional[int] = OMIT,
        FrameInfo: typing.Optional[int] = OMIT,
        RobotInfo: typing.Optional[int] = OMIT,
        AudioData: typing.Optional[int] = OMIT,
        BallModel: typing.Optional[int] = OMIT,
        BallCandidates: typing.Optional[int] = OMIT,
        BallCandidatesTop: typing.Optional[int] = OMIT,
        BehaviorStateComplete: typing.Optional[int] = OMIT,
        BehaviorStateSparse: typing.Optional[int] = OMIT,
        CameraMatrix: typing.Optional[int] = OMIT,
        CameraMatrixTop: typing.Optional[int] = OMIT,
        FieldPercept: typing.Optional[int] = OMIT,
        FieldPerceptTop: typing.Optional[int] = OMIT,
        GoalPercept: typing.Optional[int] = OMIT,
        GoalPerceptTop: typing.Optional[int] = OMIT,
        MultiBallPercept: typing.Optional[int] = OMIT,
        RansacLinePercept: typing.Optional[int] = OMIT,
        RansacCirclePercept2018: typing.Optional[int] = OMIT,
        ShortLinePercept: typing.Optional[int] = OMIT,
        ScanLineEdgelPercept: typing.Optional[int] = OMIT,
        ScanLineEdgelPerceptTop: typing.Optional[int] = OMIT,
        TeamMessageDecision: typing.Optional[int] = OMIT,
        TeamState: typing.Optional[int] = OMIT,
        OdometryData: typing.Optional[int] = OMIT,
        Image: typing.Optional[int] = OMIT,
        ImageTop: typing.Optional[int] = OMIT,
        ImageJPEG: typing.Optional[int] = OMIT,
        ImageJPEGTop: typing.Optional[int] = OMIT,
        WhistlePercept: typing.Optional[int] = OMIT,
        IMUData: typing.Optional[int] = OMIT,
        FSRData: typing.Optional[int] = OMIT,
        ButtonData: typing.Optional[int] = OMIT,
        SensorJointData: typing.Optional[int] = OMIT,
        AccelerometerData: typing.Optional[int] = OMIT,
        InertialSensorData: typing.Optional[int] = OMIT,
        MotionStatus: typing.Optional[int] = OMIT,
        MotorJointData: typing.Optional[int] = OMIT,
        GyrometerData: typing.Optional[int] = OMIT,
        num_motion_frames: typing.Optional[int] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> LogStatus:
        """

        Parameters
        ----------

        Returns
        -------

        Examples
        --------
        ```python
        from vaapi.client import Vaapi

        client = Vaapi(
            base_url='https://vat.berlin-united.com/',
            api_key="YOUR_API_KEY",
        )
        ```
        """
        _response = self._client_wrapper.httpx_client.request(
            "api/log-status/",
            method="POST",
            json={
                "log": log,
                "FrameInfo": FrameInfo,
                "RobotInfo": RobotInfo,
                "AudioData": AudioData,
                "BallModel": BallModel,
                "BallCandidates": BallCandidates,
                "BallCandidatesTop": BallCandidatesTop,
                "BehaviorStateComplete": BehaviorStateComplete,
                "BehaviorStateSparse": BehaviorStateSparse,
                "CameraMatrix": CameraMatrix,
                "CameraMatrixTop": CameraMatrixTop,
                "FieldPercept": FieldPercept,
                "FieldPerceptTop": FieldPerceptTop,
                "GoalPercept": GoalPercept,
                "GoalPerceptTop": GoalPerceptTop,
                "MultiBallPercept": MultiBallPercept,
                "RansacLinePercept": RansacLinePercept,
                "RansacCirclePercept2018": RansacCirclePercept2018,
                "ShortLinePercept": ShortLinePercept,
                "ScanLineEdgelPercept": ScanLineEdgelPercept,
                "ScanLineEdgelPerceptTop": ScanLineEdgelPerceptTop,
                "TeamMessageDecision": TeamMessageDecision,
                "TeamState": TeamState,
                "OdometryData": OdometryData,
                "Image": Image,
                "ImageTop": ImageTop,
                "ImageJPEG": ImageJPEG,
                "ImageJPEGTop": ImageJPEGTop,
                "WhistlePercept": WhistlePercept,
                "IMUData": IMUData,
                "FSRData": FSRData,
                "ButtonData": ButtonData,
                "SensorJointData": SensorJointData,
                "AccelerometerData": AccelerometerData,
                "InertialSensorData": InertialSensorData,
                "MotionStatus": MotionStatus,
                "MotorJointData": MotorJointData,
                "GyrometerData": GyrometerData,
                "num_motion_frames": num_motion_frames,
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return pydantic_v1.parse_obj_as(LogStatus, _response.json())  # type: ignore
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

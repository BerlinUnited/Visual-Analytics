import datetime as dt
import typing

from ..core.datetime_utils import serialize_datetime
from ..core.pydantic_utilities import deep_union_pydantic_dicts, pydantic_v1


class LogStatus(pydantic_v1.BaseModel):
    #: Foreign key to the log the image belongs to
    log: typing.Optional[int] = pydantic_v1.Field(default=None)

    #: FrameInfo
    FrameInfo: typing.Optional[int] = pydantic_v1.Field(default=None)

    RobotInfo: typing.Optional[int] = None

    AudioData: typing.Optional[int] = None

    #: BallModel
    BallModel: typing.Optional[int] = None

    #: BallCandidates
    BallCandidates: typing.Optional[int] = None

    #: BallCandidatesTop
    BallCandidatesTop: typing.Optional[int] = None

    BehaviorStateComplete: typing.Optional[int] = None

    BehaviorStateSparse: typing.Optional[int] = None

    #: CameraMatrix
    CameraMatrix: typing.Optional[int] = None

    #: CameraMatrixTop
    CameraMatrixTop: typing.Optional[int] = pydantic_v1.Field(default=None)

    #: FieldPercept
    FieldPercept: typing.Optional[int] = pydantic_v1.Field(default=None)

    #: FieldPerceptTop
    FieldPerceptTop: typing.Optional[int] = pydantic_v1.Field(default=None)

    #: GoalPercept
    GoalPercept: typing.Optional[int] = pydantic_v1.Field(default=None)

    #: GoalPerceptTop
    GoalPerceptTop: typing.Optional[int] = pydantic_v1.Field(default=None)

    #: MultiBallPercept
    MultiBallPercept: typing.Optional[int] = pydantic_v1.Field(default=None)

    #: RansacLinePercept
    RansacLinePercept: typing.Optional[int] = pydantic_v1.Field(default=None)

    #: RansacCirclePercept2018
    RansacCirclePercept2018: typing.Optional[int] = pydantic_v1.Field(default=None)

    #: ShortLinePercept
    ShortLinePercept: typing.Optional[int] = pydantic_v1.Field(default=None)

    #: ScanLineEdgelPercept
    ScanLineEdgelPercept: typing.Optional[int] = pydantic_v1.Field(default=None)

    #: ScanLineEdgelPerceptTop
    ScanLineEdgelPerceptTop: typing.Optional[int] = pydantic_v1.Field(default=None)

    TeamMessageDecision: typing.Optional[int] = pydantic_v1.Field(default=None)

    TeamState: typing.Optional[int] = pydantic_v1.Field(default=None)

    #: OdometryData
    OdometryData: typing.Optional[int] = pydantic_v1.Field(default=None)

    #: Image
    Image: typing.Optional[int] = pydantic_v1.Field(default=None)

    #: ImageTop
    ImageTop: typing.Optional[int] = pydantic_v1.Field(default=None)

    #: ImageJPEG
    ImageJPEG: typing.Optional[int] = pydantic_v1.Field(default=None)

    #: ImageJPEGTop
    ImageJPEGTop: typing.Optional[int] = pydantic_v1.Field(default=None)

    WhistlePercept: typing.Optional[int] = pydantic_v1.Field(default=None)

    #: IMUData
    IMUData: typing.Optional[int] = pydantic_v1.Field(default=None)

    #: FSRData
    FSRData: typing.Optional[int] = pydantic_v1.Field(default=None)

    #: ButtonData
    ButtonData: typing.Optional[int] = pydantic_v1.Field(default=None)

    #: SensorJointData
    SensorJointData: typing.Optional[int] = pydantic_v1.Field(default=None)

    #: AccelerometerData
    AccelerometerData: typing.Optional[int] = pydantic_v1.Field(default=None)

    #: InertialSensorData
    InertialSensorData: typing.Optional[int] = pydantic_v1.Field(default=None)

    #: MotionStatus
    MotionStatus: typing.Optional[int] = pydantic_v1.Field(default=None)

    #: MotorJointData
    MotorJointData: typing.Optional[int] = pydantic_v1.Field(default=None)

    #: GyrometerData
    GyrometerData: typing.Optional[int] = pydantic_v1.Field(default=None)

    #: num_motion_frames
    num_motion_frames: typing.Optional[int] = pydantic_v1.Field(default=None)

    def json(self, **kwargs: typing.Any) -> str:
        kwargs_with_defaults: typing.Any = {
            "by_alias": True,
            "exclude_unset": True,
            **kwargs,
        }
        return super().json(**kwargs_with_defaults)

    def dict(self, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
        kwargs_with_defaults_exclude_unset: typing.Any = {
            "by_alias": True,
            "exclude_unset": True,
            **kwargs,
        }
        kwargs_with_defaults_exclude_none: typing.Any = {
            "by_alias": True,
            "exclude_none": True,
            **kwargs,
        }

        return deep_union_pydantic_dicts(
            super().dict(**kwargs_with_defaults_exclude_unset),
            super().dict(**kwargs_with_defaults_exclude_none),
        )

    class Config:
        frozen = True
        smart_union = True
        extra = pydantic_v1.Extra.allow
        json_encoders = {dt.datetime: serialize_datetime}

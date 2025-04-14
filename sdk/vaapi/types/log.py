import datetime as dt
import typing

from ..core.datetime_utils import serialize_datetime
from ..core.pydantic_utilities import deep_union_pydantic_dicts, pydantic_v1


class Log(pydantic_v1.BaseModel):
    #: Id assigned by django
    id: typing.Optional[int] = None

    #: Foreign key to the game this log is from
    game: typing.Optional[int] = None

    #: Foreign key to the experiment this log is from
    experiment: typing.Optional[int] = None

    #: Robot Version, either v5 or v6
    robot_version: typing.Optional[str] = None

    #: player_number
    player_number: typing.Optional[int] = None

    #: head_number
    head_number: typing.Optional[str] = pydantic_v1.Field(default=None)

    #: body_serial
    body_serial: typing.Optional[str] = pydantic_v1.Field(default=None)

    #: head_serial
    head_serial: typing.Optional[str] = pydantic_v1.Field(default=None)

    #: representation_list
    representation_list: typing.Optional[typing.Dict[str, typing.Any]] = (
        pydantic_v1.Field(default=None)
    )

    #: sensor_log_path
    sensor_log_path: typing.Optional[str] = pydantic_v1.Field(default=None)

    #: log_path
    log_path: typing.Optional[str] = pydantic_v1.Field(default=None)

    #: combined_log_path
    combined_log_path: typing.Optional[str] = pydantic_v1.Field(default=None)

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

    def __str__(self):
        return f"{self.id} - {self.log_path}"

    class Config:
        frozen = True
        smart_union = True
        extra = pydantic_v1.Extra.allow
        json_encoders = {dt.datetime: serialize_datetime}

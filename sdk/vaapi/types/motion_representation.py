import datetime as dt
import typing

from ..core.datetime_utils import serialize_datetime
from ..core.pydantic_utilities import deep_union_pydantic_dicts, pydantic_v1


class MotionRepresentation(pydantic_v1.BaseModel):
    # Id assigned by django
    id: typing.Optional[int] = None

    # reference to a specific motion frame
    frame: typing.Optional[int] = pydantic_v1.Field(default=None)

    # start byte position in sensor.log for this instance of the representation
    start_pos: typing.Optional[int] = pydantic_v1.Field(default=None)
    # size of representation in bytes
    size: typing.Optional[int] = pydantic_v1.Field(default=None)

    # representation_data as json
    representation_data: typing.Optional[typing.Dict[str, typing.Any]] = pydantic_v1.Field(default=None)

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

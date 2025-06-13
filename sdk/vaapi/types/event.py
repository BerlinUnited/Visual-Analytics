import datetime as dt
import typing

from ..core.datetime_utils import serialize_datetime
from ..core.pydantic_utilities import deep_union_pydantic_dicts, pydantic_v1


class Event(pydantic_v1.BaseModel):
    # Id assigned by django
    id: typing.Optional[int] = None

    name: typing.Optional[str] = pydantic_v1.Field(default=None)

    # First Setup Day
    start_day: typing.Optional[dt.date] = None

    # Last Game Day
    end_day: typing.Optional[dt.date] = None

    # Timezone of Country the event took place
    timezone: typing.Optional[str] = pydantic_v1.Field(default=None)

    # Country the event took place
    country: typing.Optional[str] = pydantic_v1.Field(default=None)

    # Latitude and Longitude of event location
    # Right click anywhere in google maps to get the coordinates. It should look like
    # 51.41388562549216, 5.477373810494177
    location: typing.Optional[str] = pydantic_v1.Field(default=None)

    event_folder: typing.Optional[str] = pydantic_v1.Field(default=None)

    comment: typing.Optional[str] = pydantic_v1.Field(default=None)

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

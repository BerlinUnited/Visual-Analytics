import datetime as dt
import typing

from ..core.datetime_utils import serialize_datetime
from ..core.pydantic_utilities import deep_union_pydantic_dicts, pydantic_v1


class Game(pydantic_v1.BaseModel):
    # Id assigned by django
    id: typing.Optional[int] = None

    # Foreign key to the event this game belongs to.
    event: typing.Optional[int] = pydantic_v1.Field(default=None)

    team1: typing.Optional[str] = None

    team2: typing.Optional[str] = None

    half: typing.Optional[str] = pydantic_v1.Field(default=None)

    is_testgame: typing.Optional[bool] = pydantic_v1.Field(default=None)

    head_ref: typing.Optional[str] = pydantic_v1.Field(default=None)

    assistent_ref: typing.Optional[str] = pydantic_v1.Field(default=None)

    field: typing.Optional[str] = pydantic_v1.Field(default=None)

    start_time: typing.Optional[dt.datetime] = pydantic_v1.Field(default=None)

    score: typing.Optional[str] = pydantic_v1.Field(default=None)

    game_folder: typing.Optional[str] = pydantic_v1.Field(default=None)

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

import datetime as dt
import typing

from ..core.datetime_utils import serialize_datetime
from ..core.pydantic_utilities import deep_union_pydantic_dicts, pydantic_v1


class Annotation(pydantic_v1.BaseModel):
    """
    #: 1:1 relationship to image
    """

    image: typing.Optional[int] = None

    """
    #: List of annotation results for the task
    FIXME: 
    """
    annotation: typing.Optional[typing.Dict[str, typing.Any]] = pydantic_v1.Field(
        default=None
    )

    """
    created timestamp, set automatically
    """
    created: typing.Optional[dt.datetime] = pydantic_v1.Field(default=None)

    """
    modified timestamp, set automatically
    """
    modified: typing.Optional[dt.datetime] = pydantic_v1.Field(default=None)

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

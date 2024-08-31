import datetime as dt
import typing

from ..core.datetime_utils import serialize_datetime
from ..core.pydantic_utilities import deep_union_pydantic_dicts, pydantic_v1
from .annotation_last_action import AnnotationLastAction


class Annotation(pydantic_v1.BaseModel):
    id: typing.Optional[int] = None
    result: typing.Optional[typing.List[typing.Dict[str, typing.Any]]] = pydantic_v1.Field(default=None)
    """
    List of annotation results for the task
    """

    created_username: typing.Optional[str] = pydantic_v1.Field(default=None)
    """
    Username string
    """

    created_ago: typing.Optional[str] = pydantic_v1.Field(default=None)
    """
    Time delta from creation time
    """

    completed_by: typing.Optional[int] = None
    unique_id: typing.Optional[str] = None
    was_cancelled: typing.Optional[bool] = pydantic_v1.Field(default=None)
    """
    User skipped the task
    """

    ground_truth: typing.Optional[bool] = pydantic_v1.Field(default=None)
    """
    This annotation is a Ground Truth (ground_truth)
    """

    created_at: typing.Optional[dt.datetime] = pydantic_v1.Field(default=None)
    """
    Creation time
    """

    updated_at: typing.Optional[dt.datetime] = pydantic_v1.Field(default=None)
    """
    Last updated time
    """

    draft_created_at: typing.Optional[dt.datetime] = pydantic_v1.Field(default=None)
    """
    Draft creation time
    """

    lead_time: typing.Optional[float] = pydantic_v1.Field(default=None)
    """
    How much time it took to annotate the task
    """

    import_id: typing.Optional[int] = pydantic_v1.Field(default=None)
    """
    Original annotation ID that was at the import step or NULL if this annotation wasn't imported
    """

    last_action: typing.Optional[AnnotationLastAction] = pydantic_v1.Field(default=None)
    """
    Action which was performed in the last annotation history item
    """

    task: typing.Optional[int] = pydantic_v1.Field(default=None)
    """
    Corresponding task for this annotation
    """

    project: typing.Optional[int] = pydantic_v1.Field(default=None)
    """
    Project ID for this annotation
    """

    updated_by: typing.Optional[int] = pydantic_v1.Field(default=None)
    """
    Last user who updated this annotation
    """

    parent_prediction: typing.Optional[int] = pydantic_v1.Field(default=None)
    """
    Points to the prediction from which this annotation was created
    """

    parent_annotation: typing.Optional[int] = pydantic_v1.Field(default=None)
    """
    Points to the parent annotation from which this annotation was created
    """

    last_created_by: typing.Optional[int] = pydantic_v1.Field(default=None)
    """
    User who created the last annotation history item
    """

    def json(self, **kwargs: typing.Any) -> str:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().json(**kwargs_with_defaults)

    def dict(self, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
        kwargs_with_defaults_exclude_unset: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        kwargs_with_defaults_exclude_none: typing.Any = {"by_alias": True, "exclude_none": True, **kwargs}

        return deep_union_pydantic_dicts(
            super().dict(**kwargs_with_defaults_exclude_unset), super().dict(**kwargs_with_defaults_exclude_none)
        )

    class Config:
        frozen = True
        smart_union = True
        extra = pydantic_v1.Extra.allow
        json_encoders = {dt.datetime: serialize_datetime}
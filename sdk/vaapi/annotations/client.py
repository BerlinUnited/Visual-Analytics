import typing
from json.decoder import JSONDecodeError

from ..core.api_error import ApiError
from ..core.client_wrapper import SyncClientWrapper
from ..core.jsonable_encoder import jsonable_encoder
from ..core.pydantic_utilities import pydantic_v1
from ..core.request_options import RequestOptions
from ..types.annotation import Annotation

# this is used as the default value for optional parameters
OMIT = typing.cast(typing.Any, ...)

class AnnotationsClient:
    def __init__(self, *, client_wrapper: SyncClientWrapper):
        self._client_wrapper = client_wrapper

    def get(self, id: int, *, request_options: typing.Optional[RequestOptions] = None) -> Annotation:
        _response = self._client_wrapper.httpx_client.request(
            f"api/annotations/{jsonable_encoder(id)}/", method="GET", request_options=request_options
        )
        try:
            if 200 <= _response.status_code < 300:
                return pydantic_v1.parse_obj_as(Annotation, _response.json())  # type: ignore
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def delete(self, id: int, *, request_options: typing.Optional[RequestOptions] = None) -> None:
        """
        Delete an annotation.

        <Warning>This action can't be undone!</Warning>

        You will need to supply the annotation's unique ID. You can find the ID in the Label Studio UI listed at the top of the annotation in its tab. It is also listed in the History panel when viewing the annotation. Or you can use [Get all task annotations](list) to find all annotation IDs.

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
        from label_studio_sdk.client import LabelStudio

        client = LabelStudio(
            api_key="YOUR_API_KEY",
        )
        client.annotations.delete(
            id=1,
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            f"api/annotations/{jsonable_encoder(id)}/", method="DELETE", request_options=request_options
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
        result: typing.Optional[typing.Sequence[typing.Dict[str, typing.Any]]] = OMIT,
        task: typing.Optional[int] = OMIT,
        project: typing.Optional[int] = OMIT,
        completed_by: typing.Optional[int] = OMIT,
        updated_by: typing.Optional[int] = OMIT,
        was_cancelled: typing.Optional[bool] = OMIT,
        ground_truth: typing.Optional[bool] = OMIT,
        lead_time: typing.Optional[float] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> Annotation:
        """
        Update attributes for an existing annotation.

        You will need to supply the annotation's unique ID. You can find the ID in the Label Studio UI listed at the top of the annotation in its tab. It is also listed in the History panel when viewing the annotation. Or you can use [Get all task annotations](list) to find all annotation IDs.

        For information about the JSON format used in the result, see [Label Studio JSON format of annotated tasks](https://labelstud.io/guide/export#Label-Studio-JSON-format-of-annotated-tasks).

        Parameters
        ----------
        id : int
            A unique integer value identifying this annotation.

        result : typing.Optional[typing.Sequence[typing.Dict[str, typing.Any]]]
            Labeling result in JSON format. Read more about the format in [the Label Studio documentation.](https://labelstud.io/guide/task_format)

        task : typing.Optional[int]
            Corresponding task for this annotation

        project : typing.Optional[int]
            Project ID for this annotation

        completed_by : typing.Optional[int]
            User ID of the person who created this annotation

        updated_by : typing.Optional[int]
            Last user who updated this annotation

        was_cancelled : typing.Optional[bool]
            User skipped the task

        ground_truth : typing.Optional[bool]
            This annotation is a Ground Truth

        lead_time : typing.Optional[float]
            How much time it took to annotate the task (in seconds)

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        Annotation
            Updated annotation

        Examples
        --------
        from label_studio_sdk.client import LabelStudio

        client = LabelStudio(
            api_key="YOUR_API_KEY",
        )
        client.annotations.update(
            id=1,
            result=[
                {
                    "original_width": 1920,
                    "original_height": 1080,
                    "image_rotation": 0,
                    "from_name": "bboxes",
                    "to_name": "image",
                    "type": "rectanglelabels",
                    "value": {
                        "x": 20,
                        "y": 30,
                        "width": 50,
                        "height": 60,
                        "rotation": 0,
                        "values": {"rectanglelabels": ["Person"]},
                    },
                }
            ],
            was_cancelled=False,
            ground_truth=True,
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            f"api/annotations/{jsonable_encoder(id)}/",
            method="PATCH",
            json={
                "result": result,
                "task": task,
                "project": project,
                "completed_by": completed_by,
                "updated_by": updated_by,
                "was_cancelled": was_cancelled,
                "ground_truth": ground_truth,
                "lead_time": lead_time,
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return pydantic_v1.parse_obj_as(Annotation, _response.json())  # type: ignore
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def list(self, id: int, *, request_options: typing.Optional[RequestOptions] = None) -> typing.List[Annotation]:
        """
        List all annotations for a task.

        You will need to supply the task ID. You can find this in Label Studio by opening a task and checking the URL. It is also listed at the top of the labeling interface. Or you can use [Get tasks list](../tasks/list).

        Parameters
        ----------
        id : int
            Task ID

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        typing.List[Annotation]
            Annotation

        Examples
        --------
        from label_studio_sdk.client import LabelStudio

        client = LabelStudio(
            api_key="YOUR_API_KEY",
        )
        client.annotations.list(
            id=1,
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            f"api/tasks/{jsonable_encoder(id)}/annotations/", method="GET", request_options=request_options
        )
        try:
            if 200 <= _response.status_code < 300:
                return pydantic_v1.parse_obj_as(typing.List[Annotation], _response.json())  # type: ignore
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def create(
        self,
        id: int,
        *,
        result: typing.Optional[typing.Sequence[typing.Dict[str, typing.Any]]] = OMIT,
        task: typing.Optional[int] = OMIT,
        project: typing.Optional[int] = OMIT,
        completed_by: typing.Optional[int] = OMIT,
        updated_by: typing.Optional[int] = OMIT,
        was_cancelled: typing.Optional[bool] = OMIT,
        ground_truth: typing.Optional[bool] = OMIT,
        lead_time: typing.Optional[float] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> Annotation:
        """
        Add annotations to a task like an annotator does.

        You will need to supply the task ID. You can find this in Label Studio by opening a task and checking the URL. It is also listed at the top of the labeling interface. Or you can use [Get tasks list](../tasks/list).

        The content of the result field depends on your labeling configuration. For example, send the following data as part of your POST
        request to send an empty annotation with the ID of the user who completed the task:

        ```json
        {
        "result": {},
        "was_cancelled": true,
        "ground_truth": true,
        "lead_time": 0,
        "task": 0
        "completed_by": 123
        }
        ```

        Parameters
        ----------
        id : int
            Task ID

        result : typing.Optional[typing.Sequence[typing.Dict[str, typing.Any]]]
            Labeling result in JSON format. Read more about the format in [the Label Studio documentation.](https://labelstud.io/guide/task_format)

        task : typing.Optional[int]
            Corresponding task for this annotation

        project : typing.Optional[int]
            Project ID for this annotation

        completed_by : typing.Optional[int]
            User ID of the person who created this annotation

        updated_by : typing.Optional[int]
            Last user who updated this annotation

        was_cancelled : typing.Optional[bool]
            User skipped the task

        ground_truth : typing.Optional[bool]
            This annotation is a Ground Truth

        lead_time : typing.Optional[float]
            How much time it took to annotate the task (in seconds)

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        Annotation
            Created annotation

        Examples
        --------
        from label_studio_sdk.client import LabelStudio

        client = LabelStudio(
            api_key="YOUR_API_KEY",
        )
        client.annotations.create(
            id=1,
            result=[
                {
                    "original_width": 1920,
                    "original_height": 1080,
                    "image_rotation": 0,
                    "from_name": "bboxes",
                    "to_name": "image",
                    "type": "rectanglelabels",
                    "value": {
                        "x": 20,
                        "y": 30,
                        "width": 50,
                        "height": 60,
                        "rotation": 0,
                        "values": {"rectanglelabels": ["Person"]},
                    },
                }
            ],
            was_cancelled=False,
            ground_truth=True,
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            f"api/tasks/{jsonable_encoder(id)}/annotations/",
            method="POST",
            json={
                "result": result,
                "task": task,
                "project": project,
                "completed_by": completed_by,
                "updated_by": updated_by,
                "was_cancelled": was_cancelled,
                "ground_truth": ground_truth,
                "lead_time": lead_time,
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return pydantic_v1.parse_obj_as(Annotation, _response.json())  # type: ignore
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

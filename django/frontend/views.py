from django.shortcuts import render, redirect
from django.views.generic import TemplateView, DetailView, View
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import json

from common.models import Event, Game, Log, Experiment
from image.models import NaoImage
from annotation.models import Annotation, AnnotationClass
from cognition.models import CognitionFrame, FrameFilter
from django.http import JsonResponse


@method_decorator(login_required(login_url="mylogin"), name="dispatch")
class EventListView(TemplateView):
    template_name = "frontend/events.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["events"] = Event.objects.all()
        return context


@method_decorator(login_required(login_url="mylogin"), name="dispatch")
class GameListView(DetailView):
    # could also be called EventDetailView
    model = Event
    template_name = "frontend/games.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["games"] = Game.objects.filter(event_id=context["event"])

        return context


@method_decorator(login_required(login_url="mylogin"), name="dispatch")
class GameLogListView(DetailView):
    # could also be called GameDetailView
    model = Game
    template_name = "frontend/logs.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["game_logs"] = Log.objects.filter(game=context["game"].id)

        return context


@method_decorator(login_required(login_url="mylogin"), name="dispatch")
class ExperimentLogListView(DetailView):
    # could also be called ExperimentDetailView
    model = Experiment
    template_name = "frontend/logs.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["experiment_logs"] = Log.objects.filter(
            experiment=context["experiment"].id
        )

        return context


@method_decorator(login_required(login_url="mylogin"), name="dispatch")
class LogDetailView(DetailView):
    model = Log
    template_name = "frontend/image.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        filter_name = request.GET.get("filter")

        # Get first frame based on filter
        first_frame_number = self.get_first_frame_number(filter_name)

        if first_frame_number:
            base_url = reverse(
                "image_detail", kwargs={"pk": self.object.id, "img": first_frame_number}
            )
            return redirect(f"{base_url}?filter={filter_name or 'None'}")

        # Handle case where no images exist
        if self.object.game_id is not None:
            return redirect("game_detail", pk=self.object.game.id)
        elif self.object.experiment_id is not None:
            return redirect("experiment_detail", pk=self.object.experiment.id)

    def get_first_frame_number(self, filter_name):
        """Helper method to get the first frame number based on filter"""
        if filter_name and filter_name != "None":
            filtered_frames = FrameFilter.objects.filter(
                log_id=self.object, user=self.request.user, name=filter_name
            ).first()

            if filtered_frames:
                first_image = (
                    CognitionFrame.objects.filter(
                        log=self.object,
                        frame_number__in=filtered_frames.frames["frame_list"],
                    )
                    .order_by("frame_number")
                    .first()
                )
                if first_image:
                    return first_image.frame_number

        # Default: get first frame without filtering
        first_image = (
            CognitionFrame.objects.filter(log=self.object)
            .order_by("frame_number")
            .first()
        )

        return first_image.frame_number if first_image else None


@method_decorator(login_required(login_url="mylogin"), name="dispatch")
class ImageDetailView(View):
    def _get_image_and_annotation(self, log_id, frame_number, camera_type):
        """Fetches an image and its annotation for a given log, frame, and camera."""
        image = NaoImage.objects.filter(
            frame__log_id=log_id, camera=camera_type, frame__frame_number=frame_number
        ).first()  # Use _id for FK efficiency if not needing the whole frame object

        image_url = None
        annotation_json = json.dumps({})  # Default empty annotation

        if image:
            image_url = f"https://logs.berlin-united.com/{image.image_url}"
            image.image_url = image_url

            annotation_data = (
                Annotation.objects.filter(image=image)
                .values_list("annotation", flat=True)
                .first()
            )  # Use image instance directly

            if annotation_data:
                annotation_json = json.dumps(annotation_data)
        else:
            image = None

        return image, annotation_json

    def _get_frame_numbers(self, log_id, user, current_filter_name):
        """Gets the distinct list of frame numbers, potentially filtered."""
        frame_numbers_qs = (
            CognitionFrame.objects.filter(log=log_id)
            .order_by("frame_number")
            .values_list("frame_number", flat=True)
            .distinct()
        )

        # Apply specific frame filter if provided and valid
        if current_filter_name and current_filter_name != "None":
            frame_filter = FrameFilter.objects.filter(
                log_id=log_id, user=user, name=current_filter_name
            ).first()
            if frame_filter and "frame_list" in frame_filter.frames:
                # Filter the base query by the list from the FrameFilter
                frame_numbers_qs = frame_numbers_qs.filter(
                    frame__frame_number__in=frame_filter.frames["frame_list"]
                )

        return list(frame_numbers_qs)  # Return the QuerySet initially

    def get(self, request, **kwargs):
        context = {}
        log_id = context["log_id"] = self.kwargs.get("pk")
        # Default to "None" if not present
        current_filter = self.request.GET.get("filter", "None")
        context["frame_numbers"] = self._get_frame_numbers(
            log_id, request.user, current_filter
        )
        # load combobox with all available framefilter
        context["filters"] = FrameFilter.objects.filter(log=log_id)

        # load available annotation classes
        context["classes"] = AnnotationClass.objects.all()

        context["current_frame"] = current_frame = self.kwargs.get("img")

        # FIXME get images and annotations from javascript using the information in the url
        # this way we dont have to do some weird mapping from template values to javascript
        context["bottom_image"], context["bottom_annotation"] = (
            self._get_image_and_annotation(log_id, current_frame, "BOTTOM")
        )
        context["top_image"], context["top_annotation"] = (
            self._get_image_and_annotation(log_id, current_frame, "TOP")
        )

        # set information for timeline
        current_index = list(context["frame_numbers"]).index(current_frame)
        context["prev_frame"] = (
            list(context["frame_numbers"])[current_index - 1]
            if current_index > 0
            else None
        )
        context["next_frame"] = (
            list(context["frame_numbers"])[current_index + 1]
            if current_index < len(context["frame_numbers"]) - 1
            else None
        )
        context["current_index"] = current_index  # Frame number from 0 to len(frames), not equal to the actual recorded framenumber
        context["num_frames"] = len(context["frame_numbers"])

        return render(request, "frontend/image_detail.html", context)

    def post(self, request, *args, **kwargs):
        """
        this handles selecting a frame filter and redirecting it to the first frame of this filter
        """
        selected_frame_filter = request.POST.get('frame_filter')
        print(selected_frame_filter)
        # TODO fully implement this
        # old stuff moved from get function
        """
        selected_filter = request.GET.get("filter_selector")
        if selected_filter:
            base_url = reverse("log_detail", kwargs={"pk": log_id})
            redirect_url = (
                f"{base_url}?filter={context['filters'][int(selected_filter)]['name']}"
            )
            return redirect(redirect_url)
        """

    def patch(self, request, **kwargs):
        """
        This handles updating annotations via api call from js
        """
        try:
            json_data = json.loads(request.body)
            print(json_data)
            my_image = NaoImage.objects.get(id=int(json_data["image"]))

            annotation_instance, created = Annotation.objects.get_or_create(
                image=my_image,
                defaults={"annotation": json_data.get("annotations", {})},
            )

            if not created:
                annotation_instance.annotation = json_data.get("annotations", {})
                annotation_instance.save()

            return JsonResponse({"message": "Canvas data received and processed."})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

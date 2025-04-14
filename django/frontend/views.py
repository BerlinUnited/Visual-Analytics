from django.shortcuts import render, redirect
from django.views.generic import TemplateView, DetailView, View
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import json

from common.models import Event, Game, Log, Experiment
from image.models import NaoImage
from annotation.models import Annotation
from cognition.models import FrameFilter
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
class ImageListView(DetailView):
    # could also be called LogDetailView
    # TODO: maybe I should query FrameInfo from cognition representation table here sort that use that as extra parameter
    model = Log
    template_name = "frontend/image.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        filter = request.GET.get("filter")
        # TODO fix the logic after db restructure

        filtered_frames = FrameFilter.objects.filter(
            log_id=self.object,
            user=self.request.user,
            name=filter
        ).first()

        if filtered_frames and filter!="None":
            first_image = (
                NaoImage.objects.filter(
                    frame__log=self.object, frame__frame_number__in=filtered_frames.frames["frame_list"]
                )
                .order_by("frame__frame_number")
                .first()
            )
        else:
            first_image = (
                NaoImage.objects.filter(frame__log=self.object)
                .order_by("frame__frame_number")
                .first()
            )

        if first_image:
            base_url = reverse("image_detail",kwargs={"pk":self.object.id, "bla":first_image.frame.frame_number})
            return redirect(f"{base_url}?filter={filter}")
        # TODO what if no images exist for a log -> redirect somewhere else
        return super().get(
            request, *args, **kwargs
        )  # Handle cases where no images exist


@method_decorator(login_required(login_url="mylogin"), name="dispatch")
class ImageDetailView(View):
    def get(self, request, **kwargs):
        
        context = {}
        log_id = self.kwargs.get("pk")
        current_filter = self.request.GET.get("filter")
        context["filters"] = [{'id': 0, "name": "None", "selected": current_filter == "None"}] + [
            {'id': index + 1, "name": frame_filter.name, "selected": current_filter == frame_filter.name}
            for index, frame_filter in enumerate(
                FrameFilter.objects.filter(
                    log=log_id,
                    user=self.request.user,
                )
            )
        ]      
        selected_filter = request.GET.get('filter_selector')
        if selected_filter: 
            base_url = reverse("log_detail", kwargs={"pk": log_id})
            redirect_url = f"{base_url}?filter={context['filters'][int(selected_filter)]['name']}"
            return redirect(redirect_url)
        
        current_frame = self.kwargs.get("bla")
        context["bottom_image"] = NaoImage.objects.filter(
            frame__log=log_id, camera="BOTTOM", frame__frame_number=current_frame
        ).first()
        context["top_image"] = NaoImage.objects.filter(
            frame__log=log_id, camera="TOP", frame__frame_number=current_frame
        ).first()
        context["log_id"] = log_id
        context["current_frame"] = current_frame
        #load combobox with all availabe framefilter

        # we have to get the frames for top and bottom image and then remove the duplicates here, because sometime we have only one image in the
        # first frame
        frames = FrameFilter.objects.filter(
            log=log_id,
            user=self.request.user,
            name=current_filter
        ).first()
        if frames and current_filter!="None":
            context["frame_numbers"] = (
                NaoImage.objects.filter(
                    frame__log=log_id, frame__frame_number__in=frames.frames["frame_list"]
                )
                .order_by("frame__frame_number")
                .values_list("frame__frame_number", flat=True)
                .distinct()
            )
        else:
            context["frame_numbers"] = (
                NaoImage.objects.filter(frame__log=log_id)
                .order_by("frame__frame_number")
                .values_list("frame__frame_number", flat=True)
                .distinct()
            )
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
        # handle the case that we do have a bottom image in the frame
        if context["bottom_image"]:
            # update the image url
            # TODO: dynamically add the url based on which server is online
            context["bottom_image"].image_url = (
                "https://logs.berlin-united.com/" + context["bottom_image"].image_url
            )

            bottom_annotation = (
                Annotation.objects.filter(image=context["bottom_image"].id)
                .values_list("annotation", flat=True)
                .first()
            )
            if bottom_annotation:
                context["bottom_annotation"] = json.dumps(bottom_annotation)
            else:
                # add empty annotations when we could not load annotations
                context["bottom_annotation"] = json.dumps({})
        else:
            # add a dummy image if we don't have an image from the database
            context["bottom_image"] = None
            # context['bottom_image'] = Image()
            # context['bottom_image'].image_url = "https://dummyimage.com/640x4:3/"
            # context['bottom_image'].id = -1

            # add empty annotations when we don't have an image
            context["bottom_annotation"] = json.dumps({})

        # handle the case that we do have a top image in the frame
        if context["top_image"]:
            print("id:", context["top_image"].id)
            # update the image url
            # TODO: dynamically add the url based on which server is online
            context["top_image"].image_url = (
                "https://logs.berlin-united.com/" + context["top_image"].image_url
            )

            top_annotation = (
                Annotation.objects.filter(image=context["top_image"].id)
                .values_list("annotation", flat=True)
                .first()
            )
            if top_annotation:
                context["top_annotation"] = json.dumps(top_annotation)
            else:
                # add empty annotations when we could not load annotations
                context["top_annotation"] = json.dumps({})
        else:
            print("set top image to none")
            # add a dummy image if we don't have an image from the database
            context["top_image"] = None
            # context['top_image'] = Image()
            # context['top_image'].image_url = "https://dummyimage.com/640x4:3/"
            # context['top_image'].id = -1

            # add empty annotations when we don't have an image
            context["top_annotation"] = json.dumps({})
        return render(request, "frontend/image_detail.html", context)

    def patch(self, request, **kwargs):
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

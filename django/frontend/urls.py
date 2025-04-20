from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path("", RedirectView.as_view(url="/events")),
    path("events", views.EventListView.as_view(), name="events"),
    path("events/<int:pk>", views.GameListView.as_view(), name="event_detail"),
    path("games/<int:pk>", views.GameLogListView.as_view(), name="game_detail"),
    path(
        "experiments/<int:pk>",
        views.ExperimentLogListView.as_view(),
        name="experiment_detail",
    ),
    path("log/<int:pk>", views.LogDetailView.as_view(), name="log_detail"),
    path(
        "log/<int:pk>/frame/<int:img>",
        views.ImageDetailView.as_view(),
        name="image_detail",
    ),
]

from django.contrib import admin
from .models import Event, Game, Log, LogStatus, Experiment, VideoRecording, Team
from unfold.admin import ModelAdmin
from unfold.contrib.filters.admin import (
    DropdownFilter,
)

from django.contrib.admin.sites import site
from django.contrib.auth.models import Group

site.unregister(Group)


class GameAdmin(ModelAdmin):
    list_display = ("event_id", "get_id", "team1", "team2", "half", "is_testgame")

    def get_id(self, obj):
        return obj.id

    get_id.short_description = "Game ID"


class GameExperimentFilter(DropdownFilter):
    title = "Content Type"
    parameter_name = "content_type"

    def lookups(self, request, model_admin):
        return [
            ["game", "Game"],
            ["experiment", "Experiment"],
        ]

    def queryset(self, request, queryset):
        if self.value() == "game":
            # Return only entries where experiment is null
            return queryset.filter(experiment__isnull=True)
        elif self.value() == "experiment":
            # Return only entries where experiment is not null
            return queryset.filter(experiment__isnull=False)
        return queryset


class LogAdmin(ModelAdmin):
    search_fields = [
        "game_id__team1__icontains",
        "game_id__team2__icontains",
        "head_number",
        "player_number",
    ]
    list_display = [
        "get_event_id",
        "get_game_id",
        "get_id",
        "get_team1",
        "get_team2",
        "get_half",
        "player_number",
        "head_number",
        "get_start_time",
        "is_test",
    ]

    list_filter_submit = True  # Submit button at the bottom of the filter
    list_filter = [GameExperimentFilter]

    def get_event_id(self, obj):
        return obj.game.event.id

    def get_game_id(self, obj):
        return obj.game.id

    def get_id(self, obj):
        return obj.id

    def get_team1(self, obj):
        return obj.game.team1

    def get_team2(self, obj):
        return obj.game.team2

    def get_half(self, obj):
        return obj.game.half

    def get_start_time(self, obj):
        return obj.game.start_time

    def is_test(self, obj):
        return obj.game.is_testgame

    get_id.short_description = "Log ID"
    get_game_id.short_description = "Game ID"
    get_event_id.short_description = "Event ID"
    get_start_time.short_description = "Time"
    get_team1.short_description = "Team 1"
    get_team2.short_description = "Team 2"


class LogStatusAdmin(ModelAdmin):
    # TODO: add this search field to every model that is related to log
    search_fields = ["log__log_path__icontains"]
    list_display = ["get_log_id", "get_log_path"]

    def get_log_id(self, obj):
        return obj.log.id

    def get_log_path(self, obj):
        return obj.log.log_path

    get_log_id.short_description = "Log ID"
    get_log_path.short_description = "Log Path"


class TeamAdmin(ModelAdmin):
    list_display = ["id", "get_team_id", "get_team_name"]

    def get_team_id(self, obj):
        return obj.team_id

    def get_team_name(self, obj):
        return obj.name

    get_team_id.short_description = "Team ID"
    get_team_name.short_description = "Team Name"


# this is required for every model
@admin.register(Event)
@admin.register(Experiment)
@admin.register(VideoRecording)
class CustomAdminClass(ModelAdmin):
    pass


admin.site.register(Game, GameAdmin)
admin.site.register(Log, LogAdmin)
admin.site.register(LogStatus, LogStatusAdmin)
admin.site.register(Team, TeamAdmin)

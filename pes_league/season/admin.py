from django.contrib import admin

from .models import Season, Team, Game


class SeasonAdmin(admin.ModelAdmin):
    pass


class TeamAdmin(admin.ModelAdmin):
    pass


class GameAdmin(admin.ModelAdmin):
    pass


admin.site.register(Season, SeasonAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Game, GameAdmin)

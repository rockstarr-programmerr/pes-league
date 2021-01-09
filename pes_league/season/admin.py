from django.contrib import admin

from .models import Season, Team


class SeasonAdmin(admin.ModelAdmin):
    pass


class TeamAdmin(admin.ModelAdmin):
    pass


admin.site.register(Season, SeasonAdmin)
admin.site.register(Team, TeamAdmin)

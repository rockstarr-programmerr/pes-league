from django.contrib import admin

from .models import Season


class SeasonAdmin(admin.ModelAdmin):
    pass


admin.site.register(Season, SeasonAdmin)

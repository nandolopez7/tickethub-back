from django.contrib import admin

from tickethub_back.events.models import  Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    ordering = ('pk',)
    list_display = ('name', 'date', 'time', 'place', 'is_active', 'created', 'updated')
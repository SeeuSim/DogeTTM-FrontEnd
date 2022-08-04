from django.contrib import admin

from .models import *
# Register your models here.


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ("name", "address", "owners", "token_count")
    readonly_fields = ("address", "name", "owners", "token_count")


@admin.register(DataPoint)
class DataPointAdmin(admin.ModelAdmin):
    list_display = ("collection", "timestamp")
    readonly_fields = ("collection", "timestamp")


@admin.register(Asset)
class DataPointAdmin(admin.ModelAdmin):
    list_display = ('parent_collection', 'data', 'mimeType')
    readonly_fields = ('parent_collection', 'data', 'mimeType')


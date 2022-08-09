from django.contrib import admin

from django.utils import timezone
from .models import *
# Register your models here.


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ("name", "address", "owners", "total_minted", "total_burned")
    readonly_fields = ("address", "name", "owners", "total_minted", "total_burned")


@admin.register(DataPoint)
class DataPointAdmin(admin.ModelAdmin):
    list_display = ("collection", "display_utc")
    readonly_fields = ("collection", "display_utc")

    @admin.display(ordering='timestamp', description="Timestamp (UTC)")
    def display_utc(self, obj:DataPoint):
        return obj.timestamp.astimezone(timezone.utc).isoformat()


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('parent_collection', 'mimeType', 'display_trunc_data')
    readonly_fields = ('parent_collection', 'mimeType', 'display_trunc_data')

    @admin.display(ordering="data", description="Data (Truncated)")
    def display_trunc_data(self, obj:Asset):
        return f'{obj.data[:30]}...' if obj.data else ''


from django.contrib import admin

from .models import *
# Register your models here.

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ("address", "name", "owners", "token_count")
    readonly_fields = ("address", "name", "owners", "token_count")

@admin.register(DataPoint)
class DataPointAdmin(admin.ModelAdmin):
    list_display = ("collection", "timestamp")
    readonly_fields = ("collection", "timestamp")

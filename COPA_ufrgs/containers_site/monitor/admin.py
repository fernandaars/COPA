from django.contrib import admin

from .models import KPICommand, KPILink, KPIResources, KPIWireless


# Register your models here.
@admin.register(KPIResources)
class KPIResourcesAdmin(admin.ModelAdmin):
    list_display = ("pk", "timestamp", "locus", "CPU", "memory")


@admin.register(KPICommand)
class KPICommandAdmin(admin.ModelAdmin):
    list_display = ("pk", "timestamp", "locus", "proc_time", "response_time")


@admin.register(KPILink)
class KPILinkAdmin(admin.ModelAdmin):
    list_display = ("pk", "timestamp", "locus1", "locus2")


@admin.register(KPIWireless)
class KPIWirelessAdmin(admin.ModelAdmin):
    list_display = ("pk", "timestamp", "locus", "mac")

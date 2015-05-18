from django.contrib import admin
from .models import ContestPanel
# Register your models here.


class ContestPanelAdmin(admin.ModelAdmin):
    class Meta:
        model = ContestPanel
    list_display = ('ContestName', 'ContestImage', 'Active', 'DateAdded')
admin.site.register(ContestPanel, ContestPanelAdmin)

from django.contrib import admin
from .models import AdminUser
# Register your models here.


class AdminUserAdmin(admin.ModelAdmin):
    class Meta:
        model = AdminUser
admin.site.register(AdminUser, AdminUserAdmin)

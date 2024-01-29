from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import ECGModel, UserModel


class ECGAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'date',
        'leads'
    )

    # Grant add permission unless the user is an admin
    def has_add_permission(self, request):
        # This can also be done from admin panel
        # create admin group that can not add ECG model ->
        # add created group to the admin
        return not request.user.is_admin


class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'name', 'last_name', 'is_admin')
    search_fields = ('username', 'email', 'name', 'last_name')
    ordering = ('username',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (('Personal Info'), {'fields': ('name', 'last_name', 'second_last_name', 'email')}),
        (('Permissions'), {'fields': ('is_active', 'is_admin', 'groups', 'is_staff')}),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )


admin.site.register(ECGModel, ECGAdmin)
admin.site.register(UserModel, UserAdmin)

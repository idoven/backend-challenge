from django.contrib import admin

from .models import ECGModel, LeadsModel, UserModel


class ECGAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'date',
        'leads'
    )


class LeadsAdmin(admin.ModelAdmin):
    list_display = (
        'ecg',
        'name',
        'num_samples',
        'signal'
    )


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'name',
        'last_name',
        'id'
    )


admin.site.register(ECGModel, ECGAdmin)
admin.site.register(LeadsModel, LeadsAdmin)
admin.site.register(UserModel, UserAdmin)

from django.contrib import admin

from gallery import models


class PatientAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('first_name', 'last_name', 'picture', 'deceased')
        }),
    )
    list_display = ('first_name', 'last_name', 'deceased')
    search_fields = ('first_name', 'last_name')


admin.site.register(models.Patient, PatientAdmin)

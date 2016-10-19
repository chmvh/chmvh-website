from django.contrib import admin

from gallery import models


class PatientAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (
                'first_name', 'last_name', 'picture', 'featured', 'deceased'
            )
        }),
    )
    list_display = ('first_name', 'last_name', 'featured', 'deceased')
    list_filter = ('deceased', 'featured')
    search_fields = ('first_name', 'last_name')


admin.site.register(models.Patient, PatientAdmin)

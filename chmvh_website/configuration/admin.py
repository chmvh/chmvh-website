from django.contrib import admin

from solo.admin import SingletonModelAdmin

from configuration import models


class PracticeInfoAdmin(SingletonModelAdmin):
    fieldsets = (
        (None, {
            'fields': (
                'accepting_clients', 'address', 'email', 'phone', 'fax'
            ),
        }),
    )


admin.site.register(models.PracticeInfo, PracticeInfoAdmin)
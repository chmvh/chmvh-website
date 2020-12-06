from django.contrib import admin

from solo.admin import SingletonModelAdmin

from configuration import models


class PracticeInfoAdmin(SingletonModelAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "accepting_clients",
                    "address",
                    "email",
                    "phone",
                    "fax",
                ),
            },
        ),
        (
            "Edit Conditional Messages",
            {
                "classes": ("collapse",),
                "fields": (
                    "accepting_clients_text",
                    "not_accepting_clients_text",
                ),
            },
        ),
    )


admin.site.register(models.PracticeInfo, PracticeInfoAdmin)

from django.contrib import admin

from gallery import models


class PatientAdmin(admin.ModelAdmin):
    actions = ("make_featured", "remove_featured")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "description",
                    "picture",
                    "featured",
                    "deceased",
                )
            },
        ),
    )
    list_display = ("first_name", "last_name", "featured", "deceased")
    list_filter = ("deceased", "featured")
    search_fields = ("first_name", "last_name")

    def make_featured(self, request, queryset):
        rows_updated = queryset.update(featured=True)

        if rows_updated == 1:
            message_bit = "1 pet"
        else:
            message_bit = "{} pets".format(rows_updated)

        self.message_user(
            request, "{} marked as featured.".format(message_bit)
        )

    make_featured.short_description = "Mark selected pets as featured"

    def remove_featured(self, request, queryset):
        rows_updated = queryset.update(featured=False)

        if rows_updated == 1:
            message_bit = "1 pet"
        else:
            message_bit = "{} pets".format(rows_updated)

        self.message_user(
            request, "{} removed from featured list.".format(message_bit)
        )

    remove_featured.short_description = "Remove selected from featured pets"


admin.site.register(models.Patient, PatientAdmin)

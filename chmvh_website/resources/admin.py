from django.contrib import admin

from resources import models


class CategoryAdmin(admin.ModelAdmin):
    fieldsets = ((None, {"fields": ("title", "important")}),)
    list_display = ("title", "important")
    search_fields = ("title",)


class ResourceAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": ("category", "title", "description")}),
        (
            "Contact Information",
            {"fields": ("address", "email", "phone", "url")},
        ),
    )
    list_display = ("title", "category")
    search_fields = ("title", "category__title", "description", "url")


admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Resource, ResourceAdmin)

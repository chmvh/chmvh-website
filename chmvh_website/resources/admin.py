from django.contrib import admin

from resources import models


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'important')
    search_fields = ('title',)


class ResourceAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('category', 'title', 'description')
        }),
        ('Contact Information', {
            'fields': ('address', 'email', 'phone', 'url')
        }),
    )
    list_display = ('title',)
    search_fields = ('title', 'description', 'url')


admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Resource, ResourceAdmin)

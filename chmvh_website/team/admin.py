from django.contrib import admin

from team import models


class TeamMemberAdmin(admin.ModelAdmin):
    fields = ('name', 'picture', 'bio')
    list_display = ('name',)


admin.site.register(models.TeamMember, TeamMemberAdmin)

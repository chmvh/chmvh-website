from django.views.generic.base import TemplateView

from team import models


class TeamListView(TemplateView):
    template_name = "team/team.html"

    def get_context_data(self, *args, **kwargs):
        context = super(TeamListView, self).get_context_data(*args, **kwargs)

        context["team_members"] = models.TeamMember.objects.all()

        return context

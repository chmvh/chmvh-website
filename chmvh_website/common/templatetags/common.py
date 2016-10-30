from django import template
from django.utils import timezone
from django.utils.html import format_html


register = template.Library()


@register.simple_tag
def copyright_years():
    """
    Generate the years for the copyright text.

    Returns:
        An HTML snippet containing the years for the copyright text.
    """
    cur_year = timezone.now().year

    if cur_year == 2016:
        return str(cur_year)

    return format_html(
        '{} &ndash; {}',
        2016,
        cur_year)

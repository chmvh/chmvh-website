import re

from django import template
from django.utils import timezone
from django.utils.html import format_html
from django.utils.safestring import mark_safe


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


@register.simple_tag
def phone_number(number: str) -> str:
    """
    Replace the spaces in a phone number with non-breaking ones.

    Args:
        number:
            The phone number to format.
    Returns:
        The phone number with spaces replaced with non-breaking spaces.
    """
    return mark_safe(re.sub(r'[\s]+', '&nbsp;', number))

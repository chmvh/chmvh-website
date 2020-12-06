from django.conf import settings


def analytics(request):
    """
    Add GOOGLE_ANALYTICS_ID to the request context.
    """
    return {
        "GOOGLE_ANALYTICS_ID": getattr(settings, "GOOGLE_ANALYTICS_ID", ""),
    }

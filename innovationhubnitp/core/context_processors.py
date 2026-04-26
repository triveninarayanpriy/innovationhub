"""Context processors to make site configuration and navbar links available globally."""
from django.db import OperationalError
from .models import SiteConfiguration, NavbarLink


def site_context(request):
    """
    Add site_config and nav_links to all template contexts.
    
    Gracefully handles database unavailability by returning defaults.
    This prevents page crashes when Supabase/database is unreachable.
    
    Usage in templates:
        {{ site_config.site_name }}
        {{ site_config.vision_statement }}
        {% for link in nav_links %}...{% endfor %}
    """
    try:
        site_config = SiteConfiguration.get_solo()
    except (OperationalError, Exception):
        # If DB is unavailable, return a default config object
        site_config = SiteConfiguration(
            site_name="Innovation Hub",
            vision_statement="Beyond placements: To build a culture at NIT Patna where students learn from each other, explore innovation fearlessly, share knowledge selflessly, and grow into engineers who create solutions — not just resumes.",
            footer_text="© 2026 Innovation Hub NIT Patna • By Students, For Students"
        )
    
    try:
        # Force evaluation of queryset to list to catch DB errors here, not in template
        nav_links = list(NavbarLink.objects.filter(is_active=True))
    except (OperationalError, Exception):
        nav_links = []
    
    return {
        'site_config': site_config,
        'nav_links': nav_links,
    }

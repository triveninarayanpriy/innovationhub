"""Context processors to make site configuration and navbar links available globally."""
from .models import SiteConfiguration, NavbarLink


def site_context(request):
    """
    Add site_config and nav_links to all template contexts.
    
    Usage in templates:
        {{ site_config.site_name }}
        {{ site_config.vision_statement }}
        {% for link in nav_links %}...{% endfor %}
    """
    return {
        'site_config': SiteConfiguration.get_solo(),
        'nav_links': NavbarLink.objects.filter(is_active=True),
    }

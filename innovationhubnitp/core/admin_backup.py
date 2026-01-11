from django.contrib import admin
from .models import SiteConfiguration, NavbarLink, BentoCard


@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(admin.ModelAdmin):
    """Admin interface for Site Configuration (Singleton)."""
    list_display = ['site_name', 'footer_text']
    fieldsets = (
        ('Site Identity', {
            'fields': ('site_name', 'site_logo')
        }),
        ('Content', {
            'fields': ('vision_statement', 'footer_text')
        }),
    )

    def has_add_permission(self, request):
        """Prevent adding more than one instance."""
        return not SiteConfiguration.objects.exists()

    def has_delete_permission(self, request, obj=None):
        """Prevent deletion of the singleton instance."""
        return False


@admin.register(NavbarLink)
class NavbarLinkAdmin(admin.ModelAdmin):
    """Admin interface for Navbar Links."""
    list_display = ['label', 'url', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['label', 'url']
    ordering = ['order']


@admin.register(BentoCard)
class BentoCardAdmin(admin.ModelAdmin):
    """Admin interface for Bento Cards."""
    list_display = ['title', 'icon_name', 'order', 'grid_cols', 'grid_rows', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active', 'grid_cols', 'grid_rows']
    search_fields = ['title', 'description']
    ordering = ['order']
    fieldsets = (
        ('Content', {
            'fields': ('title', 'description', 'icon_name')
        }),
        ('Link & Button', {
            'fields': ('link_url', 'button_text')
        }),
        ('Layout', {
            'fields': ('grid_cols', 'grid_rows', 'bg_color', 'order')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )

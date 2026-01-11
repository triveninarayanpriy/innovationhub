from django.db import models
from django.core.exceptions import ValidationError


class SiteConfiguration(models.Model):
    """Singleton model for site-wide configuration."""
    site_name = models.CharField(max_length=100, default="Innovation Hub")
    site_logo = models.ImageField(upload_to='site/', blank=True, null=True)
    vision_statement = models.TextField(
        default="Beyond placements: To build a culture at NIT Patna where students learn from each other, explore innovation fearlessly, share knowledge selflessly, and grow into engineers who create solutions — not just resumes."
    )
    footer_text = models.CharField(
        max_length=200,
        default="© 2026 Innovation Hub NIT Patna • By Students, For Students"
    )

    class Meta:
        verbose_name = "Site Configuration"
        verbose_name_plural = "Site Configuration"

    def save(self, *args, **kwargs):
        """Ensure only one instance exists (Singleton pattern)."""
        if not self.pk and SiteConfiguration.objects.exists():
            raise ValidationError('There can be only one Site Configuration instance')
        return super().save(*args, **kwargs)

    @classmethod
    def get_solo(cls):
        """Get or create the singleton instance."""
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return self.site_name


class NavbarLink(models.Model):
    """Navigation links for header and footer."""
    label = models.CharField(max_length=50)
    url = models.CharField(max_length=200)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = "Navbar Link"
        verbose_name_plural = "Navbar Links"

    def __str__(self):
        return self.label


class BentoCard(models.Model):
    """Cards for the bento grid homepage layout."""
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon_name = models.CharField(
        max_length=50,
        help_text="Lucide icon name (e.g., 'library', 'users', 'trending-up')"
    )
    link_url = models.CharField(max_length=200, blank=True)
    button_text = models.CharField(max_length=50, blank=True, default="Learn More")
    order = models.IntegerField(default=0)
    grid_cols = models.IntegerField(default=1, help_text="Grid columns span (1-4)")
    grid_rows = models.IntegerField(default=1, help_text="Grid rows span (1-2)")
    bg_color = models.CharField(max_length=50, default="bg-zinc-900/20")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = "Bento Card"
        verbose_name_plural = "Bento Cards"

    def __str__(self):
        return self.title

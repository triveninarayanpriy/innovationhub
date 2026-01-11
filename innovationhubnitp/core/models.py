from django.db import models
from django.core.exceptions import ValidationError


class SiteConfiguration(models.Model):
    """Singleton model for site-wide configuration."""
    site_name = models.CharField(max_length=100, default="Innovation Hub")
    site_logo = models.ImageField(upload_to='site/', blank=True, null=True)
    guidance_video_url = models.URLField(blank=True, help_text="Hero section video link for guidance page")
    guidance_hero_image = models.ImageField(upload_to='guidance/', blank=True, null=True)
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


class GuidanceRoadmap(models.Model):
    """Learning roadmaps and guides for students."""
    CATEGORY_CHOICES = [
        ('ECE', 'Electronics & Communication'),
        ('CSE', 'Computer Science'),
        ('SOFTWARE', 'Software Development'),
        ('HARDWARE', 'Hardware/VLSI'),
        ('STARTUP', 'Startup & Entrepreneurship'),
        ('RESEARCH', 'Research & Academia'),
        ('OTHER', 'Other'),
    ]
    
    title = models.CharField(max_length=200)  # e.g., "VLSI Design Roadmap"
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField(help_text="Brief summary of the roadmap")
    content_link = models.URLField(help_text="Google Drive or Notion link")
    created_by = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Guidance Roadmap"
        verbose_name_plural = "Guidance Roadmaps"
    
    def __str__(self):
        return f"{self.title} ({self.get_category_display()})"


class MentorApplication(models.Model):
    """Applications from seniors to become mentors."""
    BRANCH_CHOICES = [
        ('CSE', 'Computer Science & Engineering'),
        ('ECE', 'Electronics & Communication'),
        ('EE', 'Electrical Engineering'),
        ('ME', 'Mechanical Engineering'),
        ('CE', 'Civil Engineering'),
        ('ARCH', 'Architecture'),
        ('OTHER', 'Other'),
    ]
    
    YEAR_CHOICES = [
        (2, '2nd Year'),
        (3, '3rd Year'),
        (4, '4th Year'),
        (5, 'PG/PhD'),
    ]
    
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    branch = models.CharField(max_length=10, choices=BRANCH_CHOICES)
    year = models.IntegerField(choices=YEAR_CHOICES)
    expertise = models.TextField(help_text="Areas of expertise (e.g., Web Dev, Arduino, ML)")
    linkedin_profile = models.URLField(blank=True)
    github_profile = models.URLField(blank=True)
    why_mentor = models.TextField(help_text="Why do you want to become a mentor?", blank=True)
    mentor_whatsapp = models.CharField(max_length=15, help_text="WhatsApp number (private, not shown publicly)")
    is_approved = models.BooleanField(default=False)
    applied_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-applied_at']
        verbose_name = "Mentor Application"
        verbose_name_plural = "Mentor Applications"
    
    def __str__(self):
        status = "✓ Approved" if self.is_approved else "Pending"
        return f"{self.full_name} ({self.branch} - {self.year}) - {status}"

    def save(self, *args, **kwargs):
        """Persist application then sync an approved mentor into guidance profiles."""
        super().save(*args, **kwargs)
        if self.is_approved:
            self._ensure_mentor_profile()

    def _ensure_mentor_profile(self):
        """Create or update a guidance MentorProfile when approved."""
        try:
            from django.contrib.auth import get_user_model
            from guidance.models import MentorProfile
        except Exception:
            return  # Guidance app not available; fail silently.

        User = get_user_model()
        # Derive a username safely from email.
        base_username = (self.email or '').split('@')[0] or self.email
        user_defaults = {
            'username': base_username,
            'first_name': (self.full_name or '').split(' ')[0],
            'last_name': ' '.join((self.full_name or '').split(' ')[1:]),
            'email': self.email,
        }
        user, created_user = User.objects.get_or_create(email=self.email, defaults=user_defaults)
        if created_user:
            user.set_unusable_password()
            user.save(update_fields=['password'])

        profile_defaults = {
            'branch': self.branch,
            'year': self.year,
            'bio': self.expertise or self.why_mentor,
            'mentor_whatsapp': self.mentor_whatsapp,
            'is_approved': True,
        }
        profile, created_profile = MentorProfile.objects.get_or_create(user=user, defaults=profile_defaults)
        if not created_profile:
            profile.branch = self.branch
            profile.year = self.year
            profile.bio = self.expertise or self.why_mentor
            profile.mentor_whatsapp = self.mentor_whatsapp
            profile.is_approved = True
            profile.save(update_fields=['branch', 'year', 'bio', 'mentor_whatsapp', 'is_approved'])


class Inquiry(models.Model):
    """Contact inquiries from students seeking guidance."""
    student_name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    student_whatsapp = models.CharField(max_length=15, help_text="WhatsApp number (visible to mentors)")
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Student Inquiry"
        verbose_name_plural = "Student Inquiries"
    
    def __str__(self):
        return f"{self.student_name} - {self.subject[:50]}"

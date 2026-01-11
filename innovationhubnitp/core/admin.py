from django.contrib import admin
from django.utils.timezone import now
from .models import SiteConfiguration, NavbarLink, BentoCard, GuidanceRoadmap, MentorApplication, Inquiry


@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(admin.ModelAdmin):
    """Admin interface for Site Configuration (Singleton)."""
    list_display = ['site_name', 'footer_text']
    fieldsets = (
        ('Site Identity', {
            'fields': ('site_name', 'site_logo')
        }),
        ('Guidance Hero', {
            'fields': ('guidance_hero_image', 'guidance_video_url')
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


@admin.register(GuidanceRoadmap)
class GuidanceRoadmapAdmin(admin.ModelAdmin):
    """Admin interface for Guidance Roadmaps."""
    list_display = ['title', 'category', 'created_by', 'is_active', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['title', 'description', 'created_by']
    ordering = ['-created_at']
    readonly_fields = ['created_at']
    fieldsets = (
        ('Roadmap Info', {
            'fields': ('title', 'category', 'created_by')
        }),
        ('Content', {
            'fields': ('description', 'content_link')
        }),
        ('Status', {
            'fields': ('is_active', 'created_at')
        }),
    )


@admin.register(MentorApplication)
class MentorApplicationAdmin(admin.ModelAdmin):
    """Admin interface for Mentor Applications."""
    list_display = ['full_name', 'branch', 'year', 'approval_status', 'applied_at']
    list_filter = ['is_approved', 'branch', 'year', 'applied_at']
    search_fields = ['full_name', 'email', 'expertise']
    ordering = ['-applied_at']
    readonly_fields = ['applied_at', 'reviewed_at']
    actions = ['approve_mentors', 'reject_mentors']
    
    fieldsets = (
        ('Personal Info', {
            'fields': ('full_name', 'email', 'branch', 'year')
        }),
        ('Expertise', {
            'fields': ('expertise', 'why_mentor')
        }),
        ('Profiles', {
            'fields': ('linkedin_profile', 'github_profile')
        }),
        ('Admin Status', {
            'fields': ('is_approved', 'applied_at', 'reviewed_at')
        }),
    )
    
    def approval_status(self, obj):
        """Display approval status with icon."""
        if obj.is_approved:
            return '✓ Approved'
        return '⏳ Pending'
    approval_status.short_description = 'Status'
    
    def approve_mentors(self, request, queryset):
        """Bulk approve mentor applications."""
        updated = queryset.update(is_approved=True, reviewed_at=now())
        self.message_user(request, f'{updated} mentors approved successfully.')
    approve_mentors.short_description = 'Approve selected applications'
    
    def reject_mentors(self, request, queryset):
        """Bulk reject (mark unapproved) mentor applications."""
        updated = queryset.update(is_approved=False, reviewed_at=now())
        self.message_user(request, f'{updated} mentors rejected/reset.')
    reject_mentors.short_description = 'Reject/Reset selected applications'


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    """Admin interface for Student Inquiries."""
    list_display = ['student_name', 'email', 'subject_preview', 'status_badge', 'created_at']
    list_filter = ['is_resolved', 'created_at']
    search_fields = ['student_name', 'email', 'subject', 'message']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'message_display']
    actions = ['mark_resolved', 'mark_unresolved']
    
    fieldsets = (
        ('Student Info', {
            'fields': ('student_name', 'email')
        }),
        ('Inquiry Details', {
            'fields': ('subject', 'message_display')
        }),
        ('Status', {
            'fields': ('is_resolved', 'created_at')
        }),
    )
    
    def subject_preview(self, obj):
        """Show preview of subject."""
        return obj.subject[:40] + '...' if len(obj.subject) > 40 else obj.subject
    subject_preview.short_description = 'Subject'
    
    def status_badge(self, obj):
        """Display resolution status."""
        return '✓ Resolved' if obj.is_resolved else '⏳ Pending'
    status_badge.short_description = 'Status'
    
    def message_display(self, obj):
        """Display full message as read-only."""
        return obj.message
    message_display.short_description = 'Message'
    
    def mark_resolved(self, request, queryset):
        """Mark inquiries as resolved."""
        updated = queryset.update(is_resolved=True)
        self.message_user(request, f'{updated} inquiries marked as resolved.')
    mark_resolved.short_description = 'Mark selected as resolved'
    
    def mark_unresolved(self, request, queryset):
        """Mark inquiries as unresolved."""
        updated = queryset.update(is_resolved=False)
        self.message_user(request, f'{updated} inquiries marked as unresolved.')
    mark_unresolved.short_description = 'Mark selected as unresolved'

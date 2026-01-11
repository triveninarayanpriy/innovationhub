from django.contrib import admin
from .models import Branch, Subject, Resource


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    """Admin interface for Branches."""
    list_display = ['code', 'name', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'code']
    prepopulated_fields = {'code': ('name',)}


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    """Admin interface for Subjects."""
    list_display = ['code', 'name', 'branch', 'semester', 'is_active']
    list_filter = ['branch', 'semester', 'is_active']
    search_fields = ['name', 'code']
    ordering = ['semester', 'name']
    fieldsets = (
        ('Subject Info', {
            'fields': ('name', 'code', 'branch', 'semester')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    """Admin interface for Resources."""
    list_display = ['title', 'subject', 'resource_type', 'exam_type', 'is_verified', 'is_active', 'uploaded_at']
    list_filter = ['resource_type', 'exam_type', 'is_verified', 'is_active', 'subject__branch', 'subject__semester']
    search_fields = ['title', 'subject__name', 'uploaded_by']
    readonly_fields = ['uploaded_at', 'updated_at']
    ordering = ['-uploaded_at']
    fieldsets = (
        ('Resource Info', {
            'fields': ('subject', 'title', 'description', 'resource_type', 'exam_type')
        }),
        ('Link & Attribution', {
            'fields': ('file_url', 'uploaded_by')
        }),
        ('Metadata', {
            'fields': ('uploaded_at', 'updated_at', 'is_verified', 'is_active'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        qs = super().get_queryset(request)
        return qs.select_related('subject__branch')

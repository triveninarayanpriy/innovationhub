from django.shortcuts import render
from django.views.generic import ListView
from django.db.models import Q, Prefetch
from .models import Branch, Subject, Resource


def vault_list(request):
    """Display resources with filtering by branch and semester."""
    branches = Branch.objects.filter(is_active=True)
    subjects = Subject.objects.filter(is_active=True).select_related('branch')
    # Show all active resources; verified ones get a badge
    resources = Resource.objects.filter(is_active=True).select_related('subject__branch')

    # Get filter parameters
    branch_id = request.GET.get('branch')
    semester = request.GET.get('semester')
    resource_type = request.GET.get('type')

    # Apply filters
    if branch_id:
        subjects = subjects.filter(branch_id=branch_id)
        resources = resources.filter(subject__branch_id=branch_id)

    if semester:
        try:
            semester = int(semester)
            subjects = subjects.filter(semester=semester)
            resources = resources.filter(subject__semester=semester)
        except (ValueError, TypeError):
            pass

    if resource_type:
        resources = resources.filter(resource_type=resource_type)

    # Group resources by subject for better organization
    subject_resources = {}
    for resource in resources:
        subject_id = resource.subject_id
        if subject_id not in subject_resources:
            subject_resources[subject_id] = {
                'subject': resource.subject,
                'resources': []
            }
        subject_resources[subject_id]['resources'].append(resource)

    context = {
        'branches': branches,
        'semesters': range(1, 9),
        'resource_types': Resource.RESOURCE_TYPE_CHOICES,
        'exam_types': Resource.EXAM_TYPE_CHOICES,
        'subject_resources': subject_resources,
        'selected_branch': branch_id,
        'selected_semester': semester,
        'selected_type': resource_type,
        'total_resources': resources.count(),
    }
    return render(request, 'vault.html', context)


class VaultListView(ListView):
    """Class-based view for vault resources."""
    model = Resource
    template_name = 'vault.html'
    context_object_name = 'resources'
    paginate_by = 50

    def get_queryset(self):
        qs = Resource.objects.filter(
            is_active=True
        ).select_related('subject__branch')

        branch_id = self.request.GET.get('branch')
        semester = self.request.GET.get('semester')
        resource_type = self.request.GET.get('type')

        if branch_id:
            qs = qs.filter(subject__branch_id=branch_id)
        if semester:
            try:
                qs = qs.filter(subject__semester=int(semester))
            except (ValueError, TypeError):
                pass
        if resource_type:
            qs = qs.filter(resource_type=resource_type)

        return qs.order_by('-uploaded_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['branches'] = Branch.objects.filter(is_active=True)
        context['semesters'] = range(1, 9)
        context['resource_types'] = Resource.RESOURCE_TYPE_CHOICES
        context['exam_types'] = Resource.EXAM_TYPE_CHOICES
        context['selected_branch'] = self.request.GET.get('branch')
        context['selected_semester'] = self.request.GET.get('semester')
        context['selected_type'] = self.request.GET.get('type')
        return context

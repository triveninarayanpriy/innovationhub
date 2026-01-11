from django.db import models


class Branch(models.Model):
    """Engineering branch/specialization."""
    name = models.CharField(max_length=100, unique=True)  # e.g., "Electronics & Communication"
    code = models.CharField(max_length=10, unique=True)   # e.g., "ECE"
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Branches"

    def __str__(self):
        return f"{self.code} - {self.name}"


class Subject(models.Model):
    """Subject offered in a branch during a semester."""
    name = models.CharField(max_length=200)  # e.g., "Digital Signal Processing"
    code = models.CharField(max_length=20, blank=True)  # e.g., "EC401"
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='subjects')
    semester = models.IntegerField(choices=[(i, f"Sem {i}") for i in range(1, 9)])
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('branch', 'code', 'semester')
        ordering = ['semester', 'name']
        verbose_name_plural = "Subjects"

    def __str__(self):
        return f"{self.name} ({self.code}) - {self.branch.code} - Sem {self.semester}"


class Resource(models.Model):
    """Study resource (PYQ, Notes, Books) for a subject."""
    RESOURCE_TYPE_CHOICES = [
        ('PYQ', 'Previous Year Question'),
        ('NOTES', 'Notes'),
        ('BOOK', 'Book/Reference'),
    ]
    
    EXAM_TYPE_CHOICES = [
        ('MID', 'Mid-Semester'),
        ('END', 'End-Semester'),
        ('QUIZ', 'Quiz'),
        ('NA', 'N/A'),
    ]

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='resources')
    title = models.CharField(max_length=300)  # e.g., "DSP PYQ 2023"
    description = models.TextField(blank=True)
    resource_type = models.CharField(max_length=10, choices=RESOURCE_TYPE_CHOICES)
    exam_type = models.CharField(max_length=10, choices=EXAM_TYPE_CHOICES, default='NA')
    file_url = models.URLField(help_text="Google Drive link or external URL")
    uploaded_by = models.CharField(max_length=100, blank=True, help_text="Name of contributor")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_verified = models.BooleanField(default=False, help_text="Verified by admin")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name_plural = "Resources"
        indexes = [
            models.Index(fields=['subject', 'resource_type']),
            models.Index(fields=['is_active', 'is_verified']),
        ]

    def __str__(self):
        return f"{self.title} ({self.get_resource_type_display()}) - {self.subject.name}"

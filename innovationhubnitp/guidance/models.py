"""Data models for the Senior Guidance portal."""
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


def validate_nitp_email(user):
	"""Ensure user email ends with @nitp.ac.in."""
	email = (user.email or '').lower()
	if not email.endswith('@nitp.ac.in'):
		raise ValidationError('Only @nitp.ac.in emails are allowed.')


class MentorProfile(models.Model):
	"""Profile for approved mentors."""

	BRANCH_CHOICES = [
		('CSE', 'Computer Science'),
		('ECE', 'Electronics & Communication'),
		('EE', 'Electrical Engineering'),
		('ME', 'Mechanical Engineering'),
		('CE', 'Civil Engineering'),
		('ARCH', 'Architecture'),
		('OTHER', 'Other'),
	]

	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	branch = models.CharField(max_length=20, choices=BRANCH_CHOICES)
	year = models.PositiveIntegerField(help_text="Current academic year")
	bio = models.TextField(blank=True)
	mentor_whatsapp = models.CharField(max_length=20, blank=True, help_text="Private mentor WhatsApp number")
	avatar = models.ImageField(upload_to='mentors/', blank=True, null=True)
	is_approved = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-created_at']

	def clean(self):
		validate_nitp_email(self.user)

	def __str__(self):
		return f"Mentor: {self.user.get_full_name() or self.user.username}"


class MentorRequest(models.Model):
	"""Requests from students to mentors."""

	STATUS_PENDING = 'PENDING'
	STATUS_APPROVED = 'APPROVED'
	STATUS_CHOICES = [
		(STATUS_PENDING, 'Pending'),
		(STATUS_APPROVED, 'Approved'),
	]

	student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mentor_requests')
	mentor = models.ForeignKey(MentorProfile, on_delete=models.CASCADE, related_name='requests')
	message = models.TextField()
	student_whatsapp = models.CharField(max_length=20, help_text="Visible to the mentor only")
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
	created_at = models.DateTimeField(auto_now_add=True)
	approved_at = models.DateTimeField(blank=True, null=True)

	class Meta:
		ordering = ['-created_at']
		unique_together = ('student', 'mentor')

	def clean(self):
		# Only validate if student is set (not during unsaved form processing)
		if self.student_id:
			validate_nitp_email(self.student)

	def __str__(self):
		return f"Request from {self.student} to {self.mentor} ({self.get_status_display()})"


class ChatMessage(models.Model):
	"""Chat messages between student and mentor once approved."""

	request = models.ForeignKey(MentorRequest, on_delete=models.CASCADE, related_name='messages')
	sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	message = models.TextField()
	sent_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['sent_at']

	def __str__(self):
		return f"{self.sender} @ {self.sent_at:%Y-%m-%d %H:%M}"

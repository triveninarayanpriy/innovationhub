"""Views for Senior Guidance portal."""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import MentorRequestForm, ChatMessageForm
from .models import MentorProfile, MentorRequest, ChatMessage, validate_nitp_email


def guidance_view(request):
	"""Public listing of approved mentors - no login required for viewing."""
	mentors = MentorProfile.objects.filter(is_approved=True).select_related('user')
	
	# Annotate mentors with approved request IDs for authenticated users
	if request.user.is_authenticated:
		approved_req_map = {
			req.mentor_id: req.id for req in MentorRequest.objects.filter(
				student=request.user,
				status=MentorRequest.STATUS_APPROVED
			)
		}
		for mentor in mentors:
			mentor.student_request_id = approved_req_map.get(mentor.id)
	
	return render(request, 'guidance/guidance_home.html', {
		'approved_mentors': mentors,
	})


@login_required
def request_guidance(request, mentor_id):
	"""Students submit guidance requests to mentors."""
	mentor = get_object_or_404(MentorProfile, pk=mentor_id, is_approved=True)

	try:
		validate_nitp_email(request.user)
	except ValidationError as exc:
		messages.error(request, str(exc))
		return redirect('guidance:guidance_home')

	existing = MentorRequest.objects.filter(student=request.user, mentor=mentor).first()
	if existing:
		if existing.status == MentorRequest.STATUS_APPROVED:
			messages.info(request, 'You already have an approved chat with this mentor.')
			return redirect('guidance:chat', request_id=existing.id)
		messages.info(request, 'You have already requested this mentor. Await approval.')
		return redirect('guidance:guidance_home')

	if request.method == 'POST':
		form = MentorRequestForm(request.POST)
		if form.is_valid():
			mentor_request = form.save(commit=False)
			mentor_request.student = request.user
			mentor_request.mentor = mentor
			mentor_request.full_clean()
			mentor_request.save()
			messages.success(request, 'Request sent. The mentor will review and approve.')
			return redirect('guidance:guidance_home')
	else:
		form = MentorRequestForm()

	return render(request, 'guidance/request_guidance.html', {
		'mentor': mentor,
		'form': form,
	})


@login_required
def mentor_dashboard(request):
	"""Mentor view to see and approve requests."""
	profile = get_object_or_404(MentorProfile, user=request.user)

	if not profile.is_approved:
		messages.error(request, 'Your mentor profile is pending approval.')
		return redirect('guidance:guidance_home')

	if request.method == 'POST':
		req_id = request.POST.get('approve_id')
		if req_id:
			mentor_request = get_object_or_404(MentorRequest, id=req_id, mentor=profile)
			mentor_request.status = MentorRequest.STATUS_APPROVED
			mentor_request.approved_at = timezone.now()
			mentor_request.save(update_fields=['status', 'approved_at'])
			messages.success(request, 'Request approved. Chat is now open.')
			return redirect('guidance:mentor_dashboard')

	pending_requests = profile.requests.filter(status=MentorRequest.STATUS_PENDING).select_related('student')
	approved_requests = profile.requests.filter(status=MentorRequest.STATUS_APPROVED).select_related('student')

	return render(request, 'guidance/mentor_dashboard.html', {
		'pending_requests': pending_requests,
		'approved_requests': approved_requests,
	})


@login_required
def chat_view(request, request_id):
	"""Chat between student and mentor after approval."""
	mentor_request = get_object_or_404(MentorRequest.objects.select_related('mentor__user', 'student'), id=request_id)

	if mentor_request.status != MentorRequest.STATUS_APPROVED:
		messages.error(request, 'Chat is available only after approval.')
		return redirect('guidance:guidance_home')

	allowed_users = {mentor_request.student_id, mentor_request.mentor.user_id}
	if request.user.id not in allowed_users:
		messages.error(request, 'You do not have access to this chat.')
		return redirect('guidance:guidance_home')

	messages_qs = mentor_request.messages.select_related('sender')

	if request.method == 'POST':
		form = ChatMessageForm(request.POST)
		if form.is_valid():
			chat_message = form.save(commit=False)
			chat_message.sender = request.user
			chat_message.request = mentor_request
			chat_message.save()
			return redirect('guidance:chat', request_id=mentor_request.id)
	else:
		form = ChatMessageForm()

	return render(request, 'guidance/chat.html', {
		'mentor_request': mentor_request,
		'messages': messages_qs,
		'form': form,
	})

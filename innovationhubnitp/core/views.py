from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db import OperationalError
from .models import BentoCard, MentorApplication, Inquiry
from .forms import MentorApplicationForm, InquiryForm


class HomeView(TemplateView):
    """Homepage view with bento cards."""
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['bento_cards'] = BentoCard.objects.filter(is_active=True)
        except (OperationalError, Exception):
            # Gracefully handle database unavailability
            context['bento_cards'] = []
        return context


def home(request):
    """Simple function-based view for homepage."""
    try:
        bento_cards = BentoCard.objects.filter(is_active=True)
    except (OperationalError, Exception):
        # Gracefully handle database unavailability
        bento_cards = []
    
    context = {
        'bento_cards': bento_cards
    }
    return render(request, 'home.html', context)


def apply_mentor(request):
    """View for mentor application form."""
    if request.method == 'POST':
        form = MentorApplicationForm(request.POST)
        if form.is_valid():
            try:
                application = form.save()
                messages.success(
                    request,
                    f'Thank you, {application.full_name}! Your mentor application has been submitted. '
                    'We\'ll review it and get back to you soon.'
                )
                return redirect('core:home')
            except (OperationalError, Exception) as e:
                messages.error(request, 'Database error: Unable to save application. Please try again.')
    else:
        form = MentorApplicationForm()
    
    return render(request, 'apply_mentor.html', {'form': form})


def send_inquiry(request):
    """View for student inquiry/contact form."""
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            try:
                inquiry = form.save()
                messages.success(
                    request,
                    f'Thank you, {inquiry.student_name}! Your message has been received. '
                    'We\'ll get back to you soon.'
                )
                return redirect('core:home')
            except (OperationalError, Exception) as e:
                messages.error(request, 'Database error: Unable to save inquiry. Please try again.')
    else:
        form = InquiryForm()
    
    return render(request, 'send_inquiry.html', {'form': form})


def _redirect_after_login(user):
    """Redirect user to dashboard based on role (mentor vs student)."""
    from guidance.models import MentorProfile
    try:
        mentor_profile = MentorProfile.objects.get(user=user)
        if mentor_profile.is_approved:
            return redirect('guidance:mentor_dashboard')
    except (MentorProfile.DoesNotExist, OperationalError, Exception):
        pass
    # Default to student guidance view
    return redirect('guidance:guidance_home')


def login_view(request):
    """Login page for students and mentors with @nitp.ac.in email."""
    if request.user.is_authenticated:
        return _redirect_after_login(request.user)
    
    if request.method == 'POST':
        email = request.POST.get('email', '').lower()
        password = request.POST.get('password', '')
        
        # Validate @nitp.ac.in email
        if not email.endswith('@nitp.ac.in'):
            messages.error(request, 'Please use your @nitp.ac.in email address.')
            return render(request, 'login.html')
        
        # Authenticate using email as username (Django default)
        try:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            try:
                user = User.objects.get(email=email)
                user = authenticate(request, username=user.username, password=password)
                if user is not None:
                    login(request, user)
                    return _redirect_after_login(user)
                else:
                    messages.error(request, 'Invalid email or password.')
            except User.DoesNotExist:
                messages.error(request, 'No account found with this email. Please sign up first.')
                return render(request, 'login.html')
        except (OperationalError, Exception) as e:
            messages.error(request, 'Database error: Unable to process login. Please try again.')
            return render(request, 'login.html')
    
    return render(request, 'login.html')


def logout_view(request):
    """Logout view."""
    from django.contrib.auth import logout
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('guidance:guidance_home')


def health(request):
    """Lightweight health check endpoint for uptime pings."""
    return HttpResponse('ok')

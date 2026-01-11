"""Forms for Guidance & Mentorship system."""
from django import forms
from .models import MentorApplication, Inquiry


class MentorApplicationForm(forms.ModelForm):
    """Form for seniors to apply as mentors."""
    
    class Meta:
        model = MentorApplication
        fields = ['full_name', 'email', 'branch', 'year', 'expertise', 
                  'linkedin_profile', 'github_profile', 'why_mentor', 'mentor_whatsapp']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'w-full bg-zinc-900 border border-zinc-800 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-yellow-500',
                'placeholder': 'Your Full Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full bg-zinc-900 border border-zinc-800 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-yellow-500',
                'placeholder': 'your.email@nitp.ac.in'
            }),
            'branch': forms.Select(attrs={
                'class': 'w-full bg-zinc-900 border border-zinc-800 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-yellow-500'
            }),
            'year': forms.Select(attrs={
                'class': 'w-full bg-zinc-900 border border-zinc-800 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-yellow-500'
            }),
            'expertise': forms.Textarea(attrs={
                'class': 'w-full bg-zinc-900 border border-zinc-800 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-yellow-500',
                'placeholder': 'e.g., Web Development, Machine Learning, Arduino, VLSI...',
                'rows': 3
            }),
            'linkedin_profile': forms.URLInput(attrs={
                'class': 'w-full bg-zinc-900 border border-zinc-800 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-yellow-500',
                'placeholder': 'https://linkedin.com/in/yourprofile'
            }),
            'github_profile': forms.URLInput(attrs={
                'class': 'w-full bg-zinc-900 border border-zinc-800 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-yellow-500',
                'placeholder': 'https://github.com/yourusername'
            }),
            'why_mentor': forms.Textarea(attrs={
                'class': 'w-full bg-zinc-900 border border-zinc-800 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-yellow-500',
                'placeholder': 'Tell us why you want to mentor juniors...',
                'rows': 4
            }),
            'mentor_whatsapp': forms.TextInput(attrs={
                'class': 'w-full bg-zinc-900 border border-zinc-800 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-yellow-500',
                'placeholder': '+91 XXXXX XXXXX (Private - not shown publicly)',
                'type': 'tel'
            }),
        }
        labels = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'branch': 'Branch',
            'year': 'Current Year',
            'expertise': 'Your Expertise',
            'linkedin_profile': 'LinkedIn Profile (Optional)',
            'github_profile': 'GitHub Profile (Optional)',
            'why_mentor': 'Why do you want to mentor? (Optional)',
            'mentor_whatsapp': 'WhatsApp Number (Private)',
        }

    def clean_email(self):
        email = (self.cleaned_data.get('email') or '').lower()
        if not email.endswith('@nitp.ac.in'):
            raise forms.ValidationError("Please use your @nitp.ac.in email address.")
        return email


class InquiryForm(forms.ModelForm):
    """Form for students to send inquiries/contact requests."""
    
    class Meta:
        model = Inquiry
        fields = ['student_name', 'email', 'subject', 'message', 'student_whatsapp']
        widgets = {
            'student_name': forms.TextInput(attrs={
                'class': 'w-full bg-zinc-900 border border-zinc-800 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-yellow-500',
                'placeholder': 'Your Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full bg-zinc-900 border border-zinc-800 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-yellow-500',
                'placeholder': 'your.email@example.com'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'w-full bg-zinc-900 border border-zinc-800 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-yellow-500',
                'placeholder': 'e.g., Career Guidance for ECE'
            }),
            'message': forms.Textarea(attrs={
                'class': 'w-full bg-zinc-900 border border-zinc-800 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-yellow-500',
                'placeholder': "Describe what guidance you're looking for...",
                'rows': 6
            }),
            'student_whatsapp': forms.TextInput(attrs={
                'class': 'w-full bg-zinc-900 border border-zinc-800 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-yellow-500',
                'placeholder': '+91 XXXXX XXXXX (Will be shared with mentors)',
                'type': 'tel'
            }),
        }
        labels = {
            'student_name': 'Your Name',
            'email': 'Email Address',
            'subject': 'Subject',
            'message': 'Your Message',
            'student_whatsapp': 'WhatsApp Number (Shared with Mentors)',
        }

    def clean_email(self):
        email = (self.cleaned_data.get('email') or '').lower()
        if not email.endswith('@nitp.ac.in'):
            raise forms.ValidationError("Please use your @nitp.ac.in email address.")
        return email

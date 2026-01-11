"""Forms for the Senior Guidance portal."""
from django import forms
from .models import MentorRequest, ChatMessage


class MentorRequestForm(forms.ModelForm):
    """Students send request to mentors with contact number."""

    class Meta:
        model = MentorRequest
        fields = ['message', 'student_whatsapp']
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'w-full bg-zinc-900 border border-zinc-800 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-blue-500',
                'rows': 4,
                'placeholder': 'What do you need help with?'
            }),
            'student_whatsapp': forms.TextInput(attrs={
                'class': 'w-full bg-zinc-900 border border-zinc-800 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-blue-500',
                'type': 'tel',
                'placeholder': '+91 XXXXX XXXXX (Shared only with mentor)'
            }),
        }
        labels = {
            'message': 'Your Message',
            'student_whatsapp': 'WhatsApp Number (mentor can see this)',
        }


class ChatMessageForm(forms.ModelForm):
    """Simple chat message form."""

    class Meta:
        model = ChatMessage
        fields = ['message']
        widgets = {
            'message': forms.TextInput(attrs={
                'class': 'w-full bg-zinc-900 border border-zinc-800 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-blue-500',
                'placeholder': 'Type a message...'
            })
        }
        labels = {'message': ''}

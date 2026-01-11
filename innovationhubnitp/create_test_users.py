"""
Script to create test users and mentor profiles for testing
Run: python create_test_users.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'innovationhubnitp.settings')
django.setup()

from django.contrib.auth import get_user_model
from guidance.models import MentorProfile

User = get_user_model()

# Create test student user
student_email = 'student@nitp.ac.in'
if not User.objects.filter(email=student_email).exists():
    student = User.objects.create_user(
        username='student',
        email=student_email,
        password='student123',
        first_name='John',
        last_name='Student'
    )
    print(f"✓ Created student user: {student_email} / password: student123")
else:
    print(f"✓ Student user already exists: {student_email}")
    student = User.objects.get(email=student_email)

# Create test mentor user and profile
mentor_email = 'mentor@nitp.ac.in'
if not User.objects.filter(email=mentor_email).exists():
    mentor_user = User.objects.create_user(
        username='mentor',
        email=mentor_email,
        password='mentor123',
        first_name='Jane',
        last_name='Mentor'
    )
    print(f"✓ Created mentor user: {mentor_email} / password: mentor123")
else:
    print(f"✓ Mentor user already exists: {mentor_email}")
    mentor_user = User.objects.get(email=mentor_email)

# Create mentor profile if it doesn't exist
if not MentorProfile.objects.filter(user=mentor_user).exists():
    mentor_profile = MentorProfile.objects.create(
        user=mentor_user,
        branch='CSE',
        year=4,
        bio='Experienced mentor in Web Development and Machine Learning',
        mentor_whatsapp='+91 9876543210',
        is_approved=True
    )
    print(f"✓ Created mentor profile for {mentor_email}")
else:
    print(f"✓ Mentor profile already exists for {mentor_email}")

print("\n" + "="*60)
print("Test Credentials:")
print("="*60)
print("\nSTUDENT LOGIN:")
print(f"  Email: student@nitp.ac.in")
print(f"  Password: student123")
print("\nMENTOR LOGIN:")
print(f"  Email: mentor@nitp.ac.in")
print(f"  Password: mentor123")
print("="*60)

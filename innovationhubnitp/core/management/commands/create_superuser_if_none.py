from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from decouple import config

User = get_user_model()

class Command(BaseCommand):
    help = 'Create a superuser if none exists'

    def handle(self, *args, **options):
        if not User.objects.filter(is_superuser=True).exists():
            username = config('DJANGO_SUPERUSER_USERNAME', default='admin')
            email = config('DJANGO_SUPERUSER_EMAIL', default='admin@innovationhub.com')
            password = config('DJANGO_SUPERUSER_PASSWORD', default='admin123')
            
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" created successfully!'))
        else:
            self.stdout.write(self.style.WARNING('Superuser already exists.'))

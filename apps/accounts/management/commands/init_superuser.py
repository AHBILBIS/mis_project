import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = "Creates an initial superuser if it does not exist"

    def handle(self, *args, **options):
        User = get_user_model()
        username = os.getenv("DJANGO_SUPERUSER_USERNAME", "admin")
        email = os.getenv("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
        password = os.getenv("DJANGO_SUPERUSER_PASSWORD", "AdminPass123!")

        if not User.objects.filter(username=username).exists():
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            if hasattr(user, "role"):
                user.role = "ADMIN"
                user.save()
            self.stdout.write(self.style.SUCCESS(f"Superuser \"{username}\" created successfully!"))
        else:
            self.stdout.write(self.style.WARNING(f"Superuser \"{username}\" already exists."))

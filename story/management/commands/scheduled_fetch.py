from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from story.views import fetch_stories

User = get_user_model()


class Command(BaseCommand):
    help = "Fetch RSS stories"

    def handle(self, *args, **kwargs):
        for user in User.objects.select_related("company"):
            fetch_stories(user)

        self.stdout.write(self.style.SUCCESS("Stories fetched"))

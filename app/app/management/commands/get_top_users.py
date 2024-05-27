from app.models import Profile

from django.core.management.base import BaseCommand
from django.core.cache import cache


class Command(BaseCommand):
    help = 'Calculate top users'

    def handle(self, *args, **options):
        top_users = Profile.objects.get_best_profiles()
        cache.set('top_users', top_users, 80)

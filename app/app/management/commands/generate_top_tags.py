from app.models import Tag

from django.core.management.base import BaseCommand
from django.core.cache import cache


class Command(BaseCommand):
    help = 'Calculate top tags'

    def handle(self, *args, **options):
        top_users = Tag.objects.get_popular_tags()
        cache.set('top_tags', top_users, 80)

from django.core.management import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Clear database schema'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            cursor.execute("DROP SCHEMA public CASCADE;")
            cursor.execute("CREATE SCHEMA public;")

"""
Django custom command for checking if the database is available.
if te database is available, then the django app "app" can continue

"""

from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options:):
        pass
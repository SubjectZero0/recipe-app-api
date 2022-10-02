"""
Django custom command for checking if the database is available.
if the database is available, then the django app "app" can continue

"""

from django.core.management.base import BaseCommand
import time

from psycopg2 import OperationalError as Psycopg2Error
from django.db.utils import OperationalError


class Command(BaseCommand):
    """django command to wait for database to be ready"""
    def handle(self, *args, **options):

        self.stdout.write('Waiting for database...') #print message

        db_up = False #initially database is unavailable

        #Make a loop that checks if the database is available every 1 sec
        while db_up is False:
            try:
                self.check(databases=['default']) #if the check fails, raise the exceptions
                db_up = True #if the exceptions arent raised, database is available
            except (Psycopg2Error, OperationalError):
                self.stdout.write('Database unavailable. Waiting 1 sec')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database Available!'))
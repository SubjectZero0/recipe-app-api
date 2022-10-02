"""
Run test for 'wait_for_db' command
"""

from unittest.mock import patch

from psycopg2 import OperationalError as Psycopg2Error

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase

@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test commands"""

    def test_wait_for_db_ready(self, patched_check):
        """test for waiting for db, if db is ready"""
        patched_check.return_value = True #mock the check to be true

        call_command('wait_for_db') #call the custom command

        #check that its called once with the right db
        patched_check.assert_called_once_with(database=['default']) 

    @patch('time.sleep') #mock the passing of time between tests without delaying the test
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for db when getting OperationalError"""

        #mock the check to raise 5 errors and a final True
        patched_check.side_effect = [Psycopg2Error] *2 + [OperationalError] * 3 + [True] 

        call_command('wait _for_db') #call the custom command

        #check that the command was called 6 times
        self.assertEqual(patched_check.call_count, 6) 

        #check that its called with the right db
        patched_check.assert_called_with(database=['default']) 
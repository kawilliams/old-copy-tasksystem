from django.test import TestCase
from django.db import connections
from django.db.utils import OperationalError

class DatabaseConfigTest(TestCase):
    def test_database_connection(self):
        db_conn = connections['default']
        try:
            c = db_conn.cursor()
            c.execute('SELECT 1')  # Simple query to test the connection
            self.assertTrue(c.fetchone()[0] == 1)
        except OperationalError:
            self.fail("KATY -- Database connection failed")
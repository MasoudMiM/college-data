import unittest
import sys
sys.path.append('/home/masoudmim/Documents/Projects/college-data')

from ipeds_college_data.data_extraction import database

#### global variables
HOST='localhost'
USER='root'
PASSWORD= 'password'
DATABASE= 'IPEDS200405'
TABLE_NAME = 'C2004_A'

class TestDatabaseFunctions(unittest.TestCase):
    def test_database_connection(self):
        # Test whether the database connection is successful
        db = database.DatabaseConnection(HOST, USER, PASSWORD, DATABASE)
        self.assertIsNotNone(db.connect())
        db.close()

    def test_data_extraction(self):
        # Test the extraction of data from the database
        db = database.DatabaseConnection(HOST, USER, PASSWORD, DATABASE)
        db.connect()
        data = db.execute_query(f"SELECT * FROM {TABLE_NAME} LIMIT 10;")
        self.assertIsInstance(data, list)
        # Add more specific tests for the extracted data if needed
        db.close()

if __name__ == '__main__':
    unittest.main()

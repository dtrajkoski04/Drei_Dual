import pytest
from flask_testing import TestCase

from src import flaskAPI
from src.flaskAPI import get_db_connection
class MyTest(TestCase):
    def create_app(self):
        flaskAPI.app.config['TESTING'] = True
        return flaskAPI

    def setUp(self):
        """Prepare environment for testing."""
        self.db = get_db_connection()
        self.db.execute("CREATE TABLE IF NOT EXISTS customers (customer_id INTEGER PRIMARY KEY, first_name TEXT, last_name TEXT, company TEXT, city TEXT, sales_2021 INTEGER, sales_2022 INTEGER)")
        self.db.execute("INSERT INTO customers (customer_id, first_name, last_name, company, city, sales_2021, sales_2022) VALUES (1, 'John', 'Doe', 'Company X', 'New York', 100, 150)")
        self.db.execute("INSERT INTO customers (customer_id, first_name, last_name, company, city, sales_2021, sales_2022) VALUES (2, 'Jane', 'Doe', 'Company Y', 'Los Angeles', 200, 250)")
        self.db.commit()
        self._pre_setup()

    def tearDown(self):
        """Clean up after tests."""
        self.db.execute("DROP TABLE customers")
        self.db.close()

    def test_customer_retrieval(self):
        response = self.client.get('/customers')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 2)

    def test_filtered_customer_retrieval(self):
        response = self.client.get('/customers?filter_type=city&filter_value=New')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)
        self.assertEqual(response.json[0]['city'], 'New York')

    def test_sorted_customer_retrieval(self):
        response = self.client.get('/customers?sort_by=first_name&sort_order=desc')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json[0]['first_name'] >= response.json[1]['first_name'])

    def test_sales_data_retrieval(self):
        response = self.client.get('/sales_data?customer_id=1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json['sales_shares']), 1)
        self.assertEqual(response.json['sales_shares'][0]['customer_id'], 1)
        self.assertEqual(response.json['sales_shares'][0]['2021_share'], 40.0)
        self.assertEqual(response.json['sales_shares'][0]['2022_share'], 60.0)

if __name__ == '__main__':
    pytest.main()

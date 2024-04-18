import pytest
from src.app import app

# Fixture to create a test client for the Flask application
@pytest.fixture
def client():
    # Provides a test client for the app, i.e., a simulated browser
    with app.test_client() as client:
        yield client  # `yield` is used to provide the client for the duration of the test

# Test case to verify that the customer list can be retrieved
def test_customer_list_retrieval(client):
    """Test retrieval of customer list."""
    # Sends a GET request to the '/customers' route
    response = client.get('/customers')
    # Asserts that the response status code is 200 (HTTP OK)
    assert response.status_code == 200
    # Asserts that the response contains a list
    assert isinstance(response.json, list)

# Test case to verify that the sorting by first name works correctly
def test_sorting(client):
    """Test sorting by name."""
    # Sends a GET request with parameters to sort by first name in ascending order
    response = client.get('/customers?sort_by=first_name&sort_order=ASC')
    # Asserts that the HTTP response status is OK
    assert response.status_code == 200
    # Extracts first names from the response and checks if they are sorted correctly
    names = [customer['first_name'] for customer in response.json]
    # The sorted list of names should be the same as the list of names
    assert names == sorted(names)

# Test case to verify that filtering by city works correctly
def test_filtering(client):
    """Test filtering by city 'Cindychester' """
    # Sends a GET request to filter customers by city 'New York'
    response = client.get('/customers?filter_type=city&filter_value=New York')
    # Checks that the server responds with a status code of 200
    assert response.status_code == 200
    # Ensures that all entries in the response have the city set to 'Cindychester'
    all_active = all(customer['city'] == 'Cindychester' for customer in response.json)
    # Asserts that all entries meet the filter criteria
    assert all_active

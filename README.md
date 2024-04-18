# DREI Flask Application

## Project Overview
This project is a Flask-based web application that displays customer data and sales details. The system allows users to view, sort, and filter customer data through a user-friendly interface. The backend serves data from a SQLite database which is setup using a provided Python script from a CSV file.

## Directory Structure

- **`/DB`**: Contains the Python script to convert CSV data into a SQLite database for the application's use.
- **`/src`**: Houses the main Flask application and the UI files
- **`/test`**: Includes test cases for both the backend and frontend, ensuring the application functions as expected.

## Getting Started

### Prerequisites
Ensure you have Python and Flask installed on your system. You can install Flask using pip:
```bash
pip install Flask
```

### Running the Application

To start the service, navigate to the `FlaskApplication/src`directory and run:

```bash
python3 app.py
```

This command starts the Flask server on `127.0.0.1`.

### Using the Executable Release

1. **Downloading the Release Page:**
- Navigate to GitHub Repository
- Click on "Releases"
- Download the Executable of the Release Version

2. **Running the Executable**
- **Windows Users:**
	- Double-click the downloaded .exe file to run the application.
	-  If a security warning appears, click “More Info” and then “Run Anyway” to proceed.
- **Mac Users:**
	- Right-click the downloaded file and select “Open” to bypass the security warning that appears for unrecognized apps.
- **Linux Users:**
	- Open a terminal window.
	-  Navigate to the download directory.
	- Make the file executable by running chmod +x YourApplicationName.

•  Execute the application by typing ./YourApplicationName.

### Endpoints

-   **`/`** (Home): Displays the UI for viewing and interacting with customer data.
-   **`/details`**: Shows sales details for individual customers.
-   **`/customers`**: Displays customer data in JSON format directly from the database.
-   **`/sales_data`**: Provides sales data for each customer in JSON format.

## Testing

### Backend Testing with Pytest

To run the backend tests using purest, follow these steps:

1. Navigate to the root directory
2. Install the required packages if not already installed:
`pip install pytest flask_testing`
3. Run the tests
`pytest test_app.py`

This will execute all defined tests in the test suite, testing various backend functionalities like API responses and data processing.

### Frontend testing with cypress

To set up Cypress for running end-to-end tests, you'll need first to install the necessary dependencies. Run the following command in your project directory:

`npm install cypress`

**Running Tests:**

To open Cypress and run the tests interactively, use following command:

`npx cypress open`

This will open the Cypress Test Runner, where you can run individual test suites interactively.

**Test File:**

The file is located in `cypress/e2e` directory as a `.cy.js` File.

from flask import Flask, request, jsonify, render_template
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)   # Enables Cross-Origin Resource Sharing for all endpoints

# Route to render the main dashboard page from templates
@app.route('/')
def index():
    return render_template('index.html')

# Route to render the details page that likely contains more specific data visualization
@app.route('/details')
def details():
    return render_template('details.html')

# Function to establish a connection to the SQLite database
def get_db_connection():
    conn = sqlite3.connect('../DB/customer_sales.db')  # Path to your database file
    conn.row_factory = sqlite3.Row  # Configures cursor to return rows as dictionaries
    return conn

# Route to fetch customer data, with filtering and sorting options
@app.route('/customers', methods=['GET'])
def get_customers():
    # Retrieves filter and sorting options from query parameters, or uses defaults
    filter_type = request.args.get('filter_type', default="first_name")
    filter_value = request.args.get('filter_value', default="")
    sort_by = request.args.get('sort_by', default="customer_id")
    sort_order = request.args.get('sort_order', default="ASC").upper()

    # Protects against SQL injection by validating filter type
    valid_filters = ['first_name', 'last_name', 'company', 'city']
    if filter_type not in valid_filters:
        return jsonify({'error': 'Invalid filter type provided'}), 400

    # SQL query for retrieving customers, safely inserting filter type and using placeholders for values
    query = f"""
    SELECT * FROM customers
    WHERE {filter_type} LIKE ?
    ORDER BY {sort_by} {sort_order}
    """

    conn = get_db_connection()
    cursor = conn.cursor()
    # Executes the query with user-provided filter value, surrounded by % for partial matching
    cursor.execute(query, ('%' + filter_value + '%',))
    customers = cursor.fetchall()
    conn.close()

    # Converts row objects to dictionaries to make them serializable
    return jsonify([dict(customer) for customer in customers])

# Route to fetch sales data, possibly for building charts or further analysis
@app.route('/sales_data', methods=['GET'])
def get_sales_data():
    customer_id = request.args.get('customer_id')
    conn = get_db_connection()
    cursor = conn.cursor()

    # Basic query to retrieve sales data from the customers table
    query = """
    SELECT customer_id, first_name, last_name, sales_2021, sales_2022,
           (sales_2021 + sales_2022) as total_sales
    FROM customers
    """

    # Modifies query to filter by customer_id if provided
    if customer_id:
        query += " WHERE customer_id = ?"
        cursor.execute(query, (customer_id,))
    else:
        cursor.execute(query)

    sales_data = cursor.fetchall()
    conn.close()

    # Processes each row to compute sales shares for pie charts
    sales_shares = []
    for row in sales_data:
        total_customer_sales = row['sales_2021'] + row['sales_2022']
        if total_customer_sales > 0:
            sales_shares.append({
                'customer_id': row['customer_id'],
                'name': f"{row['first_name']} {row['last_name']}",
                '2021_share': row['sales_2021'] / total_customer_sales * 100,
                '2022_share': row['sales_2022'] / total_customer_sales * 100
            })
        else:
            sales_shares.append({
                'customer_id': row['customer_id'],
                'name': f"{row['first_name']} {row['last_name']}",
                '2021_share': 0,
                '2022_share': 0
            })

    # Prepares data specifically for a line chart of sales over time
    sales_development = [
        {'customer_id': row['customer_id'], 'name': f"{row['first_name']} {row['last_name']}",
         'sales_over_time': {'2021': row['sales_2021'], '2022': row['sales_2022']}}
        for row in sales_data
    ]

    # Returns structured data for front-end to use in charts
    return jsonify({'sales_shares': sales_shares, 'sales_development': sales_development})

# Main entry point for the application, runs the app with debug information
if __name__ == '__main__':
    app.run(debug=True)

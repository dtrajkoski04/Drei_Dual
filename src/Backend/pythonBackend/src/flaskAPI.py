from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Database file path
DB_PATH = '../DB/customer_sales.db'


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # This allows dictionary access to row data
    return conn


@app.route('/customers', methods=['GET'])
def get_customers():
    conn = get_db_connection()
    query = 'SELECT * FROM customers'

    # Handling sorting
    sort_by = request.args.get('sort_by')
    if sort_by in ['first_name', 'last_name', 'country', 'sales_2021', 'sales_2022']:
        query += f' ORDER BY {sort_by}'

    # Executing the query
    customers = conn.execute(query).fetchall()
    conn.close()

    # Converting the result to a list of dicts
    customers_list = [dict(customer) for customer in customers]
    return jsonify(customers_list)


if __name__ == '__main__':
    app.run(debug=True)

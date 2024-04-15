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
    base_query = 'SELECT * FROM customers'
    conditions = []
    params = []

    # Handling sorting
    sort_by = request.args.get('sort_by')
    if sort_by in ['FirstName', 'LastName', 'country', 'sales2021', 'sales2022']:
        sort_order = request.args.get('sort_order', 'ASC').upper()
        if sort_order not in ['ASC', 'DESC']:
            sort_order = 'ASC'
        base_query += f' ORDER BY {sort_by} {sort_order}'

    # Handling filtering
    active_filter = request.args.get('active', 'false').lower()
    if active_filter == 'true':
        conditions.append("sales_2022 > ?")
        params.append(0)  # Assuming active participants have sales greater than 0 in 2022

    # Constructing the final query
    if conditions:
        query = f"{base_query} WHERE {' AND '.join(conditions)}"
    else:
        query = base_query

    # Executing the query
    customers = conn.execute(query, params).fetchall()
    conn.close()

    # Converting the result to a list of dicts
    customers_list = [dict(customer) for customer in customers]
    return jsonify(customers_list)


if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect('../DB/customer_sales.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/customers', methods=['GET'])
def get_customers():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Start with a basic query
    query = 'SELECT * FROM customers'

    # Handle sorting
    sort_by = request.args.get('sort_by')
    if sort_by:
        try:
            cursor.execute(f"SELECT {sort_by} FROM customers LIMIT 1")
        except sqlite3.OperationalError:
            return jsonify({'error': f'No such column: {sort_by}'}), 404

        sort_order = request.args.get('sort_order', 'ASC').upper()
        if sort_order not in ['ASC', 'DESC']:
            sort_order = 'ASC'
        query += f' ORDER BY {sort_by} {sort_order}'

    # Execute the query
    cursor.execute(query)
    customers = cursor.fetchall()
    conn.close()

    # Convert the results to a list of dicts
    customers_list = [dict(customer) for customer in customers]
    return jsonify(customers_list)


if __name__ == '__main__':
    app.run(debug=True)

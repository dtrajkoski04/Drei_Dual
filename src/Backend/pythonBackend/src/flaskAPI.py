from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)   # Implements Cross-Origin-Ressource-Sharing for all endpoints

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


@app.route('/sales_data', methods=['GET'])
def get_sales_data():
    customer_id = request.args.get('customer_id')
    conn = get_db_connection()
    cursor = conn.cursor()

    # Data for the diagrams
    query = """
    SELECT customer_id, first_name, last_name, sales_2021, sales_2022,
           (sales_2021 + sales_2022) as total_sales
    FROM customers
    """

    if customer_id:
        query += " WHERE customer_id = ?"
        cursor.execute(query, (customer_id,))
    else:
        cursor.execute(query)

    sales_data = cursor.fetchall()
    conn.close()

    # Calculating the total sales for each year
    total_sales_2021 = sum([row['sales_2021'] for row in sales_data])
    total_sales_2022 = sum([row['sales_2022'] for row in sales_data])

    # Data for the Pie-Chart
    sales_shares = [
        {'customer_id': row['customer_id'], 'name': f"{row['first_name']} {row['last_name']}",
         '2021_share': row['sales_2021'] / total_sales_2021 * 100,
         '2022_share': row['sales_2022'] / total_sales_2022 * 100}
        for row in sales_data
    ]

    # Data for the Line-Chart
    sales_development = [
        {'customer_id': row['customer_id'], 'name': f"{row['first_name']} {row['last_name']}",
         'sales_over_time': {'2021': row['sales_2021'], '2022': row['sales_2022']}}
        for row in sales_data
    ]

    return jsonify({'sales_shares': sales_shares, 'sales_development': sales_development})



if __name__ == '__main__':
    app.run(debug=True)

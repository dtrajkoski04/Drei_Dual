from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS
from flask import render_template

app = Flask(__name__)
CORS(app)   # Implements Cross-Origin-Ressource-Sharing for all endpoints

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/details')
def details():
    return render_template('details.html')

def get_db_connection():
    conn = sqlite3.connect('../DB/customer_sales.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/customers', methods=['GET'])
def get_customers():
    filter_type = request.args.get('filter_type', default="first_name")
    filter_value = request.args.get('filter_value', default="")
    sort_by = request.args.get('sort_by', default="customer_id")
    sort_order = request.args.get('sort_order', default="ASC").upper()

    # Validate filter_type to prevent SQL injection
    valid_filters = ['first_name', 'last_name', 'company', 'city']
    if filter_type not in valid_filters:
        return jsonify({'error': 'Invalid filter type provided'}), 400

    # Construct query using safe filter_type
    query = f"""
    SELECT * FROM customers
    WHERE {filter_type} LIKE ?
    ORDER BY {sort_by} {sort_order}
    """

    conn = get_db_connection()
    cursor = conn.cursor()
    # Using % around filter_value for partial matching
    cursor.execute(query, ('%' + filter_value + '%',))
    customers = cursor.fetchall()
    conn.close()

    return jsonify([dict(customer) for customer in customers])


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

    # Recalculate the sales shares
    sales_shares = []
    for row in sales_data:
        total_customer_sales = row['sales_2021'] + row['sales_2022']
        if total_customer_sales > 0:  # Prevent division by zero
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

    # Data for the Line-Chart
    sales_development = [
        {'customer_id': row['customer_id'], 'name': f"{row['first_name']} {row['last_name']}",
         'sales_over_time': {'2021': row['sales_2021'], '2022': row['sales_2022']}}
        for row in sales_data
    ]

    return jsonify({'sales_shares': sales_shares, 'sales_development': sales_development})




if __name__ == '__main__':
    app.run(debug=True)

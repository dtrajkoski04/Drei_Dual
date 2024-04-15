import sqlite3
import pandas as pd

# Path to the CSV file
csv_file_path = 'customers_sales_2021_2022.csv'
# Database file path
db_path = 'customer_sales.db'

# Create a connection to the SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create the customers table
cursor.execute('''
CREATE TABLE IF NOT EXISTS customers (
    customer_index INTEGER PRIMARY KEY,
    customer_id TEXT,
    first_name TEXT,
    last_name TEXT,
    company TEXT,
    city TEXT,
    country TEXT,
    phone1 TEXT,
    phone2 TEXT,
    email TEXT,
    subscription_date DATE,
    website TEXT,
    sales_2021 REAL,
    sales_2022 REAL
)
''')

# Read the CSV data, considering the semicolon delimiter
df = pd.read_csv(csv_file_path, delimiter=';', parse_dates=['Subscription Date'], dayfirst=True)

# Rename the DataFrame columns to match the database schema
df.columns = ['customer_index', 'customer_id', 'first_name', 'last_name', 'company', 'city',
              'country', 'phone1', 'phone2', 'email', 'subscription_date', 'website', 'sales_2021', 'sales_2022']

# Insert the data into the SQLite database
df.to_sql('customers', conn, if_exists='replace', index=False, index_label='customer_index')

# Commit changes and close the database connection
conn.commit()
conn.close()

print("Data imported successfully into the SQLite database.")

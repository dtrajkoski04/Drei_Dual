import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('customer_sales.db')
cursor = conn.cursor()

# Fetch and display table schema
cursor.execute("PRAGMA table_info(customers)")
columns = cursor.fetchall()
for col in columns:
    print(col)

# Close the connection
conn.close()

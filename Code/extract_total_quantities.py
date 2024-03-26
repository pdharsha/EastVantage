import sqlite3
import csv
import os

curr_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
db_file_name = "eastVantage.db"
db_file = os.path.join(curr_path, "Database", db_file_name)
output_file_name = "sales_results.csv"
output_file = os.path.join(curr_path, "Output", output_file_name)

# Connect to the SQLite database
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# SQL query to get total quantities of each item bought per customer aged 18-35
sql_query = """
SELECT c.customer_id, c.age, s.item_id, SUM(s.quantity) AS Total_Quantity
FROM customers c
INNER JOIN ( SELECT sl.customer_id, o.quantity, o.item_id FROM sales sl 
INNER JOIN orders o ON sl.sales_id = o.sales_id) s 
ON c.customer_id = s.customer_id
WHERE c.age BETWEEN 18 AND 35 AND s.quantity IS NOT NULL
GROUP BY c.customer_id, s.item_id
HAVING Total_Quantity > 0
"""

# Execute the query
cursor.execute(sql_query)

# Fetch all the results
results = cursor.fetchall()

# Write results to CSV file
with open(output_file, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile, delimiter=';')
    # Write header
    csv_writer.writerow(['Customer', 'Age', 'Item', 'Quantity'])
    # Write rows
    csv_writer.writerows(results)

# Close the database connection
conn.close()

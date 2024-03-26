import pandas as pd
import sqlite3
import os

curr_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
db_file_name = "eastVantage.db"
db_file = os.path.join(curr_path, "Database", db_file_name)
output_file_name = "sales_results_df.csv"
output_file = os.path.join(curr_path, "Output", output_file_name)

# Connect to the SQLite database
conn = sqlite3.connect(db_file)

# SQL query to get total quantities of each item bought per customer aged 18-35
sql_query = """
SELECT c.customer_id, c.age, s.item_id, SUM(s.quantity) AS Total_Quantity
FROM customers c
INNER JOIN ( SELECT sl.customer_id, o.quantity, o.item_id FROM sales sl 
INNER JOIN orders o ON sl.sales_id = o.sales_id) s 
ON c.customer_id = s.customer_id
WHERE c.age BETWEEN 18 AND 35 AND s.quantity IS NOT NULL
GROUP BY c.customer_id, s.item_id
"""

# Read SQL query results into a pandas DataFrame
df = pd.read_sql_query(sql_query, conn)

# Filter out rows with total quantity equal to 0
df = df[df['Total_Quantity'] != 0]

# Write DataFrame to CSV file
df.to_csv(output_file, sep=';', index=False)

# Close the database connection
conn.close()

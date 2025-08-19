import sqlite3

QUERIES_FILE_PATH = "sql/queries_15.sql"
DB_PATH = 'db/lfwms.db'

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Load queries
with open(QUERIES_FILE_PATH, "r") as f:
    sql_script = f.read()

# Split by ; and remove empty lines
queries = [q.strip() for q in sql_script.split(";") if q.strip()]

# Execute each query and print results
for i, query in enumerate(queries, start=1):
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        print(f"\n--- Query {i} ---")
        print(query)
        for row in rows:
            print(row)
    except Exception as e:
        print(f"\nError in Query {i}: {e}")

conn.close()

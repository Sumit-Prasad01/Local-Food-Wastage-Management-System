import sqlite3

QUERIES_FILE_PATH = "sql/queries_15.sql"
DB_PATH = 'sql/lfwms.db'

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

with open(QUERIES_FILE_PATH, "r") as f:
    sql_script = f.read()

cursor.executescript(sql_script)
conn.close()

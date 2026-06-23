import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
try:
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="sherupapa",
        host="localhost",
        port=5432,
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute("CREATE DATABASE events")
    cur.close()
    conn.close()
    print("Database 'events' created successfully!")
except psycopg2.errors.DuplicateDatabase:
    print("Database 'events' already exists. Skipping creation.")
except Exception as e:
    print(f"Error: {e}")

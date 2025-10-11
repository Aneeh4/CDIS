"""
mysql_client.py
---------------
Handles MySQL connections and queries safely for Streamlit & pipelines.
"""

import os
import mysql.connector
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
MYSQL_DB_NAME = os.getenv("MYSQL_DB_NAME", "company_insights")


def get_connection():
    """Creates a new MySQL connection each time."""
    return mysql.connector.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB_NAME
    )


def execute_query(query, params=None):
    """
    Executes a SELECT query and returns list of dicts.
    Each call creates and closes its own connection safely.
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, params or ())
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results


def execute_non_query(query, params=None):
    """
    Executes INSERT/UPDATE/DELETE queries with commit.
    Each call opens and closes a new connection.
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, params or ())
    conn.commit()
    cursor.close()
    conn.close()


def test_connection():
    """Simple check to verify database connectivity."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DATABASE();")
        db_name = cursor.fetchone()
        print(f"✅ Connected to database: {db_name[0]}")
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"❌ Connection failed: {e}")

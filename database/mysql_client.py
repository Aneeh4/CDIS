"""
mysql_client.py
---------------
Creates MySQL client connection to use across the project.
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

# Create MySQL connection
connection = mysql.connector.connect(
    host=MYSQL_HOST,
    port=MYSQL_PORT,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    database=MYSQL_DB_NAME
)

cursor = connection.cursor(dictionary=True)  # results as dicts

def execute_query(query, params=None):
    """Run SELECT queries and return results as list of dicts."""
    cursor.execute(query, params or ())
    return cursor.fetchall()

def execute_non_query(query, params=None):
    """Run INSERT/UPDATE/DELETE queries and commit changes."""
    cursor.execute(query, params or ())
    connection.commit()

def close_connection():
    cursor.close()
    connection.close()

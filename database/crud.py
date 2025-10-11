"""
crud.py
-------
Implements Create, Read, Update, Delete operations for MySQL tables.
Used by loaders and pipelines to insert/retrieve structured data.
"""

from database.mysql_client import execute_query, execute_non_query

# Table name for non-financial data
TABLE_NAME = "non_financial_data"

def create_table():
    query = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        id INT AUTO_INCREMENT PRIMARY KEY,
        company VARCHAR(255),
        quarter VARCHAR(10),
        year VARCHAR(10),
        category VARCHAR(100),
        title TEXT,
        body TEXT,
        published_date DATE,
        url TEXT UNIQUE
    )
    """
    execute_non_query(query)




def insert_non_financial_data(record):
    """
    Inserts a single news/event record into non_financial_data table.
    Prevents duplicates using url as UNIQUE key.
    """
    query = f"""
    INSERT INTO {TABLE_NAME} (company, quarter, year, category, title, body, published_date, url)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        company=VALUES(company),
        quarter=VALUES(quarter),
        year=VALUES(year),
        category=VALUES(category),
        title=VALUES(title),
        body=VALUES(body),
        published_date=VALUES(published_date)
    """
    params = (
        record.get("company"),
        record.get("quarter", "").upper(),
        str(record.get("year")),
        record.get("category"),
        record.get("title"),
        record.get("body"),
        record.get("date"),   
        record.get("url"),
    )


    execute_non_query(query, params)
    print(f"Inserted/Updated: {record['title']}")


def get_non_financial_data(company, quarter, year, news_type=None):
    """
    Fetches news/event records from non_financial_data table
    based on filters (company, quarter, year, optional news_type).
    """
    query = f"""
    SELECT company, quarter, year, category, title, url
    FROM {TABLE_NAME}
    WHERE company = %s AND quarter = %s AND year = %s
    """
    params = [company, quarter.upper(), str(year)]

    if news_type:
        query += " AND category = %s"
        params.append(news_type)

    results = execute_query(query, tuple(params))
    return results


SUMMARY_TABLE = "non_financial_data_summary"

def create_summary_table():
    query = f"""
    CREATE TABLE IF NOT EXISTS {SUMMARY_TABLE} (
        id INT AUTO_INCREMENT PRIMARY KEY,
        company VARCHAR(255),
        quarter VARCHAR(10),
        year VARCHAR(10),
        category VARCHAR(100),
        title TEXT,
        url TEXT,
        summary TEXT,
        key_terms TEXT
    )
    """
    execute_non_query(query)


def insert_summary(record):
    """
    Inserts summarized news into non_financial_data_summary table.
    Prevents duplicates using url.
    """
    query = f"""
    INSERT INTO {SUMMARY_TABLE} (company, quarter, year, category, title, url, summary, key_terms)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        summary=VALUES(summary),
        key_terms=VALUES(key_terms)
    """
    params = (
        record.get("company"),
        record.get("quarter", "").upper(),
        str(record.get("year")),
        record.get("category"),
        record.get("title"),
        record.get("url"),
        record.get("summary"),
        record.get("key_terms"),
    )
    execute_non_query(query, params)
    print(f"✅ Summary saved for: {record['title']}")

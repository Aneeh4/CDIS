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

# -----------------------------
# 📊 Financial Data Section
# -----------------------------
FIN_TABLE = "financial_data"

def create_financial_table():
    """
    Creates the financial_data table if it does not exist.
    Each metric is stored as a separate row.
    """
    query = f"""
    CREATE TABLE IF NOT EXISTS {FIN_TABLE} (
        id INT AUTO_INCREMENT PRIMARY KEY,
        company VARCHAR(255),
        quarter VARCHAR(10),
        year VARCHAR(10),
        metric_name VARCHAR(255),
        metric_value DECIMAL(30, 4),
        unit VARCHAR(20),
        UNIQUE KEY uq_metric (company, quarter, year, metric_name)
    )
    """
    execute_non_query(query)


def insert_financial_data(company: str, quarter: str, year: str, metrics: list):
    """
    Inserts multiple metrics for a company into financial_data table.
    Each metric becomes a separate row.
    
    metrics: list of dicts with keys: metric, value, unit
    Example:
    [
        {"metric": "Revenue", "value": 9444, "unit": "$M"},
        {"metric": "Operating Cash Flow", "value": 1983, "unit": "$M"}
    ]
    """
    for m in metrics:
        query = f"""
        INSERT INTO {FIN_TABLE} (company, quarter, year, metric_name, metric_value, unit)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            metric_value = VALUES(metric_value),
            unit = VALUES(unit)
        """
        params = (
            company,
            quarter.upper(),
            str(year),
            m.get("metric"),
            m.get("value"),
            m.get("unit")
        )
        execute_non_query(query, params)
    print(f"✅ Inserted/Updated {len(metrics)} financial metrics for {company} {quarter} {year}")


def get_financial_data(company: str, quarter: str, year: str):
    """
    Fetches financial metrics for a given company, quarter, and year.
    Returns each metric as a separate row.
    """
    query = f"""
    SELECT company, quarter, year, metric_name, metric_value, unit
    FROM {FIN_TABLE}
    WHERE company = %s AND quarter = %s AND year = %s
    """
    params = (company, quarter.upper(), str(year))
    results = execute_query(query, params)
    return results
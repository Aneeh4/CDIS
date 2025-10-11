# utils/data_loader.py
import pandas as pd
from database.crud import get_non_financial_data
from database.mysql_client import execute_query

def load_financial_data():
    """
    Placeholder for now (still from CSV or DB later).
    """
    return pd.read_csv("data/financial_data.csv")

def load_non_financial_data(company=None, quarter=None, year=None, news_type=None):
    """
    Loads non-financial summarized data directly from MySQL.
    Pulls from the non_financial_data_summary table.
    """
    query = """
        SELECT company, quarter, year, category, title, url, summary, key_terms
        FROM non_financial_data_summary
    """
    params = []
    conditions = []

    if company:
        conditions.append("company = %s")
        params.append(company)
    if quarter:
        conditions.append("quarter = %s")
        params.append(quarter.upper())
    if year:
        conditions.append("year = %s")
        params.append(str(year))
    if news_type:
        conditions.append("category = %s")
        params.append(news_type)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " ORDER BY year DESC, quarter ASC"

    results = execute_query(query, tuple(params))
    if not results:
        return pd.DataFrame(columns=["company", "quarter", "year", "category", "title", "url", "summary", "key_terms"])

    # Convert results (list of tuples or dicts) → DataFrame
    df = pd.DataFrame(results, columns=["company", "quarter", "year", "category", "title", "url", "summary", "key_terms"])
    return df

def get_companies():
    """
    Fetch unique company names from the summary table.
    """
    query = "SELECT DISTINCT company FROM non_financial_data_summary ORDER BY company"
    results = execute_query(query)
    return [r['company'] for r in results] if results else []


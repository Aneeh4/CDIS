"""
financial_loader.py
-------------------
Loads structured financial metrics into MongoDB (FINANCIAL_DATA collection).
Checks for duplicates before insertion.
"""
# load/financial_loader.py
from database.crud import insert_financial_data

# def save_financial_metrics(company, quarter, year, metrics):
#     return insert_financial_data(company, quarter, year, metrics)


# def save_financial_metrics(company_name, quarter, year, metrics_dict):
#     data = {
#         "company": company_name,
#         "quarter": quarter,
#         "year": year,
#         "metrics": metrics_dict
#     }
#     insert_financial_data(data)
#     print(f"Financial metrics saved for {company_name} {quarter} {year}")

def save_financial_metrics(company_name, quarter, year, metrics_dict):
    """Save financial metrics into DB using the CRUD function (4-arg signature)."""
    # Defensive defaults
    quarter = quarter or "Unknown"
    year = year or "Unknown"

    # Call insert_financial_data with explicit arguments (not a single dict)
    insert_financial_data(company_name, quarter, year, metrics_dict)
    print(f"✅ Financial metrics saved for {company_name} {quarter} {year}")
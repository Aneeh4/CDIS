"""
Automated Multi-Company News Scraper (Google News RSS)
------------------------------------------------------
Fetches news for selected company/quarter/year,
classifies into HR/Product Releases/Major Events,
and stores in MongoDB.
"""

import feedparser
from datetime import datetime
from database.crud import insert_non_financial_data

# ------------------------
# 1. Helper Functions
# ------------------------
def get_quarter_dates(quarter, year):
    if quarter == "Q1": return datetime(int(year), 1, 1), datetime(int(year), 3, 31)
    if quarter == "Q2": return datetime(int(year), 4, 1), datetime(int(year), 6, 30)
    if quarter == "Q3": return datetime(int(year), 7, 1), datetime(int(year), 9, 30)
    if quarter == "Q4": return datetime(int(year), 10, 1), datetime(int(year), 12, 31)

def classify_news(text, news_type):
    text = text.lower()

    if news_type == "HR":
        if any(word in text for word in ["hiring", "recruitment", "layoff", "job cuts", "talent", "employee"]):
            return "HR"
    elif news_type == "Product Releases":
        if any(word in text for word in ["launch", "release", "product", "innovation", "solution", "platform"]):
            return "Product Release"
    elif news_type == "Major Events":
        if any(word in text for word in ["conference", "summit", "event", "forum", "partnership", "collaboration"]):
            return "Major Event"

    return "Other"

# ------------------------
# 2. Google News Scraper
# ------------------------
def scrape_google_news(company, quarter, year, news_type):
    start, end = get_quarter_dates(quarter, year)
    feed_url = f"https://news.google.com/rss/search?q={company}&hl=en-IN&gl=IN&ceid=IN:en"

    feed = feedparser.parse(feed_url)
    inserted_count = 0

    for entry in feed.entries:
        pub_date = datetime(*entry.published_parsed[:6])

        # Check if article falls in selected quarter/year
        if not (start <= pub_date <= end):
            continue

        title = entry.title
        summary = entry.summary if hasattr(entry, "summary") else ""
        link = entry.link

        category = classify_news(title + " " + summary, news_type)

        if category == "Other":
            continue  # skip irrelevant

        record = {
            "company": company,
            "title": title,
            "date": pub_date.strftime("%Y-%m-%d"),
            "body": summary,
            "url": link,
            "category": category,
            "quarter": quarter,
            "year": year
        }

        insert_non_financial_data(record)
        inserted_count += 1
        print(f"Inserted: {title} [{category}]")

    print(f"\nScraping done! Total {inserted_count} {news_type} articles inserted for {company} ({quarter} {year})")

# ------------------------
# 3. Run Script
# ------------------------
if __name__ == "__main__":
    print("Multi-Company Automated News Scraper (Google News RSS)")

    companies = ["Accenture", "Deloitte", "Capgemini"]
    news_types = ["HR", "Product Releases", "Major Events"]

    print("\nSelect Company:")
    for i, c in enumerate(companies, 1):
        print(f"{i}. {c}")
    company_choice = int(input("Enter choice (1-3): "))
    company = companies[company_choice - 1]

    quarter = input("Enter quarter (Q1/Q2/Q3/Q4): ").strip().upper()
    year = input("Enter year (e.g., 2025): ").strip()

    print("\nSelect News Type:")
    for i, t in enumerate(news_types, 1):
        print(f"{i}. {t}")
    type_choice = int(input("Enter choice (1-3): "))
    news_type = news_types[type_choice - 1]

    scrape_google_news(company, quarter, year, news_type)

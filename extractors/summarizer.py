
import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import google.generativeai as genai
from database.crud import get_non_financial_data, insert_summary, create_summary_table

# -------------------------------
# 0. Ensure summary table exists
# -------------------------------
create_summary_table()  # This ensures table is ready

# -------------------------------
# 1. Load Gemini API key from .env
# -------------------------------
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("❌ GEMINI_API_KEY not found in .env file")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5 flash")



def fetch_article_text(url):
    """Fetch and clean article text from URL."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract paragraphs
        paragraphs = [p.get_text() for p in soup.find_all("p")]
        text = " ".join(paragraphs)
        return text.strip()
    except Exception as e:
        print(f"❌ Error fetching {url}: {e}")
        return None

def summarize_text(text):
    """Summarize text using Gemini model."""
    if not text:
        return None
    try:
        # Truncate text if too long
        text = text[:2000]  # Gemini can handle more than 1024

        response = model.generate(
            prompt=f"Summarize the following article focusing on key points and numbers:\n\n{text}",
            max_output_tokens=150
        )
        summary = response.text  # Gemini returns summary in .text
        return summary.strip()
    except Exception as e:
        print(f"❌ Summarization failed: {e}")
        return None


def summarize_news(company, quarter, year, news_type):
    """Main function to query DB and summarize news."""
    print(f"\n🔎 Fetching {news_type} articles for {company} ({quarter} {year})...\n")
    
    # Step 1: Query MongoDB (you’ll define get_articles_from_db)
    articles = get_non_financial_data(company, quarter, year, news_type)
    if not articles:
        print("⚠️ No matching articles found in DB.")
        return
    
    for art in articles:
        print(f"\n📰 {art['title']} ({art['url']})")
        
        # Step 2: Fetch article content
        text = fetch_article_text(art['url'])
        if not text:
            continue
        
        # Step 3: Summarize
        summary = summarize_text(text)
        if summary:
            print(f"📌 Summary: {summary}")
            
            # Step 4: Insert into MySQL
            try:
                insert_summary({
                    "company": company,
                    "quarter": quarter.upper(),
                    "year": str(year),
                    "category": news_type,
                    "title": art['title'],
                    "url": art['url'],
                    "summary": summary,
                    "key_terms": ""  # optional, you can extract keywords later
                })
                print("✅ Summary saved in DB.")
            except Exception as e:
                print(f"❌ Failed to insert summary: {e}")
        else:
            print("⚠️ Could not summarize this article.")


# Example CLI runner
if __name__ == "__main__":
    company = input("Enter company (Accenture/Deloitte/Capgemini): ")
    quarter = input("Enter quarter (Q1/Q2/Q3/Q4): ")
    year = input("Enter year (e.g., 2025): ")
    news_type = input("Enter news type (HR/Product Releases/Major Events): ")

    summarize_news(company, quarter, year, news_type)

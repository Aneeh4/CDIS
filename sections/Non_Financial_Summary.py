import streamlit as st
from utils.data_loader import load_non_financial_data, get_companies
import time

# -------------------------
# Page Configuration
# -------------------------
st.set_page_config(
    page_title="Non-Financial Summary",
    layout="wide"
)

# -------------------------
# Custom CSS Styling
# -------------------------
st.markdown("""
<style>
    /* Global font and color theme */
    body {
        font-family: 'Inter', sans-serif;
        color: #222;
        background-color: #fafafa;
    }
    /* Titles */
    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        color: #1a1a1a;
    }
    /* Dropdowns and widgets */
    .stSelectbox, .stButton button {
        font-size: 15px;
    }
    /* News cards */
    .news-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 18px 24px;
        margin-bottom: 20px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.1);
    }
    .news-title {
        font-size: 20px;
        font-weight: 600;
        margin-bottom: 4px;
    }
    .news-meta {
        color: #666;
        font-size: 14px;
        margin-bottom: 10px;
    }
    .key-terms {
        font-size: 14px;
        color: #444;
        margin-top: 6px;
    }
    a {
        color: #0056b3 !important;
        text-decoration: none;
    }
    a:hover {
        text-decoration: underline;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------
# Page Header
# -------------------------
st.title("Non-Financial Summary")

# Fetch list of available companies from DB
companies = get_companies()

if not companies:
    st.warning("No data found in the database yet. Please run the summarization pipeline.")
    st.stop()

# -------------------------
# Filter Selection
# -------------------------
col1, col2, col3, col4 = st.columns(4)
with col1:
    selected_company = st.selectbox("Select Company", ["Select a company"] + companies)
with col2:
    selected_quarter = st.selectbox("Select Quarter", ["Select quarter", "Q1", "Q2", "Q3", "Q4"])
with col3:
    selected_year = st.selectbox("Select Year", ["Select year", "2025", "2024"])
with col4:
    selected_category = st.selectbox("Filter by Category", ["All", "HR", "Major Events", "Product Releases", "Research"])

# -------------------------
# Conditional Data Loading
# -------------------------
if (
    selected_company != "Select a company"
    and selected_quarter != "Select quarter"
    and selected_year != "Select year"
):
    # Prepare filters
    quarter = None if selected_quarter == "All" else selected_quarter
    year = None if selected_year == "All" else selected_year
    category = None if selected_category == "All" else selected_category

    # Spinner with small delay for realism
    with st.spinner(f"Fetching data for {selected_company} ({selected_quarter} {selected_year})..."):
        time.sleep(4)  # 4-second buffer delay
        df = load_non_financial_data(selected_company, quarter, year, category)

    # -------------------------
    # Display Results
    # -------------------------
    if df.empty:
        st.info(f"No summarized news found for {selected_company} in {selected_quarter} {selected_year}.")
    else:
        st.subheader(f"News & Summaries for {selected_company} — {selected_quarter} {selected_year}")
        for _, row in df.iterrows():
            with st.container():
                st.markdown(f"""
                    <div class="news-card">
                        <div class="news-title">{row['title']}</div>
                        <div class="news-meta">{row['quarter']} {row['year']} | {row['category']}</div>
                        <div>{row['summary']}</div>
                        {f"<div class='key-terms'><strong>Key Terms:</strong> {row['key_terms']}</div>" if row.get('key_terms') else ''}
                        {f"<div><a href='{row['url']}' target='_blank'>Read more</a></div>" if row.get('url') else ''}
                    </div>
                """, unsafe_allow_html=True)
else:
    st.info("Please select a company, quarter, and year to view summaries.")

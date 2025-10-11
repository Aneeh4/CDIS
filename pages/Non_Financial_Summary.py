import streamlit as st
from utils.data_loader import load_non_financial_data, get_companies

st.title("🧠 Non-Financial Summary")

# Fetch list of available companies from DB
companies = get_companies()

if not companies:
    st.warning("⚠️ No data found in the database yet. Please run the summarization pipeline.")
    st.stop()

selected_company = st.selectbox("Select Company", companies)
selected_quarter = st.selectbox("Select Quarter", ["All", "Q1", "Q2", "Q3", "Q4"])
selected_year = st.selectbox("Select Year", ["All", "2025", "2024"])
selected_category = st.selectbox("Filter by Category", ["All", "HR", "Major Events", "Product Releases", "Research"])

# Fetch filtered data from DB
quarter = None if selected_quarter == "All" else selected_quarter
year = None if selected_year == "All" else selected_year
category = None if selected_category == "All" else selected_category

df = load_non_financial_data(selected_company, quarter, year, category)

if df.empty:
    st.info(f"No summarized news found for {selected_company}.")
else:
    st.subheader(f"📰 News & Summaries for {selected_company}")

    for _, row in df.iterrows():
        st.markdown(f"### {row['title']}")
        st.caption(f"📅 {row['quarter']} {row['year']} | 🏷️ {row['category']}")
        st.write(row['summary'])
        if row['key_terms']:
            st.markdown(f"**Key Terms:** {row['key_terms']}")
        if row['url']:
            st.markdown(f"[🔗 Read more]({row['url']})")
        st.divider()

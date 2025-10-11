import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import load_financial_data, get_companies

st.title("📊 Financial Analysis")

df = load_financial_data()
companies = get_companies()

selected_company = st.selectbox("Select Company", companies)

filtered_df = df[df["Company"] == selected_company]

st.subheader(f"📈 Financial Metrics for {selected_company}")
st.dataframe(filtered_df)

metric = st.selectbox("Select Metric to Visualize", ["Revenue (in $B)", "Net Profit (in $B)", "EPS", "Operating Margin (%)"])

fig = px.line(filtered_df, x="Quarter", y=metric, color="Year", markers=True, title=f"{metric} Trend - {selected_company}")
st.plotly_chart(fig, use_container_width=True)

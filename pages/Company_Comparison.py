import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import load_financial_data, get_companies

st.title("🏢 Company Comparison")

df = load_financial_data()
companies = get_companies()

selected_companies = st.multiselect("Select Companies to Compare", companies, default=["Accenture", "Deloitte"])
metric = st.selectbox("Select Metric", ["Revenue (in $B)", "Net Profit (in $B)", "EPS", "Operating Margin (%)"])

filtered_df = df[df["Company"].isin(selected_companies)]

st.subheader(f"📊 Comparing {metric} across Selected Companies")

fig = px.bar(filtered_df, x="Quarter", y=metric, color="Company", barmode="group",
             facet_col="Year", title=f"{metric} Comparison by Quarter & Year")
st.plotly_chart(fig, use_container_width=True)

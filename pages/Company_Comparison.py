import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import load_financial_data, get_companies

# -------------------------
# Page Configuration
# -------------------------
st.set_page_config(
    page_title="Company Comparison",
    layout="wide"
)

# -------------------------
# Custom Styling
# -------------------------
st.markdown("""
<style>
    body {
        font-family: 'Inter', sans-serif;
        background-color: #fafafa;
        color: #1a1a1a;
    }

    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        color: #1a1a1a;
    }

    .stSelectbox label, .stMultiSelect label {
        font-weight: 500 !important;
        font-size: 15px !important;
        color: #333 !important;
    }

    .stPlotlyChart {
        margin-top: 25px;
    }

    .stSubheader {
        font-size: 18px;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------
# Page Header
# -------------------------
st.title("Company Comparison")

# -------------------------
# Load Data
# -------------------------
df = load_financial_data()
companies = get_companies()

if df.empty or not companies:
    st.warning("No financial data available. Please ensure data has been loaded into the database.")
    st.stop()

# -------------------------
# Filter Controls
# -------------------------
col1, col2 = st.columns([2, 1])

with col1:
    selected_companies = st.multiselect(
        "Select Companies to Compare",
        companies,
        default=["Accenture", "Deloitte"] if "Accenture" in companies and "Deloitte" in companies else companies[:2]
    )

with col2:
    metric = st.selectbox(
        "Select Metric",
        ["Revenue (in $B)", "Net Profit (in $B)", "EPS", "Operating Margin (%)"]
    )

# -------------------------
# Filtered Data
# -------------------------
filtered_df = df[df["Company"].isin(selected_companies)]

if filtered_df.empty:
    st.info("No matching data found for the selected companies.")
else:
    st.markdown(
        f"<h3 style='font-weight:600; color:#1a1a1a;'>Comparison of {metric} Across Companies</h3>",
        unsafe_allow_html=True
    )

    # -------------------------
    # Plotly Bar Chart
    # -------------------------
    fig = px.bar(
        filtered_df,
        x="Quarter",
        y=metric,
        color="Company",
        barmode="group",
        facet_col="Year",
        title=f"{metric} Comparison by Quarter & Year",
        template="simple_white"
    )

    fig.update_layout(
        title_font=dict(size=18, family="Inter", color="#1a1a1a"),
        xaxis_title="Quarter",
        yaxis_title=metric,
        legend_title="Company",
        font=dict(family="Inter", size=14, color="#1a1a1a"),
        margin=dict(l=40, r=40, t=60, b=40),
        hovermode="x unified",
    )

    st.plotly_chart(fig, use_container_width=True)

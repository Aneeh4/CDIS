import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import load_financial_data, get_companies

# -------------------------
# Page Configuration
# -------------------------
st.set_page_config(
    page_title="Financial Analysis",
    layout="wide"
)

# -------------------------
# Custom Styling
# -------------------------
st.markdown("""
<style>
    /* Global styles */
    body {
        font-family: 'Inter', sans-serif;
        background-color: #fafafa;
        color: #1a1a1a;
    }

    h1, h2, h3, h4 {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        color: #1a1a1a;
    }

    /* Select boxes */
    .stSelectbox label {
        font-weight: 500 !important;
        font-size: 15px !important;
    }

    /* DataFrame styling */
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
    }

    /* Subheader */
    .metric-header {
        margin-top: 20px;
        font-size: 18px;
        font-weight: 600;
        color: #222;
    }

    /* Plotly chart container */
    .stPlotlyChart {
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------
# Page Header
# -------------------------
st.title("Financial Analysis")

# -------------------------
# Load Data
# -------------------------
df = load_financial_data()
companies = get_companies()

if df.empty or not companies:
    st.warning("No financial data found in the database. Please ensure data is available.")
    st.stop()

# -------------------------
# Filters
# -------------------------
col1, col2 = st.columns([2, 1])
with col1:
    selected_company = st.selectbox("Select Company", companies)
with col2:
    metric = st.selectbox(
        "Select Metric to Visualize",
        ["Revenue (in $B)", "Net Profit (in $B)", "EPS", "Operating Margin (%)"]
    )

# -------------------------
# Filter Data
# -------------------------
filtered_df = df[df["Company"] == selected_company]

if filtered_df.empty:
    st.info(f"No financial metrics available for {selected_company}.")
else:
    # -------------------------
    # Display Table
    # -------------------------
    st.markdown(f"<div class='metric-header'>Financial Metrics for {selected_company}</div>", unsafe_allow_html=True)
    st.dataframe(filtered_df, use_container_width=True)

    # -------------------------
    # Plotly Line Chart
    # -------------------------
    fig = px.line(
        filtered_df,
        x="Quarter",
        y=metric,
        color="Year",
        markers=True,
        title=f"{metric} Trend — {selected_company}",
        template="simple_white"
    )

    fig.update_layout(
        title_font=dict(size=18, family="Inter", color="#1a1a1a"),
        xaxis_title="Quarter",
        yaxis_title=metric,
        legend_title="Year",
        font=dict(family="Inter", size=14, color="#1a1a1a"),
        margin=dict(l=40, r=40, t=60, b=40),
        hovermode="x unified",
    )

    st.plotly_chart(fig, use_container_width=True)

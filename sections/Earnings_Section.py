# Earnings_Section.py
import streamlit as st
import yaml
import os
import re
import json
import pandas as pd

from extractors.pdf_loader import select_pdf_file, extract_text_from_pdf
from transform.financial_parser import parse_financial_metrics
from load.financial_loader import save_financial_metrics
from database.crud import insert_financial_data

# -------------------------
# Helper Function
# -------------------------
def extract_quarter_year(filename: str):
    base = os.path.basename(filename)
    name, _ = os.path.splitext(base)
    quarter_match = re.search(r'(q[1-4])', name, re.IGNORECASE)
    year_match = re.search(r'(20\d{2})', name)
    quarter = quarter_match.group(1).upper() if quarter_match else None
    year = year_match.group(1) if year_match else None
    return quarter, year

# -------------------------
# CSS for Modern UI
# -------------------------
def inject_css():
    st.markdown(
        """
        <style>
        :root{
            --brand:#1F3A5F;
            --accent:#0EA5E9;
            --neutral-50:#F8FAFC;
            --neutral-700:#334155;
            --success:#10B981;
            --warn:#F59E0B;
            --radius:12px;
        }
        .wrap{max-width:1100px;margin:0 auto;padding:12px 12px 24px;}
        .hero{padding:8px 8px 6px;text-align:center;}
        .hero h1{color:var(--brand);font-weight:800;letter-spacing:-0.01em;margin:0 0 8px;}
        .hero p{color:var(--neutral-700);font-size:18px;line-height:1.6;max-width:820px;margin:0 auto;}
        .section-title{color:var(--brand);font-weight:700;margin:10px 0 8px;}
        .steps{display:grid;grid-template-columns:repeat(1,minmax(0,1fr));gap:8px;margin:8px 0 0;}
        @media (min-width:760px){.steps{grid-template-columns:repeat(3,minmax(0,1fr));}}
        .step{background:var(--neutral-50);border:1px solid rgba(31,58,95,0.12);border-radius:var(--radius);padding:12px;}
        .step .num{display:inline-flex;align-items:center;justify-content:center;width:26px;height:26px;border-radius:999px;background:var(--accent);color:white;font-weight:700;margin-right:8px;}
        .step h4{display:flex;align-items:center;margin:0;color:var(--brand);font-weight:700;}
        .step p{margin:6px 0 0;color:var(--neutral-700);font-size:14px;line-height:1.6;}
        .cards{display:grid;grid-template-columns:repeat(1,minmax(0,1fr));gap:12px;}
        @media (min-width:760px){.cards{grid-template-columns:repeat(3,minmax(0,1fr));}}
        .card{background:var(--neutral-50);border:1px solid rgba(31,58,95,0.12);border-radius:var(--radius);padding:14px;text-align:center;transition:transform 120ms ease, box-shadow 120ms ease;}
        .card:hover{transform:translateY(-2px);box-shadow:0 8px 24px rgba(15,23,42,0.08);}
        .card .title{color:var(--brand);font-weight:700;margin:0 0 4px;}
        .card .meta{font-size:14px;color:var(--neutral-700);}
        .hint{font-size:13px;color:var(--neutral-700);margin-top:6px;}
        </style>
        """, unsafe_allow_html=True
    )

# -------------------------
# Hero Section
# -------------------------
def hero():
    st.markdown(
        """
        <div class="wrap">
          <section class="hero">
            <h1>Earnings Metrics Extraction</h1>
            <p>Upload a company earnings PDF, extract financial metrics, review, and save to your database.</p>
          </section>
        </div>
        """, unsafe_allow_html=True
    )

# -------------------------
# How it Works Section
# -------------------------
def how_it_works():
    st.markdown('<div class="wrap"><h3 class="section-title">How it works</h3>', unsafe_allow_html=True)
    cols = st.columns(3, gap="small")
    with cols[0]:
        st.markdown('<div class="step"><h4><span class="num">1</span>Ingest</h4><p>Upload an earnings PDF.</p></div>', unsafe_allow_html=True)
    with cols[1]:
        st.markdown('<div class="step"><h4><span class="num">2</span>Extract</h4><p>Parse financial metrics automatically.</p></div>', unsafe_allow_html=True)
    with cols[2]:
        st.markdown('<div class="step"><h4><span class="num">3</span>Save</h4><p>Review results and save to database.</p></div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------
# Summary Cards
# -------------------------
def show_summary_cards(company, quarter, year):
    st.markdown('<div class="wrap"><h3 class="section-title">Detected Context</h3></div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f'<div class="card"><div class="title">Company</div><div class="meta">{company or "—"}</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="card"><div class="title">Quarter</div><div class="meta">{quarter or "—"}</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="card"><div class="title">Year</div><div class="meta">{year or "—"}</div></div>', unsafe_allow_html=True)

# -------------------------
# Metrics Preview
# -------------------------
def metrics_preview(metrics):
    try:
        if isinstance(metrics, list):
            if metrics and isinstance(metrics[0], dict):
                st.dataframe(pd.DataFrame(metrics), use_container_width=True, height=320)
            else:
                st.json(metrics)
        elif isinstance(metrics, dict):
            rows = [{"metric": k, "value": v} for k, v in metrics.items()]
            st.dataframe(pd.DataFrame(rows), use_container_width=True, height=320)
        else:
            st.json(metrics)
    except Exception:
        st.json(metrics)

# -------------------------
# Main Page
# -------------------------
def show_page():
    st.set_page_config(page_title="Earnings Extraction", layout="wide")
    inject_css()
    hero()
    how_it_works()

    # Load YAML
    config_path = "config/merged_metric_synonyms_config_final.yaml"
    if not os.path.exists(config_path):
        st.error("YAML configuration file not found.")
        return
    with open(config_path, encoding="utf-8") as f:
        config = yaml.safe_load(f)

    companies = [k for k in config.keys() if k != "GLOBAL_DEFAULTS"]
    selected_company = st.selectbox("Select Company", companies)
    #api_key = 'AIzaSyB_t9RrIGjmp_Fd8_PrnGnZAfDQ2rqyDOs'  

    selected_config = config[selected_company]

    # Upload PDF
    uploaded_pdf = select_pdf_file("Upload PDF")
    if uploaded_pdf:
        pdf_text = extract_text_from_pdf(uploaded_pdf)
        st.success("PDF loaded successfully!")

        with st.spinner("Extracting financial metrics..."):
            st.session_state.final_metrics = parse_financial_metrics(pdf_text, selected_config, api_key)

        # Extract quarter/year
        quarter, year = extract_quarter_year(uploaded_pdf)
        st.session_state.quarter, st.session_state.year = quarter, year

        # Display Metrics
        show_summary_cards(selected_company, quarter, year)
        with st.expander("Preview metrics", expanded=True):
            metrics_preview(st.session_state.final_metrics)
            try:
                raw_json = st.session_state.final_metrics
                if not isinstance(raw_json, str):
                    raw_json = json.dumps(raw_json, indent=2, ensure_ascii=False)
                st.download_button(
                    "Download JSON",
                    data=raw_json.encode("utf-8"),
                    file_name=f"{selected_company}_{quarter or 'Qx'}_{year or 'YYYY'}_metrics.json",
                    mime="application/json",
                    use_container_width=True
                )
            except Exception:
                pass

        # Save Button
        if st.button("Save to Database", type="primary", use_container_width=True):
            metrics_to_save = st.session_state.final_metrics
            if isinstance(metrics_to_save, str):
                metrics_to_save = json.loads(metrics_to_save)
            if isinstance(metrics_to_save, dict):
                metrics_to_save = [metrics_to_save]

            try:
                save_financial_metrics(selected_company, quarter, year, metrics_to_save)
                insert_financial_data(selected_company, quarter, year, metrics_to_save)
                st.success(f"✅ Metrics saved for {selected_company} {quarter} {year}!")
            except Exception as e:
                st.error(f"Failed to save metrics: {e}")
    else:
        st.info("Please upload a PDF to extract financial metrics.")

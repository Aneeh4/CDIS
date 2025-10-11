# import streamlit as st
# from transformers import pipeline

# # Initialize Hugging Face QA pipeline
# @st.cache_resource
# def load_model():
#     return pipeline("question-answering", model="distilbert-base-cased-distilled-squad")

# qa_pipe = load_model()

# st.title("Interactive Question-Answering System")

# st.write("Enter the context text below (e.g. company summary, article):")
# context = st.text_area("Context", height=200)

# if context:
#     st.write("Now, ask any question based on the above context.")
#     question = st.text_input("Your Question")

#     if question:
#         with st.spinner("Finding answer..."):
#             result = qa_pipe(question=question, context=context)
#         st.markdown(f"**Answer:** {result['answer']}")


import streamlit as st

st.set_page_config(
    page_title="Corporate Document Intelligent System (CDIS)",
    page_icon="📘",
    layout="wide"
)

st.title("📘 Corporate Document Intelligent System (CDIS)")

st.markdown("""
Welcome to **Corporate Document Intelligent System (CDIS)** — an advanced AI-driven platform designed to analyze, extract, and summarize both **financial** and **non-financial** information from corporate documents such as quarterly reports, press releases, and news articles.

### 🔍 What is CDIS?
CDIS automates the understanding of complex corporate documents using Natural Language Processing (NLP) and Machine Learning models.  
It transforms unstructured text data into **structured, actionable insights** for analysts, researchers, and decision-makers.

### ⚙️ How It Works
1. **Document Ingestion**  
   Upload or fetch company reports and press releases. The system supports both local files and automated collection from online sources.

2. **Intelligent Extraction**  
   Using AI models and regex-based logic, CDIS extracts key **financial metrics** such as *Revenue, EPS, Operating Margin, and Growth Rates*, along with **non-financial insights** like *HR updates, sustainability initiatives, R&D progress, and major events*.

3. **Summarization & Structuring**  
   The extracted data is summarized into concise, human-readable insights.  
   - Financial data is structured into canonical metrics.  
   - Non-financial text is categorized (HR, Product Releases, Research, etc.) and summarized.  

4. **Storage & Analysis**  
   All processed information is stored in a **local or Oracle database**, allowing quick retrieval and comparison across time periods or companies.

5. **Visualization & Comparison**  
   Users can navigate through interactive modules to:
   - 📊 **Analyze financial trends** across quarters  
   - 🧠 **Explore non-financial updates and summaries**  
   - 🏢 **Compare multiple companies** side by side  

### 🧠 Why CDIS?
- Reduces manual effort in analyzing lengthy corporate documents  
- Ensures consistency and accuracy in extracted insights  
- Enables data-driven decision-making for analysts and stakeholders  

Use the **sidebar** to explore the different modules:
- 📊 **Financial Analysis** – Extracted and structured key metrics  
- 🧠 **Non-Financial Summary** – Summarized news and qualitative insights  
- 🏢 **Company Comparison** – Compare insights across companies and periods  
            
""")

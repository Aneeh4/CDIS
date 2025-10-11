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
Welcome to **CDIS** — an AI-powered platform that extracts, summarizes, and compares **financial** and **non-financial** insights from corporate documents.

Use the sidebar to navigate between modules:
- 📊 Financial Analysis  
- 🧠 Non-Financial Summary  
- 🏢 Company Comparison  
""")

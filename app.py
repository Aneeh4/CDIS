import streamlit as st
from transformers import pipeline

# Initialize Hugging Face QA pipeline
@st.cache_resource
def load_model():
    return pipeline("question-answering", model="distilbert-base-cased-distilled-squad")

qa_pipe = load_model()

st.title("Interactive Question-Answering System")

st.write("Enter the context text below (e.g. company summary, article):")
context = st.text_area("Context", height=200)

if context:
    st.write("Now, ask any question based on the above context.")
    question = st.text_input("Your Question")

    if question:
        with st.spinner("Finding answer..."):
            result = qa_pipe(question=question, context=context)
        st.markdown(f"**Answer:** {result['answer']}")

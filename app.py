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
# from sections import Financial_Analysis, Non_Financial_Summary, Company_Comparison, Earnings_Section

# ------------------------------
# Page Configuration
# ------------------------------
st.set_page_config(
    page_title="Corporate Document Intelligent System (CDIS)",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)
hide_pages_style = """
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    </style>
"""
st.markdown(hide_pages_style, unsafe_allow_html=True)
# ------------------------------
# Sidebar Navigation
# ------------------------------
page = st.sidebar.radio(
    "Select a Page",
    ["Home", "Financial Analysis", "Non-Financial Summary", "Company Comparison", "Earnings Extraction"],
    index=0,
    label_visibility="collapsed"
)

# ------------------------------
# Global Styling
# ------------------------------
st.markdown("""
<style>
    /* Global font and text color */
    html, body, [class*="css"] {
        font-family: 'Segoe UI', sans-serif;
        color: #2c2c2c;
    }

    /* Sidebar radio styling */
    section[data-testid="stSidebar"] div[role="radiogroup"] > label {
        font-size: 15px !important;
        padding: 6px 12px;
        border-radius: 8px;
        margin-bottom: 5px;
        transition: all 0.3s ease;
    }
    section[data-testid="stSidebar"] div[role="radiogroup"] > label:hover {
        background-color: #f0f2ff;
        color: #4e5cf6 !important;
    }

    /* Feature card styling */
    .feature-card {
        border: 1px solid #e6e6e6;
        border-radius: 15px;
        padding: 25px;
        text-align: center;
        background-color: #f9f9f9;
        transition: 0.3s;
        height: 100%;
        box-shadow: 0 3px 8px rgba(0,0,0,0.05);
    }
    .feature-card:hover {
        background-color: #f1f1ff;
        box-shadow: 0 6px 15px rgba(0,0,0,0.08);
        transform: translateY(-4px);
    }
    .feature-icon {
        height: 80px;
        margin-bottom: 12px;
    }
    .feature-title {
        font-size: 18px;
        font-weight: 600;
        color: #333;
        margin-bottom: 6px;
    }
    .feature-desc {
        font-size: 14px;
        color: #555;
    }

    /* Section header styling */
    h1, h2, h3 {
        color: #4e5cf6;
    }

    /* Button hover improvement */
    .stButton button {
        background-color: #4e5cf6;
        color: white;
        font-weight: bold;
        border-radius: 10px;
        padding: 10px 20px;
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        background-color: #3c48d3;
        transform: scale(1.03);
    }
</style>
""", unsafe_allow_html=True)

# ------------------------------
# Home Page
# ------------------------------
# ------------------------------
# Custom CSS for entire home
# ------------------------------
def inject_css():
    st.markdown(
        """
        <style>
          :root {
            --brand: #2B4162;
            --accent: #0EA5E9;
            --neutral-50: #F9FAFB;
            --neutral-700: #374151;
          }

          .home-wrap {
            max-width: 1100px;
            margin: 0 auto;
            padding: 12px 12px 24px;
          }

          .section-title {
            color: var(--brand);
            font-weight: 700;
            font-size: 24px;
            margin: 20px 0 12px;
          }

          .description {
            font-size: 16px;
            color: var(--neutral-700);
            line-height: 1.6;
            max-width: 900px;
            margin-bottom: 20px;
          }

          .how-it-works {
            padding: 32px 0 0;
            max-width: 1100px;
            margin: 0 auto;
          }

          .how-it-works h2 {
            color: var(--brand);
            font-size: 26px;
            font-weight: 800;
            margin-bottom: 4px;
          }

          .how-it-works p.lead {
            color: #4B5563;
            font-size: 15px;
            margin-bottom: 24px;
          }

          .how-cards {
            display: flex;
            flex-wrap: wrap;
            gap: 16px;
            justify-content: center;
          }

          .how-card {
            background: #fff;
            border: 1px solid #E5E7EB;
            border-radius: 12px;
            padding: 20px;
            width: 200px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.06);
            transition: all 0.2s ease;
            text-align: left;
          }

          .how-card:hover {
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            transform: translateY(-2px);
          }

          .how-card img {
            width: 28px;
            height: 28px;
            margin-bottom: 12px;
          }

          .how-card-title {
            font-weight: 700;
            color: #111827;
            font-size: 15px;
            margin-bottom: 6px;
          }

          .how-card-desc {
            font-size: 14px;
            color: #4B5563;
            line-height: 1.5;
          }

          .card {
            background: var(--neutral-50);
            border: 1px solid rgba(43, 65, 98, 0.12);
            border-radius: 12px;
            padding: 16px;
            text-align: center;
            transition: transform 120ms ease, box-shadow 120ms ease;
          }
          .card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 24px rgba(15, 23, 42, 0.08);
          }
          .card img {
            width: 80px;
            height: 80px;
            object-fit: contain;
            margin-bottom: 10px;
          }
          .card .title {
            font-weight: 700;
            color: var(--brand);
            font-size: 16px;
            margin-bottom: 4px;
          }
          .card .desc {
            font-size: 14px;
            color: var(--neutral-700);
            line-height: 1.6;
          }
        </style>
        """,
        unsafe_allow_html=True
    )


# ------------------------------
# How It Works Section (with images)
# ------------------------------
def how_it_works_section():
    st.markdown("<div class='how-it-works'>", unsafe_allow_html=True)
    st.markdown("<h2>How it works</h2>", unsafe_allow_html=True)
    st.markdown("<p class='lead'>CDIS streamlines your workflow from ingestion to insight with a reliable, repeatable process.</p>", unsafe_allow_html=True)

    # Each card in a Streamlit column layout instead of raw HTML
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.image("images/ingestion.png", width=40)
        st.markdown(
            """
            <div class='how-card-title'>Document Ingestion</div>
            <div class='how-card-desc'>Upload annual reports or earnings releases.</div>
            """, unsafe_allow_html=True
        )

    with col2:
        st.image("images/extraction.png", width=40)
        st.markdown(
            """
            <div class='how-card-title'>Intelligent Extraction</div>
            <div class='how-card-desc'>Automatically extract financial and qualitative metrics.</div>
            """, unsafe_allow_html=True
        )

    with col3:
        st.image("images/summarization.png", width=40)
        st.markdown(
            """
            <div class='how-card-title'>Summarization</div>
            <div class='how-card-desc'>Generate concise, structured summaries for insights.</div>
            """, unsafe_allow_html=True
        )

    with col4:
        st.image("images/storage.png", width=40)
        st.markdown(
            """
            <div class='how-card-title'>Storage & Analysis</div>
            <div class='how-card-desc'>Save, organize, and query reports easily.</div>
            """, unsafe_allow_html=True
        )

    with col5:
        st.image("images/visualization.png", width=40)
        st.markdown(
            """
            <div class='how-card-title'>Visualization & Comparison</div>
            <div class='how-card-desc'>View trends and compare companies interactively.</div>
            """, unsafe_allow_html=True
        )

    st.markdown("</div>", unsafe_allow_html=True)



import streamlit as st

def module_grid():
    st.markdown("<h2 style='text-align:left;'>Explore CDIS Modules</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:left; color: gray;'>Overview of available modules and features.</p>", unsafe_allow_html=True)

    cards = [
        {
            "icon": "images/question-mark.png",
            "title": "QA System",
            "desc": "Ask context-aware questions on uploaded documents.",
            "action": lambda: st.experimental_set_query_params(page="QA_System"),
            "disabled": False,
        },
        {
            "icon": "images/filter.png",
            "title": "Earnings Extraction",
            "desc": "Extract structured financial metrics from PDFs.",
            "action": lambda: st.experimental_set_query_params(page="Earnings_Section"),
            "disabled": False,
        },
        {
            "icon": "images/chatbot.png",
            "title": "AI Chatbot",
            "desc": "Conversational assistant for smart insights.",
            "disabled": True,
        },
        {
            "icon": "images/exploration.png",
            "title": "Analysis",
            "desc": "Track financial trends across multiple quarters.",
            "disabled": True,
        },
        {
            "icon": "images/export.png",
            "title": "Export",
            "desc": "Download reports or export extracted data.",
            "action": lambda: st.experimental_set_query_params(page="Non_Financial_Summary"),
            "disabled": False,
        },
        {
            "icon": "images/decision.png",
            "title": "Company Comparison",
            "desc": "Compare insights and performance across firms.",
            "action": lambda: st.experimental_set_query_params(page="Company_Comparison"),
            "disabled": False,
        },
    ]

    # Adjust this height based on your longest description (in px)
    description_box_height = 80  

    cols = st.columns(3)
    for idx, card in enumerate(cards):
        with cols[idx % 3]:
            st.image(card["icon"], width=40)
            st.markdown(f"**{card['title']}**")
            st.markdown(
                f"""
                <div style="color: #6b7280; min-height: {description_box_height}px;">
                    {card['desc']}
                </div>
                """,
                unsafe_allow_html=True
            )

# ------------------------------
# Render Full Home Page
# ------------------------------
def render_home():
    inject_css()

    st.markdown(
    """
    <div style="max-width: 700px; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
        <h1 style="text-align: left; color: #0B3D91; font-weight: 800">
            Corporate Document Intelligent System (CDIS)
        </h1>
        <p style="text-align: left; color: #444; line-height: 1.5;">
            Welcome to <strong>Corporate Document Intelligent System (CDIS)</strong> — an advanced AI-driven platform 
            designed to analyze, extract, and summarize both <strong>financial</strong> and <strong>non-financial</strong> information 
            from corporate documents such as quarterly reports, press releases, and news articles.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

    how_it_works_section()
    module_grid()

    st.markdown("<br>", unsafe_allow_html=True)
    st.info("💡 Use the **sidebar** to navigate through different modules of CDIS.")

if page == "Home":
    render_home()
   #  import homeapp  # Home page code in homeapp.py
   #  homeapp.show_home()  # Ensure your home page is wrapped in a show_home() function

elif page == "Financial Analysis":
    from sections import Financial_Analysis
    Financial_Analysis.show_page()  # wrap code in Financial_Analysis.py inside show_page()

elif page == "Non-Financial Summary":
    from sections import Non_Financial_Summary
    Non_Financial_Summary.show_page()

elif page == "Company Comparison":
    from sections import Company_Comparison
    Company_Comparison.show_page()

elif page == "Earnings Extraction":
    from sections import Earnings_Section
    Earnings_Section.show_page()
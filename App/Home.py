import streamlit as st

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="Real Estate Analytics | Home",
    page_icon="🏠",
    layout="wide"
)

# ---------------------------------------------------
# CUSTOM CSS FOR HOME PAGE
# ---------------------------------------------------
st.markdown("""
<style>
    .stApp { background-color: #f8fafc; }
    
    .hero-section {
        background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 50px;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }
    
    .section-card {
        background: white;
        padding: 25px;
        border-radius: 15px;
        border-left: 5px solid #2563eb;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    
    .step-header {
        color: #1e3a8a;
        font-weight: 700;
        font-size: 1.2rem;
        margin-bottom: 10px;
    }

    .module-card {
        text-align: center;
        padding: 20px;
        background: #eff6ff;
        border-radius: 15px;
        border: 1px solid #dbeafe;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# HERO SECTION
# ---------------------------------------------------
st.markdown("""
<div class="hero-section">
    <h1 style="margin:0; font-size:2.5rem;">Data-Driven Real Estate Valuation & Recommendation Engine</h1>
    <p style="font-size:1.2rem; opacity:0.9; margin-top:10px;">
        A Comprehensive Data Science Application for the Gurgaon Real Estate Market
    </p>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# PROJECT OVERVIEW
# ---------------------------------------------------
st.subheader("📌 Project Overview")
st.info("""
In this comprehensive capstone project, the primary focus was on leveraging data science techniques to provide insights, predictions, and recommendations in the real estate domain. 
The project covers everything from **Data Scraping** to **Machine Learning Modeling** and **Explainable AI (SHAP)**.
""")

# ---------------------------------------------------
# APP MODULES (3 SECTIONS)
# ---------------------------------------------------
st.write("")
st.subheader("🚀 Application Modules")
m1, m2, m3 = st.columns(3)

with m1:
    st.markdown("""
    <div class="module-card">
        <h3>💰 Price Predictor</h3>
        <p>Predict accurate property prices using optimized Machine Learning algorithms.</p>
    </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown("""
    <div class="module-card">
        <h3>📊 Analysis App</h3>
        <p>Interactive EDA and market trends visualization using geographical maps and charts.</p>
    </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown("""
    <div class="module-card">
        <h3>🏢 Recommender</h3>
        <p>Personalized apartment suggestions based on facilities, price, and location.</p>
    </div>
    """, unsafe_allow_html=True)

st.write("---")

# ---------------------------------------------------
# TECHNICAL WORKFLOW (Expandable Sections)
# ---------------------------------------------------
st.subheader("🛠️ Technical Workflow")

with st.expander("📂 Data Gathering & Preprocessing"):
    st.write("""
    - **Data Gathering:** Self-scraped from 99acres and other property portals.
    - **Cleaning & Merging:** Handled missing values and merged house/flat datasets into a unified format.
    - **Feature Engineering:** Added new features like Luxury Score, Age of Possession, and Furnish details.
    """)

with st.expander("📈 Exploratory Data Analysis (EDA)"):
    st.write("""
    - **Univariate & Multivariate Analysis:** Patterns and relationships identified using Pandas Profiling.
    - **Outlier Treatment:** Identified and removed outliers to ensure model robustness.
    - **Imputation:** Critical columns like Area and Bedroom addressed using advanced imputation techniques.
    """)

with st.expander("📊 Feature Selection & Statistical Analysis"):
    st.write("""
    We employed multiple statistical and machine learning techniques to identify the most impactful variables for property valuation:
    - **Correlation Analysis:** To identify linear relationships between features like Area, BHK, and Price.
    - **Random Forest Importance:** Used an ensemble-based approach to rank features based on their predictive power.
    - **Gradient Boosting & LASSO:** Applied regularization and boosting techniques to filter out redundant variables and prevent overfitting.
    - **Recursive Feature Elimination (RFE):** Systematically removed less significant features to optimize the model's efficiency.
    """)

with st.expander("🤖 Model Selection (10+ Regressors Compared)"):
    st.write("We compared various regression models to find the best performer:")
    col_a, col_b = st.columns(2)
    with col_a:
        st.write("- **Random Forest Regressor** (Best Performer)")
        st.write("- Linear, Ridge, & LASSO Regression")
        st.write("- SVR & K-Nearest Neighbors")
    with col_b:
        st.write("- Gradient Boosting & ElasticNet")
        st.write("- Decision Tree & MLP (Neural Network)")

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------
with st.sidebar:
    st.title("Project Details")
    st.markdown("**Domain:** Real Estate")
    st.markdown("**Tech Stack:** Python, Scikit-Learn, Streamlit, Pandas")
    st.write("---")
    st.success("App Status: Live")

# ---------------------------------------------------
# FOOTER & CONTACT SECTION (Home.py ke niche add karein)
# ---------------------------------------------------
st.write("---")

# Layout for Footer
footer_col1, footer_col2 = st.columns([4, 1])

with footer_col1:
    st.markdown("""
        <h4 style='color: #1e3a8a;'>Feedback & Collaboration</h4>
        <p style='color: #64748b;'>
            I'm always looking to improve this engine! If you have suggestions, find a bug, 
            or want to discuss the data science methodology, feel free to reach out.
        </p>
    """, unsafe_allow_html=True)

with footer_col2:
    # Yahan apni LinkedIn URL daalein
    linkedin_url = "https://www.linkedin.com/in/rajeshxdatascience/" 
    
    st.markdown(f"""
        <div style="text-align: center;">
            <p style="color: #64748b; font-size: 0.9rem; margin-bottom: 5px;">Contact Developer</p>
            <a href="{linkedin_url}" target="_blank">
                <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="50" style="transition: transform 0.3s;" onmouseover="this.style.transform='scale(1.1)'" onmouseout="this.style.transform='scale(1)'">
            </a>
        </div>
    """, unsafe_allow_html=True)

st.write("")
st.caption("© 2026 | Real Estate Data Science Capstone | Built with Streamlit")
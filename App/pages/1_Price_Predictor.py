import streamlit as st
import pickle
import pandas as pd
import numpy as np
import time

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="Real Estate Valuation Engine",
    page_icon="🏢",
    layout="wide"
)

# ---------------------------------------------------
# STYLING & UI FIXES
# ---------------------------------------------------
st.markdown("""
<style>
    .stApp { background-color: #f8fafc; }
    
    /* Dropdown & Input Visibility */
    div[data-baseweb="select"], .stNumberInput input {
        background-color: white !important;
        border: 2px solid #cbd5e1 !important;
        border-radius: 10px !important;
        color: #1e293b !important;
    }
    
    div[data-baseweb="select"]:hover { border-color: #2563eb !important; }

    /* Header Styling */
    .main-header {
        background: #1e3a8a;
        padding: 30px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
    }

    /* Prediction Result Card */
    .prediction-box {
        background: #ffffff;
        border: 3px solid #10b981;
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 10px 25px rgba(16, 185, 129, 0.15);
    }

    /* Disclaimer Box */
    .disclaimer {
        background-color: #fff7ed;
        border-left: 5px solid #f97316;
        padding: 15px;
        border-radius: 8px;
        margin-top: 15px;
        color: #9a3412;
        font-size: 0.85rem;
    }

    /* Sidebar Styling */
    .sidebar-card {
        background: white;
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# ASSET LOADING
# ---------------------------------------------------
@st.cache_resource
def load_assets():
    try:
        df = pickle.load(open(r'App/pickle/df.pkl', 'rb'))
        pipeline = pickle.load(open(r'App/pickle/pipeline.pkl', 'rb'))
        return df, pipeline
    except Exception as e:
        st.error(f"Error loading files: {e}")
        return None, None

df, pipeline = load_assets()

# ---------------------------------------------------
# SIDEBAR (Settings & Help)
# ---------------------------------------------------
with st.sidebar:
    st.title("🛠️ Settings & Help")
    
    st.markdown("### 💡 Accuracy Tips")
    st.markdown('<div class="sidebar-card">📍 <b>Sector Logic:</b> Premium sectors like 54 or 42 usually have higher predictions.</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-card">📐 <b>BHK-Area Ratio:</b> Ensure area is realistic for the BHK (e.g. 1500 sqft for 3BHK).</div>', unsafe_allow_html=True)
    
    st.write("---")
    if st.button("🔄 Reset All Inputs", use_container_width=True):
        st.rerun()
    
    st.write("---")
    st.caption("AI Model: Random Forest | Data: Gurgaon 2026")

# ---------------------------------------------------
# MAIN UI
# ---------------------------------------------------
st.markdown('<div class="main-header"><h1>Data-Driven Real Estate Valuation</h1></div>', unsafe_allow_html=True)

# Result Area (Top placement for visibility)
result_area = st.empty()

if df is not None:
    st.subheader("📋 Enter Property Details")
    
    with st.container():
        c1, c2, c3 = st.columns(3)
        with c1:
            sector = st.selectbox('📍 Sector', sorted(df['sector'].unique().tolist()))
            bedroom = st.selectbox('🛏 BHK', sorted(df['bedRoom'].unique().tolist()), index=2)
            bathroom = st.selectbox('🛁 Bathrooms', sorted(df['bathroom'].unique().tolist()), index=2)
        with c2:
            balcony = st.selectbox('🌇 Balconies', sorted(df['balcony'].unique().tolist()), index=3)
            area = st.number_input('📐 Area (Sq.ft)', min_value=100.0, value=float(bedroom*700))
            age = st.selectbox('🏗 Age', sorted(df['agePossession'].unique().tolist()))
        with c3:
            facing = st.selectbox('🧭 Facing', sorted(df['facing'].unique().tolist()))
            floor = st.selectbox('🏢 Floor', sorted(df['floor_category'].unique().tolist()))
            st.write("**Features:**")
            s_room, st_room = st.columns(2)
            servant = s_room.checkbox("Servant")
            store = st_room.checkbox("Store")

    if area < (bedroom * 350):
        st.warning("⚠️ **Note:** Select kiya gaya Area iss BHK ke liye kaafi kam lag raha hai.")

    st.write("---")
    
    if st.button('💰 Calculate Valuation', use_container_width=False):
        input_df = pd.DataFrame([[
            sector, bedroom, bathroom, balcony, facing, age, area, int(servant), int(store), floor
        ]], columns=['sector', 'bedRoom', 'bathroom', 'balcony', 'facing', 'agePossession', 'built_up_area', 'servant room', 'store room', 'floor_category'])
        
        with st.spinner("Analyzing market data..."):
            time.sleep(0.5)
            val = np.expm1(pipeline.predict(input_df))[0]

        with result_area.container():
            st.markdown(f"""
                <div class="prediction-box">
                    <h3 style="margin:0; color:#64748b; font-weight:400;">Estimated Market Value</h3>
                    <h1 style="color:#10b981; font-size:3.5rem; margin:10px 0;">₹ {val:.2f} Cr</h1>
                    <p style="color:#94a3b8;">Range: ₹ {val*0.95:.2f} Cr - ₹ {val*1.05:.2f} Cr</p>
                </div>
                <div class="disclaimer">
                    <b>⚠️ Disclaimer:</b> This is an AI-generated estimation based on historical trends. 
                    Actual prices depend on interior work, builder quality, and current market demand.
                </div>
                <br>
            """, unsafe_allow_html=True)
            st.toast("Valuation Updated!")
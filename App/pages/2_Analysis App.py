import streamlit as st
import pandas as pd
import plotly.express as px
import pickle
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(page_title="Real Estate Analytics", page_icon="📊", layout="wide")

# ---------------------------------------------------
# CUSTOM CSS FOR SPACING & INSIGHTS
# ---------------------------------------------------
st.markdown("""
<style>
    .stApp { background-color: #f8fafc; }
    .insight-card {
        background-color: #ffffff;
        border-left: 5px solid #3b82f6;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-top: 10px;
        margin-bottom: 40px;
    }
    .graph-title {
        color: #1e3a8a;
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 20px;
    }
    hr { margin: 40px 0; border: 0.5px solid #e2e8f0; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# DATA LOADING
# ---------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv(r'App/datasets/data_for_viz2.csv')
    txt = pickle.load(open(r"App/datasets/feature_text.pkl",'rb'))
    return df, txt

new_df, feature_text = load_data()

st.title('📊 Gurgaon Real Estate Market Analysis')
st.markdown("Detailed insights into pricing, geography, and property configurations.")
st.write("---")

# ---------------------------------------------------
# 1. SECTOR PRICE GEOMAP (Full Width)
# ---------------------------------------------------
st.markdown('<p class="graph-title">📍 Sector Price Hotspots</p>', unsafe_allow_html=True)

group_df = new_df.groupby('sector').mean(numeric_only=True)[['price','price_per_sqft','built_up_area','latitude','longitude']]

fig = px.scatter_mapbox(group_df, lat='latitude', lon='longitude', color='price_per_sqft', size='built_up_area',
                        color_continuous_scale='Viridis', zoom=10,
                        mapbox_style="open-street-map", height=600,
                        hover_name=group_df.index)

st.plotly_chart(fig, use_container_width=True)

st.markdown("""
<div class="insight-card">
    <b>💡 Key Insights (Geography):</b><br>
    • <b>Premium Zones:</b> Most high-value properties (Yellow/Green dots) are concentrated along <b>Golf Course Road</b> and <b>Golf Course Extension</b>.<br>
    • <b>Affordability:</b> Southern and Northern peripheral sectors (Purple/Dark Blue) offer more competitive price-per-sqft rates.
</div>
""", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ---------------------------------------------------
# 2. POPULAR FEATURES & AREA VS PRICE (Side by Side)
# ---------------------------------------------------
c1, c2 = st.columns(2, gap="large")

with c1:
    st.markdown('<p class="graph-title">☁️ Property Features</p>', unsafe_allow_html=True)
    wordcloud = WordCloud(width=800, height=800, background_color='white', 
                          stopwords=set(['s']), min_font_size=10, 
                          colormap='Blues').generate(feature_text)
    fig_wc, ax = plt.subplots(figsize=(6,6))
    ax.imshow(wordcloud)
    ax.axis('off')
    st.pyplot(fig_wc)
    st.markdown("""
    <div class="insight-card">
        <b>💡 Feature Trends:</b><br>
        • High demand for <b>Servant Rooms</b>, <b>Vaastu Compliance</b>, and <b>Piped Gas</b>.<br>
        • "Ceiling Height" and "Back up" are major selling points in luxury listings.
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown('<p class="graph-title">📐 Area vs Price</p>', unsafe_allow_html=True)
    fig_area = px.scatter(new_df, x="built_up_area", y="price", color="bedRoom", 
                          labels={'built_up_area': 'Area (Sqft)', 'price': 'Price (Cr)'},
                          opacity=0.7, color_continuous_scale='Turbo')
    st.plotly_chart(fig_area, use_container_width=True)
    st.markdown("""
    <div class="insight-card">
        <b>💡 Market Correlation:</b><br>
        • <b>Exponential Growth:</b> Price increases linearly up to 3000 sqft, then spikes significantly for luxury penthouses.<br>
        • <b>Density:</b> Most inventory sits between 1000-2500 sqft for 2 & 3 BHK units.
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ---------------------------------------------------
# 3. BHK PIE & BOX PLOT (Spaced)
# ---------------------------------------------------
st.markdown('<p class="graph-title">💰 Price Distribution by BHK</p>', unsafe_allow_html=True)

col_pie, col_box = st.columns([1, 1.5], gap="large")

with col_pie:
    sector_options = sorted(new_df['sector'].unique().tolist())
    sector_options.insert(0,'Overall')
    selected_sector = st.selectbox('Select Sector for BHK Mix', sector_options)

    if selected_sector == 'Overall':
        fig_pie = px.pie(new_df, names='bedRoom', hole=0.5, color_discrete_sequence=px.colors.qualitative.Safe)
    else:
        fig_pie = px.pie(new_df[new_df['sector'] == selected_sector], names='bedRoom', hole=0.5)
    
    st.plotly_chart(fig_pie, use_container_width=True)
    st.markdown('<div class="insight-card"><b>BHK Mix:</b> 3BHK units (58%) dominate the Gurgaon market, followed by 4BHK and 2BHK.</div>', unsafe_allow_html=True)

with col_box:
    fig_box = px.box(new_df[new_df['bedRoom'] <= 4], x='bedRoom', y='price', 
                     color='bedRoom', points="all")
    st.plotly_chart(fig_box, use_container_width=True)
    st.markdown("""
    <div class="insight-card">
        <b>💡 Price Variation:</b><br>
        • 4BHK units show the highest <b>variance</b>, with luxury outliers reaching 15Cr+.<br>
        • 2BHK and 3BHK pricing is more standardized and tightly clustered.
    </div>
    """, unsafe_allow_html=True)

# Footer
st.write("---")
st.caption("Data Analysis Module | Real Estate Valuation & Recommendation Engine")
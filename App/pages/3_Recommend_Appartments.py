import streamlit as st
import pickle 
import pandas as pd
import numpy as np

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(page_title="Apartment Recommender", page_icon="🏢", layout="wide")

# ---------------------------------------------------
# STYLING
# ---------------------------------------------------
st.markdown("""
<style>
    .stApp { background-color: #f8fafc; }
    .rec-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #2563eb;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }
    .property-name { color: #1e3a8a; font-size: 1.2rem; font-weight: 700; }
    .visit-btn {
        background-color: #2563eb;
        color: white !important;
        padding: 8px 15px;
        border-radius: 8px;
        text-decoration: none;
        display: inline-block;
        margin-top: 10px;
        font-size: 0.9rem;
    }
    .visit-btn:hover { background-color: #1e40af; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# LOAD ASSETS
# ---------------------------------------------------
@st.cache_resource
def load_recommender_assets():
    location_df = pickle.load(open(r'App/pickle/location_distance.pkl','rb'))
    cosine_sim1 = pickle.load(open(r'App/pickle/cosine_sim1.pkl','rb'))
    cosine_sim2 = pickle.load(open(r'App/pickle/cosine_sim2.pkl','rb'))
    cosine_sim3 = pickle.load(open(r'App/pickle/cosine_sim3.pkl','rb'))
    # Dataset for links (Ensure path is correct)
    data = pd.read_csv(r'App/datasets/appartments.csv') # Assuming this has 'society' and 'link'
    return location_df, cosine_sim1, cosine_sim2, cosine_sim3, data

location_df, cosine_sim1, cosine_sim2, cosine_sim3, data = load_recommender_assets()

# ---------------------------------------------------
# RECOMMENDATION ENGINE
# ---------------------------------------------------
def recommend_properties_with_scores(property_name, top_n=10):
    # Combined Similarity Matrix
    cosine_sim_matrix = 0.5*cosine_sim1 + 0.8*cosine_sim2 + 1*cosine_sim3
    
    # Get index
    idx = location_df.index.get_loc(property_name)
    sim_scores = list(enumerate(cosine_sim_matrix[idx]))
    
    # Sort
    sorted_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # Top indices and scores
    top_indices = [i[0] for i in sorted_scores[1:top_n+1]]
    top_scores = [i[1] for i in sorted_scores[1:top_n+1]]
    
    # Property names
    top_properties = location_df.index[top_indices].tolist()
    
    return pd.DataFrame({'PropertyName': top_properties, 'SimilarityScore': top_scores})

# ---------------------------------------------------
# MAIN UI
# ---------------------------------------------------
st.title("🏢 Apartment Recommendation Engine")
st.markdown("Discover properties similar to your favorites based on amenities, price segment, and location advantages.")
st.write("---")

# Input Section
st.subheader("🔍 Find Similar Properties")
selected_apartment = st.selectbox("Select an apartment you like:", sorted(location_df.index.to_list()))

if st.button('Recommend Best Matches'):
    with st.spinner('Analyzing patterns...'):
        recommendation_df = recommend_properties_with_scores(selected_apartment)
        
        st.write(f"Top recommendations similar to **{selected_apartment}**:")
        st.write("")
        
        # Displaying Results as Cards
        for i, row in recommendation_df.iterrows():
            prop_name = row['PropertyName']
            score = row['SimilarityScore']
            
            # Fetch link from data (Matching with society name)
            # Assuming 'society' column in your csv matches the PropertyName
            link_row = data[data['PropertyName'] == prop_name]
            # Use a dummy link if not found for testing, otherwise use actual link column
            prop_link = link_row['Link'].values[0]
            
            st.markdown(f"""
                <div class="rec-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div class="property-name">{prop_name}</div>
                            <div style="color: #64748b; font-size: 0.9rem;">Match Score: {round(score*100)}%</div>
                        </div>
                        <a href="{prop_link}" target="_blank" class="visit-btn">Visit on 99acres ↗</a>
                    </div>
                </div>
            """, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3063/3063822.png", width=80)
    st.title("About the Engine")
    st.info("""
    Our hybrid recommender combines:
    - **Contextual Similarity:** Amenities & Facilities.
    - **Price Proximity:** Budget segment matching.
    - **Location Distance:** Geographic closeness.
    """)
import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime
from mapping_logic import preprocess_data, transform_data, generate_fashion_description

# --- Page Config & Styling ---
st.set_page_config(page_title="Formulaman Pro", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #F8F9FA; }
    html, body, [class*="st-"] { color: #000000 !important; }
    .stButton>button { background-color: #D1F2EB !important; color: black; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🧪 Formulaman: Fashion Hub")

# Step 1: Mandatory Category Selection
selected_cat = st.selectbox(
    "Choose a category to unlock the engine:",
    ["", "Dress", "Top & Tunic", "Kurti/Kurta", "Tshirts"]
)

if selected_cat != "":
    # Step 2: Upload
    uploaded_file = st.file_uploader(f"Upload {selected_cat} Master File", type=["csv"])

    if uploaded_file:
        df_raw = pd.read_csv(uploaded_file)
        df_processed = preprocess_data(df_raw, selected_cat)
        
        # This now matches the function name in mapping_logic.py
        df_processed['Product Description*'] = df_processed.apply(generate_fashion_description, axis=1)

        st.success(f"Processing {len(df_processed)} variations for {selected_cat}.")
        st.dataframe(df_processed, use_container_width=True)

        # Step 3: Export Hub
        st.divider()
        channels = st.pills("Select Channels:", ["Amazon", "Flipkart", "Meesho"], selection_mode="multi")

        if channels:
            tabs = st.tabs(channels)
            for i, channel in enumerate(channels):
                with tabs[i]:
                    final_df = transform_data(df_processed, channel, selected_cat)
                    csv_buffer = BytesIO()
                    final_df.to_csv(csv_buffer, index=False)
                    st.download_button(f"📥 Download {channel} CSV", csv_buffer, f"{channel}_list.csv", "text/csv")

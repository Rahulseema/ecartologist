import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime
from mapping_logic import preprocess_data, transform_data, generate_fashion_description

# --- Page Config ---
st.set_page_config(page_title="Formulaman | Admin Dashboard", layout="wide", page_icon="📊")

# --- Forced AdminUIUX Theme (Aggressive CSS for Visibility) ---
st.markdown("""
    <style>
    /* 1. Main Dashboard Background (Light Blue-Grey) */
    .stApp { 
        background-color: #F0F4F8 !important; 
    }
    
    /* 2. Global Text Force (Deep Black) */
    html, body, [class*="st-"], .stMarkdown, p, h1, h2, h3, h5, label, span {
        color: #1A202C !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* 3. White Cards for Content */
    div[data-testid="stVerticalBlock"] > div:has(div.stMarkdown), 
    div.stFileUploader, div.stDataFrame, .stSelectbox {
        background-color: #FFFFFF !important;
        padding: 24px !important;
        border-radius: 8px !important;
        border: 1px solid #E2E8F0 !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
        margin-bottom: 24px !important;
    }

    /* 4. DROPDOWN (SELECTBOX) SPECIFIC FIX */
    /* This ensures the text inside the dropdown and the options are BLACK on WHITE */
    div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border-radius: 4px;
    }
    
    /* Options list visibility */
    ul[data-testid="stSelectboxVirtualList"] li {
        color: #000000 !important;
        background-color: #FFFFFF !important;
    }

    /* Sidebar Background */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0;
    }

    /* Primary Buttons (Dark Navy/Black) */
    .stButton>button {
        background-color: #2D3748 !important;
        color: #FFFFFF !important;
        border-radius: 6px;
        font-weight: 600;
        border: none;
        width: 100%;
        height: 45px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Header ---
st.title("📊 Formulaman Dashboard")
st.markdown("##### *Enterprise-Grade Multi-Channel Listing Engine*")

# Step 1: Mandatory Category Selection
st.subheader("1️⃣ Initialize Business Vertical")
selected_cat = st.selectbox(
    "Select Category (This maps your 300+ fields):",
    ["", "Dress", "Top & Tunic", "Kurti/Kurta", "Tshirts"],
    index=0
)

if selected_cat == "":
    st.info("👋 System Standby. Please select a category vertical above to load the mapping engine.")
else:
    with st.sidebar:
        st.header("Formula Man Control")
        st.write(f"Mode: **{selected_cat}**")
        st.divider()
        try:
            with open("Master_Template_Pro_Formulaman.csv", "rb") as f:
                st.download_button("📥 Get Master Template", f, "Master_Template.csv", "text/csv")
        except: st.error("Template file missing.")

    # Step 2: Dataset Upload
    st.subheader(f"2️⃣ Upload {selected_cat} Dataset")
    uploaded_file = st.file_uploader("Drop your CSV file here for bulk processing", type=["csv"])

    if uploaded_file:
        df_raw = pd.read_csv(uploaded_file)
        df_processed = preprocess_data(df_raw, selected_cat)
        
        # Generation
        df_processed['Product Description*'] = df_processed.apply(generate_fashion_description, axis=1)

        st.success(f"Processing {len(df_processed)} SKU variations for {selected_cat}.")

        # Step 3: Analytics Preview
        st.dataframe(df_processed, use_container_width=True, hide_index=True)

        # Step 4: Export Hub
        st.divider()
        st.subheader("3️⃣ Distribution Hub")
        channels = st.pills("Select Channels:", ["Amazon", "Flipkart", "Meesho"], selection_mode="multi", default=["Amazon", "Flipkart"])

        if channels:
            date_str = datetime.now().strftime("%d-%m-%Y")
            tabs = st.tabs(channels)
            for i, channel in enumerate(channels):
                with tabs[i]:
                    final_df = transform_data(df_processed, channel, selected_cat)
                    file_name = f"{channel}_{selected_cat.replace(' ', '_')}_{date_str}.csv"
                    
                    st.write(f"Export format for **{channel}**")
                    st.dataframe(final_df.head(10), use_container_width=True)
                    
                    csv_buffer = BytesIO()
                    final_df.to_csv(csv_buffer, index=False)
                    csv_buffer.seek(0)
                    st.download_button(label=f"📥 Download {file_name}", data=csv_buffer, file_name=file_name, key=f"dl_{channel}")

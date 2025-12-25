import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime
from mapping_logic import preprocess_data, transform_data, generate_fashion_description

# --- Page Config ---
st.set_page_config(page_title="Formulaman | Admin Dashboard", layout="wide", page_icon="📊")

# --- AdminUIUX Dashboard Styling ---
st.markdown("""
    <style>
    /* Admin Dashboard Background */
    .stApp { background-color: #F0F4F8; } 
    
    /* Clean Black Typography */
    html, body, [class*="st-"] { 
        color: #1A202C !important; 
        font-family: 'Inter', sans-serif;
    }

    /* Enterprise White Cards */
    div[data-testid="stVerticalBlock"] > div:has(div.stMarkdown), 
    div.stFileUploader, div.stSelectbox, .stDataFrame {
        background-color: #FFFFFF !important;
        padding: 24px !important;
        border-radius: 8px !important;
        border: 1px solid #E2E8F0 !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
        margin-bottom: 24px !important;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E2E8F0;
    }

    /* Action Buttons */
    .stButton>button {
        background-color: #2D3748 !important;
        color: white !important;
        border-radius: 6px;
        font-weight: 600;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 Formulaman Dashboard")
st.markdown("##### *Strategic Multi-Channel Inventory Management*")

# Step 1: Mandatory Category Selection
selected_cat = st.selectbox(
    "Select Business Vertical:",
    ["", "Dress", "Top & Tunic", "Kurti/Kurta", "Tshirts"],
    index=0
)

if selected_cat == "":
    st.info("👋 Select a business vertical to initialize the listing engine.")
else:
    with st.sidebar:
        st.header("Admin Control")
        st.write(f"Active Vertical: **{selected_cat}**")
        st.divider()

    # Step 2: Enterprise Upload
    uploaded_file = st.file_uploader(f"Upload {selected_cat} Master Dataset", type=["csv"])

    if uploaded_file:
        df_raw = pd.read_csv(uploaded_file)
        df_processed = preprocess_data(df_raw, selected_cat)
        df_processed['Product Description*'] = df_processed.apply(generate_fashion_description, axis=1)

        st.success(f"Processing {len(df_processed)} SKU variations for {selected_cat}.")

        # Step 3: Analytical Preview
        st.dataframe(df_processed, use_container_width=True, hide_index=True)

        # Step 4: Distribution Hub
        st.divider()
        st.subheader("Distribution Channels")
        channels = st.pills("Active Channels:", ["Amazon", "Flipkart", "Meesho"], selection_mode="multi", default=["Amazon"])

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

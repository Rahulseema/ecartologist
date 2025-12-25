import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime
from mapping_logic import preprocess_data, transform_data, generate_fashion_description

# --- Page Config ---
st.set_page_config(page_title="Formulaman Pro", layout="wide", page_icon="🧪")

# --- Premium UI Customization (Blue-Grey & White) ---
st.markdown("""
    <style>
    /* Background and Text */
    .stApp { background-color: #E1E5EA; } /* Light Blue-Grey Background */
    html, body, [class*="st-"] { color: #000000 !important; font-weight: 500; }
    
    /* White Content Boxes */
    div[data-testid="stVerticalBlock"] > div:has(div.stMarkdown), 
    div[data-testid="stVerticalBlock"] > div:has(div.stDataFrame),
    div.stFileUploader, div.stSelectbox {
        background-color: #FFFFFF !important;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }

    /* Buttons and UI Elements */
    .stButton>button { background-color: #F0F2F6 !important; color: black; border: 1px solid #D1D5DB; border-radius: 8px; font-weight: bold; }
    .stTabs [aria-selected="true"] { background-color: #FFFFFF !important; border-bottom: 3px solid #2C3E50 !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🧪 Formulaman: Deep Listing Pro")
st.markdown("##### *Unified Automation for Amazon, Flipkart, and Meesho*")

# Step 1: Mandatory Category Selection
st.subheader("1️⃣ Select Business Category")
selected_cat = st.selectbox(
    "Choose your product category to unlock the engine:",
    ["", "Dress", "Top & Tunic", "Kurti/Kurta", "Tshirts"],
    index=0
)

if selected_cat == "":
    st.info("👋 Welcome! Please select a category above to start your automation formula.")
else:
    # Sidebar Template Download
    with st.sidebar:
        st.header("Formula Man HQ")
        st.write(f"Category: **{selected_cat}**")
        try:
            with open("Master_Template_Pro_Formulaman.csv", "rb") as f:
                st.download_button("📥 Download Master CSV", f, "Master_Template.csv", "text/csv")
        except: st.warning("Master Template file not found in directory.")

    # Step 2: Upload
    st.subheader(f"2️⃣ Upload {selected_cat} Master File")
    uploaded_file = st.file_uploader("Drop your Master Template here", type=["csv"])

    if uploaded_file:
        df_raw = pd.read_csv(uploaded_file)
        df_processed = preprocess_data(df_raw, selected_cat)
        
        # Auto-SEO Descriptions
        df_processed['Product Description*'] = df_processed.apply(generate_fashion_description, axis=1)

        st.success(f"Processing {len(df_processed)} variations for {selected_cat}.")

        # Step 3: Preview
        st.dataframe(
            df_processed, 
            column_config={"Main Image*": st.column_config.ImageColumn("Image")},
            use_container_width=True, hide_index=True
        )

        # Step 4: Export Hub
        st.divider()
        st.subheader("3️⃣ Marketplace Export Hub")
        channels = st.pills("Select Channels:", ["Amazon", "Flipkart", "Meesho"], selection_mode="multi", default=["Amazon", "Flipkart"])

        if channels:
            date_str = datetime.now().strftime("%d-%m-%Y")
            tabs = st.tabs(channels)
            for i, channel in enumerate(channels):
                with tabs[i]:
                    final_df = transform_data(df_processed, channel, selected_cat)
                    file_name = f"{channel}_{selected_cat.replace(' ', '_')}_{date_str}.csv"
                    
                    st.write(f"Generating file for **{channel}**")
                    st.dataframe(final_df.head(10), use_container_width=True)
                    
                    csv_buffer = BytesIO()
                    final_df.to_csv(csv_buffer, index=False)
                    csv_buffer.seek(0)
                    st.download_button(label=f"📥 Download {file_name}", data=csv_buffer, file_name=file_name, mime="text/csv", key=f"dl_{channel}")

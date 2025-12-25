import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime
from mapping_logic import preprocess_data, transform_data, generate_fashion_description

# --- Page Config ---
st.set_page_config(page_title="Formulaman | Admin Console", layout="wide", page_icon="📊")

# --- Forced High-Visibility CSS ---
st.markdown("""
    <style>
    /* 1. Main Background: Light Blue-Grey */
    .stApp { background-color: #F0F4F8 !important; }
    
    /* 2. Global Text: Solid Black */
    html, body, [class*="st-"], .stMarkdown, p, h1, h2, h3, h5, label, span {
        color: #000000 !important;
        font-weight: 600 !important;
    }

    /* 3. White Cards for Visibility */
    .stSelectbox, .stFileUploader, .stDataFrame, .stAlert {
        background-color: #FFFFFF !important;
        padding: 20px !important;
        border-radius: 10px !important;
        border: 2px solid #D1D5DB !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
        margin-bottom: 20px !important;
    }

    /* 4. Dropdown (Selectbox) Specific Fix: White BG + Black Text */
    div[data-testid="stSelectbox"] div[data-baseweb="select"] {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        cursor: pointer;
    }
    
    /* 5. File Uploader Text visibility */
    div[data-testid="stFileUploader"] section {
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }

    /* 6. Action Buttons: High Contrast Dark Navy */
    .stButton>button {
        background-color: #1F2937 !important;
        color: #FFFFFF !important;
        border-radius: 8px;
        font-weight: bold;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 Formulaman Admin Console")
st.markdown("##### *Unified Listing Engine for Multi-Channel Scaling*")

# Step 1: Vertical Selection
with st.container():
    st.subheader("1️⃣ Select Category Vertical")
    selected_cat = st.selectbox(
        "Choose your product category to activate the engine:",
        ["", "Dress", "Top & Tunic", "Kurti/Kurta", "Tshirts"],
        index=0
    )

if selected_cat == "":
    st.info("👋 System Standby. Select a vertical to begin.")
else:
    # --- Generate Dummy Sample Data ---
    sample_df = pd.DataFrame({
        'SKU Code*': ['SKU001'], 'Product Name*': [f'Sample {selected_cat}'],
        'Brand*': ['Formula Man'], 'MRP*': [1999], 'Selling Price*': [899],
        'Inventory*': [100], 'Material*': ['Cotton'], 'HSN*': ['6204'],
        'Weight_KG*': [0.4], 'Length_CM*': [30], 'Breadth_CM*': [25], 'Height_CM*': [5],
        'Main Image*': ['https://example.com/image.jpg'],
        'Variations (comma separated)*': ['S, M, L, XL']
    })
    csv_sample = sample_df.to_csv(index=False).encode('utf-8')

    # Step 2: Data Import
    with st.container():
        st.subheader(f"2️⃣ {selected_cat} Dataset Import")
        
        # Download Sample Template
        st.download_button(
            label=f"📥 Download {selected_cat} Sample Template",
            data=csv_sample,
            file_name=f"Sample_{selected_cat.replace(' ', '_')}.csv",
            mime="text/csv"
        )
        
        uploaded_file = st.file_uploader("Upload your completed Master File below:", type=["csv"])

    if uploaded_file:
        df_raw = pd.read_csv(uploaded_file)
        df_processed = preprocess_data(df_raw, selected_cat)
        df_processed['Product Description*'] = df_processed.apply(generate_fashion_description, axis=1)

        st.success(f"Processing SKU Variations for {selected_cat}...")
        st.dataframe(df_processed, use_container_width=True, hide_index=True)

        # Step 3: Distribution
        st.divider()
        st.subheader("3️⃣ Marketplace Distribution Hub")
        tabs = st.tabs(["Amazon", "Flipkart", "Meesho"])
        
        channel_names = ["Amazon", "Flipkart", "Meesho"]
        for i, channel in enumerate(channel_names):
            with tabs[i]:
                final_df = transform_data(df_processed, channel, selected_cat)
                st.dataframe(final_df.head(10), use_container_width=True)
                
                csv_out = final_df.to_csv(index=False).encode('utf-8')
                st.download_button(f"📥 Download {channel} CSV", csv_out, f"{channel}_{selected_cat}.csv", key=f"dl_{channel}")

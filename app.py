import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime
from mapping_logic import preprocess_data, transform_data, generate_fashion_description

# --- Page Config ---
st.set_page_config(page_title="Formulaman | Admin Dashboard", layout="wide", page_icon="📊")

# --- Aggressive AdminUIUX Styling (Forced Stability) ---
st.markdown("""
    <style>
    .stApp { background-color: #F0F4F8 !important; }
    html, body, [class*="st-"], .stMarkdown, p, h1, h2, h3, h5, label, span {
        color: #000000 !important;
        font-weight: 500 !important;
    }
    /* White Cards */
    .stSelectbox, .stFileUploader, div[data-testid="stVerticalBlock"] > div:has(div.stDataFrame) {
        background-color: #FFFFFF !important;
        padding: 20px !important;
        border-radius: 8px !important;
        border: 1px solid #E2E8F0 !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
        margin-bottom: 20px !important;
    }
    /* Dropdown Text Visibility */
    div[data-testid="stSelectbox"] div[data-baseweb="select"] {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 1px solid #CBD5E0 !important;
    }
    /* Buttons */
    .stButton>button { background-color: #2D3748 !important; color: white !important; border-radius: 6px; }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 Formulaman Admin Console")

# Step 1: Category Vertical
with st.container():
    st.subheader("1️⃣ Select Business Vertical")
    selected_cat = st.selectbox(
        "Business Category:",
        ["", "Dress", "Top & Tunic", "Kurti/Kurta", "Tshirts"],
        index=0
    )

if selected_cat == "":
    st.info("👋 Select a vertical to unlock the processing engine.")
else:
    # --- DUMMY SAMPLE DATA GENERATION ---
    sample_data = {
        'SKU Code*': ['SKU001'], 'Product Name*': [f'Sample {selected_cat}'],
        'Brand*': ['Formula Man'], 'MRP*': [1999], 'Selling Price*': [899],
        'Inventory*': [100], 'Material*': ['Cotton'], 'HSN*': ['6204'],
        'Weight_KG*': [0.4], 'Length_CM*': [30], 'Breadth_CM*': [25], 'Height_CM*': [5],
        'Main Image*': ['https://example.com/image.jpg'],
        'Variations (comma separated)*': ['S, M, L, XL']
    }
    sample_df = pd.DataFrame(sample_data)
    csv_sample = sample_df.to_csv(index=False).encode('utf-8')

    # --- Step 2: Download & Upload Area ---
    with st.container():
        st.subheader(f"2️⃣ Data Import: {selected_cat}")
        
        # Download Sample (Just above Upload)
        st.download_button(
            label=f"📥 Download {selected_cat} Sample Template",
            data=csv_sample,
            file_name=f"Sample_Template_{selected_cat.replace(' ', '_')}.csv",
            mime="text/csv",
            help="Download this file, fill your data, and upload it below."
        )
        
        uploaded_file = st.file_uploader("Upload your completed Master File", type=["csv"])

    if uploaded_file:
        df_raw = pd.read_csv(uploaded_file)
        df_processed = preprocess_data(df_raw, selected_cat)
        df_processed['Product Description*'] = df_processed.apply(generate_fashion_description, axis=1)

        st.success(f"Successfully processed variations for {selected_cat}.")
        st.dataframe(df_processed, use_container_width=True, hide_index=True)

        # Step 3: Distribution
        st.divider()
        st.subheader("3️⃣ Marketplace Distribution Hub")
        channels = st.tabs(["Amazon", "Flipkart", "Meesho"])
        
        channel_names = ["Amazon", "Flipkart", "Meesho"]
        for i, channel in enumerate(channel_names):
            with channels[i]:
                final_df = transform_data(df_processed, channel, selected_cat)
                st.dataframe(final_df.head(10), use_container_width=True)
                
                csv_out = final_df.to_csv(index=False).encode('utf-8')
                st.download_button(f"📥 Download {channel} CSV", csv_out, f"{channel}_list.csv", key=f"dl_{channel}")

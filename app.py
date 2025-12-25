import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime
from mapping_logic import preprocess_data, transform_data, generate_fashion_description

# --- Page Config ---
st.set_page_config(page_title="Formulaman | Admin Console", layout="wide", page_icon="📊")

# --- Forced AdminUIUX Dashboard Styling ---
st.markdown("""
    <style>
    .stApp { background-color: #F0F4F8 !important; }
    html, body, [class*="st-"], .stMarkdown, p, h1, h2, h3, h5, label, span {
        color: #000000 !important;
        font-weight: 500 !important;
    }
    /* White Card containers */
    .stFileUploader, .stDataFrame, .stAlert {
        background-color: #FFFFFF !important;
        padding: 24px !important;
        border-radius: 8px !important;
        border: 1px solid #E2E8F0 !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
    }
    /* Modern Tab Styling for Category Selection */
    .stTabs [data-baseweb="tab-list"] { background-color: #FFFFFF; padding: 10px; border-radius: 8px; border: 1px solid #E2E8F0; }
    .stTabs [data-baseweb="tab"] { color: #4A5568 !important; padding: 12px 24px; }
    .stTabs [aria-selected="true"] { background-color: #2D3748 !important; color: #FFFFFF !important; border-radius: 6px; }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 Formulaman Admin Console")
st.markdown("### 1️⃣ Choose Your Listing Vertical")

# --- Category Tabs ---
categories = ["Dress", "Top & Tunic", "Kurti/Kurta", "Tshirts"]
cat_tabs = st.tabs(categories)

for idx, cat in enumerate(categories):
    with cat_tabs[idx]:
        st.subheader(f"Listing Engine: {cat}")
        
        # Dummy Template for specific category
        sample_df = pd.DataFrame({
            'SKU Code*': ['SKU_001'], 'Product Name*': [f'Sample {cat}'],
            'Brand*': ['Formula Man'], 'MRP*': [1999], 'Selling Price*': [899],
            'Inventory*': [100], 'Material*': ['Cotton'], 'HSN*': ['6204'],
            'Weight_KG*': [0.4], 'Main Image*': ['https://example.com/img.jpg'],
            'Variations (comma separated)*': ['S, M, L']
        })
        csv_sample = sample_df.to_csv(index=False).encode('utf-8')

        # Download and Upload Section
        col1, col2 = st.columns([1, 2])
        with col1:
            st.download_button(f"📥 Download {cat} Template", csv_sample, f"{cat}_template.csv", "text/csv")
        with col2:
            uploaded_file = st.file_uploader(f"Upload {cat} Master File", type=["csv"], key=f"upload_{cat}")

        if uploaded_file:
            df_raw = pd.read_csv(uploaded_file)
            df_processed = preprocess_data(df_raw, cat)
            df_processed['Product Description*'] = df_processed.apply(generate_fashion_description, axis=1)

            st.success(f"Processing SKU variations for {cat} mode...")
            st.dataframe(df_processed, use_container_width=True, hide_index=True)

            # Marketplace Distribution Hub
            st.divider()
            st.subheader("2️⃣ Marketplace Distribution Hub")
            m_tabs = st.tabs(["Amazon", "Flipkart", "Meesho"])
            
            for i, channel in enumerate(["Amazon", "Flipkart", "Meesho"]):
                with m_tabs[i]:
                    final_df = transform_data(df_processed, channel, cat)
                    st.dataframe(final_df.head(10), use_container_width=True)
                    csv_out = final_df.to_csv(index=False).encode('utf-8')
                    st.download_button(f"📥 Export {channel} CSV", csv_out, f"{channel}_{cat}.csv", key=f"dl_{channel}_{cat}")

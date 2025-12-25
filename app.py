import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime
from mapping_logic import preprocess_data, transform_data, generate_fashion_description

# --- Enterprise Configuration ---
st.set_page_config(page_title="Formulaman | Admin Console", layout="wide", page_icon="📊")

# --- Forced High-Visibility Dashboard Styling ---
st.markdown("""
    <style>
    /* 1. AdminUIUX Background: Light Blue-Grey */
    .stApp { background-color: #F0F4F8 !important; }
    
    /* 2. Global Text: High-Contrast Black */
    html, body, [class*="st-"], .stMarkdown, p, h1, h2, h3, h5, label, span {
        color: #000000 !important;
        font-weight: 600 !important;
    }

    /* 3. White Cards for Visibility */
    .stFileUploader, .stDataFrame, .stAlert, .stSelectbox {
        background-color: #FFFFFF !important;
        padding: 24px !important;
        border-radius: 10px !important;
        border: 2px solid #E2E8F0 !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
        margin-bottom: 24px !important;
    }

    /* 4. INTERACTIVE TABS: Charcoal on Hover/Selection */
    .stTabs [data-baseweb="tab-list"] { background-color: #FFFFFF; padding: 10px; border-radius: 8px; gap: 10px; }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #F8FAFC !important;
        color: #000000 !important;
        border-radius: 6px !important;
        padding: 12px 24px !important;
        transition: 0.3s ease !important;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background-color: #333333 !important; /* Charcoal BG */
        color: #FFFFFF !important; /* White Text */
    }

    .stTabs [aria-selected="true"] {
        background-color: #000000 !important; /* Solid Black */
        color: #FFFFFF !important;
        font-weight: bold !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 Formulaman Admin Console")
st.markdown("### 1️⃣ Initialize Listing Vertical")

# --- Category Selection (Tabbed Switcher) ---
categories = ["Dress", "Top & Tunic", "Kurti/Kurta", "Tshirts"]
main_tabs = st.tabs(categories)

for idx, cat in enumerate(categories):
    with main_tabs[idx]:
        st.subheader(f"Current Engine: {cat} Mode")
        
        # --- Generate Category-Specific Dummy Template ---
        sample_df = pd.DataFrame({
            'SKU Code*': ['SKU_123'], 'Product Name*': [f'Premium {cat}'],
            'Brand*': ['Formula Man'], 'MRP*': [2499], 'Selling Price*': [999],
            'Inventory*': [50], 'Material*': ['Viscose'], 'HSN*': ['6204'],
            'Weight_KG*': [0.5], 'Main Image*': ['https://example.com/item.jpg'],
            'Variations (comma separated)*': ['S, M, L, XL']
        })
        csv_sample = sample_df.to_csv(index=False).encode('utf-8')

        # Download & Upload Section
        col_dl, col_ul = st.columns([1, 2])
        with col_dl:
            st.download_button(
                label=f"📥 Download {cat} Template",
                data=csv_sample,
                file_name=f"Template_{cat.replace(' ', '_')}.csv",
                mime="text/csv"
            )
        with col_ul:
            uploaded_file = st.file_uploader(f"Upload {cat} Master File", type=["csv"], key=f"up_{cat}")

        if uploaded_file:
            df_raw = pd.read_csv(uploaded_file)
            df_processed = preprocess_data(df_raw, cat)
            df_processed['Product Description*'] = df_processed.apply(generate_fashion_description, axis=1)

            st.success(f"Processing SKU Variations for {cat} vertical...")
            st.dataframe(df_processed, use_container_width=True, hide_index=True)

            # --- Distribution Tab ---
            st.divider()
            st.subheader("2️⃣ Distribution Hub")
            m_tabs = st.tabs(["Amazon", "Flipkart", "Meesho"])
            for i, channel in enumerate(["Amazon", "Flipkart", "Meesho"]):
                with m_tabs[i]:
                    final_df = transform_data(df_processed, channel, cat)
                    st.dataframe(final_df.head(10), use_container_width=True)
                    csv_out = final_df.to_csv(index=False).encode('utf-8')
                    st.download_button(f"📥 Export {channel} CSV", csv_out, f"{channel}_{cat}.csv", key=f"dl_{channel}_{cat}")

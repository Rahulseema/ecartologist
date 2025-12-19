import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime
from mapping_logic import preprocess_data, transform_data, generate_dynamic_description

st.set_page_config(page_title="Formulaman Pro", layout="wide", page_icon="🧪")

# --- Premium Pastel UI ---
st.markdown("""
    <style>
    .stApp { background-color: #F8F9F9; }
    html, body, [class*="st-"] { color: #000000 !important; font-weight: 500; }
    .stButton>button { background-color: #D6EAF8 !important; color: black !important; border-radius: 12px; font-weight: bold; border: 1px solid #AED6F1; transition: 0.3s; }
    .stButton>button:hover { background-color: #AED6F1 !important; transform: scale(1.02); }
    .stTabs [aria-selected="true"] { background-color: #D1F2EB !important; color: black !important; border-radius: 10px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🧪 Formulaman: Deep Listing Pro")
st.markdown("##### *Unified Master Template for Amazon, Flipkart, and Meesho*")

with st.sidebar:
    st.header("Formula Man HQ")
    st.info("Goal: Maximize Revenue through Master Automation")
    st.write("v4.0 (Deep Mapping Edition)")

# 1. File Upload
uploaded_file = st.file_uploader("📂 Upload Master Template Pro CSV", type=["csv"])

if uploaded_file:
    df_raw = pd.read_csv(uploaded_file)
    df_processed = preprocess_data(df_raw)
    
    # Auto-Description Generation
    if 'Product Description*' not in df_processed.columns or df_processed['Product Description*'].isnull().all():
        df_processed['Product Description*'] = df_processed.apply(generate_dynamic_description, axis=1)

    st.success(f"Successfully standardizing {len(df_processed)} variations across all deep fields.")

    # 2. Deep Data Verification
    st.subheader("🔍 Deep Field Verification")
    st.dataframe(
        df_processed,
        column_config={
            "Main Image*": st.column_config.ImageColumn("Preview"),
            "Product Description*": st.column_config.TextColumn("Generated Description", width="large")
        },
        use_container_width=True,
        hide_index=True
    )

    # 3. Channel Tabs & Download
    st.divider()
    st.subheader("🎯 Marketplace Export Hub")
    selected_channels = st.pills("Select Channels:", options=["Amazon", "Flipkart", "Meesho"], selection_mode="multi", default=["Amazon", "Flipkart"])

    if selected_channels:
        cat_name = str(df_processed['Product Category*'].iloc[0]).replace(" ", "_") if 'Product Category*' in df_processed.columns else "List"
        date_str = datetime.now().strftime("%d-%m-%Y")
        
        tabs = st.tabs(selected_channels)
        for i, channel in enumerate(selected_channels):
            with tabs[i]:
                final_df = transform_data(df_processed, channel)
                file_name = f"{channel}_{cat_name}_{date_str}.csv"
                
                st.write(f"Generating **{len(final_df)}** rows for {channel}")
                st.dataframe(final_df.head(10), use_container_width=True)

                csv_buffer = BytesIO()
                final_df.to_csv(csv_buffer, index=False)
                csv_buffer.seek(0)
                st.download_button(label=f"📥 Download {file_name}", data=csv_buffer, file_name=file_name, mime="text/csv", key=f"dl_{channel}")

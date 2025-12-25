import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime
from mapping_logic import preprocess_data, transform_data, generate_fashion_description

# --- Page Config ---
st.set_page_config(page_title="Formulaman Pro", layout="wide", page_icon="🧪")

# --- UI Customization ---
st.markdown("""
    <style>
    .stApp { background-color: #FDF9F3; } /* Pastel Cream */
    html, body, [class*="st-"] { color: #000000 !important; font-weight: 500; }
    .stButton>button { background-color: #E8F8F5 !important; border-radius: 12px; font-weight: bold; border: 1px solid #A3E4D7; }
    .stTabs [aria-selected="true"] { background-color: #FADBD8 !important; color: black !important; border-radius: 8px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🧪 Formulaman: Deep Listing Pro")
st.markdown("##### *Unified Master Engine for Fashion Marketplaces*")

# --- Sidebar ---
with st.sidebar:
    st.header("Formula Man Control")
    st.info("Automate 300+ fields with one master formula.")
    st.divider()
    st.write("v6.0 (Enterprise Edition)")

# Step 1: Category Lock
st.subheader("1️⃣ Select Business Category")
selected_cat = st.selectbox(
    "Identify your product niche to unlock the engine:",
    ["", "Dress", "Top & Tunic", "Kurti/Kurta", "Tshirts"],
    index=0
)

if selected_cat == "":
    st.warning("⚠️ Please select a category to proceed.")
else:
    # Step 2: Upload
    st.subheader(f"2️⃣ Upload {selected_cat} Master Sheet")
    uploaded_file = st.file_uploader("Drop your Master CSV here", type=["csv"])

    if uploaded_file:
        df_raw = pd.read_csv(uploaded_file)
        
        # Step 3: Engine Processing
        df_processed = preprocess_data(df_raw, selected_cat)
        
        # Auto-SEO content generation
        df_processed['Product Description*'] = df_processed.apply(generate_fashion_description, axis=1)

        st.success(f"Successfully standardizing listings for: {selected_cat}")

        # Verification Preview
        st.dataframe(
            df_processed, 
            column_config={"Main Image*": st.column_config.ImageColumn("Visual Preview")},
            use_container_width=True, hide_index=True
        )

        # Step 4: Marketplace Export
        st.divider()
        st.subheader("3️⃣ Marketplace Export Hub")
        channels = st.pills("Active Channels:", ["Amazon", "Flipkart", "Meesho"], selection_mode="multi", default=["Amazon", "Flipkart"])

        if channels:
            date_str = datetime.now().strftime("%d-%m-%Y")
            tabs = st.tabs(channels)
            for i, channel in enumerate(channels):
                with tabs[i]:
                    final_df = transform_data(df_processed, channel, selected_cat)
                    file_name = f"{channel}_{selected_cat.replace(' ', '_')}_{date_str}.csv"
                    
                    st.write(f"Generating **{len(final_df)}** SKU variations for {channel}")
                    st.dataframe(final_df.head(10), use_container_width=True)
                    
                    csv_buffer = BytesIO()
                    final_df.to_csv(csv_buffer, index=False)
                    csv_buffer.seek(0)
                    st.download_button(
                        label=f"📥 Download {file_name}",
                        data=csv_buffer,
                        file_name=file_name,
                        mime="text/csv",
                        key=f"dl_{channel}"
                    )

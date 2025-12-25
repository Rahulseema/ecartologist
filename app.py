import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime
from mapping_logic import preprocess_data, transform_data, generate_dynamic_description

st.set_page_config(page_title="Formulaman Pro", layout="wide", page_icon="🧪")

# --- Custom Pastel UI Theme (Black Text) ---
st.markdown("""
    <style>
    .stApp { background-color: #F9F9FB; }
    html, body, [class*="st-"] { color: #000000 !important; font-weight: 500; }
    .stButton>button { background-color: #E8F6F3 !important; color: black !important; border-radius: 10px; border: 1px solid #A3E4D7; }
    .stSelectbox label { color: black !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🧪 Formulaman: Deep Fashion Hub")

# Step 1: Mandatory Category Selection
st.subheader("1️⃣ Select Category First")
selected_cat = st.selectbox(
    "Choose a category to unlock the Master Template and Uploader:",
    ["", "Dress", "Top & Tunic", "Kurti/Kurta", "Tshirts"],
    index=0
)

if selected_cat == "":
    st.info("👋 Select a category above to get started.")
else:
    # Sidebar Sample Download
    with st.sidebar:
        st.header("Formula Man HQ")
        st.write(f"Active Mode: **{selected_cat}**")
        with open("Master_Template_Pro_Formulaman.csv", "rb") as f:
            st.download_button("📥 Download Master Template", f, "Master_Template.csv", "text/csv")

    # Step 2: File Upload
    st.subheader(f"2️⃣ Upload your {selected_cat} Master File")
    uploaded_file = st.file_uploader("📂 Drop Master CSV Here", type=["csv"])

    if uploaded_file:
        df_raw = pd.read_csv(uploaded_file)
        df_processed = preprocess_data(df_raw, selected_cat)
        
        # Auto-SEO Descriptions
        df_processed['Product Description*'] = df_processed.apply(generate_dynamic_description, axis=1)

        st.success(f"Successfully mapped {len(df_processed)} variations for {selected_cat}!")

        # Step 3: Preview and Export
        st.dataframe(df_processed, column_config={"Main Image*": st.column_config.ImageColumn("Preview")}, use_container_width=True)
        
        st.divider()
        channels = st.pills("Select Channels:", ["Amazon", "Flipkart", "Meesho"], selection_mode="multi", default=["Amazon", "Flipkart"])

        if channels:
            date_str = datetime.now().strftime("%d-%m-%Y")
            tabs = st.tabs(channels)
            for i, channel in enumerate(channels):
                with tabs[i]:
                    final_df = transform_data(df_processed, channel, selected_cat)
                    file_name = f"{channel}_{selected_cat.replace(' ', '_')}_{date_str}.csv"
                    
                    st.write(f"### {channel} Export Preview")
                    st.dataframe(final_df.head(5), use_container_width=True)
                    
                    csv_buffer = BytesIO()
                    final_df.to_csv(csv_buffer, index=False)
                    csv_buffer.seek(0)
                    st.download_button(f"📥 Download {file_name}", csv_buffer, file_name, "text/csv", key=f"dl_{channel}")

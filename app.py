import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime
from mapping_logic import preprocess_data, transform_data, generate_ai_description

st.set_page_config(page_title="Formulaman AI", layout="wide", page_icon="🧪")

st.title("🧪 Formulaman AI: Smart Listing Creator")

# Sidebar for API Key and Branding
with st.sidebar:
    st.header("Settings")
    user_api_key = st.text_input("Enter Google Gemini API Key", type="password")
    st.info("Get a free key at aistudio.google.com")
    st.divider()
    st.write("Channel: Formula Man")

uploaded_file = st.file_uploader("Upload Master CSV", type=["csv"])

if uploaded_file:
    df_raw = pd.read_csv(uploaded_file)
    df_processed = preprocess_data(df_raw)
    
    st.subheader("🔍 Step 1: Verify & Generate AI Content")
    
    # Button to trigger AI
    if st.button("✨ Generate AI Descriptions"):
        if not user_api_key:
            st.warning("Please enter your API Key in the sidebar.")
        else:
            with st.spinner("AI is writing descriptions for all variations..."):
                # Apply AI function to each row
                df_processed['Product Description*'] = df_processed.apply(
                    lambda row: generate_ai_description(
                        row.get('Product Name*', ''),
                        row.get('Brand*', ''),
                        row.get('Fabric Type*', ''),
                        row.get('Variations (comma separated)*', ''),
                        user_api_key
                    ), axis=1
                )
            st.success("Descriptions Generated!")

    # Display the table with Image and the new AI Description
    st.dataframe(
        df_processed,
        column_config={
            "Main Image*": st.column_config.ImageColumn("Preview"),
            "Product Description*": st.column_config.TextColumn("AI Description", width="large")
        },
        use_container_width=True,
        hide_index=True
    )

    # ... (Rest of your Channel Selection & Download logic)
    st.divider()
    channels = st.multiselect("Select Channels:", ["Amazon", "Flipkart", "Meesho"], default=["Amazon"])
    
    if st.button("Generate Downloadable Files"):
        # (Include your existing download logic here)
        st.write("Ready for download!")

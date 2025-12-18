import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime
from mapping_logic import preprocess_data, transform_data, generate_ai_description

st.set_page_config(page_title="Formulaman", layout="wide", page_icon="🧪")

st.title("🧪 Formulaman: AI Listing Lab")

# Sidebar for API Key & Branding
with st.sidebar:
    st.header("Formula Man Control Panel")
    api_key = st.text_input("Gemini API Key", type="password", help="Get it from aistudio.google.com")
    st.divider()
    st.write("Goal: Scale Sales & Earn Money")

# 1. File Upload
uploaded_file = st.file_uploader("Upload Master CSV", type=["csv"])

if uploaded_file:
    df_raw = pd.read_csv(uploaded_file)
    
    # Pre-process: Explode Variations
    df_processed = preprocess_data(df_raw)
    
    # 2. AI Generation Action
    if st.button("✨ Generate AI Descriptions"):
        if not api_key:
            st.error("Please enter an API Key in the sidebar!")
        else:
            with st.spinner("AI is crafting descriptions..."):
                df_processed['Product Description*'] = df_processed.apply(
                    lambda row: generate_ai_description(
                        row.get('Product Name*', ''),
                        row.get('Brand*', ''),
                        row.get('Fabric Type*', ''),
                        row.get('Variations (comma separated)*', ''),
                        api_key
                    ), axis=1
                )
            st.success("Descriptions Ready!")

    # 3. Verification Table with IMAGE Column
    st.subheader("🔍 Verification Table")
    st.dataframe(
        df_processed,
        column_config={
            "Main Image*": st.column_config.ImageColumn("Preview"),
            "Product Description*": st.column_config.TextColumn("AI Description", width="large")
        },
        use_container_width=True,
        hide_index=True
    )

    # 4. Export Logic
    st.divider()
    channels = st.multiselect("Select Channels:", ["Amazon", "Flipkart", "Meesho", "Ajio"], default=["Amazon"])
    
    # Get category for dynamic naming
    cat = str(df_processed['Product Category*'].iloc[0]).replace(" ", "_") if 'Product Category*' in df_processed.columns else "Listing"
    date_str = datetime.now().strftime("%d-%m-%Y")

    if st.button("Prepare Final Files"):
        tabs = st.tabs(channels)
        for i, channel in enumerate(channels):
            with tabs[i]:
                final_df = transform_data(df_processed, channel)
                file_name = f"{channel}_{cat}_{date_str}.csv"
                
                st.write(f"Preview for {file_name}")
                st.dataframe(final_df.head())

                # Download button
                csv_buffer = BytesIO()
                final_df.to_csv(csv_buffer, index=False)
                csv_buffer.seek(0)
                
                st.download_button(
                    label=f"📥 Download {file_name}",
                    data=csv_buffer,
                    file_name=file_name,
                    mime="text/csv",
                    key=f"btn_{channel}"
                )

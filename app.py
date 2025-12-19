import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime
from mapping_logic import preprocess_data, transform_data, generate_template_description

st.set_page_config(page_title="Formulaman", layout="wide", page_icon="🧪")

# Branding
st.title("🧪 Formulaman: Bulk Listing Automator")
st.markdown("##### Explode Variations and Generate Listings Instantly.")

with st.sidebar:
    st.header("Formula Man HQ")
    st.info("Goal: Maximize Revenue via Automation")
    st.write("v2.0 (Stable - No AI Errors)")

# 1. File Upload
uploaded_file = st.file_uploader("Upload Master CSV", type=["csv"])

if uploaded_file:
    df_raw = pd.read_csv(uploaded_file)
    
    # Process Data
    df_processed = preprocess_data(df_raw)
    
    # Generate Template Descriptions automatically (Reliable Alternative to AI)
    if 'Product Description*' not in df_processed.columns or df_processed['Product Description*'].isnull().all():
        df_processed['Product Description*'] = df_processed.apply(generate_template_description, axis=1)

    st.success(f"Successfully processed {len(df_processed)} variations!")

    # 2. Verification Table
    st.subheader("🔍 Verification Table")
    st.dataframe(
        df_processed,
        column_config={
            "Main Image*": st.column_config.ImageColumn("Image Preview", width="medium"),
            "Product Description*": st.column_config.TextColumn("Description", width="large")
        },
        use_container_width=True,
        hide_index=True
    )

    # 3. Channel Selection & Export
    st.divider()
    channels = st.multiselect("Select Marketplace Formats:", ["Amazon", "Flipkart", "Meesho"], default=["Amazon", "Flipkart"])

    if st.button("Generate Marketplace Files"):
        # Dynamic Naming Logic
        cat = str(df_processed['Product Category*'].iloc[0]).replace(" ", "_") if 'Product Category*' in df_processed.columns else "List"
        date_str = datetime.now().strftime("%d-%m-%Y")
        
        tabs = st.tabs(channels)
        for i, channel in enumerate(channels):
            with tabs[i]:
                final_df = transform_data(df_processed, channel)
                file_name = f"{channel}_{cat}_{date_str}.csv"
                
                st.write(f"**Previewing:** `{file_name}`")
                st.dataframe(final_df.head(5), use_container_width=True)

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

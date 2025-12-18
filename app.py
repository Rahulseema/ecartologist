import streamlit as st
import pandas as pd
from io import BytesIO
from mapping_logic import preprocess_data, transform_data

st.set_page_config(page_title="Formulaman", layout="wide", page_icon="🧪")

st.title("🧪 Formulaman: Marketplace Listing Tool")
st.markdown("### Automate your e-commerce listings for Amazon, Flipkart, Meesho & more.")

# Sidebar for instructions/branding
with st.sidebar:
    st.header("About Formulaman")
    st.info("Upload your master sheet. We expand variations and format columns automatically.")
    st.write("Created by: Formula Man")

# 1. Upload Section
uploaded_file = st.file_uploader("Upload your Master CSV file", type=["csv"])

if uploaded_file:
    # Read CSV (First row is header by default)
    df_raw = pd.read_csv(uploaded_file)
    
    st.success("File uploaded successfully!")
    
    # 2. Preprocess (Variation Explosion)
    df_processed = preprocess_data(df_raw)
    
    st.subheader("Data Preview (Variations Expanded)")
    st.dataframe(df_processed.head(10))

    # 3. Channel Selection
    channels = st.multiselect(
        "Select Channels to Generate Files for:",
        ["Amazon", "Flipkart", "Meesho", "Myntra", "Ajio"],
        default=["Amazon", "Flipkart"]
    )

    if st.button("Generate Listing Files"):
        tabs = st.tabs(channels)
        
        for i, channel in enumerate(channels):
            with tabs[i]:
                # Map data to channel format
                final_df = transform_data(df_processed, channel)
                
                st.write(f"### {channel} Template Preview")
                st.dataframe(final_df.head())

                # Prepare for download
                csv_buffer = BytesIO()
                final_df.to_csv(csv_buffer, index=False)
                csv_buffer.seek(0)
                
                st.download_button(
                    label=f"Download {channel} CSV",
                    data=csv_buffer,
                    file_name=f"Formulaman_{channel}_Listing.csv",
                    mime="text/csv",
                    key=f"dl_{channel}"
                )

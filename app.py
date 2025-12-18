import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Formulaman - Listing Creator", layout="wide")

st.title("🧪 Formulaman: Marketplace Listing Generator")
st.subheader("Upload your master CSV to generate channel-ready files")

# 1. File Uploader
uploaded_file = st.file_uploader("Choose your master CSV file", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("### Preview of Master Data", df.head())

    # 2. Select Channels
    channels = st.multiselect(
        "Select target channels",
        ["Amazon", "Flipkart", "Meesho", "Myntra", "Ajio"]
    )

    if st.button("Generate Files"):
        tabs = st.tabs(channels)

        for i, channel in enumerate(channels):
            with tabs[i]:
                st.info(f"Processing data for {channel}...")
                
                # --- Logic Placeholder ---
                # This is where you transform columns to match specific channel templates
                processed_df = df.copy() 
                
                if channel == "Amazon":
                    # Example: Rename 'Product_Name' to 'item_name' for Amazon
                    # processed_df = processed_df.rename(columns={'Product_Name': 'item_name'})
                    pass
                
                st.dataframe(processed_df.head())

                # 3. Download Button for each channel
                towrite = BytesIO()
                processed_df.to_csv(towrite, index=False)
                towrite.seek(0)
                
                st.download_button(
                    label=f"Download {channel} CSV",
                    data=towrite,
                    file_name=f"formulaman_{channel.lower()}_list.csv",
                    mime="text/csv"
                )

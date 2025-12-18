import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime
from mapping_logic import preprocess_data, transform_data

st.set_page_config(page_title="Formulaman", layout="wide", page_icon="🧪")

st.title("🧪 Formulaman: Listing & Image Preview")
st.markdown("Automate listings and preview product visuals instantly.")

# 1. File Upload
uploaded_file = st.file_uploader("Upload your Master CSV file", type=["csv"])

if uploaded_file:
    df_raw = pd.read_csv(uploaded_file)
    st.success("File uploaded!")

    # 2. Process Data (Variations)
    df_processed = preprocess_data(df_raw)
    
    # Extract Category for naming (using first available row)
    category_name = "General"
    if 'Product Category*' in df_processed.columns:
        category_name = str(df_processed['Product Category*'].iloc[0]).replace(" ", "_")

    # 3. Image Preview Section
    if 'Main Image*' in df_processed.columns:
        st.subheader("🖼️ Product Image Preview")
        # Get unique images to avoid repeating the same image for every variation row
        unique_images = df_processed['Main Image*'].unique()
        
        cols = st.columns(5) # Display 5 images per row
        for idx, img_url in enumerate(unique_images):
            with cols[idx % 5]:
                try:
                    st.image(img_url, use_container_width=True, caption=f"Product {idx+1}")
                except:
                    st.error(f"Could not load image {idx+1}")

    # 4. Channel Selection & Generation
    st.divider()
    channels = st.multiselect(
        "Select Target Channels:",
        ["Amazon", "Flipkart", "Meesho", "Myntra", "Ajio"],
        default=["Amazon"]
    )

    if st.button("Generate Downloadable Files"):
        tabs = st.tabs(channels)
        current_date = datetime.now().strftime("%Y-%m-%d")

        for i, channel in enumerate(channels):
            with tabs[i]:
                final_df = transform_data(df_processed, channel)
                
                st.write(f"### {channel} Preview")
                st.dataframe(final_df.head(10))

                # Dynamic Filename: "Channel_Category_Date"
                file_name = f"{channel}_{category_name}_{current_date}.csv"

                csv_buffer = BytesIO()
                final_df.to_csv(csv_buffer, index=False)
                csv_buffer.seek(0)
                
                st.download_button(
                    label=f"📥 Download {file_name}",
                    data=csv_buffer,
                    file_name=file_name,
                    mime="text/csv",
                    key=f"dl_{channel}_{idx}"
                )

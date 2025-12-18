import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime
from mapping_logic import preprocess_data, transform_data

st.set_page_config(page_title="Formulaman", layout="wide", page_icon="🧪")

st.title("🧪 Formulaman: Listing Automator")
st.markdown("Upload your sheet to explode variations and verify images row-by-row.")

# 1. File Upload
uploaded_file = st.file_uploader("Upload your Master CSV file", type=["csv"])

if uploaded_file:
    # Load with first row as header
    df_raw = pd.read_csv(uploaded_file)
    
    # 2. Process Data (Variations Explosion)
    df_processed = preprocess_data(df_raw)
    
    # Extract Category for the dynamic filename
    category_name = "General"
    if 'Product Category*' in df_processed.columns:
        category_name = str(df_processed['Product Category*'].iloc[0]).replace(" ", "_")

    # 3. Verification Table with Image Column
    st.subheader("🔍 Verify Items & Variations")
    
    # We display the dataframe and configure the 'Main Image*' column to render as an actual image
    st.dataframe(
        df_processed,
        column_config={
            "Main Image*": st.column_config.ImageColumn(
                "Preview", help="Verification image fetched from URL"
            )
        },
        use_container_width=True,
        hide_index=True
    )

    # 4. Channel Selection & Download
    st.divider()
    channels = st.multiselect(
        "Select Target Channels:",
        ["Amazon", "Flipkart", "Meesho", "Myntra", "Ajio"],
        default=["Amazon", "Flipkart", "Meesho"]
    )

    if st.button("Generate Downloadable Files"):
        tabs = st.tabs(channels)
        current_date = datetime.now().strftime("%d-%m-%Y")

        for i, channel in enumerate(channels):
            with tabs[i]:
                final_df = transform_data(df_processed, channel)
                
                # Naming Logic: "Channel_Category_Date"
                file_name = f"{channel}_{category_name}_{current_date}.csv"

                st.write(f"### {channel} Template Preview")
                st.dataframe(final_df.head(10), use_container_width=True)

                # Export to CSV
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

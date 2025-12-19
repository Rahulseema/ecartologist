import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime
from mapping_logic import preprocess_data, transform_data, generate_dynamic_description

st.set_page_config(page_title="Formulaman", layout="wide")
st.title("🧪 Formulaman: Bulk Listing Engine")

uploaded_file = st.file_uploader("Upload Master CSV", type=["csv"])

if uploaded_file:
    df_raw = pd.read_csv(uploaded_file)
    df_processed = preprocess_data(df_raw)
    
    # Automatically generate description using keywords/categories if empty
    df_processed['Product Description*'] = df_processed.apply(generate_dynamic_description, axis=1)

    st.subheader("🔍 Verification Table")
    st.dataframe(
        df_processed,
        column_config={"Main Image*": st.column_config.ImageColumn("Preview")},
        use_container_width=True
    )

    # Export Section
    channels = st.multiselect("Select Channels:", ["Amazon", "Flipkart", "Meesho"], default=["Amazon"])
    if st.button("Generate Downloadable Files"):
        cat = str(df_processed['Product Category*'].iloc[0]).replace(" ", "_")
        date_str = datetime.now().strftime("%d-%m-%Y")
        
        for channel in channels:
            final_df = transform_data(df_processed, channel)
            file_name = f"{channel}_{cat}_{date_str}.csv"
            
            csv_buffer = BytesIO()
            final_df.to_csv(csv_buffer, index=False)
            csv_buffer.seek(0)
            st.download_button(label=f"📥 Download {file_name}", data=csv_buffer, file_name=file_name, mime="text/csv")

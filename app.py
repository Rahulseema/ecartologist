import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime
from mapping_logic import preprocess_data, transform_data, generate_ai_description, get_available_models

# --- Page Configuration ---
st.set_page_config(
    page_title="Formulaman | AI Listing Engine", 
    layout="wide", 
    page_icon="🧪"
)

# --- Custom Styling for Formula Man Brand ---
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #007bff;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🧪 Formulaman: AI Marketplace Lab")
st.markdown("##### Upload, Explode Variations, Generate AI Content, and Export.")

# --- Sidebar for Settings & Debugging ---
with st.sidebar:
    st.header("Formula Man Control Panel")
    api_key = st.text_input("Gemini API Key", type="password", help="Enter key from aistudio.google.com")
    
    st.divider()
    if st.button("🔍 Check AI Connection"):
        if api_key:
            with st.spinner("Testing models..."):
                models = get_available_models(api_key)
                if any("gemini" in m for m in models):
                    st.success(f"Connected! Available: {len(models)} models")
                    st.write(models[:3]) # Show top 3 models
                else:
                    st.error("No compatible models found for this key.")
        else:
            st.warning("Please enter an API Key first.")
    
    st.divider()
    st.info("Primary Goal: Maximize E-commerce Revenue")

# --- Step 1: File Upload ---
uploaded_file = st.file_uploader("Upload Master CSV File", type=["csv"])

if uploaded_file:
    # Read the file
    df_raw = pd.read_csv(uploaded_file)
    
    # Process Variations (Comma Separated -> Separate Rows)
    df_processed = preprocess_data(df_raw)
    
    st.success(f"Data Loaded: {len(df_raw)} original rows expanded to {len(df_processed)} variations.")

    # --- Step 2: AI Description Generation ---
    st.subheader("✨ AI Content Generation")
    col1, col2 = st.columns([1, 2])
    
    with col1:
        if st.button("🚀 Generate AI Descriptions"):
            if not api_key:
                st.error("Missing API Key in sidebar!")
            else:
                with st.spinner("AI is writing SEO descriptions..."):
                    df_processed['Product Description*'] = df_processed.apply(
                        lambda row: generate_ai_description(
                            row.get('Product Name*', ''),
                            row.get('Brand*', ''),
                            row.get('Fabric Type*', ''),
                            row.get('Variations (comma separated)*', ''),
                            api_key
                        ), axis=1
                    )
                st.success("Descriptions Generated Successfully!")

    # --- Step 3: Verification Table ---
    st.subheader("🔍 Listing Verification Preview")
    
    # Rendering images inside the table for verification
    st.dataframe(
        df_processed,
        column_config={
            "Main Image*": st.column_config.ImageColumn("Image Preview", width="medium"),
            "Product Description*": st.column_config.TextColumn("AI Description", width="large"),
            "Variations (comma separated)*": "Size/Var"
        },
        use_container_width=True,
        hide_index=True
    )

    # --- Step 4: Channel Selection & Export ---
    st.divider()
    st.subheader("📤 Marketplace Export")
    
    selected_channels = st.multiselect(
        "Select Target Marketplaces:",
        ["Amazon", "Flipkart", "Meesho", "Ajio", "Myntra"],
        default=["Amazon", "Flipkart", "Meesho"]
    )

    if st.button("📦 Prepare Final Files"):
        # Get Category Name for Dynamic Filename
        cat_name = "Listing"
        if 'Product Category*' in df_processed.columns:
            cat_name = str(df_processed['Product Category*'].iloc[0]).replace(" ", "_")
        
        date_str = datetime.now().strftime("%d-%m-%Y")
        
        tabs = st.tabs(selected_channels)
        
        for i, channel in enumerate(selected_channels):
            with tabs[i]:
                # Transform data using logic from mapping_logic.py
                final_df = transform_data(df_processed, channel)
                
                # Filename Format: "Channel_Category_Date"
                file_name = f"{channel}_{cat_name}_{date_str}.csv"
                
                st.write(f"**Previewing:** `{file_name}`")
                st.dataframe(final_df.head(5), use_container_width=True)

                # CSV Download Buffer
                csv_buffer = BytesIO()
                final_df.to_csv(csv_buffer, index=False)
                csv_buffer.seek(0)
                
                st.download_button(
                    label=f"📥 Download {file_name}",
                    data=csv_buffer,
                    file_name=file_name,
                    mime="text/csv",
                    key=f"dl_btn_{channel}"
                )

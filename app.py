import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime
from mapping_logic import preprocess_data, transform_data, generate_dynamic_description

# --- Page Config ---
st.set_page_config(page_title="Formulaman", layout="wide", page_icon="🧪")

# --- Custom Pastel UI Theme (Black Text) ---
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-color: #F7FBFF; /* Very light pastel blue */
    }
    
    /* Global Text Color */
    html, body, [class*="st-"] {
        color: #000000 !important;
        font-weight: 500;
    }

    /* Sidebar Background */
    section[data-testid="stSidebar"] {
        background-color: #FFF5F8 !important; /* Pastel pinkish-white */
        border-right: 1px solid #FFE4E1;
    }

    /* Buttons Style */
    .stButton>button {
        background-color: #D1EAFF !important; /* Pastel Blue */
        color: black !important;
        border: none;
        border-radius: 12px;
        padding: 0.6rem 1.2rem;
        transition: all 0.3s ease;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #A5D8FF !important;
        transform: translateY(-2px);
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #E8F9EE; /* Pastel Green */
        border-radius: 8px 8px 0px 0px;
        padding: 10px 20px;
        color: black !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #B2F2BB !important;
        font-weight: bold;
    }

    /* Dataframe Styling */
    [data-testid="stDataFrame"] {
        border: 2px solid #E0E0E0;
        border-radius: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🧪 Formulaman: Premium Listing Hub")
st.markdown("##### *One Master Formula. All Marketplaces.*")

with st.sidebar:
    st.header("Formula Man HQ")
    st.image("https://cdn-icons-png.flaticon.com/512/3022/3022244.png", width=80)
    st.info("Goal: Maximize Revenue via Automation")
    st.divider()
    st.write("Current Version: v3.0 (Pastel Edition)")

# 1. File Upload
uploaded_file = st.file_uploader("📂 Upload Master Template CSV", type=["csv"])

if uploaded_file:
    df_raw = pd.read_csv(uploaded_file)
    df_processed = preprocess_data(df_raw)
    
    # Keyword/Category Based Description Generation
    df_processed['Product Description*'] = df_processed.apply(generate_dynamic_description, axis=1)

    st.success(f"✅ Processed {len(df_processed)} variations successfully!")

    # 2. Verification Table with Image Column
    st.subheader("🔍 Verification Preview")
    st.dataframe(
        df_processed,
        column_config={
            "Main Image*": st.column_config.ImageColumn("Preview", width="medium"),
            "Product Description*": st.column_config.TextColumn("Generated Content", width="large")
        },
        use_container_width=True,
        hide_index=True
    )

    st.divider()
    
    # 3. Channel Selector (Button/Pill Format)
    st.subheader("🎯 Select Target Channels")
    selected_channels = st.pills(
        "Activate marketplaces to generate files:",
        options=["Amazon", "Flipkart", "Meesho"],
        selection_mode="multi",
        default=["Amazon", "Flipkart"]
    )

    if selected_channels:
        st.write(f"Generating for: {', '.join(selected_channels)}")
        
        # 4. Tabbed Download Interface
        st.subheader("📦 Download Listing Files")
        cat_name = str(df_processed['Product Category*'].iloc[0]).replace(" ", "_") if 'Product Category*' in df_processed.columns else "List"
        date_str = datetime.now().strftime("%d-%m-%Y")
        
        tabs = st.tabs(selected_channels)
        for i, channel in enumerate(selected_channels):
            with tabs[i]:
                final_df = transform_data(df_processed, channel)
                file_name = f"{channel}_{cat_name}_{date_str}.csv"
                
                st.write(f"Previewing format for **{channel}**")
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
    else:
        st.warning("Please select at least one channel above to continue.")

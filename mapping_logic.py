import pandas as pd
import google.generativeai as genai

def preprocess_data(df):
    """
    1. Fixes header issues.
    2. Explodes comma-separated variations into individual rows.
    """
    var_col = 'Variations (comma separated)*'
    
    # Ensure the column exists before processing
    if var_col in df.columns:
        # Convert to string and split by comma
        df[var_col] = df[var_col].astype(str).str.split(',')
        # Create a new row for every item in the list
        df = df.explode(var_col)
        # Strip whitespace from the newly created variation strings
        df[var_col] = df[var_col].str.strip()
    
    return df

def get_available_models(api_key):
    """
    Debug helper to verify API Key and check which Gemini models 
    are active for your account.
    """
    try:
        genai.configure(api_key=api_key, transport='rest')
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        return models
    except Exception as e:
        return [f"Connection Error: {str(e)}"]

def generate_ai_description(product_name, brand, material, variation, api_key):
    """
    Generates high-conversion e-commerce descriptions using Gemini 1.5 Flash.
    Uses 'rest' transport to bypass 404/gRPC errors.
    """
    if not api_key or not product_name:
        return "Missing data for AI generation."
    
    try:
        # The 'rest' transport is the critical fix for Streamlit Cloud connectivity
        genai.configure(api_key=api_key, transport='rest')
        
        # We use gemini-1.5-flash for speed and lower latency
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        Act as a professional e-commerce copywriter for the brand '{brand}'.
        Write an SEO-optimized product description for: {product_name}.
        Specific details: Material is {material}, Size/Variation is {variation}.
        
        Requirements:
        1. Catchy opening line.
        2. 3 Benefit-driven bullet points.
        3. Professional and persuasive tone.
        Max 80 words.
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"AI Error: {str(e)}"

def transform_data(df, channel):
    """
    Maps the 'Formulaman' master data to specific marketplace templates.
    """
    processed_df = pd.DataFrame()
    
    # Extracting common variables from your uploaded template
    name = df.get('Product Name*', '')
    variation = df.get('Variations (comma separated)*', '')
    sku = df.get('SKU Code*', '')
    mrp = df.get('MRP*', 0)
    price = df.get('Selling Price*', 0)
    img = df.get('Main Image*', '')
    desc = df.get('Product Description*', 'Standard Description')

    if channel == "Amazon":
        processed_df['item_name'] = name + " (" + variation + ")"
        processed_df['external_product_id'] = sku
        processed_df['external_product_id_type'] = 'UPC'
        processed_df['standard_price'] = price
        processed_df['main_image_url'] = img
        processed_df['product_description'] = desc

    elif channel == "Flipkart":
        processed_df['Seller SKU ID'] = sku
        processed_df['Size'] = variation
        processed_df['MRP'] = mrp
        processed_df['Selling Price'] = price
        processed_df['Main Image'] = img
        processed_df['Description'] = desc

    elif channel == "Meesho":
        processed_df['Product Name'] = name
        processed_df['Size'] = variation
        processed_df['Price'] = price
        processed_df['SKU'] = sku
        processed_df['Description'] = desc
        processed_df['Main Image'] = img

    elif channel == "Ajio" or channel == "Myntra":
        # Placeholder for Ajio/Myntra logic
        processed_df['Style ID'] = sku
        processed_df['Size'] = variation
        processed_df['Description'] = desc
        processed_df['MRP'] = mrp

    else:
        # Default fallback
        processed_df = df.copy()

    return processed_df

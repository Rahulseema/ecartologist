import pandas as pd
import google.generativeai as genai
from google.generativeai.types import RequestOptions

def preprocess_data(df):
    """Explodes comma-separated variations into multiple rows."""
    var_col = 'Variations (comma separated)*'
    if var_col in df.columns:
        df[var_col] = df[var_col].astype(str).str.split(',')
        df = df.explode(var_col)
        df[var_col] = df[var_col].str.strip()
    return df

def get_available_models(api_key):
    """Debug helper to check model access."""
    try:
        genai.configure(api_key=api_key, transport='rest')
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        return models
    except Exception as e:
        return [f"Error: {str(e)}"]

def generate_ai_description(product_name, brand, material, variation, api_key):
    """FORCED V1 API CALL: Bypasses the 404 v1beta error."""
    if not api_key or not product_name:
        return "Missing data"
    
    try:
        genai.configure(api_key=api_key, transport='rest')
        
        # Explicitly defining the stable v1 version in request_options
        model = genai.GenerativeModel(model_name='gemini-1.5-flash')
        
        prompt = f"""
        Write a professional e-commerce product description for:
        Product: {product_name}
        Brand: {brand}
        Material: {material}
        Variation/Size: {variation}
        
        Include 3 short bullet points. Max 80 words.
        """
        
        # This is the secret fix for the 404 error
        response = model.generate_content(
            prompt, 
            request_options=RequestOptions(api_version='v1')
        )
        return response.text
    except Exception as e:
        return f"AI Error: {str(e)}"

def transform_data(df, channel):
    """Maps internal data to marketplace columns."""
    processed_df = pd.DataFrame()
    
    # Common variables
    name = df.get('Product Name*', '')
    variation = df.get('Variations (comma separated)*', '')
    sku = df.get('SKU Code*', '')
    price = df.get('Selling Price*', 0)
    img = df.get('Main Image*', '')
    desc = df.get('Product Description*', '')

    if channel == "Amazon":
        processed_df['item_name'] = f"{name} ({variation})"
        processed_df['external_product_id'] = sku
        processed_df['standard_price'] = price
        processed_df['main_image_url'] = img
        processed_df['description'] = desc
    elif channel == "Flipkart":
        processed_df['Seller SKU ID'] = sku
        processed_df['Size'] = variation
        processed_df['Selling Price'] = price
        processed_df['Description'] = desc
    elif channel == "Meesho":
        processed_df['Product Name'] = name
        processed_df['Size'] = variation
        processed_df['Price'] = price
        processed_df['Description'] = desc
    else:
        processed_df = df.copy()
        
    return processed_df

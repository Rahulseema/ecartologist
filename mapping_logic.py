import pandas as pd
import google.generativeai as genai

def preprocess_data(df):
    """Explodes variations into separate rows."""
    var_col = 'Variations (comma separated)*'
    if var_col in df.columns:
        df[var_col] = df[var_col].astype(str).str.split(',')
        df = df.explode(var_col)
        df[var_col] = df[var_col].str.strip()
    return df

def get_available_models(api_key):
    """Debug function to see what your key can access."""
    try:
        genai.configure(api_key=api_key, transport='rest')
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        return models
    except Exception as e:
        return [f"Error listing models: {str(e)}"]

def generate_ai_description(product_name, brand, material, variation, api_key):
    """Calls Google Gemini AI using REST transport for stability."""
    if not api_key or not product_name:
        return "Missing data"
    
    try:
        # transport='rest' is the FIX for Streamlit 404/Connection issues
        genai.configure(api_key=api_key, transport='rest')
        
        # Try the most stable path
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        Write a professional e-commerce product description for:
        Product: {product_name}
        Brand: {brand}
        Material: {material}
        Variation/Size: {variation}
        
        Include 3 bullet points. Max 80 words.
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"AI Error: {str(e)}"

def transform_data(df, channel):
    """Maps columns to marketplace templates."""
    processed_df = pd.DataFrame()
    
    desc = df.get('Product Description*', '')
    name = df.get('Product Name*', '')
    var = df.get('Variations (comma separated)*', '')
    sku = df.get('SKU Code*', '')
    price = df.get('Selling Price*', 0)
    img = df.get('Main Image*', '')

    if channel == "Amazon":
        processed_df['item_name'] = f"{name} {var}"
        processed_df['sku'] = sku
        processed_df['price'] = price
        processed_df['description'] = desc
    elif channel == "Flipkart":
        processed_df['Seller SKU ID'] = sku
        processed_df['Description'] = desc
    elif channel == "Meesho":
        processed_df['Product Name'] = name
        processed_df['Description'] = desc
    return processed_df

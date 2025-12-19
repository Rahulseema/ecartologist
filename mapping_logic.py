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

def generate_ai_description(product_name, brand, material, variation, api_key):
    """Calls Google Gemini AI with a fallback mechanism."""
    if not api_key or not product_name:
        return "Missing data"
    
    genai.configure(api_key=api_key)
    
    # List of models to try in order of preference
    model_options = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-1.0-pro']
    
    last_error = ""
    for model_name in model_options:
        try:
            model = genai.GenerativeModel(model_name)
            prompt = f"Write a professional e-commerce description for a {brand} {product_name} made of {material} (Size: {variation}). Use 3 bullet points. Max 100 words."
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            last_error = str(e)
            continue # Try the next model
            
    return f"AI Error after trying all models: {last_error}"

def transform_data(df, channel):
    """Maps columns to marketplace templates."""
    processed_df = pd.DataFrame()
    if channel == "Amazon":
        processed_df['item_name'] = df.get('Product Name*', '') + " " + df.get('Variations (comma separated)*', '')
        processed_df['sku'] = df.get('SKU Code*', '')
        processed_df['description'] = df.get('Product Description*', '')
    elif channel == "Flipkart":
        processed_df['Seller SKU ID'] = df.get('SKU Code*', '')
        processed_df['Description'] = df.get('Product Description*', '')
    elif channel == "Meesho":
        processed_df['Product Name'] = df.get('Product Name*', '')
        processed_df['Description'] = df.get('Product Description*', '')
    else:
        processed_df = df.copy()
    return processed_df

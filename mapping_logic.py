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
    """Calls Google Gemini AI using the most stable model path."""
    if not api_key or not product_name:
        return "Missing data"
    
    try:
        genai.configure(api_key=api_key)
        
        # Use the explicit model name that is currently standard
        # If 'gemini-1.5-flash' fails, we use the model's full resource name
        model = genai.GenerativeModel(model_name='models/gemini-1.5-flash')
        
        prompt = f"""
        Write a professional e-commerce product description for:
        Product: {product_name}
        Brand: {brand}
        Material: {material}
        Variation/Size: {variation}
        
        Format: 
        - One catchy intro sentence.
        - 3 short bullet points of key benefits.
        Max 80 words.
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"AI Error: {str(e)}"

def transform_data(df, channel):
    """Maps columns to marketplace templates for Formulaman."""
    processed_df = pd.DataFrame()
    
    # Common fields for all channels
    desc = df.get('Product Description*', 'No description generated')
    name = df.get('Product Name*', '')
    var = df.get('Variations (comma separated)*', '')
    sku = df.get('SKU Code*', '')
    price = df.get('Selling Price*', 0)
    img = df.get('Main Image*', '')

    if channel == "Amazon":
        processed_df['item_name'] = f"{name} ({var})"
        processed_df['external_product_id'] = sku
        processed_df['standard_price'] = price
        processed_df['main_image_url'] = img
        processed_df['description'] = desc

    elif channel == "Flipkart":
        processed_df['Seller SKU ID'] = sku
        processed_df['Size'] = var
        processed_df['Selling Price'] = price
        processed_df['Description'] = desc

    elif channel == "Meesho":
        processed_df['Product Name'] = name
        processed_df['Size'] = var
        processed_df['Price'] = price
        processed_df['Description'] = desc
        
    else:
        processed_df = df.copy()

    return processed_df

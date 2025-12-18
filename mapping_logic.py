import pandas as pd
import google.generativeai as genai

def preprocess_data(df):
    """
    Expands comma-separated variations into multiple rows.
    """
    var_col = 'Variations (comma separated)*'
    if var_col in df.columns:
        df[var_col] = df[var_col].astype(str).str.split(',')
        df = df.explode(var_col)
        df[var_col] = df[var_col].str.strip()
    return df

def generate_ai_description(product_name, brand, material, variation, api_key):
    """
    Calls Google Gemini AI to write a description.
    """
    if not api_key or not product_name:
        return "Missing info for AI"
    
    try:
        genai.configure(api_key=api_key)
        # UPDATED MODEL NAME HERE
        model = genai.GenerativeModel('gemini-1.5-flash') 
        
        prompt = f"""
        Write a professional e-commerce product description for:
        Product: {product_name}
        Brand: {brand}
        Material: {material}
        Variation/Size: {variation}
        
        Include 3 bullet points. Max 100 words.
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"AI Error: {str(e)}"

def transform_data(df, channel):
    """
    Maps the internal data to the specific marketplace format.
    """
    processed_df = pd.DataFrame()

    if channel == "Amazon":
        processed_df['item_name'] = df.get('Product Name*', '') + " " + df.get('Variations (comma separated)*', '')
        processed_df['external_product_id'] = df.get('SKU Code*', '')
        processed_df['standard_price'] = df.get('Selling Price*', 0)
        processed_df['main_image_url'] = df.get('Main Image*', '')
        processed_df['description'] = df.get('Product Description*', '')

    elif channel == "Flipkart":
        processed_df['Seller SKU ID'] = df.get('SKU Code*', '')
        processed_df['Size'] = df.get('Variations (comma separated)*', '')
        processed_df['Selling Price'] = df.get('Selling Price*', 0)
        processed_df['Description'] = df.get('Product Description*', '')

    elif channel == "Meesho":
        processed_df['Product Name'] = df.get('Product Name*', '')
        processed_df['Size'] = df.get('Variations (comma separated)*', '')
        processed_df['Price'] = df.get('Selling Price*', 0)
        processed_df['Description'] = df.get('Product Description*', '')
        
    else:
        processed_df = df.copy()

    return processed_df

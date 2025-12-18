import pandas as pd
import google.generativeai as genai

def generate_ai_description(product_name, brand, material, variation, api_key):
    if not api_key:
        return "API Key missing"
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
    
    prompt = f"""
    Write a professional, SEO-friendly e-commerce product description for:
    Product: {product_name}
    Brand: {brand}
    Material: {material}
    Size/Variation: {variation}
    
    Tone: Persuasive and professional. Include 3 bullet points of key benefits.
    Keep it under 150 words.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

def preprocess_data(df):
    # (Keep your existing variation explosion logic here)
    var_col = 'Variations (comma separated)*'
    if var_col in df.columns:
        df[var_col] = df[var_col].astype(str).str.split(',')
        df = df.explode(var_col)
        df[var_col] = df[var_col].str.strip()
    return df

# ... (Keep your transform_data function here)

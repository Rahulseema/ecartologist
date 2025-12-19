import pandas as pd

def preprocess_data(df):
    """Explodes variations into separate rows."""
    var_col = 'Variations (comma separated)*'
    if var_col in df.columns:
        df[var_col] = df[var_col].astype(str).str.split(',')
        df = df.explode(var_col)
        df[var_col] = df[var_col].str.strip()
    return df

def generate_template_description(row):
    """
    Alternative to AI: Creates a professional description using product data.
    Fast, reliable, and SEO-friendly.
    """
    name = row.get('Product Name*', 'Product')
    brand = row.get('Brand*', 'Generic')
    material = row.get('Fabric Type*', 'High Quality Material')
    variation = row.get('Variations (comma separated)*', '')
    cat = row.get('Product Category*', 'Item')
    
    description = (
        f"Buy this premium {brand} {name} today. "
        f"This {cat} is crafted from {material} for maximum durability and style. "
        f"Available in size/variation: {variation}. "
        f"Perfect for daily use and gifting."
    )
    return description

def transform_data(df, channel):
    """Maps internal data to marketplace columns for Formulaman."""
    processed_df = pd.DataFrame()
    
    # Common variables
    name = df.get('Product Name*', '')
    variation = df.get('Variations (comma separated)*', '')
    sku = df.get('SKU Code*', '')
    price = df.get('Selling Price*', 0)
    mrp = df.get('MRP*', 0)
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
        processed_df['MRP'] = mrp
        processed_df['Description'] = desc

    elif channel == "Meesho":
        processed_df['Product Name'] = name
        processed_df['Size'] = variation
        processed_df['Price'] = price
        processed_df['SKU'] = sku
        processed_df['Description'] = desc
        processed_df['Main Image'] = img
        
    else:
        processed_df = df.copy()

    return processed_df

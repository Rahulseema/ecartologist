import pandas as pd

def preprocess_data(df):
    """Explodes variations from your CSV into separate rows."""
    var_col = 'Variations (comma separated)*'
    if var_col in df.columns:
        df[var_col] = df[var_col].astype(str).str.split(',')
        df = df.explode(var_col)
        df[var_col] = df[var_col].str.strip()
    return df

def generate_dynamic_description(row):
    """
    Creates high-conversion descriptions using Category and Product data.
    """
    name = row.get('Product Name*', 'Premium Product')
    brand = row.get('Brand*', 'Our Brand')
    material = row.get('Fabric Type*', 'High-Quality Material')
    variation = row.get('Variations (comma separated)*', '')
    category = row.get('Product Category*', 'Essentials')
    
    # Dynamic SEO Template
    description = (
        f"Enhance your lifestyle with the {brand} {name}. "
        f"This premium {category} is expertly crafted from {material} "
        f"to ensure long-lasting durability and peak performance. "
        f"Perfect for daily use, this {variation} variation is a must-have for those "
        f"who value quality and style in their {category} collection."
    )
    return description

def transform_data(df, channel):
    """Maps the final data to marketplace templates."""
    processed_df = pd.DataFrame()
    
    # Common mapped fields
    desc = df.get('Product Description*', '')
    name = df.get('Product Name*', '')
    var = df.get('Variations (comma separated)*', '')
    sku = df.get('SKU Code*', '')
    price = df.get('Selling Price*', 0)
    img = df.get('Main Image*', '')

    if channel == "Amazon":
        processed_df['item_name'] = f"{name} - {var}"
        processed_df['sku'] = sku
        processed_df['main_image_url'] = img
        processed_df['description'] = desc
    elif channel == "Flipkart":
        processed_df['Seller SKU ID'] = sku
        processed_df['Size'] = var
        processed_df['Description'] = desc
    elif channel == "Meesho":
        processed_df['Product Name'] = name
        processed_df['Description'] = desc
        processed_df['Main Image'] = img
    return processed_df

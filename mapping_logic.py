import pandas as pd

def preprocess_data(df):
    """Explodes variations from the 'Variations (comma separated)*' column."""
    var_col = 'Variations (comma separated)*'
    if var_col in df.columns:
        df[var_col] = df[var_col].astype(str).str.split(',')
        df = df.explode(var_col)
        df[var_col] = df[var_col].str.strip()
    return df

def generate_dynamic_description(row):
    """Creates descriptions using Category and Keyword logic."""
    name = row.get('Product Name*', 'Product')
    brand = row.get('Brand*', 'Premium')
    cat = row.get('Product Category*', 'Essentials')
    fabric = row.get('Fabric Type*', 'High-quality material')
    variation = row.get('Variations (comma separated)*', '')
    
    return (f"Elevate your style with the {brand} {name}. "
            f"This {cat} is made from premium {fabric}, ensuring comfort and durability. "
            f"Available in the {variation} variant, it's a perfect addition to your collection.")

def transform_data(df, channel):
    """Maps Master Template to specific marketplace headers based on uploaded sheets."""
    processed_df = pd.DataFrame()
    
    # Common variables from Master Template
    name = df.get('Product Name*', '')
    sku = df.get('SKU Code*', '')
    price = df.get('Selling Price*', 0)
    mrp = df.get('MRP*', 0)
    img = df.get('Main Image*', '')
    desc = df.get('Product Description*', '')
    var = df.get('Variations (comma separated)*', '')
    weight = df.get('Weight*', 0)

    if channel == "Amazon":
        processed_df['SKU'] = sku
        processed_df['Item Name'] = f"{name} ({var})"
        processed_df['Your Price INR (Sell on Amazon, IN)'] = price
        processed_df['Maximum Retail Price (Sell on Amazon, IN)'] = mrp
        processed_df['Quantity (IN)'] = df.get('Inventory*', 0)
        processed_df['Main Image URL'] = img
        processed_df['Product Description'] = desc
        processed_df['Item Weight'] = weight

    elif channel == "Flipkart":
        processed_df['Seller SKU ID'] = sku
        processed_df['Product Title'] = name
        processed_df['MRP (INR)'] = mrp
        processed_df['Your selling price (INR)'] = price
        processed_df['Stock'] = df.get('Inventory*', 0)
        processed_df['Size'] = var
        processed_df['Main Image URL'] = img
        processed_df['Description'] = desc
        processed_df['Weight (KG)'] = weight

    elif channel == "Meesho":
        # Meesho follows the original master template structure closely
        processed_df = df.copy()

    return processed_df

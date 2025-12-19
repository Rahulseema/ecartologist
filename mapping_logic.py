import pandas as pd

def preprocess_data(df):
    """Explodes variations while preserving context rows."""
    # Ensure we don't treat the context row (Row 2) as product data
    if len(df) > 0:
        # If the first row of data contains 'Text' or 'Single', it's likely context
        if 'Text' in str(df.iloc[0].values):
            df = df.iloc[1:].reset_index(drop=True)

    var_col = 'Variations (comma separated)*'
    if var_col in df.columns:
        df[var_col] = df[var_col].astype(str).str.split(',')
        df = df.explode(var_col)
        df[var_col] = df[var_col].str.strip()
    return df

def generate_dynamic_description(row):
    """Generates SEO descriptions using Category/Keywords."""
    name = row.get('Product Name*', 'Product')
    cat = row.get('Product Category*', 'Item')
    brand = row.get('Brand*', 'Premium')
    fabric = row.get('Fabric Type*', 'high-quality fabric')
    return f"Professional {brand} {name} from our {cat} range. Crafted with {fabric} for durability."

def transform_data(df, channel):
    """Deep Mapping for 20+ columns per marketplace."""
    p = pd.DataFrame()
    
    # Core Data Extraction
    name = df.get('Product Name*', '')
    var = df.get('Variations (comma separated)*', '')
    sku = df.get('SKU Code*', '')
    price = df.get('Selling Price*', 0)
    mrp = df.get('MRP*', 0)
    img = df.get('Main Image*', '')
    desc = df.get('Product Description*', '')

    if channel == "Amazon":
        p['SKU'] = sku
        p['Item Name'] = f"{name} ({var})"
        p['Product Type'] = df.get('Product Category*', 'SHIRT')
        p['Brand Name'] = df.get('Brand*', '')
        p['Your Price INR (Sell on Amazon, IN)'] = price
        p['Maximum Retail Price (Sell on Amazon, IN)'] = mrp
        p['Quantity (IN)'] = df.get('Inventory*', 0)
        p['Main Image URL'] = img
        p['Product Description'] = desc
        p['Bullet Point'] = df.get('Bullet 1', '')
        p['Fabric Type'] = df.get('Fabric Type*', '')
        p['HSN'] = df.get('HSN*', '')

    elif channel == "Flipkart":
        p['Seller SKU ID'] = sku
        p['Product Title'] = name
        p['MRP (INR)'] = mrp
        p['Your selling price (INR)'] = price
        p['Stock'] = df.get('Inventory*', 0)
        p['Size'] = var
        p['Main Image URL'] = img
        p['Description'] = desc
        p['HSN'] = df.get('HSN*', '')
        p['Weight (KG)'] = df.get('Weight*', 0)
        p['Brand Fabric'] = df.get('Fabric Type*', '')
        p['Key Features'] = df.get('Bullet 1', '')

    elif channel == "Meesho":
        p = df.copy() # Meesho usually follows your master sample closely

    return p

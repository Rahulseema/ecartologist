import pandas as pd

def preprocess_data(df):
    """Explodes variations while cleaning context rows."""
    # Clean if context row exists
    if len(df) > 0 and 'Text' in str(df.iloc[0].values):
        df = df.iloc[1:].reset_index(drop=True)

    var_col = 'Variations (comma separated)*'
    if var_col in df.columns:
        df[var_col] = df[var_col].astype(str).str.split(',')
        df = df.explode(var_col)
        df[var_col] = df[var_col].str.strip()
    return df

def generate_dynamic_description(row):
    """Generates SEO descriptions using Keywords."""
    name = row.get('Product Name*', 'Product')
    brand = row.get('Brand*', 'Premium')
    cat = row.get('Product Category*', 'Item')
    material = row.get('Material*', 'high-quality fabric')
    return f"Professional {brand} {name} from our {cat} range. Crafted with {material} for durability and style."

def transform_data(df, channel):
    """Maps Master Template Pro to Deep Marketplace Headers."""
    p = pd.DataFrame()
    
    # Common variables
    sku = df.get('SKU Code*', '')
    name = df.get('Product Name*', '')
    var = df.get('Variations (comma separated)*', '')
    price = df.get('Selling Price*', 0)
    mrp = df.get('MRP*', 0)
    brand = df.get('Brand*', '')
    hsn = df.get('HSN*', '')
    weight = df.get('Weight_KG*', 0)
    mat = df.get('Material*', '')
    img = df.get('Main Image*', '')
    desc = df.get('Product Description*', '')

    if channel == "Amazon":
        p['SKU'] = sku
        p['Item Name'] = f"{name} ({var})"
        p['Product Type'] = df.get('Product Category*', 'SHIRT')
        p['Brand Name'] = brand
        p['Your Price INR (Sell on Amazon, IN)'] = price
        p['Maximum Retail Price (Sell on Amazon, IN)'] = mrp
        p['Quantity (IN)'] = df.get('Inventory*', 0)
        p['Item Weight'] = weight
        p['Item Weight Unit'] = 'kg'
        p['HSN'] = hsn
        p['Fabric Type'] = mat
        p['Main Image URL'] = img
        p['Product Description'] = desc
        # Dimensions
        p['Item Length'] = df.get('Length_CM*', 0)
        p['Item Width'] = df.get('Breadth_CM*', 0)
        p['Item Height'] = df.get('Height_CM*', 0)

    elif channel == "Flipkart":
        p['Seller SKU ID'] = sku
        p['Product Title'] = name
        p['MRP (INR)'] = mrp
        p['Your selling price (INR)'] = price
        p['Stock'] = df.get('Inventory*', 0)
        p['Size'] = var
        p['Brand'] = brand
        p['HSN'] = hsn
        p['Weight (KG)'] = weight
        p['Brand Fabric'] = mat
        p['Main Image URL'] = img
        p['Description'] = desc
        # Dimensions
        p['Length (CM)'] = df.get('Length_CM*', 0)
        p['Breadth (CM)'] = df.get('Breadth_CM*', 0)
        p['Height (CM)'] = df.get('Height_CM*', 0)

    elif channel == "Meesho":
        p = df.copy() # Meesho usually follows the sample structure

    return p

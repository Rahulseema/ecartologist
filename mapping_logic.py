import pandas as pd

def preprocess_data(df, selected_category):
    """Explodes variations and standardizes data based on the business vertical."""
    df['Product Category*'] = selected_category
    
    # Strip instruction/context rows if they exist in the master template
    if len(df) > 0 and any(x in str(df.iloc[0].values) for x in ['Text', 'Single', 'Example']):
        df = df.iloc[1:].reset_index(drop=True)

    # Vin Lister style variation explosion
    var_col = 'Variations (comma separated)*'
    if var_col in df.columns:
        df[var_col] = df[var_col].astype(str).str.split(',')
        df = df.explode(var_col)
        df[var_col] = df[var_col].str.strip()
    return df

def generate_fashion_description(row):
    """Dynamic SEO content generation tailored to the fashion vertical."""
    name = row.get('Product Name*', 'Product')
    brand = row.get('Brand*', 'Formula Man')
    cat = row.get('Product Category*', 'Apparel')
    material = row.get('Material*', 'premium fabric')
    
    templates = {
        "Dress": f"Stunning {brand} {name}. Designed with {material} for an elegant look.",
        "Top & Tunic": f"Chic {brand} {name} Top. Made from breathable {material} for daily style.",
        "Kurti/Kurta": f"Traditional {brand} {name}. Classic {material} ethnic wear for comfort.",
        "Tshirts": f"Essential {brand} {name} Tee. Soft {material} for a perfect everyday fit."
    }
    return templates.get(cat, f"Premium {brand} {cat} crafted for excellence.")

def transform_data(df, channel, category):
    """Maps Master Pro fields to deep marketplace headers (Amazon 344, Flipkart 70)."""
    p = pd.DataFrame()
    
    sku = df.get('SKU Code*', '')
    name = df.get('Product Name*', '')
    var = df.get('Variations (comma separated)*', '')
    price = df.get('Selling Price*', 0)
    mrp = df.get('MRP*', 0)
    img = df.get('Main Image*', '')
    hsn = df.get('HSN*', '')

    if channel == "Amazon":
        p['SKU'] = sku
        p['Item Name'] = f"{name} ({var})"
        p['Product Type'] = category.upper().replace(" ", "_")
        p['Your Price INR (Sell on Amazon, IN)'] = price
        p['Maximum Retail Price (Sell on Amazon, IN)'] = mrp
        p['Main Image URL'] = img
        p['HSN'] = hsn
        p['Product Description'] = df.get('Product Description*', '')

    elif channel == "Flipkart":
        p['Seller SKU ID'] = sku
        p['Product Title'] = name
        p['MRP (INR)'] = mrp
        p['Your selling price (INR)'] = price
        p['Size'] = var
        p['Main Image URL'] = img
        p['Description'] = df.get('Product Description*', '')
        p['HSN'] = hsn

    elif channel == "Meesho":
        # Fashion-specific header logic for Meesho
        if category == "Top & Tunic":
            p['Catalog Name'] = name
            p['Top/Tunic SKU'] = sku
            p['Top/Tunic Size'] = var
        else:
            p['Product Name'] = name
            p['SKU'] = sku
            p['Size'] = var
        p['Price'] = price
        p['Main Image'] = img

    return p

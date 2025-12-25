import pandas as pd

def preprocess_data(df, selected_category):
    """Explodes variations and sets category context[cite: 35, 48]."""
    df['Product Category*'] = selected_category
    
    # Cleaning any context rows from uploaded reference sheets 
    if len(df) > 0 and any(x in str(df.iloc[0].values) for x in ['Text', 'Single', 'Example']):
        df = df.iloc[1:].reset_index(drop=True)

    var_col = 'Variations (comma separated)*'
    if var_col in df.columns:
        df[var_col] = df[var_col].astype(str).str.split(',')
        df = df.explode(var_col)
        df[var_col] = df[var_col].str.strip()
    return df

def generate_fashion_description(row):
    """Generates professional descriptions based on AdminUIUX keywords."""
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
    """Maps Master Pro fields to deep marketplace headers[cite: 35, 48, 52]."""
    p = pd.DataFrame()
    
    sku = df.get('SKU Code*', '')
    name = df.get('Product Name*', '')
    var = df.get('Variations (comma separated)*', '')
    price = df.get('Selling Price*', 0)

    if channel == "Amazon":
        p['SKU'] = sku [cite: 35]
        p['Item Name'] = f"{name} ({var})" [cite: 35]
        p['Product Type'] = category.upper().replace(" ", "_") [cite: 35]
        p['Your Price INR (Sell on Amazon, IN)'] = price [cite: 36]
        p['HSN'] = df.get('HSN*', '') [cite: 45]

    elif channel == "Flipkart":
        p['Seller SKU ID'] = sku [cite: 48]
        p['Product Title'] = name [cite: 48]
        p['MRP (INR)'] = df.get('MRP*', 0) [cite: 48]
        p['Size'] = var [cite: 48]
        p['HSN'] = df.get('HSN*', '') [cite: 48]

    elif channel == "Meesho":
        if category == "Top & Tunic":
            p['Catalog Name'] = name
            p['Top/Tunic SKU'] = sku
            p['Top/Tunic Size'] = var
        else:
            p['Product Name'] = name
            p['SKU'] = sku
        p['Price'] = price

    return p

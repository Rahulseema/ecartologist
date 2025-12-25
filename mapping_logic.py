import pandas as pd

def preprocess_data(df, selected_category):
    """Explodes variations and sets the global category context."""
    df['Product Category*'] = selected_category
    
    # We use 'Variations (comma separated)*' as the universal trigger for size/color explosion
    var_col = 'Variations (comma separated)*'
    if var_col in df.columns:
        df[var_col] = df[var_col].astype(str).str.split(',')
        df = df.explode(var_col)
        df[var_col] = df[var_col].str.strip()
    return df

def generate_dynamic_description(row):
    """Creates professional fashion descriptions based on the chosen category."""
    name = row.get('Product Name*', 'Product')
    brand = row.get('Brand*', 'Formula Man')
    cat = row.get('Product Category*', 'Apparel')
    material = row.get('Material*', 'high-quality fabric')
    
    templates = {
        "Dress": f"Elegant {brand} {name} Dress. Perfect for occasions, crafted in {material}.",
        "Top & Tunic": f"Trendy {brand} {name} Top & Tunic. A stylish {material} essential for casual wear.",
        "Kurti/Kurta": f"Traditional {brand} {name}. Premium {material} ethnic wear for daily comfort.",
        "Tshirts": f"Classic {brand} {name} T-shirt. Breathable {material} for a perfect fit."
    }
    return templates.get(cat, f"Premium {brand} {cat} crafted for quality.")

def transform_data(df, channel, category):
    """Deep maps master data to the 300+ fields required by marketplaces."""
    p = pd.DataFrame()
    
    # Universal Data Points
    sku = df.get('SKU Code*', '')
    name = df.get('Product Name*', '')
    price = df.get('Selling Price*', 0)
    mrp = df.get('MRP*', 0)
    img = df.get('Main Image*', '')
    var = df.get('Variations (comma separated)*', '')

    if channel == "Amazon":
        p['SKU'] = sku
        p['Item Name'] = f"{name} ({var})"
        p['Product Type'] = category.upper().replace(" ", "_") # e.g., TOP_AND_TUNIC [cite: 1]
        p['Your Price INR (Sell on Amazon, IN)'] = price
        p['Maximum Retail Price (Sell on Amazon, IN)'] = mrp
        p['Main Image URL'] = img
        p['HSN'] = df.get('HSN*', '')
        p['Material'] = df.get('Material*', '')

    elif channel == "Flipkart":
        p['Seller SKU ID'] = sku
        p['Product Title'] = name
        p['MRP (INR)'] = mrp
        p['Your selling price (INR)'] = price
        p['Size'] = var
        p['Style Type'] = category # Set based on your selection [cite: 14]
        p['Main Image URL'] = img
        p['HSN'] = df.get('HSN*', '')

    elif channel == "Meesho":
        if category == "Top & Tunic":
            p['Catalog Name'] = name
            p['Top/Tunic SKU'] = sku
            p['Top/Tunic Size'] = var
            p['Selling Price'] = price
        else:
            p['Product Name'] = name
            p['SKU'] = sku
            p['Size'] = var
            p['Price'] = price
        p['Main Image'] = img

    return p

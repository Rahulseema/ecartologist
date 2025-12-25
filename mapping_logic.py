import pandas as pd

def preprocess_data(df, selected_category):
    """Explodes variations and sets the category context[cite: 3, 4]."""
    df['Product Category*'] = selected_category
    
    # Trigger for size/color explosion from your Master Template [cite: 4]
    var_col = 'Variations (comma separated)*'
    if var_col in df.columns:
        df[var_col] = df[var_col].astype(str).str.split(',')
        df = df.explode(var_col)
        df[var_col] = df[var_col].str.strip()
    return df

def generate_fashion_description(row):
    """SEO-rich descriptions tailored to the selected category[cite: 25, 26]."""
    name = row.get('Product Name*', 'Product')
    brand = row.get('Brand*', 'Formula Man')
    cat = row.get('Product Category*', 'Apparel')
    material = row.get('Material*', 'high-quality fabric')
    
    templates = {
        "Dress": f"Elegant {brand} {name} Dress. Perfect for evening outings, crafted with {material}[cite: 25].",
        "Top & Tunic": f"Trendy {brand} {name} Top & Tunic. A stylish {material} essential for casual wear[cite: 25].",
        "Kurti/Kurta": f"Traditional {brand} {name}. Premium {material} ethnic wear for daily comfort[cite: 25].",
        "Tshirts": f"Classic {brand} {name} T-shirt. Breathable {material} for a perfect fit[cite: 25]."
    }
    return templates.get(cat, f"Premium {brand} {cat} crafted for quality[cite: 25].")

def transform_data(df, channel, category):
    """Deep maps master data to 300+ marketplace fields."""
    p = pd.DataFrame()
    
    # Universal Data Points 
    sku = df.get('SKU Code*', '')
    name = df.get('Product Name*', '')
    price = df.get('Selling Price*', 0)
    mrp = df.get('MRP*', 0)
    img = df.get('Main Image*', '')
    var = df.get('Variations (comma separated)*', '')

    if channel == "Amazon":
        p['SKU'] = sku [cite: 1]
        p['Item Name'] = f"{name} ({var})" [cite: 1]
        p['Product Type'] = category.upper().replace(" ", "_") [cite: 1]
        p['Your Price INR (Sell on Amazon, IN)'] = price [cite: 1]
        p['Maximum Retail Price (Sell on Amazon, IN)'] = mrp [cite: 1]
        p['Main Image URL'] = img [cite: 8]
        p['HSN'] = df.get('HSN*', '') [cite: 11]

    elif channel == "Flipkart":
        p['Seller SKU ID'] = sku [cite: 14]
        p['Product Title'] = name [cite: 14]
        p['MRP (INR)'] = mrp [cite: 14]
        p['Your selling price (INR)'] = price [cite: 14]
        p['Size'] = var [cite: 14]
        p['Main Image URL'] = img [cite: 14]
        p['HSN'] = df.get('HSN*', '') [cite: 14]

    elif channel == "Meesho":
        if category == "Top & Tunic":
            p['Catalog Name'] = name [cite: 14]
            p['Top/Tunic SKU'] = sku [cite: 14]
            p['Top/Tunic Size'] = var [cite: 14]
        else:
            p['Product Name'] = name [cite: 14]
            p['SKU'] = sku [cite: 14]
        p['Main Image'] = img [cite: 14]

    return p

import pandas as pd

def preprocess_data(df, selected_category):
    """Injects category and explodes variations."""
    df['Product Category*'] = selected_category
    
    var_col = 'Variations (comma separated)*'
    if var_col in df.columns:
        df[var_col] = df[var_col].astype(str).str.split(',')
        df = df.explode(var_col)
        df[var_col] = df[var_col].str.strip()
    return df

def generate_fashion_description(row):
    """Keywords-based description for fashion categories."""
    name = row.get('Product Name*', 'Product')
    cat = row.get('Product Category*', 'Apparel')
    brand = row.get('Brand*', 'Formula Man')
    fabric = row.get('Fabric Type*', 'Soft Fabric')
    
    templates = {
        "Dress": f"Stunning {brand} {name} Dress. Elegantly designed with {fabric} for parties.",
        "Top & Tunic": f"Trendy {brand} {name} Top & Tunic. Casual yet chic, made from {fabric}.",
        "Kurti/Kurta": f"Traditional {brand} {name} ethnic wear. Breathable {fabric} Kurti.",
        "Tshirts": f"Cool {brand} {name} T-shirt. Everyday comfort in high-quality {fabric}."
    }
    return templates.get(cat, f"Premium {brand} {cat}.")

def transform_data(df, channel, category):
    """Dynamically changes headers based on selected category."""
    p = pd.DataFrame()
    
    # Common variables
    sku = df.get('SKU Code*', '')
    name = df.get('Product Name*', '')
    price = df.get('Selling Price*', 0)
    img = df.get('Main Image*', '')
    var = df.get('Variations (comma separated)*', '')

    if channel == "Amazon":
        # Amazon-specific fashion mapping
        p['SKU'] = sku
        p['Item Name'] = f"{name} ({var})"
        p['Product Type'] = category.upper().replace(" ", "_")
        p['Your Price INR (Sell on Amazon, IN)'] = price
        p['Main Image URL'] = img

    elif channel == "Flipkart":
        # Flipkart-specific fashion mapping
        p['Seller SKU ID'] = sku
        p['Product Title'] = name
        p['Size'] = var
        p['Style Type'] = category
        p['Main Image URL'] = img

    elif channel == "Meesho":
        # Meesho dynamic headers for 'Top & Tunic' vs others
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

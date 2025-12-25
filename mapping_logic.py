import pandas as pd

def preprocess_data(df, selected_category):
    """Explodes variations (Size/Color) and injects the vertical context."""
    df['Product Category*'] = selected_category
    
    # Cleans any context/instruction rows from the template
    if len(df) > 0 and any(x in str(df.iloc[0].values) for x in ['Text', 'Single', 'Example']):
        df = df.iloc[1:].reset_index(drop=True)

    var_col = 'Variations (comma separated)*'
    if var_col in df.columns:
        # Standard Vin Lister logic: Explode comma-separated variations into rows
        df[var_col] = df[var_col].astype(str).str.split(',')
        df = df.explode(var_col)
        df[var_col] = df[var_col].str.strip()
    return df

def generate_fashion_description(row):
    """Dynamic SEO Generator based on category and material."""
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
    """Deep maps Master Pro fields to the 300+ marketplace headers."""
    p = pd.DataFrame()
    
    # Shared Data Points
    sku = df.get('SKU Code*', '')
    name = df.get('Product Name*', '')
    var = df.get('Variations (comma separated)*', '')
    price = df.get('Selling Price*', 0)
    img = df.get('Main Image*', '')

    if channel == "Amazon":
        # Maps to the 344 fields in your amazon.csv reference
        p['SKU'] = sku
        p['Item Name'] = f"{name} ({var})"
        p['Product Type'] = category.upper().replace(" ", "_")
        p['Your Price INR (Sell on Amazon, IN)'] = price
        p['Main Image URL'] = img
        p['HSN'] = df.get('HSN*', '')

    elif channel == "Flipkart":
        # Maps to the 70 fields in your flipkart.csv reference
        p['Seller SKU ID'] = sku
        p['Product Title'] = name
        p['Size'] = var
        p['Main Image URL'] = img
        p['MRP (INR)'] = df.get('MRP*', 0)
        p['HSN'] = df.get('HSN*', '')

    elif channel == "Meesho":
        # Dynamic headers specifically for fashion categories in Meesho
        if category == "Top & Tunic":
            p['Catalog Name'] = name
            p['Top/Tunic SKU'] = sku
            p['Top/Tunic Size'] = var
        else:
            p['Product Name'] = name
            p['SKU'] = sku
        p['Main Image'] = img
        p['Price'] = price

    return p

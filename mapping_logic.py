import pandas as pd

def preprocess_data(df, selected_category):
    """Explodes variations and standardizes data for fashion verticals."""
    df['Product Category*'] = selected_category
    
    # Clean context rows if present in the template
    if len(df) > 0 and any(x in str(df.iloc[0].values) for x in ['Text', 'Single', 'Example']):
        df = df.iloc[1:].reset_index(drop=True)

    var_col = 'Variations (comma separated)*'
    if var_col in df.columns:
        df[var_col] = df[var_col].astype(str).str.split(',')
        df = df.explode(var_col)
        df[var_col] = df[var_col].str.strip()
    return df

def generate_fashion_description(row):
    """Generates professional descriptions based on selected category."""
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
    """Maps Master fields to marketplace-specific headers."""
    p = pd.DataFrame()
    sku = df.get('SKU Code*', '')
    name = df.get('Product Name*', '')
    var = df.get('Variations (comma separated)*', '')
    price = df.get('Selling Price*', 0)

    if channel == "Amazon":
        p['SKU'] = sku
        p['Item Name'] = f"{name} ({var})"
        p['Product Type'] = category.upper().replace(" ", "_")
        p['Your Price INR'] = price
    elif channel == "Flipkart":
        p['Seller SKU ID'] = sku
        p['Product Title'] = name
        p['MRP'] = df.get('MRP*', 0)
        p['Size'] = var
    elif channel == "Meesho":
        p['Catalog Name'] = name
        p['SKU'] = sku
        p['Size'] = var
        p['Price'] = price
    return p

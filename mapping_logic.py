import pandas as pd

def preprocess_data(df, selected_category):
    """Explodes variations and injects category context."""
    df['Product Category*'] = selected_category
    
    # Standard variation column from your template
    var_col = 'Variations (comma separated)*'
    if var_col in df.columns:
        df[var_col] = df[var_col].astype(str).str.split(',')
        df = df.explode(var_col)
        df[var_col] = df[var_col].str.strip()
    return df

def generate_fashion_description(row):
    """SEO-rich description using category and material keywords."""
    name = row.get('Product Name*', 'Product')
    cat = row.get('Product Category*', 'Apparel')
    brand = row.get('Brand*', 'Formula Man')
    fabric = row.get('Fabric Type*', 'Soft Fabric')
    
    templates = {
        "Dress": f"Elegant {brand} {name} Dress. Expertly crafted with {fabric} for style and comfort[cite: 25, 26].",
        "Top & Tunic": f"Trendy {brand} {name} Top & Tunic. Casual yet chic, made from breathable {fabric}[cite: 25, 26].",
        "Kurti/Kurta": f"Traditional {brand} {name} ethnic wear. Premium {fabric} Kurti for ultimate comfort[cite: 25, 26].",
        "Tshirts": f"Cool {brand} {name} T-shirt. High-quality {fabric} for a perfect everyday fit[cite: 25, 26]."
    }
    return templates.get(cat, f"Premium {brand} {cat} collection.")

def transform_data(df, channel, category):
    """Deep maps master data to marketplace-specific headers[cite: 1, 14, 18]."""
    p = pd.DataFrame()
    
    # Extraction from your provided master fields
    sku = df.get('SKU Code*', '')
    name = df.get('Product Name*', '')
    price = df.get('Selling Price*', 0)
    mrp = df.get('MRP*', 0)
    img = df.get('Main Image*', '')
    var = df.get('Variations (comma separated)*', '')
    hsn = df.get('HSN*', '')

    if channel == "Amazon":
        # Mapping for Amazon's deep structure 
        p['SKU'] = sku
        p['Item Name'] = f"{name} ({var})"
        p['Product Type'] = category.upper().replace(" ", "_")
        p['Your Price INR (Sell on Amazon, IN)'] = price
        p['Maximum Retail Price (Sell on Amazon, IN)'] = mrp
        p['Quantity (IN)'] = df.get('Inventory*', 0)
        p['Main Image URL'] = img
        p['HSN'] = hsn
        p['Product Description'] = df.get('Product Description*', '')

    elif channel == "Flipkart":
        # Mapping for Flipkart's specific fashion headers [cite: 14, 18]
        p['Seller SKU ID'] = sku
        p['Product Title'] = name
        p['MRP (INR)'] = mrp
        p['Your selling price (INR)'] = price
        p['Stock'] = df.get('Inventory*', 0)
        p['Size'] = var
        p['Style Type'] = category
        p['Description'] = df.get('Product Description*', '')
        p['Main Image URL'] = img
        p['HSN'] = hsn

    elif channel == "Meesho":
        # Dynamic headers for Meesho based on category selection
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
        p['Description'] = df.get('Product Description*', '')

    return p

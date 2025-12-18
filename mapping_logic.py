import pandas as pd

def preprocess_data(df):
    """
    Cleans the data and expands comma-separated variations into multiple rows.
    """
    # Define the variation column name exactly as it appears in your template
    var_col = 'Variations (comma separated)*'
    
    if var_col in df.columns:
        # Convert to string and split by comma
        df[var_col] = df[var_col].astype(str).str.split(',')
        # Explode into separate rows
        df = df.explode(var_col)
        # Clean whitespace
        df[var_col] = df[var_col].str.strip()
    
    return df

def transform_data(df, channel):
    """
    Applies marketplace-specific column mappings.
    """
    processed_df = pd.DataFrame()

    if channel == "Amazon":
        processed_df['item_name'] = df.get('Product Name*', '') + " - " + df.get('Variations (comma separated)*', '')
        processed_df['external_product_id'] = df.get('SKU Code*', '')
        processed_df['standard_price'] = df.get('Selling Price*', 0)
        processed_df['quantity'] = df.get('Inventory*', 0)
        processed_df['main_image_url'] = df.get('Main Image*', '')

    elif channel == "Flipkart":
        processed_df['Seller SKU ID'] = df.get('SKU Code*', '')
        processed_df['Size'] = df.get('Variations (comma separated)*', '')
        processed_df['MRP'] = df.get('MRP*', 0)
        processed_df['Selling Price'] = df.get('Selling Price*', 0)
        processed_df['Main Image'] = df.get('Main Image*', '')

    elif channel == "Meesho":
        processed_df['Product Name'] = df.get('Product Name*', '')
        processed_df['Size'] = df.get('Variations (comma separated)*', '')
        processed_df['Price'] = df.get('Selling Price*', 0)
        processed_df['SKU'] = df.get('SKU Code*', '')
        processed_df['Image 1'] = df.get('Main Image*', '')

    else:
        # Default for Myntra/Ajio if mapping isn't defined yet
        processed_df = df.copy()

    return processed_df

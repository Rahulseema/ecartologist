import pandas as pd

def transform_data(df, channel):
    """
    Transforms the master CSV into the specific format 
    required by the chosen marketplace.
    """
    processed_df = pd.DataFrame()

    if channel == "Amazon":
        # Example Amazon Mapping
        # Mapping: Master Column -> Amazon Template Column
        processed_df['item_name'] = df.get('Product Name', '')
        processed_df['external_product_id'] = df.get('SKU', '')
        processed_df['external_product_id_type'] = 'UPC'
        processed_df['standard_price'] = df.get('Price', 0)
        processed_df['quantity'] = df.get('Stock', 0)
        # Amazon often requires specific static values
        processed_df['feed_product_type'] = 'GENERIC'

    elif channel == "Flipkart":
        # Example Flipkart Mapping
        processed_df['FSN'] = df.get('Serial Number', '')
        processed_df['Listing Price'] = df.get('Price', 0)
        processed_df['Stock'] = df.get('Stock', 0)
        processed_df['Shipping Provider'] = 'Flipkart'
        processed_df['Status'] = 'Active'

    elif channel == "Meesho":
        # Example Meesho Mapping
        processed_df['Catalog Name'] = df.get('Product Name', '')
        processed_df['Price'] = df.get('Price', 0)
        processed_df['GST %'] = 18
        processed_df['Product Weight'] = df.get('Weight', 500)

    else:
        # Fallback if no logic is defined yet
        processed_df = df.copy()

    return processed_df

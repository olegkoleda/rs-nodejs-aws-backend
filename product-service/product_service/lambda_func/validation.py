def validate_product_data(product_data):
    """
    Validates product_data before creating a product.
    Returns True if valid, False otherwise.
    """
    if not isinstance(product_data, dict):
        return False
    
    required_fields = ['title', 'description', 'price', 'count']
    for field in required_fields:
        if field not in product_data:
            return False
    
    if not isinstance(product_data['title'], str):
        return False
    
    if not isinstance(product_data['description'], str):
        return False
    
    if not isinstance(product_data['price'], (int, float)):
        return False
    
    if not isinstance(product_data['count'], int):
        return False
    
    return True

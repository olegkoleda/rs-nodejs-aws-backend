import json
from mock_data import products

def handler(event, context):
    product_id = int(event['pathParameters']['productId'])
    product = next((product for product in products if product["id"] == product_id), None)
    
    if product is None:
        return {
            "statusCode": 404,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET",
                "Content-Type": "application/json"
            },
            "body": json.dumps({"message": "Product not found"})
        }
    
    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET",
            "Content-Type": "application/json"
        },
        "body": json.dumps(product)
    }

import json
import boto3
import logging
import os

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize a session using Amazon DynamoDB
try:
    dynamodb = boto3.resource('dynamodb', region_name=os.getenv('AWS_REGION'))
    products_table = dynamodb.Table(os.getenv('PRODUCTS_TABLE_NAME'))
    stocks_table = dynamodb.Table(os.getenv('STOCKS_TABLE_NAME'))
    logger.info("Successfully connected to DynamoDB")
except Exception as e:
    logger.error(f"Error connecting to DynamoDB: {e}")
    raise

def get_product_by_id(product_id):
    try:
        response = products_table.get_item(Key={'id': product_id})
        product = response.get('Item', None)
        if product:
            logger.info(f"Retrieved product: {product_id}")
        else:
            logger.warning(f"Product not found: {product_id}")
        return product
    except Exception as e:
        logger.error(f"Error retrieving product: {e}")
        return None

def get_stock_by_product_id(product_id):
    try:
        response = stocks_table.get_item(Key={'product_id': product_id})
        stock = response.get('Item', None)
        if stock:
            logger.info(f"Retrieved stock for product: {product_id}")
        else:
            logger.warning(f"Stock not found for product: {product_id}")
        return stock
    except Exception as e:
        logger.error(f"Error retrieving stock: {e}")
        return None

def handler(event, context):
    logger.info(f"Received event: {json.dumps(event)}")
    
    try:
        product_id = event['pathParameters']['productId']
        product = get_product_by_id(product_id)
        if not product:
            return {
                "statusCode": 404,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "GET",
                    "Content-Type": "application/json"
                },
                "body": json.dumps({"message": "Product not found"})
            }

        stock = get_stock_by_product_id(product_id)
        if stock:
            product['count'] = str(stock['count'])
        else:
            product['count'] = 0

        # Serialize price to float
        product['price'] = str(product['price'])
        
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET",
                "Content-Type": "application/json"
            },
            "body": json.dumps(product)
        }
    except Exception as e:
        logger.error(f"Error in handler: {e}")
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET",
                "Content-Type": "application/json"
            },
            "body": json.dumps({"error": "Internal Server Error"})
        }

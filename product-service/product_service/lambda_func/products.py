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

def get_products():
    try:
        response = products_table.scan()
        products = response.get('Items', [])
        logger.info(f"Retrieved {len(products)} products")
        return products
    except Exception as e:
        logger.error(f"Error retrieving products: {e}")
        return []

def get_stocks():
    try:
        response = stocks_table.scan()
        stocks = response.get('Items', [])
        logger.info(f"Retrieved {len(stocks)} stocks")
        return stocks
    except Exception as e:
        logger.error(f"Error retrieving stocks: {e}")
        return []

def combine_products_and_stocks(products, stocks):
    try:
        stocks_dict = {stock['product_id']: stock['count'] for stock in stocks}
        combined = []
        for product in products:
            product_id = product['id']
            stock_count = stocks_dict.get(product_id, 0)
            combined.append({
                'id': product_id,
                'title': product['title'],
                'description': product.get('description', ''),
                'price': str(product['price']),
                'count': str(stock_count)
            })
        logger.info(f"Combined data for {len(combined)} products")
        return combined
    except Exception as e:
        logger.error(f"Error combining products and stocks: {e}")
        return []

def handler(event, context):
    logger.info(f"Received event: {json.dumps(event)}")
    try:
        products = get_products()
        stocks = get_stocks()
        combined_data = combine_products_and_stocks(products, stocks)
        
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET",
                "Content-Type": "application/json"
            },
            "body": json.dumps(combined_data)
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

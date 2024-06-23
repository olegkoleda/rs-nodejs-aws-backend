import json
import boto3
import os
from decimal import Decimal
from uuid import uuid4
from validation import validate_product_data
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Initialize a session using Amazon DynamoDB
try:
    dynamodb = boto3.resource('dynamodb', region_name=os.getenv('AWS_REGION'))
    dynamodb_client = boto3.client('dynamodb', region_name=os.getenv('AWS_REGION'))
    products_table = dynamodb.Table(os.getenv('PRODUCTS_TABLE_NAME'))
    stocks_table = dynamodb.Table(os.getenv('STOCKS_TABLE_NAME'))
    logger.info("Successfully connected to DynamoDB")
except Exception as e:
    logger.error(f"Error connecting to DynamoDB: {e}")
    raise RuntimeError(f"Error connecting to DynamoDB: {e}")

def create_product(product_data):
    try:
        logger.info(f"Creating product with data: {product_data}")
        # Validate product data
        if not validate_product_data(product_data):
            logger.warning("Invalid product data")
            return {
                "statusCode": 400,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "POST",
                    "Content-Type": "application/json"
                },
                "body": json.dumps({"error": "Invalid product data"})
            }

        # Generate unique UUID for product
        product_id = str(uuid4())
        product_data['id'] = product_id
        product_data['price'] = Decimal(product_data['price'])
        stock_data = {
            'product_id': product_id,
            'count': int(product_data['count'])
        }

        # Prepare item structure for DynamoDB
        product_item = {
            'id': {'S': product_data['id']},
            'title': {'S': product_data['title']},
            'description': {'S': product_data['description']},
            'price': {'N': str(product_data['price'])}
        }

        stock_item = {
            'product_id': {'S': stock_data['product_id']},
            'count': {'N': str(stock_data['count'])}
        }

        # Execute the transaction
        dynamodb_client.transact_write_items(
            TransactItems=[
                {
                    'Put': {
                        'TableName': os.getenv('PRODUCTS_TABLE_NAME'),
                        'Item': product_item
                    }
                },
                {
                    'Put': {
                        'TableName': os.getenv('STOCKS_TABLE_NAME'),
                        'Item': stock_item
                    }
                }
            ]
        )

        logger.info(f"Product created successfully with ID: {product_id}")
        return {
            "statusCode": 201,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST",
                "Content-Type": "application/json"
            },
            "body": json.dumps({"message": "Product created successfully", "productId": product_id})
        }

    except Exception as e:
        logger.error(f"Error creating product: {e}")
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST",
                "Content-Type": "application/json"
            },
            "body": json.dumps({"error": str(e)})
        }

def handler(event, context):
    logger.info(f"Received event: {json.dumps(event)}")
    try:
        request_body = json.loads(event['body'])
        logger.info(f"Request body: {request_body}")
        response = create_product(request_body)
        return response
    except Exception as e:
        logger.error(f"Error in handler: {e}")
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST",
                "Content-Type": "application/json"
            },
            "body": json.dumps({"error": str(e)})
        }

import boto3
import uuid
from faker import Faker

# Initialize a session using Amazon DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')

# Reference the existing DynamoDB tables
products_table = dynamodb.Table('products')
stocks_table = dynamodb.Table('stocks')

# Initialize Faker for generating mock data
fake = Faker()

# Function to create mock product data
def create_mock_product():
    product_id = str(uuid.uuid4())
    title = fake.word().capitalize()
    description = fake.sentence()
    price = fake.random_int(min=10, max=1000)
    return {
        'id': product_id,
        'title': title,
        'description': description,
        'price': price
    }

# Function to create mock stock data
def create_mock_stock(product_id):
    count = fake.random_int(min=1, max=100)
    return {
        'product_id': product_id,
        'count': count
    }

# Function to insert mock data into the tables
def insert_mock_data(num_items):
    for _ in range(num_items):
        # Create mock product data
        product = create_mock_product()
        # Insert product data into the products table
        products_table.put_item(Item=product)

        # Create mock stock data for the product
        stock = create_mock_stock(product['id'])
        # Insert stock data into the stocks table
        stocks_table.put_item(Item=stock)

        # Print the inserted data for verification
        print(f"Inserted product: {product['id']} with stock: {stock['count']}")

# Insert 10 items as an example
insert_mock_data(6)

from aws_cdk import (
    aws_dynamodb as dynamodb,
    aws_lambda as _lambda,
    Stack,
)
from constructs import Construct

from product_service.put_products import PutProductsLambdaConstruct
from product_service.get_products import GetProductsLambdaConstruct
from product_service.get_product_by_id import GetProductByIdLambdaConstruct
from product_service.api_gateway import ApiGatewayConstruct

class ProductServiceStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Table names
        products_table_name = "products"
        stocks_table_name = "stocks"

        # Reference existing DynamoDB tables
        products_table = dynamodb.Table.from_table_name(self, "ProductsTable", products_table_name)
        stocks_table = dynamodb.Table.from_table_name(self, "StocksTable", stocks_table_name)

        # Environment variables for Lambda functions
        lambda_env_vars = {
            'PRODUCTS_TABLE_NAME': products_table.table_name,
            'STOCKS_TABLE_NAME': stocks_table.table_name
        }

        # Create GetProductsLambda construct
        get_products_lambda_construct = GetProductsLambdaConstruct(self, 'GetProductsLambda', lambda_env_vars)

        # Create GetProductByIdLambda construct
        get_product_by_id_lambda_construct = GetProductByIdLambdaConstruct(self, 'GetProductByIdLambda', lambda_env_vars)
        
        # Create PutProductsLambda construct
        put_products_lambda_construct = PutProductsLambdaConstruct(self, 'PutProductsLambda', lambda_env_vars)

        # Grant read/write permissions to the Lambda functions
        products_table.grant_read_write_data(get_products_lambda_construct.function)
        products_table.grant_read_write_data(get_product_by_id_lambda_construct.function)
        products_table.grant_read_write_data(put_products_lambda_construct.function)
        stocks_table.grant_read_write_data(get_products_lambda_construct.function)
        stocks_table.grant_read_write_data(get_product_by_id_lambda_construct.function)
        stocks_table.grant_read_write_data(put_products_lambda_construct.function)

        # Create API Gateway construct with Lambda integrations
        api_gateway_construct = ApiGatewayConstruct(self, 'ApiGatewayConstruct', 
                                                    get_products_lambda_construct.function,
                                                    get_product_by_id_lambda_construct.function,
                                                    put_products_lambda_construct.function)

from aws_cdk import Stack
from constructs import Construct
from product_service.get_products import GetProductsLambdaConstruct
from product_service.get_product_by_id import GetProductByIdLambdaConstruct
from product_service.api_gateway import ApiGatewayConstruct

class ProductServiceStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create GetProductsLambda construct
        get_products_lambda_construct = GetProductsLambdaConstruct(self, 'GetProductsLambda')

        # Create GetProductByIdLambda construct
        get_product_by_id_lambda_construct = GetProductByIdLambdaConstruct(self, 'GetProductByIdLambda')

        # Create API Gateway construct with Lambda integrations
        api_gateway_construct = ApiGatewayConstruct(self, 'ApiGatewayConstruct', 
                                                    get_products_lambda_construct.function,
                                                    get_product_by_id_lambda_construct.function)

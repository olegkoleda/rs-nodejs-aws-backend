from aws_cdk import (
    aws_apigateway as apigateway,
    aws_lambda as _lambda,
    Stack,
)
from constructs import Construct

class ApiGatewayConstruct(Construct):

    def __init__(self, scope: Construct, id: str, get_products_fn: _lambda, get_product_by_id_fn: _lambda) -> None:
        super().__init__(scope, id)

        # Create API Gateway
        api = apigateway.RestApi(self, 'ProductServiceApi',
            rest_api_name='Product Service',
            description='This service serves products.'
        )

        # Integrate get_products_fn Lambda function
        products_recourse = api.root.add_resource('products')
        get_products_integration = apigateway.LambdaIntegration(get_products_fn)
        products_recourse.add_method('GET', get_products_integration)

        # Integrate get_product_by_id_fn Lambda function
        get_product_by_id_integration = apigateway.LambdaIntegration(get_product_by_id_fn)
        product_by_id_recourse = products_recourse.add_resource('{productId}')
        product_by_id_recourse.add_method('GET', get_product_by_id_integration)

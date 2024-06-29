from aws_cdk import aws_apigateway as apigateway
from aws_cdk import aws_lambda as _lambda
from aws_cdk import Stack

from constructs import Construct

class ApiGatewayConstruct(Construct):

    def __init__(self, scope: Construct, id: str, 
                 get_products_fn: _lambda.Function,
                 get_product_by_id_fn: _lambda.Function,
                 put_products_fn: _lambda.Function) -> None:
        super().__init__(scope, id)

        # Create API Gateway
        api = apigateway.RestApi(self, 'ProductServiceApi',
            rest_api_name='Product Service',
            description='This service serves products.'
        )

        # Integrate get_products_fn Lambda function
        products_resource = api.root.add_resource('products')
        products_resource.add_method('GET', apigateway.LambdaIntegration(get_products_fn))

        # Integrate get_product_by_id_fn Lambda function
        product_by_id_resource = products_resource.add_resource('{productId}')
        product_by_id_resource.add_method('GET', apigateway.LambdaIntegration(get_product_by_id_fn))

        # Integrate put_products_fn Lambda function
        products_resource.add_method('POST', apigateway.LambdaIntegration(put_products_fn))

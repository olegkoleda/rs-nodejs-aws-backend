from aws_cdk import (
    aws_apigateway as apigateway,
    aws_lambda as _lambda
)
from constructs import Construct

class ApiGatewayConstruct(Construct):

    def __init__(self, scope: Construct, id: str, lambda_function: _lambda.Function, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Define the API Gateway
        api = apigateway.RestApi(self, "importProductsFileApi",
            rest_api_name="Import Service",
            default_cors_preflight_options={
                "allow_origins": apigateway.Cors.ALL_ORIGINS,
                "allow_methods": apigateway.Cors.ALL_METHODS
            }
        )

        import_products = api.root.add_resource("import")
        import_products_lambda_integration = apigateway.LambdaIntegration(lambda_function)
        import_products.add_method("GET", import_products_lambda_integration)


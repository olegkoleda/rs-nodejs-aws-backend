from aws_cdk import (
    aws_lambda as _lambda,
    Stack,
)
from constructs import Construct

class GetProductsLambdaConstruct(Construct):

    def __init__(self, scope: Construct, id: str, environment_variables: dict) -> None:
        super().__init__(scope, id)

        self.function = _lambda.Function(
            self, 'GetProductsFunction',
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler='products.handler',
            code=_lambda.Code.from_asset('product_service/lambda_func/'),
            environment=environment_variables
        )

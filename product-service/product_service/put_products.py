from aws_cdk import aws_lambda as _lambda

from constructs import Construct

class PutProductsLambdaConstruct(Construct):

    def __init__(self, scope: Construct, id: str, environment_variables: dict, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.function = _lambda.Function(
            self, 'PutProductsFunction',
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler='create_product.handler',
            code=_lambda.Code.from_asset('product_service/lambda_func/'),
            environment=environment_variables,
        )

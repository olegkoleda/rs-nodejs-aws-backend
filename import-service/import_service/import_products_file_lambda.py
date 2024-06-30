from aws_cdk import (
    aws_lambda as _lambda,
    aws_iam as iam,
    aws_s3 as s3
)
from constructs import Construct

class ImportProductsFileLambda(Construct):

    def __init__(self, scope: Construct, id: str, bucket_name: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.function = _lambda.Function(self, "importProductsFileHandler",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="import_products_file.lambda_handler",
            code=_lambda.Code.from_asset("import_service/lambda/"),
            environment={
                'BUCKET_NAME': bucket_name
            }
        )

        # Add permissions for Lambda to interact with S3 bucket
        self.function.add_to_role_policy(iam.PolicyStatement(
            actions=["s3:PutObject"],
            resources=[f"arn:aws:s3:::{bucket_name}/*"]
        ))

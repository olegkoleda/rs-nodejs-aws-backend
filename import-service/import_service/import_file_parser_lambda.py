from aws_cdk import (
    aws_lambda as _lambda,
    aws_iam as iam,
    aws_s3 as s3,
    aws_s3_notifications as s3_notifications
)
from constructs import Construct

class ImportFileParserLambda(Construct):

    def __init__(self, scope: Construct, id: str, bucket_name: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.bucket_name = bucket_name

        self.function = _lambda.Function(self, "importFileParserHandler",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="import_file_parser.lambda_handler",
            code=_lambda.Code.from_asset("import_service/lambda/"),
            environment={
                'BUCKET_NAME': bucket_name
            }
        )

        # Add permissions for Lambda to read from and manage S3 bucket
        self.function.add_to_role_policy(iam.PolicyStatement(
            actions=["s3:GetObject", "s3:PutObject", "s3:DeleteObject", "s3:CopyObject"],
            resources=[f"arn:aws:s3:::{bucket_name}/uploaded/*", f"arn:aws:s3:::{bucket_name}/parsed/*"]
        ))

    def add_s3_event_notification(self):
        bucket = s3.Bucket.from_bucket_name(self, "ExistingBucket", self.bucket_name)

        bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED,
            s3_notifications.LambdaDestination(self.function),
            s3.NotificationKeyFilter(prefix="uploaded/")
        )

from aws_cdk import Stack
from constructs import Construct
from import_service.import_products_file_lambda import ImportProductsFileLambda
from import_service.import_file_parser_lambda import ImportFileParserLambda
from import_service.api_gateway_construct import ApiGatewayConstruct

class ImportServiceStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        bucket_name = 'products-csv-storage'

        # Create the Lambda functions
        import_products_file_lambda = ImportProductsFileLambda(self, "ImportProductsFileLambda", bucket_name=bucket_name)
        import_file_parser_lambda = ImportFileParserLambda(self, "ImportFileParserLambda", bucket_name=bucket_name)

        # Create the API Gateway and link it to the importProductsFile Lambda
        api_gateway = ApiGatewayConstruct(self, "ApiGatewayConstruct", lambda_function=import_products_file_lambda.function)

        # Add S3 event notification to trigger the importFileParser Lambda function
        import_file_parser_lambda.add_s3_event_notification()

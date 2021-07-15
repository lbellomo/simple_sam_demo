from diagrams import Diagram
from diagrams.aws.compute import LambdaFunction
from diagrams.aws.mobile import APIGatewayEndpoint
from diagrams.aws.database import DynamodbTable

with Diagram("Arquitecture"):

    lambda_write = LambdaFunction("WriteIrisFunction")
    lambda_read = LambdaFunction("ReadIrisFunction")
    lambda_process = LambdaFunction("ProcessIrisDynamoDBStream")

    dynamo_table = DynamodbTable("IrisTable")

    api_endpoint_write = APIGatewayEndpoint("Endpoint write")
    api_endpoint_read = APIGatewayEndpoint("Endpoint read")

    (
        api_endpoint_write
        >> lambda_write
        >> dynamo_table
        >> lambda_read
        >> api_endpoint_read
    )
    dynamo_table >> lambda_process >> dynamo_table

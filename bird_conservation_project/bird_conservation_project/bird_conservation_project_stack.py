from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_lambda as lambda_,
    RemovalPolicy,
    aws_iam as iam
)
from constructs import Construct

class BirdConservationProjectStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        # example resource
        # queue = sqs.Queue(
        #     self, "BirdConservationProjectQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )

        # Create S3 bucket
        bucket = s3.Bucket(self, "BirdConservationBucket",
                           bucket_name="bird-conservation-bucket",
                           versioned=True,
                           encryption=s3.BucketEncryption.S3_MANAGED,
                           removal_policy=RemovalPolicy.RETAIN
                           )

        # Create Lambda function
        etl_lambda = lambda_.Function(self, "ETLFunction",
                                      runtime=lambda_.Runtime.PYTHON_3_8,
                                      handler="lambda_function.handler",
                                      code=lambda_.Code.from_asset("lambda_function"),
                                      environment={
                                          "BUCKET_NAME": bucket.bucket_name
                                      }
                                      )

        # Grant Lambda function read/write permissions to S3 bucket
        bucket.grant_read_write(etl_lambda)

        # Add Permissions to SSM
        etl_lambda.add_to_role_policy(iam.PolicyStatement(
            actions=["ssm:GetParameter"],
            resources=["arn:aws:ssm:us-east-1:686255962431:parameter/ebird/api_key"]
        ))

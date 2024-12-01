from aws_cdk import (
    core,
    aws_s3 as s3,
    aws_lambda as lambda_,
    aws_events as events,
    aws_events_targets as targets,
)

class BirdConservationStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create S3 bucket
        bucket = s3.Bucket(self, "BirdConservationBucket",
            versioned=True,
            encryption=s3.BucketEncryption.S3_MANAGED)

        # Create Lambda function
        etl_lambda = lambda_.Function(self, "ETLFunction",
            runtime=lambda_.Runtime.PYTHON_3_8,
            handler="lambda_function.handler",
            code=lambda_.Code.from_asset("../lambda"),
            environment={
                "BUCKET_NAME": bucket.bucket_name
            }
        )

        # Grant Lambda function read/write permissions to S3 bucket
        bucket.grant_read_write(etl_lambda)

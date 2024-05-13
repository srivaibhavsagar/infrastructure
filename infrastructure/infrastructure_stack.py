from aws_cdk import (
    # Duration,
    aws_s3 as _s3,
    Stack,
    # aws_sqs as sqs,
)
from constructs import Construct

class InfrastructureStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        # example resource
        # queue = sqs.Queue(
        #     self, "InfrastructureQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )
    
        _s3.Bucket(self,"myProdArtifactBucketId",
                                )

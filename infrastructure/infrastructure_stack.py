from aws_cdk import (
    # Duration,
    
    aws_s3 as _s3,
    aws_ec2 as _ec2,
    Stack,
    # aws_sqs as sqs,
)
from aws_cdk import Stack,CfnOutput
from constructs import Construct
from infrastructure.serverless_stack.apiGateway_lambda.custom_apigw import CustomApiGatewayStack

class StartingStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, environment,**kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        self.default_vpc = _ec2.Vpc.from_lookup(self,
                                        "importedVPC",
                                        is_default=True,
                                        # vpc_id="vpc-d0a193aa"
                                        )

        default_vpc_id = CfnOutput(self,
                        "importedVpc",
                        value=self.default_vpc.vpc_id)
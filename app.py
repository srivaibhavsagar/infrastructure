#!/usr/bin/env python3
import os

import aws_cdk as cdk
from aws_cdk import Environment

from infrastructure.infrastructure_stack import InfrastructureStack
from infrastructure.serverless_stack.apiGateway_lambda.custom_apigw import CustomApiGatewayStack
from infrastructure.database_stack.rds_3tier_stack import RdsDatabase3TierStack
from infrastructure.database_stack.custom_vpc import CustomVpcStack


app = cdk.App()

environment = app.node.try_get_context("environment")
if environment is None:
    print("No environment is provided. Hence default value dev is selected as environment")
    environment = "dev"

if environment == "prod":
    account_details = Environment(account="184261415726", region="us-east-1")
else:
    account_details = Environment(account="184261415726", region="us-east-1")


# CustomApiGatewayStack(app,"apiGateway-lambda-stack",environment=environment,env=account_details)
default = InfrastructureStack(app, "InfrastructureStack",environment=environment,env=account_details)

# vpc_detail = CustomVpcStack(app,"new-vpc",env=account_details)

# RdsDatabase3TierStack(app,"rds-stack",environment,vpc=vpc_detail.custom_vpc,env=account_details)


app.synth()

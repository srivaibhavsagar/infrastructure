#!/usr/bin/env python3
import os

import aws_cdk as cdk
from aws_cdk import Environment

from infrastructure.infrastructure_stack import StartingStack
from infrastructure.serverless_stack.apiGateway_lambda.custom_apigw import CustomApiGatewayStack
from infrastructure.database_stack.rds_3tier_stack import RdsDatabase3TierStack
from infrastructure.database_stack.custom_vpc import CustomVpcStack
from infrastructure.database_stack.fargate import ServerlessContainersArchitectureWithFargateStack


app = cdk.App()

environment = app.node.try_get_context("environment")
if environment is None:
    print("No environment is provided. Hence default value dev is selected as environment")
    environment = "dev"

regions = app.node.try_get_context("envs")[environment]["region"]
account_number = app.node.try_get_context("envs")[environment]["account"]
account_details = Environment(account=account_number, region=regions)

rds_stack_name = app.node.try_get_context("envs")[environment]["rds"]["stack_name"]
ecs_stack_name = app.node.try_get_context("envs")[environment]["ecs"]["stack_name"]
vpc_stack_name = app.node.try_get_context("envs")[environment]["vpc"]["stack_name"]

# Get Default VPC
# default = StartingStack(app, "StartingStack",environment=environment,env=account_details)

# Create api gateway and lambda
# CustomApiGatewayStack(app,"apiGateway-lambda-stack",environment=environment,env=account_details)

# create vpc which should be used in rds
vpc_detail = CustomVpcStack(app,vpc_stack_name,env=account_details)

# create rds
rds_detail = RdsDatabase3TierStack(app,rds_stack_name,environment,vpc=vpc_detail.custom_vpc,env=account_details)

# create fardate container
ServerlessContainersArchitectureWithFargateStack(app,ecs_stack_name,environment,vpc=vpc_detail.custom_vpc,rds_secret= rds_detail.rds_secret,env=account_details)

app.synth()
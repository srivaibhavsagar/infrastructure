from aws_cdk import aws_apigateway as _apigw
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_logs as _logs
from aws_cdk import Stack,Duration,RemovalPolicy,CfnOutput
from constructs import Construct

class CustomApiGatewayStack(Stack):

    def __init__(self, scope: Construct, id: str,env: str, ** kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create Serverless Event Processor using Lambda):
        # Read Lambda Code
        try:
            # import os
            # print(os.system("ls -ltr"))
            with open("infrastructure/serverless_stack/lambda_src/konstone_processor.py", mode="r") as f:
                fn_code = f.read()
        except OSError:
            print("Unable to read Lambda Function Code")

        lambda_name = self.node.try_get_context('envs')[env]['lambda_name']
        fn = _lambda.Function(self,
                                       "lambdaFunction",
                                       function_name=f"{env}-{lambda_name}",
                                       runtime=_lambda.Runtime.PYTHON_3_12,
                                       handler="index.lambda_handler",
                                       code=_lambda.InlineCode(
                                           fn_code),
                                       timeout=Duration.seconds(3),
                                    #    reserved_concurrent_executions=1,
                                       environment={
                                           "LOG_LEVEL": "INFO",
                                           "Environment": "Production"
                                       }
                                       )

        # Create Custom Loggroup
        # /aws/lambda/function-name
        lg = _logs.LogGroup(self,
                                     "logGroup",
                                     log_group_name=f"/aws/lambda/{fn.function_name}",
                                     retention=_logs.RetentionDays.ONE_WEEK,
                                     removal_policy=RemovalPolicy.DESTROY
                                     )

        # Add API GW front end for the Lambda
        fn_integration = _apigw.LambdaRestApi(
            self,
            "apiEndpoint",
            handler=fn
        )

        output_1 = CfnOutput(self,
                                  "ApiUrl",
                                  value=f"{fn_integration.url}",
                                  description="Use a browser to access this url"
                                  )
        
        output_2 = CfnOutput(self,
                                  "LambdaName",
                                  value=f"{fn.function_name}",
                                  description="This is the Lambda Name"
                                  )

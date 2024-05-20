from aws_cdk import Stack,Duration,RemovalPolicy,CfnOutput
from aws_cdk import aws_ec2 as _ec2
from aws_cdk import aws_ecs as _ecs
from aws_cdk import aws_ecs_patterns as _ecs_patterns
from constructs import Construct


class ServerlessContainersArchitectureWithFargateStack(Stack):

    def __init__(self, scope: Construct, id: str, vpc,** kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Add your stack resources below):

        # Create Fargate Cluster inside the VPC
        micro_service_cluster = _ecs.Cluster(
            self,
            "microServiceCluster",
            vpc=vpc
        )

        # Deploy Container in the micro Service with an Application Load Balancer
        serverless_web_service = _ecs_patterns.ApplicationLoadBalancedFargateService(
            self,
            "webService",
            cluster=micro_service_cluster,
            memory_limit_mib=1024,
            cpu=512,
            task_image_options={
                "image": _ecs.ContainerImage.from_registry("python"),
                "environment": {
                    "ENVIRONMENT": "vaibhav"
                }
            },
            desired_count=2
        )

        # Server Health Checks
        serverless_web_service.target_group.configure_health_check(path="/")

        # Output Web Service Url
        output_1 = CfnOutput(
            self,
            "webServiceUrl",
            value=f"{serverless_web_service.load_balancer.load_balancer_dns_name}",
            description="Access the web service url from your browser"
        )

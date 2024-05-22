from aws_cdk import Stack,Duration,RemovalPolicy,CfnOutput
from aws_cdk import aws_ec2 as _ec2
from aws_cdk import aws_ecs as _ecs
from aws_cdk import aws_ecs_patterns as _ecs_patterns
from constructs import Construct
from aws_cdk import aws_iam as _iam


class ServerlessContainersArchitectureWithFargateStack(Stack):

    def __init__(self, scope: Construct, id: str,environment, vpc,rds_secret,** kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Add your stack resources below):
        ecs_details = self.node.try_get_context("envs")[environment]["ecs"]
        ecs_image = ecs_details["image"]
        ecs_taskdefinition = ecs_details["taskdefinitionname"]
        ecs_desired_count = ecs_details["desired_count"]

        # Create Fargate Cluster inside the VPC
        micro_service_cluster = _ecs.Cluster(
            self,
            "microServiceCluster",
            vpc=vpc
        )

        task_role_id = _iam.Role(self, "task_roleId",
                                    assumed_by=_iam.ServicePrincipal(
                                        'ecs-tasks.amazonaws.com'),
                                    managed_policies=[
                                        _iam.ManagedPolicy.from_aws_managed_policy_name(
                                            'AdministratorAccess'
                                        ),
                                    ])

        serverless_web_service = _ecs_patterns.NetworkLoadBalancedFargateService(
            self,
            "webService",
            cluster=micro_service_cluster,
            memory_limit_mib=1024,
            cpu=512,
            task_image_options=_ecs_patterns.NetworkLoadBalancedTaskImageOptions(
                image=_ecs.ContainerImage.from_registry(ecs_image),
                task_role=task_role_id,
                family=ecs_taskdefinition,
                environment={
                    "region": kwargs["env"].region,
                    "secret_name": rds_secret
                }
            ),   
            
            runtime_platform=_ecs.RuntimePlatform(
                cpu_architecture=_ecs.CpuArchitecture.ARM64,
                operating_system_family=_ecs.OperatingSystemFamily.LINUX
            ),
            desired_count= ecs_desired_count
        )
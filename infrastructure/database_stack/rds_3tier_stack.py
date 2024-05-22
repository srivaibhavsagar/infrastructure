from aws_cdk import Stack,CfnOutput,RemovalPolicy,Duration
from aws_cdk import aws_rds as _rds
from aws_cdk import aws_ec2 as _ec2
from constructs import Construct


class RdsDatabase3TierStack(Stack):

    def __init__(self, scope: Construct, id: str,environment, vpc, ** kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        rds_details = self.node.try_get_context("envs")[environment]["rds"]
        rds_database_name = rds_details["database_name"]
        rds_port = rds_details["port"]
        rds_user = rds_details["username"]
        self.rds_secret = rds_details["secret_name"]

        # Create an RDS Database):
        db = _rds.DatabaseInstance(self,
                                            "RDS",
                                            database_name= rds_database_name,
                                            engine=_rds.DatabaseInstanceEngine.MYSQL,
                                            credentials=_rds.Credentials.from_generated_secret(username=rds_user,secret_name= self.rds_secret),
                                            vpc=vpc,
                                            vpc_subnets=_ec2.SubnetSelection(
                                                                subnet_type=_ec2.SubnetType.PUBLIC
                                                            ),
                                            publicly_accessible=True,
                                            port= rds_port,
                                            allocated_storage=30,
                                            multi_az=False,
                                            cloudwatch_logs_exports=[
                                                "audit", "error", "general", "slowquery"],
                                            removal_policy=RemovalPolicy.DESTROY,
                                            deletion_protection=False,
                                            delete_automated_backups=True,
                                            backup_retention=Duration.days(
                                                0)
                                            )

        # for sg in asg_security_groups:
        db.connections.connections.allow_from_any_ipv4(
            _ec2.Port.tcp(rds_port),
            description="Allow Internet access on ALB Port 80"
        )
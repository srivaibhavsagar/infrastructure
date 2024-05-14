from aws_cdk import Stack,CfnOutput,RemovalPolicy,Duration
from aws_cdk import aws_rds as _rds
from aws_cdk import aws_ec2 as _ec2
from constructs import Construct


class RdsDatabase3TierStack(Stack):

    def __init__(self, scope: Construct, id: str,environment, vpc, ** kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create an RDS Database):
        db = _rds.DatabaseInstance(self,
                                            "RDS",
                                            # master_username="mystiquemaster",
                                            database_name="db",
                                            engine=_rds.DatabaseInstanceEngine.MYSQL,
                                            vpc=vpc,
                                            port=3306,
                                            allocated_storage=30,
                                            multi_az=False,
                                            cloudwatch_logs_exports=[
                                                "audit", "error", "general", "slowquery"],
                                            # instance_class=_ec2.InstanceType.of(
                                                # _ec2.InstanceClass.BURSTABLE2,
                                                # _ec2.InstanceSize.MICRO
                                            # ),
                                            removal_policy=RemovalPolicy.DESTROY,
                                            deletion_protection=False,
                                            delete_automated_backups=True,
                                            backup_retention=Duration.days(
                                                0)
                                            )

        # for sg in asg_security_groups:
        #     db.connections.allow_default_port_from(
        #         sg, "Allow EC2 ASG access to RDS MySQL")

        # Output RDS Database EndPoint Address
        output_1 = CfnOutput(self,
                                  "DatabaseConnectionCommand",
                                  value=f"mysql -h {db.db_instance_endpoint_address} -P 3306 -u rds_username -p",
                                  description="Connect to the database using this command"
                                  )

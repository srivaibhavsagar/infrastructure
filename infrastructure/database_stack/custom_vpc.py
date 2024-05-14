from aws_cdk import aws_ec2 as _ec2
from aws_cdk import Stack,CfnOutput,Tag
from constructs import Construct


class CustomVpcStack(Stack):

    def __init__(self, scope: Construct, id: str, ** kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        prod_configs = self.node.try_get_context('envs')['prod']

        self.custom_vpc = _ec2.Vpc(
            self,
            "customVpcId",
            # cidr=prod_configs['vpc_configs']['vpc_cidr'],
            max_azs=2,
            nat_gateways=1,
            subnet_configuration=[
                _ec2.SubnetConfiguration(
                    name="publicSubnet", cidr_mask=prod_configs['vpc_configs']['cidr_mask'], subnet_type=_ec2.SubnetType.PUBLIC
                ),
                _ec2.SubnetConfiguration(
                    name="privateSubnet", cidr_mask=prod_configs['vpc_configs']['cidr_mask'], subnet_type=_ec2.SubnetType.PRIVATE_WITH_EGRESS
                ),
                _ec2.SubnetConfiguration(
                    name="dbSubnet", cidr_mask=prod_configs['vpc_configs']['cidr_mask'], subnet_type=_ec2.SubnetType.PRIVATE_ISOLATED
                )
            ]
        )

        CfnOutput(self,
                       "customVpcOutput",
                       value=self.custom_vpc.vpc_id,
                       export_name="customVpcId")

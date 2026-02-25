import boto3

import schedule
import time


# ec2_resource = boto3.resource('ec2')

# new_vpc = ec2_resource.create_vpc(
#     CidrBlock="10.0.0.0/16",
# )

# new_vpc.create_subnet(
#     CidrBlock="10.0.1.0/24",
# )

# new_vpc.create_subnet(
#     CidrBlock="10.0.2.0/24",
# )

# new_vpc.create_tags(
#     Tags=[
#         {
#             'Key': 'Name',
#             'Value': 'my-vpc',
#         },
#     ]
# )




# # ec2_client = boto3.client('ec2', region_name='eu-central-1')
# ec2_client = boto3.client('ec2')

# all_available_vpcs = ec2_client.describe_vpcs()
# vpcs = all_available_vpcs["Vpcs"]


# for vpc in vpcs:
#     print(f"VPC ID: {vpc['VpcId']}")
#     print(f"CIDR Block: {vpc['CidrBlock']}")
#     print(f"State: {vpc['State']}")
#     print(f"Is Default: {vpc['IsDefault']}")
#     print("-" * 50)

#     cidr_blocks_assoc_sets = vpc["CidrBlockAssociationSet"]
#     for assoc_set in cidr_blocks_assoc_sets:
#         print(f"  CIDR Block Association ID: {assoc_set['AssociationId']}")
#         print(f"  CIDR Block: {assoc_set['CidrBlock']}")
#         print(f"  CIDR Block State: {assoc_set['CidrBlockState']}")
#         print("-" * 50)


ec2_resource = boto3.resource('ec2')
ec2_client = boto3.client('ec2')


reservations = ec2_client.describe_instances()


for reservation in reservations['Reservations']:
    for instance in reservation['Instances']:
        print(f"Instance ID: {instance['InstanceId']}")
        print(f"Instance Type: {instance['InstanceType']}")
        print(f"State: {instance['State']['Name']}")
        print(f"Public IP: {instance.get('PublicIpAddress', 'N/A')}")
        print(f"Private IP: {instance.get('PrivateIpAddress', 'N/A')}")
        print("-" * 50)

def check_instance_status():
    statuses = ec2_client.describe_instance_status(
        IncludeAllInstances=True
    )

    for status in statuses['InstanceStatuses']:
        print(f"Instance ID: {status['InstanceId']}")
        print(f"Availability Zone: {status['AvailabilityZone']}")
        print(f"Instance State: {status['InstanceState']['Name']}")
        print(f"System Status: {status['SystemStatus']['Status']}")
        print(f"Instance Status: {status['InstanceStatus']['Status']}")
        print("-" * 50)


schedule.every(10).minutes.do(check_instance_status)

while True:
    schedule.run_pending()
    time.sleep(1)

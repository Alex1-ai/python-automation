import boto3

ec2_client = boto3.client('ec2')
ec2_resource = boto3.resource('ec2')

ec2_client_frankfurt = boto3.client('ec2', region_name="eu-central-11")
ec2_resource_frankfurt = boto3.resource('ec2', region_name="eu-central-11")

instance_ids = []
instance_ids_frankfurt = []

reservations = ec2_client.describe_tags()["reservations"]

for res in reservations:
    instances = res["Instances"]
    for instance in instances:
        instance_ids.append(instance["InstanceId"])
        tags = instance["Tags"]
        for tag in tags:
            if tag["Key"] == "Environment":
                print(f"Instance ID: {instance['InstanceId']}, Environment: {tag['Value']}")

response = ec2_resource.create_tags(
    Resources=instance_ids,

    Tags = [
        {
            'Key': 'environment',
            'Value': 'prod',
        }
    ]

)



reservations_frankfurt = ec2_client_frankfurt.describe_tags()["reservations"]

for res in reservations_frankfurt:
    instances = res["Instances"]
    for instance in instances:
        instance_ids_frankfurt.append(instance["InstanceId"])
        tags = instance["Tags"]
        for tag in tags:
            if tag["Key"] == "Environment":
                print(f"Instance ID: {instance['InstanceId']}, Environment: {tag['Value']}")

response = ec2_resource_frankfurt.create_tags(
    Resources=instance_ids_frankfurt,

    Tags = [
        {
            'Key': 'environment',
            'Value': 'prod',
        }
    ]

)

import boto3
from operator import itemgetter


ec2_client = boto3.client('ec2', region_name="us-east-1")
ec2_resource = boto3.resource('ec2', region_name="us-east-1")


instance_id = "i-0b9c8e5f1a2b3c4d5"


volumes = ec2_client.describe_volumes(
    Filters=[
        {
            'Name': 'attachment.instance-id',
            'Values': [instance_id]
        }
    ]
)

instance_volume = volumes["Volumes"][0]
print(f"Volume ID: {instance_volume['VolumeId']}, State: {instance_volume['State']}")

snapshots = ec2_client.describe_snapshots(
    OwnerIds=['self'],
    Filters=[
        {
            'Name': 'volume-id',
            'Values': [instance_volume["VolumeId"]]
        }
    ]
)

latest_snapshot = sorted(snapshots["Snapshots"], key=itemgetter("StartTime"), reverse=True)[0]
print(f"Latest Snapshot ID: {latest_snapshot['SnapshotId']}")


ec2_client.create_volume(
    SnapshotId=latest_snapshot["SnapshotId"],
    AvailabilityZone=instance_volume["AvailabilityZone"],
    TagSpecifications=[
        {
            'ResourceType': 'volume',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'prod'
                },
            ]
        },
    ]

)


while True:
    vol = ec2_resource.Volume(instance_volume["VolumeId"])
    print(f"Volume state: {vol.state}")
    if vol.state == "available":
        ec2_resource.Instance(instance_id).attach_volume(

            VolumeId=instance_volume["VolumeId"],
            Device='/dev/xydb'
        )
        break




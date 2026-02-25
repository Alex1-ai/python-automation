import boto3
import schedule


ec2_client = boto3.client('ec2', region_name="us-east-1")

def create_volume_snapshots():
    try:
        volumes = ec2_client.describe_volumes(
            Filters=[
                {
                    'Name': 'tag:Name',
                    'Values': ['prod']
                }


            ]

        )
    except Exception as e:
        print(f"Error describing volumes: {e}")
        return


    for volume in volumes["Volumes"]:
        new_snapshot = ec2_client.create_snapshot(
            VolumeId=volume["VolumeId"],
            Description=f"Backup of volume {volume['VolumeId']}",
        )
        print(f"Created snapshot {new_snapshot['SnapshotId']} for volume {volume['VolumeId']}")


schedule.every().day.do(create_volume_snapshots)

while True:
    schedule.run_pending()

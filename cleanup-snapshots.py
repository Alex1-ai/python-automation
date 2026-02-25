import boto3
from operator import itemgetter





ec2_client = boto3.client('ec2')


volumes = ec2_client.describe_volumes(
    Filters=[
        {
            'Name': 'tag:Name',
            'Values': ['prod']
        }


    ]

)


for volume in volumes["Volumes"]:
    snapshots = ec2_client.describe_snapshots(
        OwnerIds=['self'],
        Filter =[
            {
                'Name': 'volume-id',
                'Values': [volume["VolumeId"]]
            }
        ]
    )
    # print(f"Created snapshot {new_snapshot['SnapshotId']} for volume {volume['VolumeId']}")




sorted_by_date = sorted(snapshots["Snapshots"], key=itemgetter("StartTime"), reverse=True)

# for snapshot in snapshots["Snapshots"]:
#     print(f"Snapshot ID: {snapshot['SnapshotId']}, Volume ID: {snapshot['VolumeId']}, Start Time: {snapshot['StartTime']}")
#     ec2_client.delete_snapshot(SnapshotId=snapshot["SnapshotId"])
#     print(f"Deleted snapshot {snapshot['SnapshotId']}")

for snapshot in sorted_by_date[2:]:
    print(f"Snapshot ID: {snapshot['SnapshotId']}, Volume ID: {snapshot['VolumeId']}, Start Time: {snapshot['StartTime']}")
    ec2_client.delete_snapshot(SnapshotId=snapshot["SnapshotId"])
    print(f"Deleted snapshot {snapshot['SnapshotId']}")

import boto3

eks_client = boto3.client('eks', region_name="us-east-1")

clusters = eks_client.list_clusters()["clusters"]


for cluster in clusters:
    cluster_info = eks_client.describe_cluster(name=cluster)["cluster"]
    print(f"Cluster Name: {cluster_info['name']}")
    print(f"Cluster ARN: {cluster_info['arn']}")
    print(f"Cluster Version: {cluster_info['version']}")
    print(f"Cluster Endpoint: {cluster_info['endpoint']}")
    print(f"Cluster Status: {cluster_info['status']}")
    print("-" * 50)

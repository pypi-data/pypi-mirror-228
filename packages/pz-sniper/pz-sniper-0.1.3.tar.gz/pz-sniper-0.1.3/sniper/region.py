# List all regions

from botocore.client import ClientError
import boto3
import sniper.aws as aws

def all(region):
    ec2_client = boto3.client('ec2', region_name=region)
    regions = [region['RegionName'] for region in ec2_client.describe_regions()['Regions']]
    for region in regions:
        print(region)

def get_available(service_name="ec2"):
    sess = aws.session()        
    return sess.get_available_regions(service_name)

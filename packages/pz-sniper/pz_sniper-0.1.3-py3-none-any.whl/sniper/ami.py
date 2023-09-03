# work with AWS AMIs

from botocore.client import ClientError
import boto3

def describe(id, region):
    conn = boto3.client(service_name="ec2", region_name=region)
    response = conn.describe_images(
        ImageIds=[id]
    )
    if len(response['Images']):
        return response['Images'][0]
    else:
        raise Exception("There is no AMI with id " + id)

def has_deleteme_tag(info):
    has_tag = False
    if "Tags" in info:
        for tag in info['Tags']:
            if tag['Key'] == "deleteme" and tag['Value'] == "yes":
                has_tag = True
    return has_tag

def deregister(id, dryrun, region):
    try:
        conn = boto3.client(service_name="ec2", region_name=region)
        conn.deregister_image(
            ImageId=id,
            DryRun=dryrun
        )
    except ClientError as ce:
        print(ce.response['Error']['Message'])
        pass
    except Exception as e:
        print(e)
        raise
    

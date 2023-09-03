# work with AWS AMIs

from botocore.client import ClientError
import boto3

def describe(id, region):
    conn = boto3.client(service_name="ec2", region_name=region)
    response = conn.describe_instances(
        InstanceIds=[id]
    )

    if len(response['Reservations'][0]['Instances']):
        return response['Reservations'][0]['Instances'][0]
    else:
        raise Exception("There is no Instance with id " + id)


def has_deleteme_tag(info):
    has_tag = False
    if "Tags" in info:
        for tag in info['Tags']:
            if tag['Key'] == "deleteme" and tag['Value'] == "yes":
                has_tag = True
    return has_tag

def terminate(id, dryrun, region):
    try:
        conn = boto3.client(service_name="ec2", region_name=region)
        conn.terminate_instances(
            InstanceIds=[id],
            DryRun=dryrun
        )
    except ClientError as ce:
        print(ce.response['Error']['Message'])
        pass
    except Exception as e:
        print(e)
        raise
    

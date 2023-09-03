from botocore.client import ClientError
import boto3
import sniper.aws as aws

def all_tagged():
    sess = aws.session()
    client = sess.client('resourcegroupstaggingapi', region_name="ca-central-1")
    response = client.get_resources(
        TagFilters=[
            {
                'Key': 'version',
            },
        ],
        ResourcesPerPage=100,
        IncludeComplianceDetails=True,
        ExcludeCompliantResources=True,
    )


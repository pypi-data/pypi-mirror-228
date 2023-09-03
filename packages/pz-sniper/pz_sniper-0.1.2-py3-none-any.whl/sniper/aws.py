import boto3

# @todo: implement connection pooling

def session():
    #   this is wrapped to provide future compatibility
    return boto3.Session()

import json
import boto3
import os

def lambda_handler(event, context):

    # Specify tagname and tagvalue in lambda as environment variables
    stop_instances_by_tag(os.environ['tagname'], os.environ['tagvalue'])


def stop_instances_by_tag(tagkey, tagvalue):

    ec2client = boto3.client('ec2')

    response = ec2client.describe_instances(
        Filters=[
            {
                'Name': 'tag:' + tagkey,
                'Values': [tagvalue]
            }
        ]
    )

    for reservation in (response["Reservations"]):

        for instance in reservation["Instances"]:
            
            try:
                print('Stopping instance : ' + instance['InstanceId'])

                # Stop the instance
                instance.stop()
                
                print('Instance stopped : ' + instance['InstanceId'])

            except UnauthorizedOperation:
                print('Lambda function\'s IAM roles does not have permissions to stop an EC2 instance')
    
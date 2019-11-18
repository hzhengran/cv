# python bake_ami.py --image_id=ami-0e577943ae94381c9

# %%
import time
import json
import boto3
import argparse

parser = argparse.ArgumentParser(description='store sensitive data to vsts')
parser.add_argument('--image_id', type=str, default='')
parser.add_argument('--aws_access_key_id', type=str,
                    default='')
parser.add_argument('--aws_secret_access_key', type=str,
                    default='')
args = parser.parse_args()

IMAGEID = args.image_id
AWS_ACCESS_KEY_ID = args.aws_access_key_id
AWS_SECRET_ACCESS_KEY = args.aws_secret_access_key

print(IMAGEID)
# %%
ec2 = boto3.client('ec2', region_name='ap-southeast-1',
                   aws_access_key_id=AWS_ACCESS_KEY_ID,
                   aws_secret_access_key=AWS_SECRET_ACCESS_KEY)


# %% check if a ami exists
response = ec2.describe_images(
    Filters=[
        {
            'Name': 'name',
            'Values': [
                'baked_'+IMAGEID,
            ]
        }
    ]
)
if len(response['Images']) > 0:
    print('ami has already been baked!')
    exit(0)

# %%

response = ec2.run_instances(
    ImageId=IMAGEID,
    BlockDeviceMappings=[
        {
            'DeviceName': '/dev/xvda',
            'Ebs': {
                'VolumeSize': 80,
                'VolumeType': 'gp2'
            }
        },
    ],
    InstanceType='t2.large',
    MinCount=1,
    MaxCount=1,
    SubnetId='subnet-03dafe4a903bf77f3',
    SecurityGroupIds=['sg-03d294231c1b99316']
)
print(response)
# %%
InstanceId = response['Instances'][0]['InstanceId']

# %% wait for instance is ok
is_running = False
while not is_running:
    print('waiting instance state...')
    time.sleep(5)
    response = ec2.describe_instance_status(
        InstanceIds=[InstanceId]
    )
    if len(response['InstanceStatuses']) > 0:
        is_running = response['InstanceStatuses'][0]['InstanceState']['Name'] == 'running'
# %%
response = ec2.create_image(
    BlockDeviceMappings=[
        {
            'DeviceName': '/dev/xvda',
            'Ebs': {
                'VolumeSize': 80,
                'VolumeType': 'gp2'
            }
        },
    ],
    Description='bake ami for damo',
    InstanceId=InstanceId,
    Name='baked_'+IMAGEID,
    NoReboot=True
)
baked_image_id = response['ImageId']
print(baked_image_id)
# %% wait for baked_image is ok
is_available = False
while not is_available:
    print('wait image state ...')
    time.sleep(5)
    response = ec2.describe_images(
        ImageIds=[baked_image_id]
    )
    if len(response['Images']) > 0:
        is_available = response['Images'][0]['State'] == 'available'

print('image is available.')

# %% terminate_instances
response = ec2.terminate_instances(
    InstanceIds=[InstanceId]
)
print('instance is terminated.')

# %% modify image attribute
response = ec2.modify_image_attribute(
    ImageId=baked_image_id,
    LaunchPermission={
        'Add': [
            {
                'UserId': '378296562282'
            },
            {
                'UserId': '048246220138'
            },
            {
                'UserId': '448652512011'
            },
            {
                'UserId': '476985428237'
            },
            {
                'UserId': '206710830665'
            },
        ]
    }
)
print('baked image is permitted.')
# %% copy image to singapore
ec2 = boto3.client('ec2', region_name='ap-southeast-1',
                   aws_access_key_id=AWS_ACCESS_KEY_ID,
                   aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

response = ec2.copy_image(
    Name='baked_'+IMAGEID,
    SourceImageId=baked_image_id,
    SourceRegion='us-east-1'
)
copied_image_id = response['ImageId']
print(copied_image_id)
# %% wait for copied_image is ok
is_available = False
while not is_available:
    print('wait copied image state ...')
    time.sleep(5)
    response = ec2.describe_images(
        ImageIds=[copied_image_id]
    )
    if len(response['Images']) > 0:
        is_available = response['Images'][0]['State'] == 'available'

print('copied image is available.')

# %% copied image permutation
response = ec2.modify_image_attribute(
    ImageId=copied_image_id,
    LaunchPermission={
        'Add': [
            {
                'UserId': '378296562282'
            },
            {
                'UserId': '048246220138'
            },
            {
                'UserId': '448652512011'
            },
            {
                'UserId': '476985428237'
            },
            {
                'UserId': '206710830665'
            },
        ]
    }
)
print('copied image is permitted.')

# python bake_ami.py --image_id=ami-0e577943ae94381c9
# ssh -i "C:\Users\wangt2\pems\cert.pem" ec2-user@10.181.160.217
# %%
import time
import json
import boto3
import argparse
from const import tags, Tags

parser = argparse.ArgumentParser(description='store sensitive data to vsts')
parser.add_argument('--image_id', type=str, default='')
parser.add_argument('--aws_access_key_id', type=str,
                    default='')
parser.add_argument('--aws_secret_access_key', type=str,
                    default='')
parser.add_argument('--env', type=str, default='dev')
parser.add_argument('--keypair', type=str, default='dmo_api')
args = parser.parse_args()

IMAGEID = args.image_id
AWS_ACCESS_KEY_ID = args.aws_access_key_id
AWS_SECRET_ACCESS_KEY = args.aws_secret_access_key
ENV = args.env
KEYPAIR = args.keypair
PROJECT_NAME = 'HistoryRetriever'

print('starting: ', ENV)

if ENV in ['dev', 'cert']:
    ACCOUNT_NUM = '476985428237'
    SECURITY_GROUPS = [
        'sg-03d294231c1b99316', 'sg-0a0cab2883f265885'
    ]
    SUBNETS = 'subnet-03dafe4a903bf77f3,subnet-09d9e4fc315254db0'
    REGION_NAME = 'ap-southeast-1'
else:  # if ENV in ['reg', 'prod']:
    ACCOUNT_NUM = '206710830665'
    SECURITY_GROUPS = [
        'sg-073570b817287fac4', 'sg-0fd573d70503a5b8b'
    ]
    SUBNETS = 'subnet-0b0a66b5da5157ed9,subnet-056a9da3e0fb617bc'
    REGION_NAME = 'us-east-1'

Tags.append({
    'Key': 'Name',
    'Value': PROJECT_NAME+'_'+ENV+'_autoscaling'
})

Tags.append({
    'Key': 'AssetGroup',
    'Value': PROJECT_NAME+'_'+ENV+'_autoscaling'
})

# %% check if an autoscaling group exists
print('check if a launch configuration exists')
autoscaling = boto3.client('autoscaling', region_name=REGION_NAME,
                           aws_access_key_id=AWS_ACCESS_KEY_ID,
                           aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

response = autoscaling.describe_launch_configurations(
    LaunchConfigurationNames=[
        PROJECT_NAME+'_'+ENV+'_autoscaling_config_'+IMAGEID,
    ]
)
print(response)
if len(response['LaunchConfigurations']) > 0:
    print(PROJECT_NAME+'_'+ENV+'_autoscaling_config_'+IMAGEID, 'has been in place.')
    exit(0)

# %% check if an ami exists before create
print('check if an ami exists before create')
ec2 = boto3.client('ec2', region_name=REGION_NAME,
                   aws_access_key_id=AWS_ACCESS_KEY_ID,
                   aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
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
if len(response['Images']) == 0:
    print('ami has not already been baked!')
    exit(1)
baked_image_id = response['Images'][0]['ImageId']
print(response)


# %% create cluster
# print('create cluster')
# ecs = boto3.client('ecs', region_name=REGION_NAME)

# response = ecs.create_cluster(
#     clusterName=PROJECT_NAME+'-cluster-'+ENV,
#     tags=tags
# )
# print(response)

# %% create launch configurations
print('create launch configurations')
response = autoscaling.create_launch_configuration(
    LaunchConfigurationName=PROJECT_NAME+'_'+ENV+'_autoscaling_config_'+IMAGEID,
    ImageId=baked_image_id,
    InstanceType='m5.xlarge',
    IamInstanceProfile='arn:aws:iam::'+ACCOUNT_NUM +':instance-profile/ecsInstanceRole',
    KeyName=KEYPAIR,
    SecurityGroups=SECURITY_GROUPS,
    UserData='''
#!/bin/sh    
# Temporarily change umask
umask 0022

# Install ecs agent
mkdir -p /etc/ecs
touch /etc/ecs/ecs.config
echo ECS_CLUSTER=HistoryRetriever-cluster-'''+ENV +
    ''' >> /etc/ecs/ecs.config
echo ECS_BACKEND_HOST= >> /etc/ecs/ecs.config
amazon-linux-extras disable docker    
amazon-linux-extras install -y ecs    
systemctl enable --now --no-block ecs

# Install/configure required packages
yum install -y awslogs
chkconfig awslogs on
# Add CloudWatch Logs Agent config for secure, ossec, cloud-init
cat << EOF >> /etc/awslogs/awslogs.conf

[/var/log/secure]
datetime_format = %b %d %H:%M:%S
file = /var/log/secure
buffer_duration = 5000
log_stream_name = {instance_id}
initial_position = start_of_file
log_group_name = /var/log/secure

[/var/ossec/logs/alerts/alerts.json]
file = /var/ossec/logs/alerts/alerts.json
buffer_duration = 5000
log_stream_name = {instance_id}
initial_position = start_of_file
mode: "000644"
owner: "root"
group: "root"
log_group_name = /var/ossec/logs/alerts/alerts.json

[/var/log/cloud-init-output.log]
datetime_format = %b %d %H:%M:%S
file = /var/log/cloud-init-output.log
buffer_duration = 5000
log_stream_name = {instance_id}
initial_position = start_of_file
log_group_name = /var/log/cloud-init-output.log

EOF

# Modify default region in /etc/awslogs/awscli.conf 
sed -i 's/us-east-1/ap-southeast-1/g' /etc/awslogs/awscli.conf

# Install and configure ossec
aws s3 --region ap-southeast-1 cp s3://damo-ai-data/app/ossec-wazuh-local-binary-installation.tar.gz /tmp/ossec-wazuh-local-binary-installation.tar.gz
cd /tmp/
tar -xzvf ossec-wazuh-local-binary-installation.tar.gz 
/tmp/ossec-wazuh/install.sh 
/bin/cp -f /tmp/ossec-wazuh/ossec.conf /var/ossec/etc/ossec.conf
rm -rf /tmp/ossec-wazuh*

# Install SNOW Client 
aws s3 --region ap-southeast-1 cp s3://damo-ai-data/app/xClientSIOS-1.9.02-1-external.x86_64.rpm /tmp/xClientSIOS-1.9.02-1-external.x86_64.rpm
rpm -ivh /tmp/xClientSIOS-1.9.02-1-external.x86_64.rpm
rm -rf /tmp/xClientSIOS-1.9.02-1-external.x86_64.rpm

# Install and activate the Qualys Vulnerability Agent
aws s3 --region ap-southeast-1 cp s3://damo-ai-data/app/qualys-cloud-agent.rpm /opt/qualys/qualys-cloud-agent.rpm
rpm -ivh /opt/qualys/qualys-cloud-agent.rpm
/usr/local/qualys/cloud-agent/bin/qualys-cloud-agent.sh CustomerId=564896bd-efd2-6cde-8182-82e5936636d1 ActivationId=a0734882-b79c-4620-a3bd-85e49ba6a5a7

# Install latest available patches for Amazon Linux
sudo yum update -y

shutdown -r now
    ''',

    # sudo docker pull amazon/amazon-ecs-agent:latest
    # sudo systemctl restart docker
    BlockDeviceMappings=[
        {
            'DeviceName': '/dev/xvda',
            'Ebs': {
                'VolumeSize': 200,
                'VolumeType': 'gp2'
            }
        },
    ],
    InstanceMonitoring={
        'Enabled': True
    },
    AssociatePublicIpAddress=False
)
print(response)

# %% create an autoscaling group
print('create/update an autoscaling group')
response = autoscaling.describe_auto_scaling_groups(
    AutoScalingGroupNames=[
        'HistoryRetriever_'+ENV+'_autoscaling_group',
    ]
)
print(response)
if len(response['AutoScalingGroups']) > 0:
    response = autoscaling.update_auto_scaling_group(
        AutoScalingGroupName='HistoryRetriever_'+ENV+'_autoscaling_group',
        LaunchConfigurationName='HistoryRetriever_'+ENV+'_autoscaling_config_'+IMAGEID
    )
    print(response)
    print('HistoryRetriever_'+ENV+'_autoscaling_group', 'has been update.')
else:
    response = autoscaling.create_auto_scaling_group(
        AutoScalingGroupName='HistoryRetriever_'+ENV+'_autoscaling_group',
        LaunchConfigurationName='HistoryRetriever_'+ENV+'_autoscaling_config_'+IMAGEID,
        HealthCheckType='EC2',
        MinSize=1,
        MaxSize=1,
        VPCZoneIdentifier=SUBNETS,
        Tags=Tags
    )
    print(response)
    print('HistoryRetriever_'+ENV+'_autoscaling_group', 'has been create.')

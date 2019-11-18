# %% 引入ecs
import boto3
import sys
from const import tags, Tags
import argparse

parser = argparse.ArgumentParser(description='store sensitive data to vsts')
parser.add_argument('--image_tag', type=str, default='')
parser.add_argument('--aws_access_key_id', type=str,
                    default='')
parser.add_argument('--aws_secret_access_key', type=str,
                    default='')
parser.add_argument('--env', type=str, default='dev')
parser.add_argument('--x_api_key', type=str, default='')
parser.add_argument('--mysql_pwd', type=str, default='')
args = parser.parse_args()

IMAGE_TAG = args.image_tag
AWS_ACCESS_KEY_ID = args.aws_access_key_id
AWS_SECRET_ACCESS_KEY = args.aws_secret_access_key
X_API_KEY = args.x_api_key
MYSQL_PWD = args.mysql_pwd
ENV = args.env
PROJECT_NAME = 'HistoryRetriever'

if ENV in ['dev', 'cert']:
    ACCOUNT_NUM = '476985428237'
    SECURITY_GROUPS = [
        'sg-03d294231c1b99316', 'sg-0a0cab2883f265885'
    ]
    SUBNETS = ['subnet-03dafe4a903bf77f3', 'subnet-09d9e4fc315254db0']
    REGION = 'ap-southeast-1'
else:  # if ENV in ['reg', 'prod']:
    ACCOUNT_NUM = '206710830665'
    SECURITY_GROUPS = [
        'sg-073570b817287fac4', 'sg-0fd573d70503a5b8b'
    ]
    SUBNETS = ['subnet-0b0a66b5da5157ed9', 'subnet-056a9da3e0fb617bc']
    REGION = 'us-east-1'

client = boto3.client('ecs', region_name=REGION, aws_access_key_id=AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY)


response = client.register_task_definition(
    family=PROJECT_NAME+'_task_'+ENV,
    taskRoleArn='arn:aws:iam::'+ACCOUNT_NUM+':role/ecsTaskExecutionRole',
    executionRoleArn='arn:aws:iam::'+ACCOUNT_NUM+':role/ecsTaskExecutionRole',
    networkMode='awsvpc',
    containerDefinitions=[
        {
            'name': PROJECT_NAME,
            'image': ACCOUNT_NUM+'.dkr.ecr.'+REGION+'.amazonaws.com/history_retriever:'+IMAGE_TAG,
            'cpu': 4000,
            'memory': 15000,
            'essential': True,
            'logConfiguration': {
                'logDriver': 'awslogs',
                'options': {
                    "awslogs-group": PROJECT_NAME+"_systemLog",
                    "awslogs-region": REGION,
                    "awslogs-stream-prefix": "syslog"
                },
            },
            'environment': [
                {
                    'name': 'env',
                    'value': ENV
                },
                {
                    'name': 'data_lake_x_api_key',
                    'value': X_API_KEY
                },
                {
                    'name': 'mysql_pwd',
                    'value': MYSQL_PWD
                }
            ],
            # 'healthCheck': {
            #     'command': [
            #         'CMD-SHELL', 'python3 -m healthcheck'
            #     ],
            #     'interval': 60,
            #     'timeout': 20,
            #     'retries': 10,
            #     'startPeriod': 60
            # },
        },
    ],
    requiresCompatibilities=['EC2'],
    cpu='4000',
    memory='15000',
    tags=tags
)
taskDefinitionArn = response['taskDefinition']['taskDefinitionArn']
print('task definition success!')
# %%
# taskDefinitionArn='arn:aws:ecs:ap-southeast-1:476985428237:task-definition/HistoryRetriever_task_dev:5'
try:
    response = client.update_service(
        cluster=PROJECT_NAME+'-cluster-'+ENV,
        service=PROJECT_NAME+'-service-'+ENV,
        taskDefinition=taskDefinitionArn,
        forceNewDeployment=True
    )
    print('send service update success!')
except:
    response = client.create_service(
        cluster=PROJECT_NAME+'-cluster-'+ENV,
        serviceName=PROJECT_NAME+'-service-'+ENV,
        launchType='EC2',
        taskDefinition=taskDefinitionArn,
        deploymentConfiguration={
            'maximumPercent': 100,
            'minimumHealthyPercent': 0
        },
        networkConfiguration={
            'awsvpcConfiguration': {
                'subnets': SUBNETS,
                'securityGroups': SECURITY_GROUPS,
                'assignPublicIp': 'DISABLED'
            }
        },
        schedulingStrategy='DAEMON',
        deploymentController={
            'type': 'ECS'
        },
        tags=tags,
        enableECSManagedTags=True,
        propagateTags='SERVICE'
    )
    response
    print('send service create success!')

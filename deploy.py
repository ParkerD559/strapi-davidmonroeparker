import boto3, base64, getpass, os
import docker as dkr
from pprint import pprint
from fabric import Connection


ECR_REGISTRY = '227682119925.dkr.ecr.us-west-1.amazonaws.com'
ECR_REPO = 'davidmonroeparker-cms'
COMPOSE_FILES = ['docker-compose.yml', 'production.yml']
EC2_INSTANCE = 'ec2-13-57-116-50.us-west-1.compute.amazonaws.com'


def main():
    push_container()
    pull_ec2()


def push_container():
    print('Connecting to docker daemon...')
    docker = dkr.from_env()
    repo = '{}/{}'.format(ECR_REGISTRY, ECR_REPO)

    print('Building image...')
    image, _ = docker.images.build(path='.', tag=repo)
    image.tag(repo, tag='latest')

    print('Getting ECR credentials...')
    username, password = ecr_creds()
    docker.login(username, password, registry=ECR_REGISTRY)

    print('Pushing to ECR...')
    for progress in docker.images.push(repo, tag='latest', stream=True):
        print(progress)


def ecr_creds():
    ecr = boto3.client('ecr', region_name='us-west-1')
    token = ecr.get_authorization_token()

    username, password = base64.b64decode(
        token['authorizationData'][0]['authorizationToken']
    ).decode().split(':')

    return username, password


def pull_ec2():
    print('Connecting to EC2 instance...')
    instance = Connection(EC2_INSTANCE, 'ec2-user', connect_kwargs={'key_filename':'{}/.ssh/id_rsa'.format(os.path.expanduser('~'))})

    print('Uploading compose files...')
    instance.run('mkdir -p app')
    for filename in COMPOSE_FILES:
        instance.put(filename, remote='app/')

    print('Logging into ECR from EC2 instance...')
    instance.run('$(aws ecr get-login --region us-west-1 --no-include-email)')
    
    print('Running compose files...')
    instance.run('cd app && docker-compose -f docker-compose.yml -f production.yml pull && docker-compose -f docker-compose.yml -f production.yml up -d cms')


if __name__ == "__main__":
    main()

import json
import boto3
import time

def lambda_handler(event, context):
    ecs_client = boto3.client('ecs', region_name='us-east-2')
    ec2_client = boto3.client('ec2', region_name='us-east-2')

    try:
        # Inicia a tarefa no ECS
        response = ecs_client.run_task(
            cluster='app02-cluster',
            launchType='FARGATE',
            taskDefinition='app02-task',
            networkConfiguration={
                'awsvpcConfiguration': {
                    'subnets': ['subnet-0b84a1df108406161'],
                    'securityGroups': ['sg-0ea44ad11c3486257'],
                    'assignPublicIp': 'ENABLED'
                }
            }
        )

        # Obtém o ARN da tarefa iniciada
        task_arn = response['tasks'][0]['taskArn']

        # Espera até que a tarefa esteja em execução para obter o IP
        time.sleep(7)  # Aguardando a tarefa iniciar  ***!!!**! AUMENTAR DO LAMBDA TAMBEM !!!****!!!!

        describe_response = ecs_client.describe_tasks(cluster='app02-cluster', tasks=[task_arn])
        eni_id = describe_response['tasks'][0]['attachments'][0]['details'][1]['value']

        eni_description = ec2_client.describe_network_interfaces(NetworkInterfaceIds=[eni_id])
        public_ip = eni_description['NetworkInterfaces'][0]['Association']['PublicIp']

        # Retornando o ARN da tarefa e o IP público
        return {
            'statusCode': 200,
            'taskArn': task_arn,
            'publicIp': public_ip
        }

    except Exception as e:
        # Se ocorrer algum erro, o erro será retornado na resposta
        return {
            'statusCode': 500,
            'error': str(e)
        }

import json
import boto3

def lambda_handler(event, context):
    client = boto3.client('ecs', region_name='us-east-2')
    
    # Listar todas as tasks em execução no cluster
    response = client.list_tasks(
        cluster='app02-cluster',
        desiredStatus='RUNNING'
    )
    
    # Se houver tasks em execução, pare todas
    if response['taskArns']:
        for task in response['taskArns']:
            client.stop_task(
                cluster='app02-cluster',
                task=task,
                reason='Encerrando tasks via Lambda'
            )
    
    return {
        'statusCode': 200,
        'body': json.dumps('Todas as tasks foram encerradas.')
    }

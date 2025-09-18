import json
import boto3
from datetime import datetime
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('CapivaraTemperaturas')

def lambda_handler(event, context):
    """
    Função Lambda para receber dados do sensor e salvar no DynamoDB
    """
    try:
        # Parse do body se vier do API Gateway
        if 'body' in event:
            body = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
        else:
            body = event
        
        # Validação dos campos obrigatórios
        required_fields = ['device_id', 'timestamp', 'temperature']
        for field in required_fields:
            if field not in body:
                return {
                    'statusCode': 400,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps({'error': f'Campo obrigatório ausente: {field}'})
                }
        
        # Preparar item para DynamoDB
        item = {
            'device_id': body['device_id'],
            'timestamp': body['timestamp'],
            'temperature': float(body['temperature']),
            'created_at': datetime.utcnow().isoformat()
        }
        
        # Salvar no DynamoDB
        table.put_item(Item=item)
        
        logger.info(f"Dados salvos: {item}")
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'message': 'Dados salvos com sucesso',
                'device_id': item['device_id'],
                'timestamp': item['timestamp']
            })
        }
        
    except Exception as e:
        logger.error(f"Erro ao processar dados: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': 'Erro interno do servidor'})
        }

def mock_handler(event):
    """Versão mock para testes locais"""
    print(f"[MOCK LAMBDA] Recebido: {json.dumps(event, indent=2)}")
    
    # Simula salvamento no DynamoDB
    item = {
        'device_id': event['device_id'],
        'timestamp': event['timestamp'],
        'temperature': event['temperature'],
        'created_at': datetime.utcnow().isoformat()
    }
    
    print(f"[MOCK DYNAMODB] Item salvo: {json.dumps(item, indent=2)}")
    
    return {
        'statusCode': 200,
        'body': {'message': 'Dados salvos com sucesso (mock)'}
    }
import unittest
import sys
import os
import json
from unittest.mock import patch, MagicMock

# Adicionar lambda ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lambda'))
from lambda_function import lambda_handler, mock_handler

class TestLambdaFunction(unittest.TestCase):
    
    def setUp(self):
        """Setup para cada teste"""
        self.valid_payload = {
            "device_id": "capivara-test-001",
            "timestamp": "2024-01-15T14:30:25.123456",
            "temperature": 27.5
        }
    
    def test_mock_handler(self):
        """Testa função mock do Lambda"""
        result = mock_handler(self.valid_payload)
        
        self.assertEqual(result['statusCode'], 200)
        self.assertIn('message', result['body'])
    
    @patch('boto3.resource')
    def test_lambda_handler_success(self, mock_boto3):
        """Testa Lambda handler com sucesso"""
        # Mock do DynamoDB
        mock_table = MagicMock()
        mock_dynamodb = MagicMock()
        mock_dynamodb.Table.return_value = mock_table
        mock_boto3.return_value = mock_dynamodb
        
        # Event do API Gateway
        event = {
            'body': json.dumps(self.valid_payload)
        }
        context = {}
        
        result = lambda_handler(event, context)
        
        self.assertEqual(result['statusCode'], 200)
        mock_table.put_item.assert_called_once()
    
    @patch('boto3.resource')
    def test_lambda_handler_missing_field(self, mock_boto3):
        """Testa Lambda handler com campo faltando"""
        invalid_payload = {
            "device_id": "capivara-test-001",
            "timestamp": "2024-01-15T14:30:25.123456"
            # temperature ausente
        }
        
        event = {
            'body': json.dumps(invalid_payload)
        }
        context = {}
        
        result = lambda_handler(event, context)
        
        self.assertEqual(result['statusCode'], 400)
        self.assertIn('error', json.loads(result['body']))

if __name__ == '__main__':
    unittest.main()
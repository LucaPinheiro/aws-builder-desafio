import unittest
import sys
import os
from unittest.mock import patch, MagicMock
from datetime import datetime
import json

# Adicionar src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from sensor import CapivaraSensor

class TestCapivaraSensor(unittest.TestCase):
    
    def setUp(self):
        """Setup para cada teste"""
        self.sensor = CapivaraSensor(device_id="test-device-001")
    
    def test_sensor_initialization(self):
        """Testa inicialização do sensor"""
        self.assertEqual(self.sensor.device_id, "test-device-001")
        self.assertTrue(self.sensor.mock_mode)
        self.assertIsNotNone(self.sensor.api_url)
    
    def test_temperature_reading(self):
        """Testa leitura de temperatura"""
        temp = self.sensor.read_temperature()
        self.assertIsInstance(temp, float)
        self.assertGreaterEqual(temp, 15.0)  # Min esperado: 25-10
        self.assertLessEqual(temp, 40.0)     # Max esperado: 25+15
    
    def test_payload_creation(self):
        """Testa criação do payload JSON"""
        payload = self.sensor.create_payload()
        
        # Verificar campos obrigatórios
        self.assertIn('device_id', payload)
        self.assertIn('timestamp', payload)
        self.assertIn('temperature', payload)
        
        # Verificar tipos
        self.assertEqual(payload['device_id'], "test-device-001")
        self.assertIsInstance(payload['temperature'], float)
        
        # Verificar formato do timestamp
        timestamp = datetime.fromisoformat(payload['timestamp'])
        self.assertIsInstance(timestamp, datetime)
    
    def test_mock_send_data(self):
        """Testa envio de dados em modo mock"""
        payload = {"device_id": "test", "temperature": 25.0, "timestamp": "2024-01-01T00:00:00"}
        result = self.sensor.send_data(payload)
        
        self.assertEqual(result['status'], 'success')
        self.assertTrue(result['mock'])

if __name__ == '__main__':
    unittest.main()
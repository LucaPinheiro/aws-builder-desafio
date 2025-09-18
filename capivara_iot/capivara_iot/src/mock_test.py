#!/usr/bin/env python3
"""
Teste local completo do sistema Capivara IoT usando mocks
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sensor import CapivaraSensor
import json
from datetime import datetime

# Importar função Lambda mock
sys.path.append('../lambda')
from lambda_function import mock_handler

class MockIoTSystem:
    def __init__(self):
        self.sensor = CapivaraSensor(device_id="capivara-test-001")
        self.mock_database = []
    
    def simulate_full_flow(self, readings=3):
        """Simula fluxo completo: sensor -> lambda -> dynamodb"""
        print("=== SIMULAÇÃO CAPIVARA IoT ===\n")
        
        for i in range(readings):
            print(f"--- Leitura {i+1}/{readings} ---")
            
            # 1. Sensor gera dados
            payload = self.sensor.create_payload()
            print(f"Sensor: {json.dumps(payload, indent=2)}")
            
            # 2. Lambda processa dados
            lambda_result = mock_handler(payload)
            print(f"Lambda: {lambda_result}")
            
            # 3. Simula salvamento no DynamoDB
            db_item = {
                **payload,
                'created_at': datetime.utcnow().isoformat(),
                'ttl': int(datetime.utcnow().timestamp()) + (30 * 24 * 60 * 60)  # 30 dias
            }
            self.mock_database.append(db_item)
            
            print(f"DynamoDB Item: {json.dumps(db_item, indent=2)}")
            print("-" * 50)
        
        self.show_database_summary()
    
    def show_database_summary(self):
        """Mostra resumo dos dados salvos"""
        print("\n=== RESUMO DO BANCO DE DADOS ===")
        print(f"Total de registros: {len(self.mock_database)}")
        
        if self.mock_database:
            temps = [item['temperature'] for item in self.mock_database]
            print(f"Temperatura média: {sum(temps)/len(temps):.2f}°C")
            print(f"Temperatura mín/máx: {min(temps):.2f}°C / {max(temps):.2f}°C")
            
            print("\nÚltimos registros:")
            for item in self.mock_database[-3:]:
                print(f"  {item['timestamp']}: {item['temperature']}°C")

if __name__ == "__main__":
    system = MockIoTSystem()
    system.simulate_full_flow(readings=5)
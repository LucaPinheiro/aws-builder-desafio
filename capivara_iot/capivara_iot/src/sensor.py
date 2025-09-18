import json
import time
import random
import requests
from datetime import datetime
import uuid
from mcp_client import weather_client, device_registry

class CapivaraSensor:
    def __init__(self, device_id=None, api_url=None, location="São Paulo"):
        self.device_id = device_id or f"capivara-{uuid.uuid4().hex[:8]}"
        self.api_url = api_url or "https://your-api-gateway-url.amazonaws.com/prod/temperature"
        self.mock_mode = api_url is None
        self.location = location
        
        # Registrar dispositivo via MCP
        device_registry.register_device(self.device_id, location)
        
    def read_temperature(self):
        """Simula leitura de sensor com calibração MCP"""
        base_temp = 25.0
        variation = random.uniform(-5.0, 10.0)
        raw_temp = round(base_temp + variation, 2)
        
        # Obter contexto meteorológico via MCP
        weather_context = weather_client.get_weather_context(self.location)
        
        # Calibrar temperatura com dados MCP
        calibration = weather_client.calibrate_sensor(raw_temp, weather_context)
        
        return calibration["calibrated_temperature"]
    
    def create_payload(self):
        """Cria payload JSON para envio"""
        return {
            "device_id": self.device_id,
            "timestamp": datetime.utcnow().isoformat(),
            "temperature": self.read_temperature()
        }
    
    def send_data(self, payload):
        """Envia dados para API Gateway ou simula envio"""
        if self.mock_mode:
            print(f"[MOCK] Enviando: {json.dumps(payload, indent=2)}")
            return {"status": "success", "mock": True}
        
        try:
            response = requests.post(
                self.api_url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            response.raise_for_status()
            return {"status": "success", "response": response.json()}
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def run(self, interval=10, max_readings=None):
        """Executa loop principal do sensor"""
        print(f"Capivara IoT Sensor iniciado - Device ID: {self.device_id}")
        print(f"Localização: {self.location}")
        print(f"Modo: {'MOCK' if self.mock_mode else 'REAL'}")
        print(f"Intervalo: {interval}s")
        print(f"MCP Weather Service: Conectado")
        
        count = 0
        try:
            while True:
                payload = self.create_payload()
                result = self.send_data(payload)
                
                # Atualizar registro MCP
                device_registry.update_last_seen(self.device_id)
                
                print(f"[{datetime.now().strftime('%H:%M:%S')}] "
                      f"Temp: {payload['temperature']}°C - "
                      f"Status: {result['status']} - "
                      f"Device: {self.device_id}")
                
                count += 1
                if max_readings and count >= max_readings:
                    break
                    
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\nSensor interrompido pelo usuário")

if __name__ == "__main__":
    # Configuração para teste local (mock)
    sensor = CapivaraSensor()
    sensor.run(interval=10, max_readings=5)  # 5 leituras para teste
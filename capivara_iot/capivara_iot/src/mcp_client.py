"""
Cliente MCP (Model Context Protocol) para integração com serviços externos
Simula integração com servidor MCP para dados meteorológicos
"""
import json
import random
from datetime import datetime, timedelta

class MCPWeatherClient:
    """Cliente MCP simulado para dados meteorológicos"""
    
    def __init__(self):
        self.server_url = "mcp://weather-service"
        self.connected = True
        
    def get_weather_context(self, location="São Paulo"):
        """Obtém contexto meteorológico via MCP"""
        # Simula resposta de servidor MCP
        weather_data = {
            "location": location,
            "external_temperature": round(random.uniform(18.0, 32.0), 1),
            "humidity": random.randint(40, 90),
            "pressure": round(random.uniform(1010, 1025), 1),
            "timestamp": datetime.utcnow().isoformat(),
            "source": "mcp://weather-service"
        }
        
        return weather_data
    
    def calibrate_sensor(self, sensor_temp, weather_context):
        """Calibra leitura do sensor com dados meteorológicos"""
        external_temp = weather_context["external_temperature"]
        
        # Simula calibração baseada em temperatura externa
        if abs(sensor_temp - external_temp) > 10:
            # Sensor pode estar com problema
            calibrated_temp = (sensor_temp + external_temp) / 2
            confidence = 0.7
        else:
            calibrated_temp = sensor_temp
            confidence = 0.95
            
        return {
            "original_temperature": sensor_temp,
            "calibrated_temperature": round(calibrated_temp, 2),
            "confidence": confidence,
            "weather_context": weather_context
        }

class MCPDeviceRegistry:
    """Registro de dispositivos via MCP"""
    
    def __init__(self):
        self.devices = {}
        
    def register_device(self, device_id, location=None):
        """Registra dispositivo no servidor MCP"""
        device_info = {
            "device_id": device_id,
            "location": location or "Unknown",
            "registered_at": datetime.utcnow().isoformat(),
            "status": "active",
            "last_seen": datetime.utcnow().isoformat()
        }
        
        self.devices[device_id] = device_info
        return device_info
    
    def get_device_info(self, device_id):
        """Obtém informações do dispositivo"""
        return self.devices.get(device_id, None)
    
    def update_last_seen(self, device_id):
        """Atualiza último contato do dispositivo"""
        if device_id in self.devices:
            self.devices[device_id]["last_seen"] = datetime.utcnow().isoformat()

# Instâncias globais dos clientes MCP
weather_client = MCPWeatherClient()
device_registry = MCPDeviceRegistry()
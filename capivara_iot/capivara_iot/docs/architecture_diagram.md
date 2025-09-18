# Diagrama de Arquitetura - Capivara IoT

## Arquitetura do Sistema

```mermaid
graph TB
    subgraph "Capivara IoT Device"
        Sensor[Sensor de Temperatura<br/>Python Script]
        Mock[Mock Data Generator<br/>25°C ± 10°C]
    end
    
    subgraph "AWS Cloud"
        subgraph "API Layer"
            APIGW[API Gateway<br/>REST API<br/>/temperature POST]
        end
        
        subgraph "Compute Layer"
            Lambda[AWS Lambda<br/>Temperature Processor<br/>Python 3.9]
        end
        
        subgraph "Storage Layer"
            DDB[(DynamoDB<br/>CapivaraTemperaturas<br/>PK: device_id<br/>SK: timestamp)]
        end
        
        subgraph "Monitoring"
            CW[CloudWatch<br/>Logs & Metrics]
        end
    end
    
    %% Connections
    Sensor --> Mock
    Sensor -->|HTTP POST<br/>JSON Payload| APIGW
    APIGW -->|Event Trigger| Lambda
    Lambda -->|Put Item| DDB
    Lambda -->|Logs| CW
    APIGW -->|Access Logs| CW
    
    %% Styling
    classDef device fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    classDef aws fill:#ff9800,stroke:#e65100,stroke-width:2px
    classDef storage fill:#4caf50,stroke:#2e7d32,stroke-width:2px
    classDef monitoring fill:#9c27b0,stroke:#6a1b9a,stroke-width:2px
    
    class Sensor,Mock device
    class APIGW,Lambda aws
    class DDB storage
    class CW monitoring
```

## Fluxo de Dados

```mermaid
sequenceDiagram
    participant Device as Capivara Device
    participant API as API Gateway
    participant Lambda as Lambda Function
    participant DDB as DynamoDB
    participant CW as CloudWatch
    
    loop Every 10 seconds
        Device->>Device: Read Temperature
        Device->>Device: Create JSON Payload
        Device->>API: POST /temperature
        API->>Lambda: Trigger Function
        Lambda->>Lambda: Validate Data
        Lambda->>DDB: Put Item
        DDB-->>Lambda: Success Response
        Lambda->>CW: Log Event
        Lambda-->>API: 200 OK Response
        API-->>Device: Success Response
    end
    
    Note over Device,DDB: Payload: {device_id, timestamp, temperature}
```

## Estrutura de Dados

```mermaid
erDiagram
    CapivaraTemperaturas {
        string device_id PK "Partition Key"
        string timestamp SK "Sort Key"
        number temperature "Temperature in Celsius"
        string created_at "ISO timestamp"
        number ttl "Time to Live (30 days)"
    }
    
    Device ||--o{ CapivaraTemperaturas : sends
```

## Componentes AWS

| Componente | Tipo | Configuração |
|------------|------|--------------|
| API Gateway | REST API | CORS habilitado, POST /temperature |
| Lambda | Function | Python 3.9, 30s timeout, DynamoDB permissions |
| DynamoDB | Table | Pay-per-request, Stream habilitado |
| CloudWatch | Logs/Metrics | Retention 14 dias |

## Estimativa de Custos (Região us-east-1)

### Cenário: 1 dispositivo, 1 leitura/10s = 8.640 requests/dia

| Serviço | Uso Mensal | Custo Estimado |
|---------|------------|----------------|
| API Gateway | 259.200 requests | $0.26 |
| Lambda | 259.200 invocações, 128MB, 100ms avg | $0.05 |
| DynamoDB | 259.200 writes, 1KB avg | $0.32 |
| CloudWatch | Logs básicos | $0.10 |
| **Total** | | **~$0.73/mês** |

### Cenário: 100 dispositivos

| Serviço | Uso Mensal | Custo Estimado |
|---------|------------|----------------|
| API Gateway | 25.920.000 requests | $25.92 |
| Lambda | 25.920.000 invocações | $5.18 |
| DynamoDB | 25.920.000 writes | $32.40 |
| CloudWatch | Logs e métricas | $10.00 |
| **Total** | | **~$73.50/mês** |
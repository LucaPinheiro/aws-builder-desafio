# Capivara IoT 🦫

**Projeto gerado com Amazon Q Developer para o TDC 2025**

Projeto simples de IoT que simula sensores de temperatura enviando dados para AWS.

![Capivara IoT](https://via.placeholder.com/800x400/FF9800/FFFFFF?text=Capivara+IoT+Running)

## 🏷️ Tags
- `q-developer-quest-tdc-2025`
- `iot`
- `aws`
- `python`
- `serverless`

## Arquitetura

```
Sensor (Python) → API Gateway → Lambda → DynamoDB
```

## Estrutura do Projeto

```
capivara_iot/
├── src/
│   ├── sensor.py          # Sensor simulado
│   └── mock_test.py       # Teste local completo
├── lambda/
│   └── lambda_function.py # Função Lambda
├── infrastructure/
│   └── template.yaml      # Template SAM
├── docs/
│   └── dynamodb_example.json
└── requirements.txt
```

## Execução Local (Mock)

1. **Instalar dependências:**
```bash
pip install -r requirements.txt
```

2. **Teste completo do sistema:**
```bash
cd src
python mock_test.py
```

3. **Sensor individual:**
```bash
cd src
python sensor.py
```

## Deploy na AWS

1. **Pré-requisitos:**
   - AWS CLI configurado
   - SAM CLI instalado

2. **Deploy:**
```bash
cd infrastructure
sam build
sam deploy --guided
```

3. **Configurar sensor para produção:**
```python
# Usar URL real do API Gateway
sensor = CapivaraSensor(
    device_id="capivara-prod-001",
    api_url="https://your-api-id.execute-api.region.amazonaws.com/prod/temperature"
)
```

## Estrutura DynamoDB

**Tabela:** `CapivaraTemperaturas`
- **Partition Key:** `device_id` (String)
- **Sort Key:** `timestamp` (String)
- **Atributos:** `temperature` (Number), `created_at` (String)

## Exemplo de Payload

```json
{
  "device_id": "capivara-12345678",
  "timestamp": "2024-01-15T14:30:25.123456",
  "temperature": 27.5
}
```

## Funcionalidades

- ✅ Sensor simulado com temperaturas aleatórias
- ✅ Envio de dados via HTTP POST
- ✅ Função Lambda para processamento
- ✅ Armazenamento no DynamoDB
- ✅ Teste local completo com mocks
- ✅ Infraestrutura como código (SAM)
- ✅ Validação de dados
- ✅ Tratamento de erros

## 🧪 Testes

```bash
# Executar todos os testes
./run_tests.sh

# Testes unitários apenas
python -m pytest tests/ -v

# Coverage
python -m pytest tests/ --cov=src
```

## 🔗 Integração MCP

O projeto utiliza Model Context Protocol (MCP) para:
- Calibração de sensores com dados meteorológicos
- Registro de dispositivos
- Contexto ambiental

## 📊 Estimativa de Custos

### Cenário: 1 dispositivo (8.640 leituras/dia)
- **API Gateway**: $0.26/mês
- **Lambda**: $0.05/mês  
- **DynamoDB**: $0.32/mês
- **CloudWatch**: $0.10/mês
- **Total**: ~$0.73/mês

### Cenário: 100 dispositivos
- **Total**: ~$73.50/mês

*Preços baseados na região us-east-1*

## 📋 Prompts Utilizados

1. "Eu quero criar um projeto em python para um jogo tetries"
2. "crie um diagram de arquitetura em mermaid do projeto autual"
3. "dentro da pasta capivara iot quero que crie um projeto simples bem simples orem modular e organizado Crie um projeto simples de IoT chamado "Capivara IoT"..."
4. "valide se nosso projeto da capivara satisfaz todos requisitos"

## 🏗️ Arquitetura

Ver [diagrama completo](docs/architecture_diagram.md)

## 📁 Estrutura Completa

```
capivara_iot/
├── .amazonq/
│   └── rules/
│       └── project_rules.md
├── src/
│   ├── sensor.py
│   ├── mcp_client.py
│   └── mock_test.py
├── lambda/
│   └── lambda_function.py
├── infrastructure/
│   └── template.yaml
├── tests/
│   ├── test_sensor.py
│   └── test_lambda.py
├── docs/
│   ├── architecture_diagram.md
│   └── dynamodb_example.json
├── requirements.txt
├── run_local.sh
└── run_tests.sh
```

## 🎯 Funcionalidades Implementadas

- ✅ Sensor simulado com MCP
- ✅ API Gateway + Lambda + DynamoDB
- ✅ Testes automatizados
- ✅ Infraestrutura como código (SAM)
- ✅ Diagrama de arquitetura (Mermaid)
- ✅ Configuração Amazon Q Developer
- ✅ Estimativa de custos
- ✅ Integração MCP

## 🔍 Monitoramento

- CloudWatch Logs para Lambda
- CloudWatch Metrics para DynamoDB
- API Gateway access logs


# 💰 Estimativa de Custo - Projeto Capivara IoT

Esta estimativa considera o uso de serviços AWS com carga leve (ex: envio de dados a cada 10 segundos por um único dispositivo), ideal para testes, demonstrações e desenvolvimento.

---

## ☁️ Componentes da Infraestrutura

| Serviço         | Detalhes                                                  | Custo Estimado Mensal |
|-----------------|-----------------------------------------------------------|------------------------|
| **API Gateway** | REST API (HTTP calls de app.py para Lambda)               | ~US$ 1,00              |
| **AWS Lambda**  | Execução simples (<128 MB, <100ms), poucas mil invocações | ~US$ 0,00 - 0,20       |
| **DynamoDB**    | Armazenamento leve, baixa taxa de leitura/gravação        | ~US$ 0,50              |
| **Data Transfer** | Tráfego de saída desprezível (dentro da AWS)           | ~US$ 0,00              |

---

## 🧮 Total Estimado: **~US$ 1,50 - 2,00/mês**

> 💡 **Observações**:
>
> - Os serviços usados estão todos dentro do **AWS Free Tier**, se for novo usuário.
> - O custo real depende do volume de dados, frequência de chamadas e quantidade de dispositivos.
> - Para 1 dispositivo enviando dados a cada 10s, o volume mensal é bem pequeno:
>   - ~259k requisições/mês
>   - ~259k gravações no DynamoDB
>   - ~1

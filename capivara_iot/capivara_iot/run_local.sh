#!/bin/bash

echo "=== CAPIVARA IoT - TESTE LOCAL ==="
echo

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 não encontrado. Instale Python 3.7+"
    exit 1
fi

# Instalar dependências se necessário
if [ ! -d "venv" ]; then
    echo "📦 Criando ambiente virtual..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

echo "🚀 Executando teste completo do sistema..."
echo

cd src
python mock_test.py

echo
echo "✅ Teste concluído!"
echo "💡 Para executar o sensor contínuo: cd src && python sensor.py"
#!/bin/bash

echo "=== CAPIVARA IoT - EXECUTANDO TESTES ==="
echo

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 não encontrado"
    exit 1
fi

# Ativar ambiente virtual se existir
if [ -d "venv" ]; then
    source venv/bin/activate
fi

echo "🧪 Executando testes unitários..."
python3 -m pytest tests/ -v --tb=short

echo
echo "📊 Executando coverage..."
python3 -m pytest tests/ --cov=src --cov-report=term-missing

echo
echo "✅ Testes concluídos!"
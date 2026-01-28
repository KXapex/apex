#!/bin/bash
# Apex Operating System - Quick Start Guide

echo "🔐 Apex Operating System - Setup Script"
echo "========================================"

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado. Instale antes de continuar."
    exit 1
fi

echo "✓ Python encontrado"

# Instalar dependências
echo ""
echo "📦 Instalando dependências..."
pip install -q -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✓ Dependências instaladas com sucesso"
else
    echo "❌ Erro ao instalar dependências"
    exit 1
fi

# Menu de opções
echo ""
echo "Escolha uma opção:"
echo "1) Executar demonstração (demo.py)"
echo "2) Ver exemplos práticos (exemplos.py)"
echo "3) Iniciar servidor FastAPI"
echo "4) Informações do projeto (project_info.py)"
echo "5) Sair"
echo ""

read -p "Opção: " opcao

case $opcao in
    1)
        echo ""
        echo "🎬 Executando demonstração..."
        python demo.py
        ;;
    2)
        echo ""
        echo "📚 Executando exemplos..."
        python exemplos.py
        ;;
    3)
        echo ""
        echo "🚀 Iniciando servidor FastAPI..."
        echo "Servidor rodará em: http://localhost:8000"
        echo "Pressione CTRL+C para parar"
        echo ""
        python server.py
        ;;
    4)
        echo ""
        python project_info.py
        ;;
    5)
        echo "Saindo..."
        exit 0
        ;;
    *)
        echo "❌ Opção inválida"
        exit 1
        ;;
esac

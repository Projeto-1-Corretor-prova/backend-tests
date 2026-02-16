#!/bin/bash

# Script para verificar e listar todos os testes criados

echo "============================================"
echo "📊 TESTES DE API - SUMÁRIO"
echo "============================================"
echo ""

# Contar total de arquivos de teste
TEST_FILES=$(find tests/api -name "test_*.py" -type f | wc -l)
echo "📁 Arquivos de teste: $TEST_FILES"
echo ""

# Listar todos os arquivos de teste
echo "📋 Arquivos criados:"
find tests/api -name "test_*.py" -type f | sort | while read file; do
    # Contar testes no arquivo
    TEST_COUNT=$(grep -c "def test_" "$file" 2>/dev/null || echo 0)
    # Extrair nome da classe
    CLASS=$(grep "^class Test" "$file" | head -1 | sed 's/class \(.*\)(.*/\1/')
    # Extrair endpoin com format melhor
    ENDPOINTS=$(grep -oP '/([-a-zA-Z0-9/{}]+)' "$file" | sort -u | head -3 | tr '\n' ', ')
    
    printf "  %-35s %3d testes  │  %s\n" "$file" "$TEST_COUNT" "$ENDPOINTS"
done

echo ""
echo "============================================"
echo "📊 RESUMO EXECUTIVO"
echo "============================================"

# Contar total de testes
TOTAL_TESTS=$(grep -r "def test_" tests/api --include="*.py" | wc -l)
echo "✅ Total de testes: $TOTAL_TESTS"

# Contar fixtures
FIXTURES=$(grep -c "@pytest.fixture" tests/fixtures/api_fixtures.py 2>/dev/null || echo 0)
echo "🔧 Total de fixtures: $FIXTURES"

# Contar marcadores
SMOKE_TESTS=$(grep -r "@pytest.mark.smoke" tests/api --include="*.py" | wc -l)
INTEGRATION_TESTS=$(grep -r "@pytest.mark.integration" tests/api --include="*.py" | wc -l)

echo "🚬 Smoke tests: $SMOKE_TESTS"
echo "🔗 Integration tests: $INTEGRATION_TESTS"

echo ""
echo "============================================"
echo "🚀 COMO EXECUTAR"
echo "============================================"
echo ""
echo "  # Todos os testes"
echo "  $ pytest tests/api/"
echo ""
echo "  # Apenas smoke tests"
echo "  $ pytest tests/api/ -m smoke"
echo ""
echo "  # Com cobertura"
echo "  $ pytest tests/api/ --cov=tests"
echo ""
echo "  # Arquivo específico"
echo "  $ pytest tests/api/test_teacher.py -v"
echo ""
echo "  # Via Makefile"
echo "  $ make test"
echo ""
echo "============================================"

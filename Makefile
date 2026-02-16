.PHONY: help install setup test test-verbose test-smoke test-integration coverage lint clean venv

help:
	@echo "Comandos disponíveis:"
	@echo "  make install           - Instala dependências"
	@echo "  make setup             - Setup completo (venv + install + config)"
	@echo "  make test              - Executa todos os testes"
	@echo "  make test-verbose      - Executa testes com saída detalhada"
	@echo "  make test-smoke        - Executa apenas testes de smoke"
	@echo "  make test-integration  - Executa apenas testes de integração"
	@echo "  make coverage          - Gera relatório de cobertura"
	@echo "  make lint              - Roda verificações de estilo"
	@echo "  make clean             - Remove arquivos temporários"
	@echo "  make venv              - Cria ambiente virtual"

venv:
	python3 -m venv venv
	@echo "✓ Ambiente virtual criado"

install:
	pip install -r requirements.txt

setup: venv install
	@if [ ! -f .env ]; then cp .env.example .env && echo "✓ .env criado a partir de .env.example"; fi
	@echo "✓ Setup completo!"

test:
	pytest

test-verbose:
	pytest -v

test-smoke:
	pytest -m smoke -v

test-integration:
	pytest -m integration -v

test-single:
	@read -p "Digite o caminho do teste: " test_path; pytest $$test_path -v

coverage:
	pytest --cov=tests --cov-report=html
	@echo "✓ Relatório gerado em htmlcov/index.html"

lint:
	@echo "Verificando código..."
	@python -m py_compile tests/**/*.py 2>/dev/null && echo "✓ Sintaxe OK" || echo "✗ Erros de sintaxe encontrados"

clean:
	rm -rf __pycache__ .pytest_cache .coverage htmlcov *.pyc
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@echo "✓ Arquivos temporários removidos"

run-specific-test:
	@read -p "Digite o padrão do teste (ex: test_users): " pattern; pytest -k "$$pattern" -v

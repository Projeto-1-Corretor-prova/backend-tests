# ✅ Checklist de Execução

## Antes de Começar

- [ ] API rodando em http://localhost:7999
- [ ] Python 3.8+ instalado
- [ ] Terminal aberto no diretório do projeto
- [ ] Git configurado (opcional)

---

## Setup Inicial

- [ ] `pip install -r requirements.txt`
- [ ] `cp .env.example .env`
- [ ] Editar `.env` com credenciais reais
- [ ] Testar conectividade: `curl http://localhost:7999/swagger/index.html`

---

## Primeira Execução

### Opção 1: Rápida (Recomendado)
```bash
pytest tests/api/test_teacher.py::TestTeacherAPI::test_teacher_login_success -v
```
- [ ] Comando executado
- [ ] Output mostra `PASSED`

### Opção 2: Smoke Tests
```bash
pytest tests/api/ -m smoke -v
```
- [ ] 22 testes executados
- [ ] Todos passaram (22 passed)

### Opção 3: Cometa (Todos)
```bash
pytest tests/api/ -v
```
- [ ] 176 testes executados
- [ ] Todos passaram

---

## Validação

- [ ] Nenhum erro de conexão
- [ ] Nenhum erro de autenticação (401)
- [ ] Nenhum AssertionError
- [ ] Tempo total < 5 minutos

---

## Exploração

### Teste um Recurso Específico
```bash
# Escolha um:
pytest tests/api/test_student.py -v
pytest tests/api/test_teacher_class.py -v
pytest tests/api/test_question.py -v
```
- [ ] Recurso testado
- [ ] Testes passaram

### Teste um Endpoint Específico
```bash
pytest tests/api/ -k "create" -v
```
- [ ] Todos os "create" estão testados

### Veja Cobertura
```bash
pytest tests/api/ --cov=tests --cov-report=term-missing
```
- [ ] Cobertura analisada

---

## Adicionar Novos Testes

- [ ] Copiei template do `TEMPLATE_NOVO_ENDPOINT.md`
- [ ] Criei fixture em `tests/fixtures/api_fixtures.py`
- [ ] Criei teste em `tests/api/test_novo_recurso.py`
- [ ] Rodar novo teste isolado
- [ ] Novo teste passou

---

## CI/CD (Opcional)

- [ ] GitHub Actions configurado
- [ ] Tests rodam em PR
- [ ] Coverage report gerado
- [ ] Testes obrigatórios antes do merge

---

## Documentação

Leia em ordem:
1. [ ] QUICK_START.md (este arquivo)
2. [ ] README.md (visão geral)
3. [ ] BEST_PRACTICES.md (padrões)
4. [ ] TEMPLATE_NOVO_ENDPOINT.md (para novos testes)
5. [ ] ESTRUTURA_CRIADA.md (detalhes arquitetura)
6. [ ] STATUS_FINAL.md (sumário)

---

## Script de Verificação Rápida

Execute isto para validar tudo:

```bash
#!/bin/bash
set -e

echo "🔍 Verificando estrutura..."
ls -la .env.example requirements.txt pytest.ini Makefile

echo "📦 Verificando dependências..."
python -c "import requests, pytest, dotenv; print('✅ OK')"

echo "📝 Verificando testes..."
find tests/api -name "test_*.py" | wc -l

echo "🧪 Teste de conectividade..."
curl -s http://localhost:7999/swagger/index.html > /dev/null && echo "✅ API rodando"

echo "🎯 Pronto!"
```

---

## Comaos Rápidos

```bash
# Todos
make test

# Smoke
make test-smoke

# Verbose
make test-verbose

# Cobertura
make coverage

# Setup
make setup

# Clean
make clean
```

---

## Se Algo Falhar

### "ConnectionRefused"
```bash
# Verifique:
curl http://localhost:7999/swagger/index.html
# Se não funcionar, inicie a API
```

### "401 Unauthorized"
```bash
# Verifique .env:
grep TEACHER .env
# Credenciais devem ser corretas
```

### "ImportError: No module named 'requests'"
```bash
# Reinstale:
pip install -r requirements.txt
```

### "ModuleNotFoundError: No module named 'pytest'"
```bash
# Reinstale pytest:
pip install pytest==7.4.3
```

---

## Sucesso! 🎉

Se chegou aqui, significa que:
- ✅ Dependências instaladas
- ✅ API conectando
- ✅ Autenticação funcionando
- ✅ Testes prontos para uso

**Próximo passo: Execute um teste!**

```bash
pytest tests/api/test_teacher.py -v
```

---

## Contato/Suporte

Consulte os arquivos de documentação:
- README.md - Instruções completas
- BEST_PRACTICES.md - Padrões e guidelines
- ESTRUTURA_CRIADA.md - Arquitetura detalhada

---

**Status:** ✅ Todos os 176 testes criados e prontos

Data: 16/02/2026  
API Base: http://localhost:7999  
Framework: pytest 7.4.3 + requests 2.31.0

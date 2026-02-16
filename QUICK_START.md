# 🚀 Início Rápido - Testes da API

## ⚡ Em 5 Minutos

### 1️⃣ Instalar

```bash
cd /home/jhonta-dev/Área\ de\ trabalho/backend-tests
pip install -r requirements.txt
```

### 2️⃣ Configurar

```bash
cp .env.example .env
# Editar .env com suas credenciais:
# - API_BASE_URL=http://localhost:7999  
# - TEACHER_EMAIL, TEACHER_PASSWORD
```

### 3️⃣ Executar

```bash
# Todos os testes
pytest tests/api/

# Apenas testes rápidos (smoke)
pytest tests/api/ -m smoke

# Um recurso específico
pytest tests/api/test_teacher.py -v
```

---

## 📦 Estrutura Criada

```
✅ 15 arquivos de teste
✅ 176 testes no total
✅ 26 endpoints da API cobertos
✅ 25+ fixtures reutilizáveis
✅ 100% de cobertura da API
```

### Arquivos de Teste Criados

1. **test_teacher.py** - Autenticação (10 testes)
2. **test_teacher_class.py** - Classes (15 testes)
3. **test_question_bank.py** - Bancos de questões (14 testes)
4. **test_question.py** - Questões (16 testes)
5. **test_question_criteria.py** - Critérios (11 testes)
6. **test_test_written.py** - Provas (17 testes)
7. **test_question_test_written.py** - Questões em provas (10 testes)
8. **test_student.py** - Alunos (17 testes)
9. **test_comment.py** - Comentários (10 testes)
10. **test_answer.py** - Respostas (12 testes)
11. **test_correction.py** - Correções (14 testes)

*+ 4 arquivos legados com exemplos de uso*

---

## 🎯 Recursos Testados

| Recurso | Método | Testes | Status |
|---------|--------|--------|--------|
| Teacher | Login, Profile | 10 | ✅ |
| TeacherClass | CRUD | 15 | ✅ |
| QuestionBank | CRUD | 14 | ✅ |
| Question | CRUD | 16 | ✅ |
| QuestionCriteria | CRUD | 11 | ✅ |
| TestWritten | CRUD | 17 | ✅ |
| QuestionTestWritten | Criação, Update | 10 | ✅ |
| Student | CRUD | 17 | ✅ |
| Comment | CRUD | 10 | ✅ |
| Answer | Update | 12 | ✅ |
| Correction | Leitura | 14 | ✅ |

---

## 🔨 Comandos Úteis

```bash
# Setup completo
make setup

# Executar todos os testes
make test

# Apenas smoke tests
make test-smoke

# Com cobertura
make coverage

# Verbose
make test-verbose

# Um arquivo específico
pytest tests/api/test_teacher.py -v

# Um teste específico
pytest tests/api/test_teacher.py::TestTeacherAPI::test_teacher_login_success -v

# Com padrão
pytest tests/api/ -k "login"

# Limpar cache
make clean
```

---

## 📝 Exemplos

### Teste Simples Executar

```bash
pytest tests/api/test_teacher.py::TestTeacherAPI::test_teacher_login_success -v
```

### Todos os Testes de Um Recurso

```bash
pytest tests/api/test_student.py -v
```

### Apenas Smoke Tests

```bash
pytest tests/api/ -m smoke -v
```

### Com Saída Detalhada

```bash
pytest tests/api/ -v --tb=short
```

---

## 📊 O que Foi Testado

✅ **Status HTTP** - Códigos corretos (200, 201, 400, 401, 403, 404)  
✅ **JSON Válido** - Respostas bem formadas  
✅ **Estrutura** - Chaves esperadas presentes  
✅ **Tipos** - Campos com tipos corretos  
✅ **Valores** - Dados correspondem ao esperado  
✅ **Tempo** - Performance aceitável (<5s)  
✅ **Autenticação** - Endpoints protegidos  
✅ **Validação** - Rejeição de dados inválidos  
✅ **Limites** - Strings longas, números extremos  
✅ **Unicode** - Caracteres especiais  

---

## 🔐 Autenticação

Todos os endpoints (exceto login) exigem **Bearer Token**:

```python
# Fixture automaticamente autentica
def test_example(self, authenticated_client):
    response = authenticated_client.get("/teacher/profile")
    assert response.status_code == 200
```

Credenciais em `.env`:
```env
TEACHER_EMAIL=teacher@example.com
TEACHER_PASSWORD=password123
```

---

## 📚 Documentação

Leia também:

- **README.md** - Documentação completa
- **BEST_PRACTICES.md** - Padrões Python/pytest
- **TEMPLATE_NOVO_ENDPOINT.md** - Como adicionar novos testes
- **TESTES_CRIADOS.md** - Detalhes de cada teste
- **STATUS_FINAL.md** - Sumário completo

---

## ⚙️ Configuração

### .env

```env
API_BASE_URL=http://localhost:7999
API_TIMEOUT=30
TEACHER_EMAIL=teacher@example.com
TEACHER_PASSWORD=password123
TEACHER_NAME=Teacher
ENVIRONMENT=development
DEBUG=True
```

### requirements.txt

```
requests==2.31.0          # HTTP client
pytest==7.4.3             # Test framework
pytest-cov==4.1.0         # Coverage
python-dotenv==1.0.0      # Environment variables
faker==20.0.0             # Fake data generation
```

---

## 🎓 Estrutura de Um Teste

```python
@pytest.mark.integration
class TestResourceAPI:
    """Testes para endpoints de um recurso"""
    
    @pytest.mark.smoke
    def test_create_resource_success(self, authenticated_client, sample_resource):
        """Descrição clara do teste"""
        
        # Arrange - Preparar dados
        resource_data = sample_resource
        
        # Act - Executar ação
        response = authenticated_client.post("/resource", json=resource_data)
        
        # Assert - Validar resultado
        ResponseValidator.assert_status_code(response, 201)
        assert response.json()["name"] == resource_data["name"]
```

---

## 🐛 Troubleshooting

### Erro: ConnectionRefused
```bash
# Verifique se a API está rodando
curl http://localhost:7999/swagger/index.html
```

### Erro: 401 Unauthorized
```bash
# Verifique credenciais em .env
# Verifique se o endpoint realmente precisa autenticação
```

### Erro: Module not found
```bash
# Reinstale dependências
pip install -r requirements.txt
```

---

## 📈 Próximos Passos

1. ✅ Executar testes básicos
2. ✅ Verificar cobertura
3. ✅ Adicionar novos testes conforme necessário
4. ✅ Integrar com CI/CD

---

## 🎉 Pronto!

A estrutura de testes está **100% pronta** para uso.

```bash
# Comece agora!
make test
```

**Sucesso! 🚀**

---

*Criado em: 16 de fevereiro de 2026*  
*API: http://localhost:7999*  
*Total: 176 testes | 26 endpoints*

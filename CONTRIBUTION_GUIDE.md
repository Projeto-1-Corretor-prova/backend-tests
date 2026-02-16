# 🎓 Guia de Contribuição - Adicionando Novos Testes

## Visão Geral

Este documento descreve como adicionar novos testes ou expandir testes existentes na suite.

---

## 🎯 Antes de Começar

✅ Leia:
- README.md (visão geral do projeto)
- BEST_PRACTICES.md (padrões e convenções)
- Um test_*.py existente (como exemplo)

---

## 📋 Passo 1: Identificar o Endpoint

### Encontre o endpoint no Swagger

1. Abra http://localhost:7999/swagger/index.html
2. Procure o recurso que quer testar
3. Anote:
   - **HTTP Method**: GET, POST, PUT, PATCH, DELETE
   - **URL Path**: exemplo: `/teacher-class/{id}`
   - **Request Body**: formato JSON esperado
   - **Response Body**: formato JSON retornado
   - **Status Codes**: 200, 201, 400, 401, 404, etc

### Exemplo

```
Endpoint: POST /student
Request:  { "name": "string", "email": "string", "classId": "uuid" }
Response: { "id": "uuid", "name": "string", "email": "string", "classId": "uuid" }
Codes:    201 (Created), 400 (Bad Request), 401 (Unauthorized)
```

---

## 🔧 Passo 2: Criar/Atualizar Fixture

### Adicionar em `tests/fixtures/api_fixtures.py`

Exemplo de fixture para um novo recurso:

```python
@pytest.fixture
def sample_new_resource():
    """Fixture com dados de exemplo para novo recurso"""
    return {
        "name": "Resource Name",
        "description": "A description",
        "value": 123
    }

@pytest.fixture
def new_resource_id(authenticated_client, sample_new_resource):
    """Fixture que cria um recurso e retorna seu ID"""
    response = authenticated_client.post(
        "/new-resource",
        json=sample_new_resource
    )
    return response.json()["id"]
```

---

## 📝 Passo 3: Criar Arquivo de Teste

### Estrutura Básica

Crie `tests/api/test_novo_recurso.py`:

```python
import pytest
from tests.utils.response_validator import ResponseValidator


@pytest.mark.integration
class TestNovoRecursoAPI:
    """Testes para endpoints de Novo Recurso"""
    
    # --- CREATE (POST) ---
    
    @pytest.mark.smoke
    def test_create_novo_recurso_success(self, authenticated_client, sample_novo_recurso):
        """Criar novo recurso com dados válidos"""
        # Arrange
        data = sample_novo_recurso
        
        # Act
        response = authenticated_client.post("/novo-recurso", json=data)
        
        # Assert
        ResponseValidator.assert_status_code(response, 201)
        ResponseValidator.assert_json_response(response)
        assert response.json()["name"] == data["name"]
    
    def test_create_novo_recurso_missing_fields(self, authenticated_client):
        """Criar novo recurso sem campos obrigatórios"""
        # Arrange
        data = {"name": ""}  # name é obrigatório
        
        # Act
        response = authenticated_client.post("/novo-recurso", json=data)
        
        # Assert
        ResponseValidator.assert_status_code(response, 400)
    
    def test_create_novo_recurso_without_auth(self, api_client, sample_novo_recurso):
        """Criar novo recurso sem autenticação"""
        # Act
        response = api_client.post("/novo-recurso", json=sample_novo_recurso)
        
        # Assert
        ResponseValidator.assert_status_code(response, 401)
    
    # --- READ (GET) ---
    
    @pytest.mark.smoke
    def test_get_novo_recurso_success(self, authenticated_client, novo_recurso_id):
        """Obter novo recurso por ID"""
        # Act
        response = authenticated_client.get(f"/novo-recurso/{novo_recurso_id}")
        
        # Assert
        ResponseValidator.assert_status_code(response, 200)
        ResponseValidator.assert_json_response(response)
        assert response.json()["id"] == novo_recurso_id
    
    def test_get_novo_recurso_not_found(self, authenticated_client):
        """Obter novo recurso com ID inválido"""
        # Act
        response = authenticated_client.get("/novo-recurso/00000000-0000-0000-0000-000000000000")
        
        # Assert
        ResponseValidator.assert_status_code(response, 404)
    
    # --- UPDATE (PUT/PATCH) ---
    
    @pytest.mark.smoke
    def test_update_novo_recurso_success(self, authenticated_client, novo_recurso_id):
        """Atualizar novo recurso"""
        # Arrange
        updated_data = {
            "name": "Updated Name",
            "description": "Updated description"
        }
        
        # Act
        response = authenticated_client.put(
            f"/novo-recurso/{novo_recurso_id}",
            json=updated_data
        )
        
        # Assert
        ResponseValidator.assert_status_code(response, 200)
        assert response.json()["name"] == updated_data["name"]
    
    def test_update_novo_recurso_not_found(self, authenticated_client):
        """Atualizar novo recurso inexistente"""
        # Act
        response = authenticated_client.put(
            "/novo-recurso/00000000-0000-0000-0000-000000000000",
            json={"name": "New Name"}
        )
        
        # Assert
        ResponseValidator.assert_status_code(response, 404)
    
    # --- DELETE ---
    
    def test_delete_novo_recurso_success(self, authenticated_client, novo_recurso_id):
        """Deletar novo recurso"""
        # Act
        response = authenticated_client.delete(f"/novo-recurso/{novo_recurso_id}")
        
        # Assert
        ResponseValidator.assert_status_code(response, 204)
    
    def test_delete_novo_recurso_not_found(self, authenticated_client):
        """Deletar novo recurso inexistente"""
        # Act
        response = authenticated_client.delete("/novo-recurso/00000000-0000-0000-0000-000000000000")
        
        # Assert
        ResponseValidator.assert_status_code(response, 404)
    
    # --- EDGE CASES ---
    
    def test_create_novo_recurso_with_special_characters(self, authenticated_client):
        """Criar novo recurso com caracteres especiais"""
        # Arrange
        data = {
            "name": "Resource @#$%&*()",
            "description": "Description with émojis 🚀✨"
        }
        
        # Act
        response = authenticated_client.post("/novo-recurso", json=data)
        
        # Assert
        ResponseValidator.assert_status_code(response, 201)
    
    def test_create_novo_recurso_with_very_long_name(self, authenticated_client):
        """Criar novo recurso com nome muito longo"""
        # Arrange
        data = {
            "name": "A" * 500,
            "description": "Long name test"
        }
        
        # Act
        response = authenticated_client.post("/novo-recurso", json=data)
        
        # Assert: Deve rejeitar ou truncar
        assert response.status_code in [201, 400]
    
    def test_response_time_acceptable(self, authenticated_client, novo_recurso_id):
        """Verificar tempo de resposta adequado"""
        # Act & Assert
        response = authenticated_client.get(f"/novo-recurso/{novo_recurso_id}")
        ResponseValidator.assert_response_time(response, max_seconds=5)
```

---

## 🏗️ Passo 4: Padrões a Seguir

### ✅ Boas Práticas

1. **Nomes Descritivos**
   ```python
   # ✅ BOM
   def test_create_student_with_valid_email_success(self):
   
   # ❌ RUIM
   def test_create(self):
   ```

2. **Arrange-Act-Assert**
   ```python
   # Arrange - Preparar dados/estado
   data = {...}
   
   # Act - Executar ação
   response = client.post(endpoint, json=data)
   
   # Assert - Validar resultado
   assert response.status_code == 201
   ```

3. **Usar Fixtures**
   ```python
   # ✅ BOM
   def test_example(self, authenticated_client, sample_student):
       response = authenticated_client.post("/student", json=sample_student)
   
   # ❌ RUIM
   def test_example(self):
       data = {"name": "John", "email": "john@..."}
       response = client.post(...)
   ```

4. **Usar ResponseValidator**
   ```python
   # ✅ BOM
   ResponseValidator.assert_status_code(response, 200)
   ResponseValidator.assert_json_response(response)
   
   # ❌ RUIM
   assert response.status_code == 200
   assert response.headers["content-type"] == "application/json"
   ```

5. **Marcar Testes**
   ```python
   @pytest.mark.smoke              # Testes rápidos
   @pytest.mark.integration        # Testes completos
   @pytest.mark.slow               # Testes lentos
   def test_something(self):
       ...
   ```

---

## 🧪 Passo 5: Executar os Testes

### Teste Individual

```bash
pytest tests/api/test_novo_recurso.py::TestNovoRecursoAPI::test_create_novo_recurso_success -v
```

### Todos do Novo Recurso

```bash
pytest tests/api/test_novo_recurso.py -v
```

### Apenas Smoke

```bash
pytest tests/api/test_novo_recurso.py -m smoke -v
```

### Com Cobertura

```bash
pytest tests/api/test_novo_recurso.py --cov=tests --cov-report=term-missing
```

---

## 📊 Passo 6: Cenários de Teste Comuns

### CRUD Basic

```python
# CREATE
def test_create_resource_success(self, authenticated_client, sample_resource):
    response = authenticated_client.post("/resource", json=sample_resource)
    assert response.status_code == 201

# READ
def test_get_resource_success(self, authenticated_client, resource_id):
    response = authenticated_client.get(f"/resource/{resource_id}")
    assert response.status_code == 200

# UPDATE
def test_update_resource_success(self, authenticated_client, resource_id):
    response = authenticated_client.put(f"/resource/{resource_id}", json={"name": "New"})
    assert response.status_code == 200

# DELETE
def test_delete_resource_success(self, authenticated_client, resource_id):
    response = authenticated_client.delete(f"/resource/{resource_id}")
    assert response.status_code == 204
```

### Validações

```python
# Campos obrigatórios
def test_create_without_required_field(self, authenticated_client):
    response = authenticated_client.post("/resource", json={})
    assert response.status_code == 400

# Tipo de dado inválido
def test_create_with_invalid_type(self, authenticated_client):
    response = authenticated_client.post("/resource", json={"id": "not-a-uuid"})
    assert response.status_code == 400

# Autenticação
def test_endpoint_unauthorized(self, api_client):
    response = api_client.get("/resource/123")
    assert response.status_code == 401
```

### Edge Cases

```python
# Valores vazios
def test_create_with_empty_string(self, authenticated_client):
    response = authenticated_client.post("/resource", json={"name": ""})
    assert response.status_code == 400

# Valores extremos
def test_create_with_very_long_input(self, authenticated_client):
    response = authenticated_client.post("/resource", json={"name": "A"*10000})
    assert response.status_code in [201, 400]

# Tamanho de lista
def test_create_with_empty_list(self, authenticated_client):
    response = authenticated_client.post("/resource", json={"tags": []})
    # Validar resposta apropriada

# Valores nulos
def test_create_with_null_value(self, authenticated_client):
    response = authenticated_client.post("/resource", json={"description": None})
    # Validar resposta apropriada
```

---

## 🔄 Passo 7: Integração com Testes Existentes

### Adicionar ao Fixture Pool

`tests/fixtures/api_fixtures.py`:

```python
@pytest.fixture
def sample_novo_recurso():
    """Dados de exemplo para novo recurso"""
    return {
        "name": "Test Resource",
        "description": "A test resource"
    }

@pytest.fixture
def novo_recurso_id(authenticated_client, sample_novo_recurso):
    """Criar recurso e retornar ID"""
    response = authenticated_client.post("/novo-recurso", json=sample_novo_recurso)
    return response.json()["id"]
```

### Usar em Outros Testes

```python
class TestTeacherClassAPI:
    def test_add_novo_recurso_to_class(self, authenticated_client, teacher_class_id, novo_recurso_id):
        """Adicionar novo recurso a uma classe"""
        response = authenticated_client.post(
            f"/teacher-class/{teacher_class_id}/resources",
            json={"resourceId": novo_recurso_id}
        )
        assert response.status_code == 200
```

---

## 📈 Passo 8: Documentação

### Adicionar ao README

```markdown
## Novo Recurso

#### Endpoints Testados
- ✅ POST /novo-recurso - Criar
- ✅ GET /novo-recurso/{id} - Obter
- ✅ PUT /novo-recurso/{id} - Atualizar
- ✅ DELETE /novo-recurso/{id} - Deletar

#### Testes Implementados
- 10 testes de sucesso
- 5 testes de erro
- 3 testes de edge case
- 1 teste de performance

**Total: 19 testes** para o recurso Novo Recurso
```

---

## ✅ Checklist Final

- [ ] Fixture criada em `tests/fixtures/api_fixtures.py`
- [ ] Arquivo de teste criado em `tests/api/test_novo_recurso.py`
- [ ] Todos os testes passam: `pytest tests/api/test_novo_recurso.py -v`
- [ ] Smoke tests marcados com `@pytest.mark.smoke`
- [ ] Padrão AAA seguido em todos os testes
- [ ] ResponseValidator usado para asserções
- [ ] Seguido BEST_PRACTICES.md guidelines
- [ ] README.md atualizado
- [ ] Sem hardcoded URLs (usar config.settings)
- [ ] Sem passwords em código (usar config.settings)

---

## 🚀 Próximos Passos

1. Criar novo arquivo de teste
2. Implementar testes
3. Executar localmente
4. Fazer commit
5. Abrir PR
6. Merge após revisão

---

## 📚 Referências

- README.md - Documentação principal
- BEST_PRACTICES.md - Padrões Python/pytest
- tests/api/test_student.py - Exemplo completo
- tests/fixtures/api_fixtures.py - Todas as fixtures

---

**Happy Testing! 🎉**

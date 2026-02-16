"""
GUIA DE BOAS PRÁTICAS - Testes de API em Python

Este documento contém as melhores práticas para escrever testes de API
robustos e manuteníveis usando pytest e requests.
"""

# ============================================================================
# 1. ESTRUTURA DE TESTES - PADRÃO AAA
# ============================================================================

"""
Sempre organize seus testes em Arrange, Act, Assert:

Arrange: Preparar dados e condições
Act:     Executar a ação
Assert:  Validar o resultado
"""

# ❌ EVITE - Teste sem estrutura clara
def test_bad_example(api_client):
    r = api_client.get("/users")
    assert r.status_code == 200
    d = r.json()
    assert len(d) > 0


# ✅ BOAS PRÁTICAS - Teste bem estruturado
def test_good_example(api_client):
    """Descrição clara do que está sendo testado"""
    # Arrange
    expected_status = 200
    
    # Act
    response = api_client.get("/users")
    
    # Assert
    assert response.status_code == expected_status
    assert len(response.json()) > 0


# ============================================================================
# 2. NOMES DESCRITIVOS
# ============================================================================

# ❌ EVITE
def test_user(api_client):
    response = api_client.get("/users/1")
    assert response.status_code == 200


# ✅ RECOMENDADO
def test_get_existing_user_returns_200_with_user_data(api_client):
    """Nomes longos mas descritivos facilitam manutenção"""
    response = api_client.get("/users/1")
    assert response.status_code == 200
    user = response.json()
    assert user["id"] == 1


# ============================================================================
# 3. USE FIXTURES PARA DADOS REUTILIZÁVEIS
# ============================================================================

# ❌ EVITE - Dados duplicados em múltiplos testes
def test_create_user_1(api_client):
    user = {"name": "João", "email": "joao@example.com"}
    response = api_client.post("/users", json=user)
    assert response.status_code == 201

def test_create_user_2(api_client):
    user = {"name": "João", "email": "joao@example.com"}
    response = api_client.post("/users", json=user)
    assert response.status_code == 201


# ✅ RECOMENDADO - Use fixtures
import pytest

@pytest.fixture
def sample_user():
    return {"name": "João", "email": "joao@example.com"}

def test_create_user(api_client, sample_user):
    response = api_client.post("/users", json=sample_user)
    assert response.status_code == 201


# ============================================================================
# 4. VALIDAÇÃO APROPRIADA
# ============================================================================

from tests.utils.response_validator import ResponseValidator

# ❌ EVITE - Validação incompleta
def test_incomplete_validation(api_client):
    response = api_client.get("/users/1")
    user = response.json()
    assert "name" in user  # Apenas 1 validação


# ✅ RECOMENDADO - Validação completa
def test_complete_validation(api_client):
    response = api_client.get("/users/1")
    
    # Status code
    ResponseValidator.assert_status_code(response, 200)
    
    # Resposta é JSON válida
    ResponseValidator.assert_json_response(response)
    
    # Chaves obrigatórias existem
    ResponseValidator.assert_json_keys(response.json(), ["id", "name", "email"])
    
    # Tipos de dados estão corretos
    user = response.json()
    assert isinstance(user["id"], int)
    assert isinstance(user["name"], str)


# ============================================================================
# 5. TESTE CASOS DE SUCESSO E FALHA
# ============================================================================

# ✅ TESTE COMPLETO
class TestUserCreation:
    """Exemplo completo com casos de sucesso e falha"""
    
    def test_create_user_with_valid_data(self, api_client, sample_user):
        """Caso positivo"""
        response = api_client.post("/users", json=sample_user)
        ResponseValidator.assert_status_code(response, 201)
    
    def test_create_user_with_invalid_email(self, api_client):
        """Caso negativo - Email inválido"""
        invalid_user = {"name": "João", "email": "invalid"}
        response = api_client.post("/users", json=invalid_user)
        assert response.status_code == 400
    
    def test_create_user_without_required_field(self, api_client):
        """Caso negativo - Campo obrigatório ausente"""
        incomplete_user = {"name": "João"}  # Sem email
        response = api_client.post("/users", json=incomplete_user)
        assert response.status_code == 400


# ============================================================================
# 6. USE PARAMETRIZE PARA TESTES REPETITIVOS
# ============================================================================

import pytest

# ❌ EVITE - Testes duplicados
def test_get_user_1(api_client):
    response = api_client.get("/users/1")
    assert response.status_code == 200

def test_get_user_2(api_client):
    response = api_client.get("/users/2")
    assert response.status_code == 200

def test_get_user_3(api_client):
    response = api_client.get("/users/3")
    assert response.status_code == 200


# ✅ RECOMENDADO - Use parametrize
@pytest.mark.parametrize("user_id", [1, 2, 3])
def test_get_user(api_client, user_id):
    response = api_client.get(f"/users/{user_id}")
    assert response.status_code == 200


# ============================================================================
# 7. TESTE CASOS EXTREMOS (EDGE CASES)
# ============================================================================

def test_boundary_values(api_client):
    """Teste valores extremos"""
    
    # Valor muito grande
    response = api_client.post("/users", json={"name": "A" * 10000})
    assert response.status_code in [400, 413]
    
    # Valor vazio
    response = api_client.post("/users", json={"name": ""})
    assert response.status_code == 400
    
    # Tipos incorretos
    response = api_client.post("/users", json={"name": 123})  # Int ao invés de str
    assert response.status_code == 400


# ============================================================================
# 8. TESTE SEQUÊNCIAS DE OPERAÇÕES
# ============================================================================

def test_complete_user_lifecycle(api_client, sample_user):
    """Teste o ciclo completo: Create -> Read -> Update -> Delete"""
    
    # CREATE
    create_response = api_client.post("/users", json=sample_user)
    ResponseValidator.assert_status_code(create_response, 201)
    user_id = create_response.json()["id"]
    
    # READ
    read_response = api_client.get(f"/users/{user_id}")
    ResponseValidator.assert_status_code(read_response, 200)
    
    # UPDATE
    update_data = {**sample_user, "name": "João Atualizado"}
    update_response = api_client.put(f"/users/{user_id}", json=update_data)
    ResponseValidator.assert_status_code(update_response, 200)
    
    # DELETE
    delete_response = api_client.delete(f"/users/{user_id}")
    assert delete_response.status_code in [200, 204]


# ============================================================================
# 9. USE MARCADORES PARA CATEGORIZAR TESTES
# ============================================================================

import pytest

@pytest.mark.smoke
def test_api_is_responsive(api_client):
    """Teste rápido que a API está respondendo"""
    response = api_client.get("/health")
    assert response.status_code == 200

@pytest.mark.slow
def test_slow_operation(api_client):
    """Teste que leva tempo"""
    response = api_client.get("/reports/generate")
    ResponseValidator.assert_response_time(response, 10000)


# ============================================================================
# 10. ORGANIZE POR CLASSES
# ============================================================================

class TestUserManagement:
    """Agrupe testes relacionados em classes"""
    
    class TestCreation:
        def test_with_valid_data(self, api_client, sample_user):
            pass
        
        def test_with_invalid_data(self, api_client):
            pass
    
    class TestRetrieval:
        def test_get_single_user(self, api_client):
            pass
        
        def test_get_all_users(self, api_client):
            pass
    
    class TestUpdate:
        def test_full_update(self, api_client):
            pass
        
        def test_partial_update(self, api_client):
            pass
    
    class TestDeletion:
        def test_delete_existing_user(self, api_client):
            pass
        
        def test_delete_nonexistent_user(self, api_client):
            pass


# ============================================================================
# RESUMO DAS MELHORES PRÁTICAS
# ============================================================================

"""
1. ✓ Use padrão AAA (Arrange, Act, Assert)
2. ✓ Nomes descritivos e em português
3. ✓ ReUse com fixtures
4. ✓ Valide status code, JSON, chaves e tipos
5. ✓ Teste casos de sucesso E falha
6. ✓ Use @pytest.mark.parametrize para repetição
7. ✓ Teste valores extremos
8. ✓ Teste sequências de operações
9. ✓ Use marcadores para categorizar
10. ✓ Organize testes em classes lógicas

NÃO FAÇA:
✗ Testes com nomes genéricos (test_1, test_a)
✗ Testes interdependentes (um teste depende do outro)
✗ Validações incompletas
✗ Dados hardcoded em múltiplos lugares
✗ Testes muito longos (cada teste = 1 conceito)
✗ Ignorar testes que falham
✗ Testar múltiplas coisas no mesmo teste
"""

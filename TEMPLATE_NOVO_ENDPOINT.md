"""
TEMPLATE - Como adicionar testes para novos endpoints

Este arquivo serve como template para adicionar testes para novos
endpoints da sua API. Copie e adapte conforme necessário.
"""

import pytest
from tests.utils.response_validator import ResponseValidator


# ============================================================================
# 1. CRIE UMA FIXTURE PARA OS DADOS DO SEU ENDPOINT
# ============================================================================
# Adicione em: tests/fixtures/api_fixtures.py

"""
@pytest.fixture
def sample_seu_recurso():
    \"\"\"Fixture com dados de exemplo do seu recurso\"\"\"
    return {
        "campo1": "valor1",
        "campo2": "valor2",
        "campo3": 123,
    }
"""


# ============================================================================
# 2. CRIE UM ARQUIVO DE TESTE PARA O ENDPOINT
# ============================================================================
# Arquivo: tests/api/test_seu_recurso.py

@pytest.mark.integration
class TestSeuRecurso:
    """Testes para endpoint /seu-recurso"""
    
    # ========================================================================
    # TESTES DE LISTAGEM (GET)
    # ========================================================================
    
    @pytest.mark.smoke
    def test_get_todos_os_recursos_com_sucesso(self, api_client):
        """
        Testa listagem de todos os recursos
        
        Given: API está disponível
        When: Faço uma requisição GET para /seu-recurso
        Then: Retorna status 200 com lista de recursos
        """
        # Arrange
        expected_status = 200
        
        # Act
        response = api_client.get("/seu-recurso")
        
        # Assert
        ResponseValidator.assert_status_code(response, expected_status)
        ResponseValidator.assert_json_response(response)
        
        resources = response.json()
        assert isinstance(resources, list)

    def test_get_com_filtros(self, api_client):
        """Testa listagem com parâmetros de filtro"""
        # Arrange
        params = {
            "campo1": "valor1",
            "page": 1,
            "limit": 10,
        }
        
        # Act
        response = api_client.get("/seu-recurso", params=params)
        
        # Assert
        ResponseValidator.assert_status_code(response, 200)
        assert len(response.json()) <= 10

    def test_get_com_paginacao(self, api_client):
        """Testa paginação dos resultados"""
        # Arrange
        limit = 5
        
        # Act
        page1 = api_client.get("/seu-recurso", params={"page": 1, "limit": limit})
        page2 = api_client.get("/seu-recurso", params={"page": 2, "limit": limit})
        
        # Assert
        ResponseValidator.assert_status_code(page1, 200)
        ResponseValidator.assert_status_code(page2, 200)

    # ========================================================================
    # TESTES DE CRIAÇÃO (POST)
    # ========================================================================
    
    def test_criar_recurso_com_dados_validos(self, api_client, sample_seu_recurso):
        """
        Testa criação de novo recurso com dados válidos
        
        Given: Tenho dados válidos do recurso
        When: Faço POST em /seu-recurso
        Then: Retorna 201 com o recurso criado
        """
        # Arrange
        dados = sample_seu_recurso
        
        # Act
        response = api_client.post("/seu-recurso", json=dados)
        
        # Assert
        ResponseValidator.assert_status_code(response, 201)
        ResponseValidator.assert_json_response(response)
        
        recurso_criado = response.json()
        assert recurso_criado["campo1"] == dados["campo1"]
        assert "id" in recurso_criado
        assert "created_at" in recurso_criado

    def test_criar_recurso_retorna_id(self, api_client, sample_seu_recurso):
        """Testa se o recurso criado retorna um ID único"""
        # Act
        response = api_client.post("/seu-recurso", json=sample_seu_recurso)
        
        # Assert
        recurso = response.json()
        assert isinstance(recurso["id"], int)
        assert recurso["id"] > 0

    def test_criar_recurso_com_dados_incompletos(self, api_client):
        """Testa criação com campo obrigatório ausente"""
        # Arrange
        dados_incompletos = {"campo1": "valor1"}  # Falta campo2
        
        # Act
        response = api_client.post("/seu-recurso", json=dados_incompletos)
        
        # Assert
        assert response.status_code == 400
        erro = response.json()
        assert "campo2" in erro.get("message", "").lower()

    @pytest.mark.parametrize("campo_invalido", [
        {"campo1": ""},  # Campo vazio
        {"campo1": "A" * 1000},  # Campo muito longo
        {"campo3": -1},  # Valor negativo inválido
        {"campo3": "texto"},  # Tipo errado
    ])
    def test_criar_recurso_com_dados_invalidos(self, api_client, campo_invalido):
        """Testa criação com diferentes tipos de dados inválidos"""
        # Act
        response = api_client.post("/seu-recurso", json=campo_invalido)
        
        # Assert
        assert response.status_code == 400

    # ========================================================================
    # TESTES DE LEITURA DETALHADA (GET /recurso/:id)
    # ========================================================================
    
    def test_obter_recurso_por_id(self, api_client):
        """Testa obtenção de um recurso específico"""
        # Arrange
        resource_id = 1
        
        # Act
        response = api_client.get(f"/seu-recurso/{resource_id}")
        
        # Assert
        ResponseValidator.assert_status_code(response, 200)
        
        recurso = response.json()
        ResponseValidator.assert_json_keys(
            recurso, 
            ["id", "campo1", "campo2", "campo3"]
        )
        assert recurso["id"] == resource_id

    def test_obter_recurso_inexistente(self, api_client):
        """Testa obtenção de recurso que não existe"""
        # Act
        response = api_client.get("/seu-recurso/999999")
        
        # Assert
        assert response.status_code == 404

    # ========================================================================
    # TESTES DE ATUALIZAÇÃO (PUT)
    # ========================================================================
    
    def test_atualizar_recurso_completo(self, api_client, sample_seu_recurso):
        """Testa atualização completa (PUT) de um recurso"""
        # Arrange
        resource_id = 1
        dados_atualizados = {
            **sample_seu_recurso,
            "campo1": "valor_novo",
        }
        
        # Act
        response = api_client.put(
            f"/seu-recurso/{resource_id}",
            json=dados_atualizados
        )
        
        # Assert
        ResponseValidator.assert_status_code(response, 200)
        
        recurso = response.json()
        assert recurso["campo1"] == "valor_novo"
        assert recurso["id"] == resource_id

    # ========================================================================
    # TESTES DE ATUALIZAÇÃO PARCIAL (PATCH)
    # ========================================================================
    
    def test_atualizar_recurso_parcial(self, api_client):
        """Testa atualização parcial (PATCH) de um recurso"""
        # Arrange
        resource_id = 1
        atualizacao_parcial = {"campo1": "novo_valor"}
        
        # Act
        response = api_client.patch(
            f"/seu-recurso/{resource_id}",
            json=atualizacao_parcial
        )
        
        # Assert
        ResponseValidator.assert_status_code(response, 200)
        
        recurso = response.json()
        assert recurso["campo1"] == "novo_valor"

    # ========================================================================
    # TESTES DE EXCLUSÃO (DELETE)
    # ========================================================================
    
    def test_deletar_recurso(self, api_client):
        """Testa exclusão de um recurso"""
        # Arrange
        resource_id = 1
        
        # Act
        response = api_client.delete(f"/seu-recurso/{resource_id}")
        
        # Assert
        assert response.status_code in [200, 204]

    def test_deletar_recurso_e_nao_encontra_depois(self, api_client):
        """Testa se o recurso realmente foi deletado"""
        # Arrange
        resource_id = 1
        
        # Act & Assert - Deletar
        delete_response = api_client.delete(f"/seu-recurso/{resource_id}")
        assert delete_response.status_code in [200, 204]
        
        # Act & Assert - Tentar obter
        get_response = api_client.get(f"/seu-recurso/{resource_id}")
        assert get_response.status_code == 404

    def test_deletar_recurso_inexistente(self, api_client):
        """Testa exclusão de recurso que não existe"""
        # Act
        response = api_client.delete("/seu-recurso/999999")
        
        # Assert
        assert response.status_code == 404

    # ========================================================================
    # TESTES DE CICLO COMPLETO (CRUD)
    # ========================================================================
    
    def test_ciclo_completo_crud(self, api_client, sample_seu_recurso):
        """
        Testa o ciclo completo de operações:
        Create -> Read -> Update -> Delete
        """
        # CREATE
        create_response = api_client.post("/seu-recurso", json=sample_seu_recurso)
        ResponseValidator.assert_status_code(create_response, 201)
        resource_id = create_response.json()["id"]
        
        # READ
        read_response = api_client.get(f"/seu-recurso/{resource_id}")
        ResponseValidator.assert_status_code(read_response, 200)
        
        # UPDATE
        atualizados = {**sample_seu_recurso, "campo1": "atualizado"}
        update_response = api_client.put(
            f"/seu-recurso/{resource_id}",
            json=atualizados
        )
        ResponseValidator.assert_status_code(update_response, 200)
        
        # DELETE
        delete_response = api_client.delete(f"/seu-recurso/{resource_id}")
        assert delete_response.status_code in [200, 204]

    # ========================================================================
    # TESTES DE PERFORMANCE
    # ========================================================================
    
    def test_tempo_de_resposta_aceitavel(self, api_client):
        """Testa se o tempo de resposta está dentro do esperado"""
        # Act
        response = api_client.get("/seu-recurso")
        
        # Assert
        ResponseValidator.assert_response_time(response, 2000)  # 2 segundos

    # ========================================================================
    # TESTES DE VALIDAÇÃO DE HEADERS
    # ========================================================================
    
    def test_respostas_retornam_headers_corretos(self, api_client):
        """Testa se as respostas contêm os headers corretos"""
        # Act
        response = api_client.get("/seu-recurso")
        
        # Assert
        ResponseValidator.assert_header_present(response, "Content-Type")
        assert "application/json" in response.headers["Content-Type"]


# ============================================================================
# 3. CHECKLIST DE IMPLEMENTAÇÃO
# ============================================================================

"""
Para cada novo endpoint, implemente testes para:

□ Listagem (GET)
  □ Sucesso com dados válidos
  □ Com filtros
  □ Com paginação
  □ Sem paginação
  
□ Criação (POST)
  □ Sucesso com dados válidos
  □ Retorna ID
  □ Dados incompletos (400)
  □ Dados inválidos (400)
  □ Email duplicado (409)
  
□ Leitura Detalhada (GET /id)
  □ Obter por ID existente
  □ Obter por ID inexistente (404)
  
□ Atualização Completa (PUT)
  □ Sucesso
  □ Dados inválidos (400)
  □ Recurso não encontrado (404)
  
□ Atualização Parcial (PATCH)
  □ Sucesso
  □ Campo parcial
  
□ Exclusão (DELETE)
  □ Sucesso
  □ Recurso não encontrado (404)
  □ Verificar se foi realmente deletado
  
□ Performance
  □ Tempo de resposta
  □ Tamanho da resposta
  
□ Headers
  □ Content-Type correto
  □ CORS headers (se aplicável)
"""

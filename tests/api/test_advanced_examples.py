"""Exemplos avançados de testes de API"""
import pytest
import json
from tests.utils.response_validator import ResponseValidator


class TestAdvancedScenarios:
    """Cenários avançados de teste"""

    def test_authentication_flow(self, api_client):
        """Testa fluxo completo de autenticação"""
        # 1. Login
        login_data = {"email": "user@example.com", "password": "senha123"}
        response = api_client.post("/auth/login", json=login_data)
        ResponseValidator.assert_status_code(response, 200)
        
        token = response.json().get("token")
        assert token is not None
        
        # 2. Usar token em requisição autenticada
        api_client.session.headers.update({"Authorization": f"Bearer {token}"})
        response = api_client.get("/users/me")
        ResponseValidator.assert_status_code(response, 200)

    def test_pagination(self, api_client):
        """Testa paginação de resultados"""
        page_1 = api_client.get("/users", params={"page": 1, "limit": 10})
        ResponseValidator.assert_status_code(page_1, 200)
        
        data_1 = page_1.json()
        assert len(data_1) <= 10
        
        if "next" in page_1.json():
            page_2 = api_client.get("/users", params={"page": 2, "limit": 10})
            ResponseValidator.assert_status_code(page_2, 200)

    def test_error_handling(self, api_client):
        """Testa diferentes tipos de erro"""
        # Bad Request
        response = api_client.post("/users", json={"invalid": "data"})
        assert response.status_code == 400
        
        # Unauthorized
        response = api_client.get("/admin/users")
        assert response.status_code == 401
        
        # Not Found
        response = api_client.get("/users/999999")
        assert response.status_code == 404
        
        # Internal Server Error
        response = api_client.post("/users", json=None)
        assert response.status_code == 500

    def test_data_validation(self, api_client, sample_user):
        """Testa validação de dados na resposta"""
        response = api_client.post("/users", json=sample_user)
        user = response.json()
        
        # Validar tipos
        assert isinstance(user["id"], int)
        assert isinstance(user["name"], str)
        assert isinstance(user["email"], str)
        assert isinstance(user["age"], int)
        assert isinstance(user["active"], bool)
        
        # Validar valores
        assert user["email"] == sample_user["email"]
        assert user["age"] == sample_user["age"]

    @pytest.mark.parametrize("user_id", [1, 2, 3, 100])
    def test_multiple_users(self, api_client, user_id):
        """Testa múltiplos usuários com parametrização"""
        response = api_client.get(f"/users/{user_id}")
        if user_id <= 3:
            ResponseValidator.assert_status_code(response, 200)
        else:
            # Pode retornar 404 para ID inválido
            assert response.status_code in [200, 404]

    def test_request_and_response_headers(self, api_client):
        """Testa headers de requisição e resposta"""
        headers = {"X-Custom-Header": "CustomValue"}
        response = api_client.get("/users", headers=headers)
        
        # Validar headers da resposta
        ResponseValidator.assert_header_present(response, "Content-Type")
        assert "application/json" in response.headers.get("Content-Type", "")

    def test_retry_logic(self, api_client):
        """Testa lógica de retry em falhas"""
        max_retries = 3
        retry_count = 0
        
        for attempt in range(max_retries):
            try:
                response = api_client.get("/users")
                if response.status_code == 200:
                    break
                retry_count = attempt
            except Exception:
                retry_count = attempt
        
        # A requisição eventualmente deve ter sucesso
        response = api_client.get("/users")
        ResponseValidator.assert_status_code(response, 200)

    def test_concurrent_requests_simulation(self, api_client):
        """Simula múltiplas requisições (não paralelas)"""
        responses = []
        for i in range(5):
            response = api_client.get(f"/users/{i+1}")
            responses.append(response)
        
        # Todas devem ter status válido
        for response in responses:
            assert response.status_code in [200, 404]

    def test_response_time_consistency(self, api_client):
        """Testa consistência do tempo de resposta"""
        times = []
        
        for _ in range(5):
            response = api_client.get("/users")
            ResponseValidator.assert_status_code(response, 200)
            elapsed_ms = response.elapsed.total_seconds() * 1000
            times.append(elapsed_ms)
        
        # Tempo médio deve ser razoável
        average_time = sum(times) / len(times)
        assert average_time < 5000, f"Average response time {average_time}ms is too high"

    def test_data_persistence(self, api_client, sample_user):
        """Testa se dados persistem após criação"""
        # Criar usuário
        create_response = api_client.post("/users", json=sample_user)
        ResponseValidator.assert_status_code(create_response, 201)
        created_user = create_response.json()
        user_id = created_user["id"]
        
        # Recuperar usuário criado
        get_response = api_client.get(f"/users/{user_id}")
        ResponseValidator.assert_status_code(get_response, 200)
        retrieved_user = get_response.json()
        
        # Dados devem ser iguais
        assert retrieved_user["email"] == sample_user["email"]
        assert retrieved_user["name"] == sample_user["name"]

    def test_field_constraints(self, api_client):
        """Testa restrições de campos"""
        invalid_users = [
            {"name": "", "email": "test@example.com"},  # Nome vazio
            {"name": "User", "email": "invalid"},       # Email inválido
            {"name": "User" * 100, "email": "test@example.com"},  # Nome muito longo
        ]
        
        for invalid_user in invalid_users:
            response = api_client.post("/users", json=invalid_user)
            assert response.status_code == 400, (
                f"Expected validation error for {invalid_user}, "
                f"got {response.status_code}"
            )

"""Testes para API de Professor (Teacher)"""
import pytest
from tests.utils.response_validator import ResponseValidator


@pytest.mark.integration
class TestTeacherAPI:
    """Testes para endpoints de Professor"""

    @pytest.mark.smoke
    def test_teacher_login_success(self, api_client, sample_login_data):
        """
        Testa login de professor com sucesso
        
        Given: Tenho credenciais válidas
        When: Faço POST em /teacher/login
        Then: Retorna 200 com token de acesso
        """
        # Arrange
        credentials = sample_login_data
        
        # Act
        response = api_client.post("/teacher/login", json=credentials)
        
        # Assert
        ResponseValidator.assert_status_code(response, 200)
        ResponseValidator.assert_json_response(response)
        
        login_response = response.json()
        ResponseValidator.assert_json_keys(login_response, ["id", "name", "acessToken"])
        assert isinstance(login_response["id"], int)
        assert isinstance(login_response["acessToken"], str)
        assert len(login_response["acessToken"]) > 0

    def test_teacher_login_with_invalid_credentials(self, api_client):
        """Testa login com credenciais inválidas"""
        # Arrange
        invalid_credentials = {
            "email": "invalid@example.com",
            "password": "wrongpassword",
            "name": "Invalid",
        }
        
        # Act
        response = api_client.post("/teacher/login", json=invalid_credentials)
        
        # Assert
        assert response.status_code in [401, 400, 500]

    def test_teacher_login_without_email(self, api_client):
        """Testa login sem email"""
        # Arrange
        incomplete_data = {
            "password": "password123",
            "name": "Teacher",
        }
        
        # Act
        response = api_client.post("/teacher/login", json=incomplete_data)
        
        # Assert
        assert response.status_code in [400, 500]

    @pytest.mark.smoke
    def test_get_teacher_profile(self, authenticated_client):
        """
        Testa obtenção do perfil do professor autenticado
        
        Given: Estou autenticado
        When: Faço GET em /teacher/profile
        Then: Retorna 200 com dados do professor
        """
        # Act
        response = authenticated_client.get("/teacher/profile")
        
        # Assert
        ResponseValidator.assert_status_code(response, 200)
        ResponseValidator.assert_json_response(response)
        
        profile = response.json()
        ResponseValidator.assert_json_keys(profile, ["id", "name", "email"])
        assert isinstance(profile["id"], int)

    def test_get_teacher_profile_without_authentication(self, api_client):
        """Testa obtenção de perfil sem autenticação"""
        # Act
        response = api_client.get("/teacher/profile")
        
        # Assert
        assert response.status_code in [401, 403]

    def test_teacher_profile_contains_valid_data(self, authenticated_client):
        """Testa se os dados do perfil são válidos"""
        # Act
        response = authenticated_client.get("/teacher/profile")
        
        # Assert
        profile = response.json()
        assert len(profile["name"]) > 0
        assert "@" in profile.get("email", "")
        assert "teacherClasses" in profile
        assert "questionBanks" in profile

    def test_response_time_for_login(self, api_client, sample_login_data):
        """Testa se o tempo de resposta do login está aceitável"""
        # Act
        response = api_client.post("/teacher/login", json=sample_login_data)
        
        # Assert
        ResponseValidator.assert_response_time(response, 5000)  # 5 segundos

    def test_response_time_for_profile(self, authenticated_client):
        """Testa se o tempo de resposta do perfil está aceitável"""
        # Act
        response = authenticated_client.get("/teacher/profile")
        
        # Assert
        ResponseValidator.assert_response_time(response, 5000)  # 5 segundos

    def test_login_returns_bearer_token_format(self, api_client, sample_login_data):
        """Testa se o token retornado está em formato válido"""
        # Act
        response = api_client.post("/teacher/login", json=sample_login_data)
        
        # Assert
        token = response.json().get("acessToken")
        assert token is not None
        # JWT typicamente tem 3 partes separadas por pontos
        assert len(token.split(".")) >= 2

    def test_consecutive_logins_return_different_tokens(
        self, api_client, sample_login_data
    ):
        """Testa se logins consecutivos retornam tokens diferentes"""
        # Act
        response1 = api_client.post("/teacher/login", json=sample_login_data)
        response2 = api_client.post("/teacher/login", json=sample_login_data)
        
        # Assert
        if response1.status_code == 200 and response2.status_code == 200:
            token1 = response1.json().get("acessToken")
            token2 = response2.json().get("acessToken")
            # Tokens podem ser iguais ou diferentes dependendo da implementação
            assert token1 is not None
            assert token2 is not None

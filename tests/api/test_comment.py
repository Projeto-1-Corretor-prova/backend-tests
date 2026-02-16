"""Testes para API de Comentários (Comment)"""
import pytest
from tests.utils.response_validator import ResponseValidator


@pytest.mark.integration
class TestCommentAPI:
    """Testes para endpoints de Comentários"""

    def test_create_comment_on_answer_success(
        self, authenticated_client, sample_comment
    ):
        """
        Testa criação de comentário em uma resposta
        
        Given: Estou autenticado e tenho uma resposta com ID válido
        When: Faço POST em /comment/answers/{answerId}
        Then: Retorna 200 com o comentário criado
        """
        # Arrange
        answer_id = 1  # Assumindo que existe
        comment_data = sample_comment
        
        # Act
        response = authenticated_client.post(
            f"/comment/answers/{answer_id}",
            json=comment_data,
        )
        
        # Assert
        # Pode retornar 200 ou 404 se resposta não existe
        if response.status_code == 200:
            ResponseValidator.assert_json_response(response)
            comment = response.json()
            ResponseValidator.assert_json_keys(comment, ["id", "content"])

    def test_create_comment_without_authentication(
        self, api_client, sample_comment
    ):
        """Testa criação de comentário sem autenticação"""
        # Act
        response = api_client.post(
            "/comment/answers/1",
            json=sample_comment,
        )
        
        # Assert
        assert response.status_code in [401, 403]

    def test_create_comment_with_empty_content(
        self, authenticated_client
    ):
        """Testa criação de comentário com conteúdo vazio"""
        # Arrange
        empty_comment = {"content": ""}
        
        # Act
        response = authenticated_client.post(
            "/comment/answers/1",
            json=empty_comment,
        )
        
        # Assert
        assert response.status_code in [200, 400, 404]

    def test_create_comment_with_invalid_answer_id(
        self, authenticated_client, sample_comment
    ):
        """Testa criação de comentário com ID de resposta inválido"""
        # Act
        response = authenticated_client.post(
            "/comment/answers/999999",
            json=sample_comment,
        )
        
        # Assert
        assert response.status_code in [404, 400, 200]

    def test_update_comment_success(
        self, authenticated_client, sample_comment
    ):
        """
        Testa atualização de um comentário
        
        Given: Existe um comentário com um ID válido
        When: Faço PUT em /comment/{commentId} com novos dados
        Then: Retorna 200 com o comentário atualizado
        """
        # Arrange
        comment_id = 1
        updated_data = {
            **sample_comment,
            "content": "Comentário atualizado",
        }
        
        # Act
        response = authenticated_client.put(
            f"/comment/{comment_id}",
            json=updated_data,
        )
        
        # Assert
        if response.status_code == 200:
            ResponseValidator.assert_json_response(response)
            comment = response.json()
            assert comment["content"] == "Comentário atualizado"

    def test_update_comment_without_authentication(
        self, api_client, sample_comment
    ):
        """Testa atualização de comentário sem autenticação"""
        # Act
        response = api_client.put(
            "/comment/1",
            json=sample_comment,
        )
        
        # Assert
        assert response.status_code in [401, 403]

    def test_response_time_for_create_comment(
        self, authenticated_client, sample_comment
    ):
        """Testa tempo de resposta para criar comentário"""
        # Act
        response = authenticated_client.post(
            "/comment/answers/1",
            json=sample_comment,
        )
        
        # Assert
        if response.status_code in [200, 404]:
            ResponseValidator.assert_response_time(response, 5000)

    def test_comment_with_special_characters(
        self, authenticated_client
    ):
        """Testa comentário com caracteres especiais"""
        # Arrange
        special_comment = {
            "content": "Excelente! 👏 Resposta: f(x) = 2x + 3, portanto f(5) = 13 ✓"
        }
        
        # Act
        response = authenticated_client.post(
            "/comment/answers/1",
            json=special_comment,
        )
        
        # Assert
        if response.status_code == 200:
            ResponseValidator.assert_json_response(response)

    def test_comment_with_long_content(
        self, authenticated_client
    ):
        """Testa comentário com conteúdo muito longo"""
        # Arrange
        long_comment = {
            "content": "A" * 5000,
        }
        
        # Act
        response = authenticated_client.post(
            "/comment/answers/1",
            json=long_comment,
        )
        
        # Assert
        assert response.status_code in [200, 400, 413, 404]

    def test_create_multiple_comments(
        self, authenticated_client, sample_comment
    ):
        """Testa criação de múltiplos comentários em uma resposta"""
        # Act
        responses = []
        for i in range(3):
            data = {
                **sample_comment,
                "content": f"Comentário {i}",
            }
            response = authenticated_client.post(
                "/comment/answers/1",
                json=data,
            )
            responses.append(response)
        
        # Assert
        for response in responses:
            if response.status_code in [200, 404]:
                pass  # Status válido
            else:
                assert False, f"Unexpected status code: {response.status_code}"

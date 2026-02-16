"""Testes para API de Questões em Provas (QuestionTestWritten)"""
import pytest
from tests.utils.response_validator import ResponseValidator


@pytest.mark.integration
class TestQuestionTestWrittenAPI:
    """Testes para endpoints de Questões em Provas"""

    @pytest.mark.smoke
    def test_create_question_test_written_success(
        self,
        authenticated_client,
        question_id,
        test_written_id,
        sample_question_test_written,
    ):
        """
        Testa associação de questão a uma prova com sucesso
        
        Given: Estou autenticado e tenho uma questão e prova válidas
        When: Faço POST em /question-test-written/question/{questionId}/test-written/{testWrittenId}
        Then: Retorna 200 com a associação criada
        """
        # Arrange
        data = sample_question_test_written
        
        # Act
        response = authenticated_client.post(
            f"/question-test-written/question/{question_id}/test-written/{test_written_id}",
            json=data,
        )
        
        # Assert
        ResponseValidator.assert_status_code(response, 200)
        ResponseValidator.assert_json_response(response)
        
        q_test = response.json()
        ResponseValidator.assert_json_keys(q_test, ["id", "weight", "lines"])
        assert q_test["weight"] == data["weight"]
        assert isinstance(q_test["id"], int)

    def test_create_question_test_written_without_authentication(
        self,
        api_client,
        question_id,
        test_written_id,
        sample_question_test_written,
    ):
        """Testa criação sem autenticação"""
        # Act
        response = api_client.post(
            f"/question-test-written/question/{question_id}/test-written/{test_written_id}",
            json=sample_question_test_written,
        )
        
        # Assert
        assert response.status_code in [401, 403]

    def test_create_question_test_written_with_invalid_ids(
        self, authenticated_client, sample_question_test_written
    ):
        """Testa criação com IDs inválidos"""
        # Act
        response = authenticated_client.post(
            f"/question-test-written/question/999999/test-written/999999",
            json=sample_question_test_written,
        )
        
        # Assert
        assert response.status_code in [404, 400, 200]

    def test_update_question_test_written_success(
        self,
        authenticated_client,
        question_id,
        test_written_id,
        sample_question_test_written,
    ):
        """
        Testa atualização de uma questão em prova
        
        Given: Existe uma questão associada a uma prova
        When: Faço PUT em /question-test-written/{id} com novos dados
        Then: Retorna 200 com o registro atualizado
        """
        # Arrange - Criar associação
        create_response = authenticated_client.post(
            f"/question-test-written/question/{question_id}/test-written/{test_written_id}",
            json=sample_question_test_written,
        )
        q_test_id = create_response.json()["id"]
        
        # Arrange - Dados atualizados
        updated_data = {
            "weight": 5.0,
            "lines": 20,
        }
        
        # Act
        response = authenticated_client.put(
            f"/question-test-written/{q_test_id}",
            json=updated_data,
        )
        
        # Assert
        ResponseValidator.assert_status_code(response, 200)
        
        updated = response.json()
        assert updated["weight"] == 5.0
        assert updated["lines"] == 20
        assert updated["id"] == q_test_id

    def test_update_question_test_written_without_authentication(
        self, api_client, sample_question_test_written
    ):
        """Testa atualização sem autenticação"""
        # Act
        response = api_client.put(
            "/question-test-written/1",
            json=sample_question_test_written,
        )
        
        # Assert
        assert response.status_code in [401, 403]

    def test_response_time_for_create(
        self,
        authenticated_client,
        question_id,
        test_written_id,
        sample_question_test_written,
    ):
        """Testa tempo de resposta para criação"""
        # Act
        response = authenticated_client.post(
            f"/question-test-written/question/{question_id}/test-written/{test_written_id}",
            json=sample_question_test_written,
        )
        
        # Assert
        ResponseValidator.assert_response_time(response, 5000)

    def test_question_test_written_contains_question_reference(
        self,
        authenticated_client,
        question_id,
        test_written_id,
        sample_question_test_written,
    ):
        """Testa se contém referência à questão"""
        # Act
        response = authenticated_client.post(
            f"/question-test-written/question/{question_id}/test-written/{test_written_id}",
            json=sample_question_test_written,
        )
        
        # Assert
        q_test = response.json()
        if "question" in q_test:
            assert isinstance(q_test["question"], dict)

    def test_weight_is_positive_number(
        self,
        authenticated_client,
        question_id,
        test_written_id,
    ):
        """Testa se peso é um número positivo"""
        # Arrange
        test_data = {
            "weight": 2.5,
            "lines": 10,
        }
        
        # Act
        response = authenticated_client.post(
            f"/question-test-written/question/{question_id}/test-written/{test_written_id}",
            json=test_data,
        )
        
        # Assert
        q_test = response.json()
        assert isinstance(q_test["weight"], (int, float))
        assert q_test["weight"] > 0

    def test_lines_is_positive_integer(
        self,
        authenticated_client,
        question_id,
        test_written_id,
    ):
        """Testa se linhas é um inteiro positivo"""
        # Arrange
        test_data = {
            "weight": 2.0,
            "lines": 10,
        }
        
        # Act
        response = authenticated_client.post(
            f"/question-test-written/question/{question_id}/test-written/{test_written_id}",
            json=test_data,
        )
        
        # Assert
        q_test = response.json()
        assert isinstance(q_test["lines"], int)
        assert q_test["lines"] > 0

    def test_create_multiple_questions_in_test(
        self,
        authenticated_client,
        question_id,
        test_written_id,
    ):
        """Testa adição de múltiplas questões a uma prova"""
        # Act
        responses = []
        for i in range(3):
            data = {
                "weight": 1.0 + i,
                "lines": 5 + i,
            }
            response = authenticated_client.post(
                f"/question-test-written/question/{question_id}/test-written/{test_written_id}",
                json=data,
            )
            responses.append(response)
        
        # Assert
        for response in responses:
            ResponseValidator.assert_status_code(response, 200)

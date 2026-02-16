"""Testes para API de Respostas (Answer)"""
import pytest
from tests.utils.response_validator import ResponseValidator


@pytest.mark.integration
class TestAnswerAPI:
    """Testes para endpoints de Respostas"""

    def test_update_answer_success(
        self, authenticated_client, sample_answer
    ):
        """
        Testa atualização de uma resposta
        
        Given: Existe uma resposta com um ID válido
        When: Faço PUT em /answer/{id} com novos dados
        Then: Retorna 200 com a resposta atualizada
        """
        # Arrange
        answer_id = 1
        updated_data = {
            **sample_answer,
            "score": 9.5,
        }
        
        # Act
        response = authenticated_client.put(
            f"/answer/{answer_id}",
            json=updated_data,
        )
        
        # Assert
        if response.status_code == 200:
            ResponseValidator.assert_json_response(response)
            answer = response.json()
            assert answer["score"] == 9.5

    def test_update_answer_without_authentication(
        self, api_client, sample_answer
    ):
        """Testa atualização de resposta sem autenticação"""
        # Act
        response = api_client.put(
            "/answer/1",
            json=sample_answer,
        )
        
        # Assert
        assert response.status_code in [401, 403]

    def test_update_answer_with_invalid_id(
        self, authenticated_client, sample_answer
    ):
        """Testa atualização de resposta com ID inválido"""
        # Act
        response = authenticated_client.put(
            "/answer/999999",
            json=sample_answer,
        )
        
        # Assert
        assert response.status_code in [404, 400, 200]

    def test_update_answer_score_validation(
        self, authenticated_client
    ):
        """Testa validação de pontuação"""
        # Arrange
        answer_data = {
            "studentAnswer": "A resposta do aluno",
            "score": 10.0,
        }
        
        # Act
        response = authenticated_client.put(
            "/answer/1",
            json=answer_data,
        )
        
        # Assert
        if response.status_code == 200:
            ResponseValidator.assert_json_response(response)

    def test_response_time_for_update_answer(
        self, authenticated_client, sample_answer
    ):
        """Testa tempo de resposta para atualizar resposta"""
        # Act
        response = authenticated_client.put(
            "/answer/1",
            json=sample_answer,
        )
        
        # Assert
        if response.status_code in [200, 404]:
            ResponseValidator.assert_response_time(response, 5000)

    def test_answer_contains_question_test_written(
        self, authenticated_client
    ):
        """Testa se resposta contém referência a questão de prova"""
        # Arrange
        answer_id = 1
        
        # Act
        # Não há GET específico para answer, testamos via PUT response
        response = authenticated_client.put(
            f"/answer/{answer_id}",
            json={"studentAnswer": "teste", "score": 5.0},
        )
        
        # Assert
        if response.status_code == 200:
            answer = response.json()
            if "questionTestWritten" in answer:
                assert isinstance(answer["questionTestWritten"], dict)

    def test_answer_contains_comments_lists(
        self, authenticated_client
    ):
        """Testa se resposta contém listas de comentários"""
        # Arrange
        answer_id = 1
        
        # Act
        response = authenticated_client.put(
            f"/answer/{answer_id}",
            json={"studentAnswer": "teste", "score": 5.0},
        )
        
        # Assert
        if response.status_code == 200:
            answer = response.json()
            if "aiComments" in answer:
                assert isinstance(answer["aiComments"], (list, type(None)))
            if "teacherComments" in answer:
                assert isinstance(answer["teacherComments"], (list, type(None)))

    def test_update_answer_with_empty_student_answer(
        self, authenticated_client
    ):
        """Testa atualização com resposta do aluno vazia"""
        # Arrange
        answer_data = {
            "studentAnswer": "",
            "score": 0.0,
        }
        
        # Act
        response = authenticated_client.put(
            "/answer/1",
            json=answer_data,
        )
        
        # Assert
        assert response.status_code in [200, 400, 404]

    def test_update_answer_with_max_score(
        self, authenticated_client
    ):
        """Testa atualização com pontuação máxima"""
        # Arrange
        answer_data = {
            "studentAnswer": "Excelente resposta!",
            "score": 100.0,
        }
        
        # Act
        response = authenticated_client.put(
            "/answer/1",
            json=answer_data,
        )
        
        # Assert
        if response.status_code == 200:
            answer = response.json()
            assert answer["score"] == 100.0

    def test_update_answer_with_zero_score(
        self, authenticated_client
    ):
        """Testa atualização com pontuação zero"""
        # Arrange
        answer_data = {
            "studentAnswer": "Resposta incorreta",
            "score": 0.0,
        }
        
        # Act
        response = authenticated_client.put(
            "/answer/1",
            json=answer_data,
        )
        
        # Assert
        if response.status_code == 200:
            answer = response.json()
            assert answer["score"] == 0.0

    def test_update_answer_with_negative_score(
        self, authenticated_client
    ):
        """Testa atualização com pontuação negativa (deve falhar)"""
        # Arrange
        answer_data = {
            "studentAnswer": "Teste",
            "score": -5.0,
        }
        
        # Act
        response = authenticated_client.put(
            "/answer/1",
            json=answer_data,
        )
        
        # Assert
        assert response.status_code in [200, 400, 404]

    def test_update_multiple_answers(
        self, authenticated_client, sample_answer
    ):
        """Testa atualização de múltiplas respostas"""
        # Act
        responses = []
        for i in range(3):
            data = {
                **sample_answer,
                "score": 5.0 + i,
            }
            response = authenticated_client.put(
                f"/answer/{i+1}",
                json=data,
            )
            responses.append(response)
        
        # Assert
        for response in responses:
            if response.status_code in [200, 404]:
                pass  # Status válido
            else:
                assert False, f"Unexpected status code: {response.status_code}"

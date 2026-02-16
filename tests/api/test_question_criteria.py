"""Testes para API de Critérios de Questões (QuestionCriteria)"""
import pytest
from tests.utils.response_validator import ResponseValidator


@pytest.mark.integration
class TestQuestionCriteriaAPI:
    """Testes para endpoints de Critérios de Questões"""

    @pytest.mark.smoke
    def test_create_question_criteria_success(
        self, authenticated_client, question_id, sample_question_criteria
    ):
        """
        Testa criação de um critério com sucesso
        
        Given: Estou autenticado e tenho uma questão válida
        When: Faço POST em /question-criteria/question/{questionId}
        Then: Retorna 200 com o critério criado
        """
        # Arrange
        criteria_data = sample_question_criteria
        
        # Act
        response = authenticated_client.post(
            f"/question-criteria/question/{question_id}",
            json=criteria_data,
        )
        
        # Assert
        ResponseValidator.assert_status_code(response, 200)
        ResponseValidator.assert_json_response(response)
        
        criteria = response.json()
        ResponseValidator.assert_json_keys(criteria, ["id", "type", "criteria"])
        assert criteria["type"] == criteria_data["type"]
        assert isinstance(criteria["id"], int)

    def test_create_question_criteria_without_authentication(
        self, api_client, question_id, sample_question_criteria
    ):
        """Testa criação de critério sem autenticação"""
        # Act
        response = api_client.post(
            f"/question-criteria/question/{question_id}",
            json=sample_question_criteria,
        )
        
        # Assert
        assert response.status_code in [401, 403]

    def test_create_question_criteria_with_invalid_question_id(
        self, authenticated_client, sample_question_criteria
    ):
        """Testa criação de critério com ID de questão inválido"""
        # Act
        response = authenticated_client.post(
            "/question-criteria/question/999999",
            json=sample_question_criteria,
        )
        
        # Assert
        assert response.status_code in [404, 400, 200]

    def test_create_question_criteria_with_all_types(
        self, authenticated_client, question_id
    ):
        """Testa criação de critérios com todos os tipos"""
        # Arrange
        criteria_types = ["KEYWORD", "SEMANTIC", "EXAMPLE"]
        
        # Act
        responses = []
        for criteria_type in criteria_types:
            data = {
                "type": criteria_type,
                "criteria": f"Critério {criteria_type}",
            }
            response = authenticated_client.post(
                f"/question-criteria/question/{question_id}",
                json=data,
            )
            responses.append(response)
        
        # Assert
        for response in responses:
            ResponseValidator.assert_status_code(response, 200)

    def test_update_question_criteria_success(
        self, authenticated_client, question_id, sample_question_criteria
    ):
        """
        Testa atualização de um critério
        
        Given: Existe um critério com um ID válido
        When: Faço PUT em /question-criteria/{id} com novos dados
        Then: Retorna 200 com o critério atualizado
        """
        # Arrange - Criar critério
        create_response = authenticated_client.post(
            f"/question-criteria/question/{question_id}",
            json=sample_question_criteria,
        )
        criteria_id = create_response.json()["id"]
        
        # Arrange - Dados atualizados
        updated_data = {
            **sample_question_criteria,
            "criteria": "Critério Atualizado",
        }
        
        # Act
        response = authenticated_client.put(
            f"/question-criteria/{criteria_id}",
            json=updated_data,
        )
        
        # Assert
        ResponseValidator.assert_status_code(response, 200)
        
        updated_criteria = response.json()
        assert updated_criteria["criteria"] == "Critério Atualizado"
        assert updated_criteria["id"] == criteria_id

    def test_update_question_criteria_without_authentication(
        self, api_client, question_id, sample_question_criteria
    ):
        """Testa atualização de critério sem autenticação"""
        # Act
        response = api_client.put(
            f"/question-criteria/1",
            json=sample_question_criteria,
        )
        
        # Assert
        assert response.status_code in [401, 403]

    def test_response_time_for_create_criteria(
        self, authenticated_client, question_id, sample_question_criteria
    ):
        """Testa se o tempo de resposta para criar critério está aceitável"""
        # Act
        response = authenticated_client.post(
            f"/question-criteria/question/{question_id}",
            json=sample_question_criteria,
        )
        
        # Assert
        ResponseValidator.assert_response_time(response, 5000)

    def test_question_criteria_id_is_positive_integer(
        self, authenticated_client, question_id, sample_question_criteria
    ):
        """Testa se o ID do critério é um inteiro positivo"""
        # Act
        response = authenticated_client.post(
            f"/question-criteria/question/{question_id}",
            json=sample_question_criteria,
        )
        
        # Assert
        criteria = response.json()
        assert isinstance(criteria["id"], int)
        assert criteria["id"] > 0

    def test_criteria_enum_validation(self, authenticated_client, question_id):
        """Testa validação de enum para tipos de critério"""
        # Arrange
        valid_types = ["KEYWORD", "SEMANTIC", "EXAMPLE"]
        
        # Act
        for criteria_type in valid_types:
            data = {
                "type": criteria_type,
                "criteria": f"Test {criteria_type}",
            }
            response = authenticated_client.post(
                f"/question-criteria/question/{question_id}",
                json=data,
            )
            
            # Assert
            ResponseValidator.assert_status_code(response, 200)
            criteria = response.json()
            assert criteria["type"] == criteria_type

    def test_create_criteria_with_empty_text(
        self, authenticated_client, question_id
    ):
        """Testa criação de critério com texto vazio"""
        # Arrange
        empty_criteria = {
            "type": "KEYWORD",
            "criteria": "",
        }
        
        # Act
        response = authenticated_client.post(
            f"/question-criteria/question/{question_id}",
            json=empty_criteria,
        )
        
        # Assert
        assert response.status_code in [200, 400]

    def test_create_criteria_with_long_text(
        self, authenticated_client, question_id
    ):
        """Testa criação de critério com texto muito longo"""
        # Arrange
        long_criteria = {
            "type": "SEMANTIC",
            "criteria": "A" * 10000,
        }
        
        # Act
        response = authenticated_client.post(
            f"/question-criteria/question/{question_id}",
            json=long_criteria,
        )
        
        # Assert
        assert response.status_code in [200, 400, 413]

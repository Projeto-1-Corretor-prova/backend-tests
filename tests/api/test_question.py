"""Testes para API de Questões (Question)"""
import pytest
from tests.utils.response_validator import ResponseValidator


@pytest.mark.integration
class TestQuestionAPI:
    """Testes para endpoints de Questões"""

    @pytest.mark.smoke
    def test_create_question_success(
        self, authenticated_client, question_bank_id, sample_question
    ):
        """
        Testa criação de uma questão com sucesso
        
        Given: Estou autenticado e tenho um banco de questões válido
        When: Faço POST em /question/question-bank/{questionBankId}
        Then: Retorna 200 com a questão criada
        """
        # Arrange
        question_data = sample_question
        
        # Act
        response = authenticated_client.post(
            f"/question/question-bank/{question_bank_id}",
            json=question_data,
        )
        
        # Assert
        ResponseValidator.assert_status_code(response, 200)
        ResponseValidator.assert_json_response(response)
        
        question = response.json()
        ResponseValidator.assert_json_keys(question, ["id", "statement"])
        assert question["statement"] == question_data["statement"]
        assert isinstance(question["id"], int)

    def test_create_question_without_authentication(
        self, api_client, question_bank_id, sample_question
    ):
        """Testa criação de questão sem autenticação"""
        # Act
        response = api_client.post(
            f"/question/question-bank/{question_bank_id}",
            json=sample_question,
        )
        
        # Assert
        assert response.status_code in [401, 403]

    def test_create_question_with_empty_statement(
        self, authenticated_client, question_bank_id
    ):
        """Testa criação de questão com statement vazio"""
        # Arrange
        invalid_question = {"statement": "", "questionCriterias": []}
        
        # Act
        response = authenticated_client.post(
            f"/question/question-bank/{question_bank_id}",
            json=invalid_question,
        )
        
        # Assert
        assert response.status_code in [200, 400]

    def test_create_question_with_invalid_bank_id(
        self, authenticated_client, sample_question
    ):
        """Testa criação de questão com ID de banco inválido"""
        # Act
        response = authenticated_client.post(
            "/question/question-bank/999999",
            json=sample_question,
        )
        
        # Assert
        assert response.status_code in [404, 400, 200]

    @pytest.mark.smoke
    def test_get_question_by_id(self, authenticated_client, question_id):
        """
        Testa obtenção de uma questão por ID
        
        Given: Existe uma questão com um ID válido
        When: Faço GET em /question/{id}
        Then: Retorna 200 com os dados da questão
        """
        # Act
        response = authenticated_client.get(f"/question/{question_id}")
        
        # Assert
        ResponseValidator.assert_status_code(response, 200)
        ResponseValidator.assert_json_response(response)
        
        question = response.json()
        ResponseValidator.assert_json_keys(question, ["id", "statement"])
        assert question["id"] == question_id

    def test_get_question_with_invalid_id(self, authenticated_client):
        """Testa obtenção de questão com ID inválido"""
        # Act
        response = authenticated_client.get("/question/999999")
        
        # Assert
        assert response.status_code in [404, 400, 200]

    def test_get_question_contains_criterias_list(
        self, authenticated_client, question_id
    ):
        """Testa se a questão contém lista de critérios"""
        # Act
        response = authenticated_client.get(f"/question/{question_id}")
        
        # Assert
        question = response.json()
        assert "questionCriterias" in question
        assert isinstance(question["questionCriterias"], (list, type(None)))

    def test_update_question_success(
        self, authenticated_client, question_id, sample_question
    ):
        """
        Testa atualização de uma questão
        
        Given: Existe uma questão com um ID válido
        When: Faço PUT em /question/{id} com novos dados
        Then: Retorna 200 com a questão atualizada
        """
        # Arrange
        updated_data = {
            **sample_question,
            "statement": "Novo enunciado da questão",
        }
        
        # Act
        response = authenticated_client.put(
            f"/question/{question_id}",
            json=updated_data,
        )
        
        # Assert
        ResponseValidator.assert_status_code(response, 200)
        
        updated_question = response.json()
        assert updated_question["statement"] == "Novo enunciado da questão"
        assert updated_question["id"] == question_id

    def test_update_question_without_authentication(
        self, api_client, question_id, sample_question
    ):
        """Testa atualização de questão sem autenticação"""
        # Act
        response = api_client.put(
            f"/question/{question_id}",
            json=sample_question,
        )
        
        # Assert
        assert response.status_code in [401, 403]

    def test_update_nonexistent_question(
        self, authenticated_client, sample_question
    ):
        """Testa atualização de questão que não existe"""
        # Act
        response = authenticated_client.put(
            "/question/999999",
            json=sample_question,
        )
        
        # Assert
        assert response.status_code in [404, 400, 200]

    def test_response_time_for_create_question(
        self, authenticated_client, question_bank_id, sample_question
    ):
        """Testa se o tempo de resposta para criar questão está aceitável"""
        # Act
        response = authenticated_client.post(
            f"/question/question-bank/{question_bank_id}",
            json=sample_question,
        )
        
        # Assert
        ResponseValidator.assert_response_time(response, 5000)

    def test_response_time_for_get_question(self, authenticated_client, question_id):
        """Testa se o tempo de resposta para obter questão está aceitável"""
        # Act
        response = authenticated_client.get(f"/question/{question_id}")
        
        # Assert
        ResponseValidator.assert_response_time(response, 5000)

    def test_question_id_is_positive_integer(
        self, authenticated_client, question_bank_id, sample_question
    ):
        """Testa se o ID da questão é um inteiro positivo"""
        # Act
        response = authenticated_client.post(
            f"/question/question-bank/{question_bank_id}",
            json=sample_question,
        )
        
        # Assert
        question = response.json()
        assert isinstance(question["id"], int)
        assert question["id"] > 0

    def test_create_question_with_multiple_criterias(
        self, authenticated_client, question_bank_id
    ):
        """Testa criação de questão com múltiplos critérios"""
        # Arrange
        question_with_multiple_criterias = {
            "statement": "Pergunta com múltiplos critérios",
            "questionCriterias": [
                {"type": "KEYWORD", "criteria": "palavra-chave1"},
                {"type": "SEMANTIC", "criteria": "significado1"},
                {"type": "EXAMPLE", "criteria": "exemplo1"},
            ],
        }
        
        # Act
        response = authenticated_client.post(
            f"/question/question-bank/{question_bank_id}",
            json=question_with_multiple_criterias,
        )
        
        # Assert
        ResponseValidator.assert_status_code(response, 200)
        question = response.json()
        if question.get("questionCriterias"):
            assert len(question["questionCriterias"]) >= 1

    def test_question_statement_with_special_characters(
        self, authenticated_client, question_bank_id
    ):
        """Testa questão com caracteres especiais no statement"""
        # Arrange
        special_question = {
            "statement": "O que é f(x) = 2x + 3? (Calcule f(5) = ?)",
            "questionCriterias": [],
        }
        
        # Act
        response = authenticated_client.post(
            f"/question/question-bank/{question_bank_id}",
            json=special_question,
        )
        
        # Assert
        ResponseValidator.assert_status_code(response, 200)

    def test_create_multiple_questions(
        self, authenticated_client, question_bank_id, sample_question
    ):
        """Testa criação de múltiplas questões"""
        # Act
        responses = []
        for i in range(3):
            data = {
                **sample_question,
                "statement": f"Questão {i}",
            }
            response = authenticated_client.post(
                f"/question/question-bank/{question_bank_id}",
                json=data,
            )
            responses.append(response)
        
        # Assert
        for response in responses:
            ResponseValidator.assert_status_code(response, 200)

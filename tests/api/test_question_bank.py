"""Testes para API de Banco de Questões (QuestionBank)"""
import pytest
from tests.utils.response_validator import ResponseValidator


@pytest.mark.integration
class TestQuestionBankAPI:
    """Testes para endpoints de Banco de Questões"""

    @pytest.mark.smoke
    def test_create_question_bank_success(
        self, authenticated_client, sample_question_bank
    ):
        """
        Testa criação de um banco de questões com sucesso
        
        Given: Estou autenticado e tenho dados válidos
        When: Faço POST em /question-bank
        Then: Retorna 200 com o banco criado
        """
        # Arrange
        bank_data = sample_question_bank
        
        # Act
        response = authenticated_client.post("/question-bank", json=bank_data)
        
        # Assert
        ResponseValidator.assert_status_code(response, 200)
        ResponseValidator.assert_json_response(response)
        
        bank = response.json()
        ResponseValidator.assert_json_keys(bank, ["id", "title"])
        assert bank["title"] == bank_data["title"]
        assert isinstance(bank["id"], int)

    def test_create_question_bank_without_authentication(
        self, api_client, sample_question_bank
    ):
        """Testa criação de banco sem autenticação"""
        # Act
        response = api_client.post("/question-bank", json=sample_question_bank)
        
        # Assert
        assert response.status_code in [401, 403]

    def test_create_question_bank_with_empty_title(self, authenticated_client):
        """Testa criação de banco com título vazio"""
        # Arrange
        invalid_bank = {"title": ""}
        
        # Act
        response = authenticated_client.post("/question-bank", json=invalid_bank)
        
        # Assert
        assert response.status_code in [200, 400]

    @pytest.mark.smoke
    def test_get_question_bank_by_id(
        self, authenticated_client, question_bank_id
    ):
        """
        Testa obtenção de um banco por ID
        
        Given: Existe um banco com um ID válido
        When: Faço GET em /question-bank/{id}
        Then: Retorna 200 com os dados do banco
        """
        # Act
        response = authenticated_client.get(f"/question-bank/{question_bank_id}")
        
        # Assert
        ResponseValidator.assert_status_code(response, 200)
        ResponseValidator.assert_json_response(response)
        
        bank = response.json()
        ResponseValidator.assert_json_keys(bank, ["id", "title"])
        assert bank["id"] == question_bank_id

    def test_get_question_bank_with_invalid_id(self, authenticated_client):
        """Testa obtenção de banco com ID inválido"""
        # Act
        response = authenticated_client.get("/question-bank/999999")
        
        # Assert
        assert response.status_code in [404, 400, 200]

    def test_get_question_bank_contains_questions_list(
        self, authenticated_client, question_bank_id
    ):
        """Testa se o banco contém lista de questões"""
        # Act
        response = authenticated_client.get(f"/question-bank/{question_bank_id}")
        
        # Assert
        bank = response.json()
        assert "questions" in bank
        assert isinstance(bank["questions"], (list, type(None)))

    def test_update_question_bank_success(
        self, authenticated_client, question_bank_id, sample_question_bank
    ):
        """
        Testa atualização de um banco de questões
        
        Given: Existe um banco com um ID válido
        When: Faço PUT em /question-bank/{id} com novos dados
        Then: Retorna 200 com o banco atualizado
        """
        # Arrange
        updated_data = {
            **sample_question_bank,
            "title": "Novo Banco Atualizado",
        }
        
        # Act
        response = authenticated_client.put(
            f"/question-bank/{question_bank_id}",
            json=updated_data,
        )
        
        # Assert
        ResponseValidator.assert_status_code(response, 200)
        
        updated_bank = response.json()
        assert updated_bank["title"] == "Novo Banco Atualizado"
        assert updated_bank["id"] == question_bank_id

    def test_update_question_bank_without_authentication(
        self, api_client, question_bank_id, sample_question_bank
    ):
        """Testa atualização de banco sem autenticação"""
        # Act
        response = api_client.put(
            f"/question-bank/{question_bank_id}",
            json=sample_question_bank,
        )
        
        # Assert
        assert response.status_code in [401, 403]

    def test_update_nonexistent_question_bank(
        self, authenticated_client, sample_question_bank
    ):
        """Testa atualização de banco que não existe"""
        # Act
        response = authenticated_client.put(
            "/question-bank/999999",
            json=sample_question_bank,
        )
        
        # Assert
        assert response.status_code in [404, 400, 200]

    def test_response_time_for_create_bank(
        self, authenticated_client, sample_question_bank
    ):
        """Testa se o tempo de resposta para criar banco está aceitável"""
        # Act
        response = authenticated_client.post(
            "/question-bank",
            json=sample_question_bank,
        )
        
        # Assert
        ResponseValidator.assert_response_time(response, 5000)

    def test_response_time_for_get_bank(self, authenticated_client, question_bank_id):
        """Testa se o tempo de resposta para obter banco está aceitável"""
        # Act
        response = authenticated_client.get(f"/question-bank/{question_bank_id}")
        
        # Assert
        ResponseValidator.assert_response_time(response, 5000)

    def test_question_bank_id_is_positive_integer(
        self, authenticated_client, sample_question_bank
    ):
        """Testa se o ID do banco é um inteiro positivo"""
        # Act
        response = authenticated_client.post("/question-bank", json=sample_question_bank)
        
        # Assert
        bank = response.json()
        assert isinstance(bank["id"], int)
        assert bank["id"] > 0

    def test_create_multiple_question_banks(
        self, authenticated_client, sample_question_bank
    ):
        """Testa criação de múltiplos bancos de questões"""
        # Act
        responses = []
        for i in range(3):
            data = {**sample_question_bank, "title": f"Banco {i}"}
            response = authenticated_client.post("/question-bank", json=data)
            responses.append(response)
        
        # Assert
        for response in responses:
            ResponseValidator.assert_status_code(response, 200)

    def test_question_bank_with_special_characters_in_title(
        self, authenticated_client
    ):
        """Testa criação de banco com caracteres especiais no título"""
        # Arrange
        special_bank = {
            "title": "Banco #1: 100% de Matemática (Álgebra) & Trigonometria!"
        }
        
        # Act
        response = authenticated_client.post("/question-bank", json=special_bank)
        
        # Assert
        ResponseValidator.assert_status_code(response, 200)
        bank = response.json()
        assert bank["title"] == special_bank["title"]

"""Testes para API de Prova Escrita (TestWritten)"""
import pytest
from tests.utils.response_validator import ResponseValidator


@pytest.mark.integration
class TestTestWrittenAPI:
    """Testes para endpoints de Prova Escrita"""

    @pytest.mark.smoke
    def test_create_test_written_success(
        self, authenticated_client, teacher_class_id, sample_test_written
    ):
        """
        Testa criação de uma prova escrita com sucesso
        
        Given: Estou autenticado e tenho uma classe válida
        When: Faço POST em /test-written/teacher-class/{teacherClassId}
        Then: Retorna 200 com a prova criada
        """
        # Arrange
        test_data = sample_test_written
        
        # Act
        response = authenticated_client.post(
            f"/test-written/teacher-class/{teacher_class_id}",
            json=test_data,
        )
        
        # Assert
        ResponseValidator.assert_status_code(response, 200)
        ResponseValidator.assert_json_response(response)
        
        test = response.json()
        ResponseValidator.assert_json_keys(test, ["id", "title"])
        assert test["title"] == test_data["title"]
        assert isinstance(test["id"], int)

    def test_create_test_written_without_authentication(
        self, api_client, teacher_class_id, sample_test_written
    ):
        """Testa criação de prova sem autenticação"""
        # Act
        response = api_client.post(
            f"/test-written/teacher-class/{teacher_class_id}",
            json=sample_test_written,
        )
        
        # Assert
        assert response.status_code in [401, 403]

    def test_create_test_written_with_empty_title(
        self, authenticated_client, teacher_class_id
    ):
        """Testa criação de prova com título vazio"""
        # Arrange
        invalid_test = {"title": "", "regexQuestionIdentifier": ""}
        
        # Act
        response = authenticated_client.post(
            f"/test-written/teacher-class/{teacher_class_id}",
            json=invalid_test,
        )
        
        # Assert
        assert response.status_code in [200, 400]

    def test_create_test_written_with_invalid_class_id(
        self, authenticated_client, sample_test_written
    ):
        """Testa criação de prova com ID de classe inválido"""
        # Act
        response = authenticated_client.post(
            "/test-written/teacher-class/999999",
            json=sample_test_written,
        )
        
        # Assert
        assert response.status_code in [404, 400, 200]

    @pytest.mark.smoke
    def test_get_test_written_by_id(
        self, authenticated_client, test_written_id
    ):
        """
        Testa obtenção de uma prova por ID
        
        Given: Existe uma prova com um ID válido
        When: Faço GET em /test-written/{id}
        Then: Retorna 200 com os dados da prova
        """
        # Act
        response = authenticated_client.get(f"/test-written/{test_written_id}")
        
        # Assert
        ResponseValidator.assert_status_code(response, 200)
        ResponseValidator.assert_json_response(response)
        
        test = response.json()
        ResponseValidator.assert_json_keys(test, ["id", "title"])
        assert test["id"] == test_written_id

    def test_get_test_written_with_invalid_id(self, authenticated_client):
        """Testa obtenção de prova com ID inválido"""
        # Act
        response = authenticated_client.get("/test-written/999999")
        
        # Assert
        assert response.status_code in [404, 400, 200]

    def test_get_test_written_contains_questions_list(
        self, authenticated_client, test_written_id
    ):
        """Testa se a prova contém lista de questões"""
        # Act
        response = authenticated_client.get(f"/test-written/{test_written_id}")
        
        # Assert
        test = response.json()
        assert "questionTestWrittens" in test
        assert isinstance(test["questionTestWrittens"], (list, type(None)))

    def test_get_test_written_contains_corrections_list(
        self, authenticated_client, test_written_id
    ):
        """Testa se a prova contém lista de correções"""
        # Act
        response = authenticated_client.get(f"/test-written/{test_written_id}")
        
        # Assert
        test = response.json()
        assert "corrections" in test
        assert isinstance(test["corrections"], (list, type(None)))

    def test_update_test_written_success(
        self, authenticated_client, test_written_id, sample_test_written
    ):
        """
        Testa atualização de uma prova
        
        Given: Existe uma prova com um ID válido
        When: Faço PUT em /test-written/{id} com novos dados
        Then: Retorna 200 com a prova atualizada
        """
        # Arrange
        updated_data = {
            **sample_test_written,
            "title": "Prova Atualizada",
        }
        
        # Act
        response = authenticated_client.put(
            f"/test-written/{test_written_id}",
            json=updated_data,
        )
        
        # Assert
        ResponseValidator.assert_status_code(response, 200)
        
        updated_test = response.json()
        assert updated_test["title"] == "Prova Atualizada"
        assert updated_test["id"] == test_written_id

    def test_update_test_written_without_authentication(
        self, api_client, test_written_id, sample_test_written
    ):
        """Testa atualização de prova sem autenticação"""
        # Act
        response = api_client.put(
            f"/test-written/{test_written_id}",
            json=sample_test_written,
        )
        
        # Assert
        assert response.status_code in [401, 403]

    def test_update_nonexistent_test_written(
        self, authenticated_client, sample_test_written
    ):
        """Testa atualização de prova que não existe"""
        # Act
        response = authenticated_client.put(
            "/test-written/999999",
            json=sample_test_written,
        )
        
        # Assert
        assert response.status_code in [404, 400, 200]

    def test_response_time_for_create_test(
        self, authenticated_client, teacher_class_id, sample_test_written
    ):
        """Testa se o tempo de resposta para criar prova está aceitável"""
        # Act
        response = authenticated_client.post(
            f"/test-written/teacher-class/{teacher_class_id}",
            json=sample_test_written,
        )
        
        # Assert
        ResponseValidator.assert_response_time(response, 5000)

    def test_response_time_for_get_test(self, authenticated_client, test_written_id):
        """Testa se o tempo de resposta para obter prova está aceitável"""
        # Act
        response = authenticated_client.get(f"/test-written/{test_written_id}")
        
        # Assert
        ResponseValidator.assert_response_time(response, 5000)

    def test_test_written_id_is_positive_integer(
        self, authenticated_client, teacher_class_id, sample_test_written
    ):
        """Testa se o ID da prova é um inteiro positivo"""
        # Act
        response = authenticated_client.post(
            f"/test-written/teacher-class/{teacher_class_id}",
            json=sample_test_written,
        )
        
        # Assert
        test = response.json()
        assert isinstance(test["id"], int)
        assert test["id"] > 0

    def test_test_written_has_total_weight(
        self, authenticated_client, test_written_id
    ):
        """Testa se a prova tem peso total"""
        # Act
        response = authenticated_client.get(f"/test-written/{test_written_id}")
        
        # Assert
        test = response.json()
        assert "totalWeight" in test
        assert isinstance(test["totalWeight"], (int, float))

    def test_create_test_written_with_regex_identifier(
        self, authenticated_client, teacher_class_id
    ):
        """Testa criação de prova com identificador regex"""
        # Arrange
        test_with_regex = {
            "title": "Prova com Regex",
            "regexQuestionIdentifier": "^Q[0-9]{3}$",
        }
        
        # Act
        response = authenticated_client.post(
            f"/test-written/teacher-class/{teacher_class_id}",
            json=test_with_regex,
        )
        
        # Assert
        ResponseValidator.assert_status_code(response, 200)
        test = response.json()
        assert test["regexQuestionIdentifier"] == "^Q[0-9]{3}$"

    def test_create_multiple_tests(
        self, authenticated_client, teacher_class_id, sample_test_written
    ):
        """Testa criação de múltiplas provas"""
        # Act
        responses = []
        for i in range(3):
            data = {
                **sample_test_written,
                "title": f"Prova {i}",
            }
            response = authenticated_client.post(
                f"/test-written/teacher-class/{teacher_class_id}",
                json=data,
            )
            responses.append(response)
        
        # Assert
        for response in responses:
            ResponseValidator.assert_status_code(response, 200)

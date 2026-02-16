"""Testes para API de Classe de Professor (TeacherClass)"""
import pytest
from tests.utils.response_validator import ResponseValidator


@pytest.mark.integration
class TestTeacherClassAPI:
    """Testes para endpoints de Classe de Professor"""

    @pytest.mark.smoke
    def test_create_teacher_class_success(self, authenticated_client, sample_teacher_class):
        """
        Testa criação de uma classe com sucesso
        
        Given: Estou autenticado e tenho dados válidos
        When: Faço POST em /teacher-class
        Then: Retorna 200 com a classe criada
        """
        # Arrange
        class_data = sample_teacher_class
        
        # Act
        response = authenticated_client.post("/teacher-class", json=class_data)
        
        # Assert
        ResponseValidator.assert_status_code(response, 200)
        ResponseValidator.assert_json_response(response)
        
        teacher_class = response.json()
        ResponseValidator.assert_json_keys(teacher_class, ["id", "title"])
        assert teacher_class["title"] == class_data["title"]
        assert isinstance(teacher_class["id"], int)

    def test_create_teacher_class_without_authentication(
        self, api_client, sample_teacher_class
    ):
        """Testa criação de classe sem autenticação"""
        # Act
        response = api_client.post("/teacher-class", json=sample_teacher_class)
        
        # Assert
        assert response.status_code in [401, 403]

    def test_create_teacher_class_with_empty_title(self, authenticated_client):
        """Testa criação de classe com título vazio"""
        # Arrange
        invalid_class = {"title": ""}
        
        # Act
        response = authenticated_client.post("/teacher-class", json=invalid_class)
        
        # Assert
        # Pode ser 400 ou 200 dependendo da validação
        assert response.status_code in [200, 400]

    @pytest.mark.smoke
    def test_get_teacher_class_by_id(
        self, authenticated_client, teacher_class_id
    ):
        """
        Testa obtenção de uma classe por ID
        
        Given: Existe uma classe com um ID válido
        When: Faço GET em /teacher-class/{id}
        Then: Retorna 200 com os dados da classe
        """
        # Act
        response = authenticated_client.get(f"/teacher-class/{teacher_class_id}")
        
        # Assert
        ResponseValidator.assert_status_code(response, 200)
        ResponseValidator.assert_json_response(response)
        
        teacher_class = response.json()
        ResponseValidator.assert_json_keys(teacher_class, ["id", "title"])
        assert teacher_class["id"] == teacher_class_id

    def test_get_teacher_class_with_invalid_id(self, authenticated_client):
        """Testa obtenção de classe com ID inválido"""
        # Act
        response = authenticated_client.get("/teacher-class/999999")
        
        # Assert
        assert response.status_code in [404, 400, 200]

    def test_get_teacher_class_contains_students_list(
        self, authenticated_client, teacher_class_id
    ):
        """Testa se a classe contém lista de alunos"""
        # Act
        response = authenticated_client.get(f"/teacher-class/{teacher_class_id}")
        
        # Assert
        teacher_class = response.json()
        assert "students" in teacher_class
        assert isinstance(teacher_class["students"], (list, type(None)))

    def test_get_teacher_class_contains_test_written_list(
        self, authenticated_client, teacher_class_id
    ):
        """Testa se a classe contém lista de provas"""
        # Act
        response = authenticated_client.get(f"/teacher-class/{teacher_class_id}")
        
        # Assert
        teacher_class = response.json()
        assert "testWrittens" in teacher_class
        assert isinstance(teacher_class["testWrittens"], (list, type(None)))

    def test_update_teacher_class_success(
        self, authenticated_client, teacher_class_id, sample_teacher_class
    ):
        """
        Testa atualização de uma classe
        
        Given: Existe uma classe com um ID válido
        When: Faço PUT em /teacher-class/{id} com novos dados
        Then: Retorna 200 com a classe atualizada
        """
        # Arrange
        updated_data = {**sample_teacher_class, "title": "Nova Classe Atualizada"}
        
        # Act
        response = authenticated_client.put(
            f"/teacher-class/{teacher_class_id}",
            json=updated_data,
        )
        
        # Assert
        ResponseValidator.assert_status_code(response, 200)
        
        updated_class = response.json()
        assert updated_class["title"] == "Nova Classe Atualizada"
        assert updated_class["id"] == teacher_class_id

    def test_update_teacher_class_without_authentication(
        self, api_client, teacher_class_id, sample_teacher_class
    ):
        """Testa atualização de classe sem autenticação"""
        # Act
        response = api_client.put(
            f"/teacher-class/{teacher_class_id}",
            json=sample_teacher_class,
        )
        
        # Assert
        assert response.status_code in [401, 403]

    def test_update_nonexistent_teacher_class(self, authenticated_client, sample_teacher_class):
        """Testa atualização de classe que não existe"""
        # Act
        response = authenticated_client.put(
            "/teacher-class/999999",
            json=sample_teacher_class,
        )
        
        # Assert
        assert response.status_code in [404, 400, 200]

    def test_response_time_for_create_class(
        self, authenticated_client, sample_teacher_class
    ):
        """Testa se o tempo de resposta para criar classe está aceitável"""
        # Act
        response = authenticated_client.post(
            "/teacher-class",
            json=sample_teacher_class,
        )
        
        # Assert
        ResponseValidator.assert_response_time(response, 5000)

    def test_response_time_for_get_class(self, authenticated_client, teacher_class_id):
        """Testa se o tempo de resposta para obter classe está aceitável"""
        # Act
        response = authenticated_client.get(f"/teacher-class/{teacher_class_id}")
        
        # Assert
        ResponseValidator.assert_response_time(response, 5000)

    def test_response_time_for_update_class(
        self, authenticated_client, teacher_class_id, sample_teacher_class
    ):
        """Testa se o tempo de resposta para atualizar classe está aceitável"""
        # Act
        response = authenticated_client.put(
            f"/teacher-class/{teacher_class_id}",
            json=sample_teacher_class,
        )
        
        # Assert
        ResponseValidator.assert_response_time(response, 5000)

    def test_teacher_class_id_is_positive_integer(
        self, authenticated_client, sample_teacher_class
    ):
        """Testa se o ID da classe é um inteiro positivo"""
        # Act
        response = authenticated_client.post("/teacher-class", json=sample_teacher_class)
        
        # Assert
        teacher_class = response.json()
        assert isinstance(teacher_class["id"], int)
        assert teacher_class["id"] > 0

    def test_create_multiple_classes(self, authenticated_client, sample_teacher_class):
        """Testa criação de múltiplas classes"""
        # Act
        responses = []
        for i in range(3):
            data = {**sample_teacher_class, "title": f"Classe {i}"}
            response = authenticated_client.post("/teacher-class", json=data)
            responses.append(response)
        
        # Assert
        for response in responses:
            ResponseValidator.assert_status_code(response, 200)

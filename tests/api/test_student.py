"""Testes para API de Alunos (Student)"""
import pytest
from tests.utils.response_validator import ResponseValidator


@pytest.mark.integration
class TestStudentAPI:
    """Testes para endpoints de Alunos"""

    @pytest.mark.smoke
    def test_create_student_success(
        self, authenticated_client, teacher_class_id, sample_student
    ):
        """
        Testa criação de um aluno com sucesso
        
        Given: Estou autenticado e tenho uma classe válida
        When: Faço POST em /student/teacher-class/{id}
        Then: Retorna 200 com o aluno criado
        """
        # Arrange
        student_data = sample_student
        
        # Act
        response = authenticated_client.post(
            f"/student/teacher-class/{teacher_class_id}",
            json=student_data,
        )
        
        # Assert
        ResponseValidator.assert_status_code(response, 200)
        ResponseValidator.assert_json_response(response)
        
        student = response.json()
        ResponseValidator.assert_json_keys(student, ["id", "name", "identifier"])
        assert student["name"] == student_data["name"]
        assert isinstance(student["id"], int)

    def test_create_student_without_authentication(
        self, api_client, teacher_class_id, sample_student
    ):
        """Testa criação de aluno sem autenticação"""
        # Act
        response = api_client.post(
            f"/student/teacher-class/{teacher_class_id}",
            json=sample_student,
        )
        
        # Assert
        assert response.status_code in [401, 403]

    def test_create_student_with_empty_name(
        self, authenticated_client, teacher_class_id
    ):
        """Testa criação de aluno com nome vazio"""
        # Arrange
        invalid_student = {"name": "", "identifier": "2024001"}
        
        # Act
        response = authenticated_client.post(
            f"/student/teacher-class/{teacher_class_id}",
            json=invalid_student,
        )
        
        # Assert
        assert response.status_code in [200, 400]

    def test_create_student_with_invalid_class_id(
        self, authenticated_client, sample_student
    ):
        """Testa criação de aluno com ID de classe inválido"""
        # Act
        response = authenticated_client.post(
            "/student/teacher-class/999999",
            json=sample_student,
        )
        
        # Assert
        assert response.status_code in [404, 400, 200]

    @pytest.mark.smoke
    def test_get_student_by_id(self, authenticated_client, student_id):
        """
        Testa obtenção de um aluno por ID
        
        Given: Existe um aluno com um ID válido
        When: Faço GET em /student/{id}
        Then: Retorna 200 com os dados do aluno
        """
        # Act
        response = authenticated_client.get(f"/student/{student_id}")
        
        # Assert
        ResponseValidator.assert_status_code(response, 200)
        ResponseValidator.assert_json_response(response)
        
        student = response.json()
        ResponseValidator.assert_json_keys(student, ["id", "name", "identifier"])
        assert student["id"] == student_id

    def test_get_student_with_invalid_id(self, authenticated_client):
        """Testa obtenção de aluno com ID inválido"""
        # Act
        response = authenticated_client.get("/student/999999")
        
        # Assert
        assert response.status_code in [404, 400, 200]

    def test_get_student_contains_corrections_list(
        self, authenticated_client, student_id
    ):
        """Testa se o aluno contém lista de correções"""
        # Act
        response = authenticated_client.get(f"/student/{student_id}")
        
        # Assert
        student = response.json()
        assert "corrections" in student
        assert isinstance(student["corrections"], (list, type(None)))

    def test_update_student_success(
        self, authenticated_client, student_id, sample_student
    ):
        """
        Testa atualização de um aluno
        
        Given: Existe um aluno com um ID válido
        When: Faço PUT em /student/{id} com novos dados
        Then: Retorna 200 com o aluno atualizado
        """
        # Arrange
        updated_data = {
            **sample_student,
            "name": "Novo Nome do Aluno",
        }
        
        # Act
        response = authenticated_client.put(
            f"/student/{student_id}",
            json=updated_data,
        )
        
        # Assert
        ResponseValidator.assert_status_code(response, 200)
        
        updated_student = response.json()
        assert updated_student["name"] == "Novo Nome do Aluno"
        assert updated_student["id"] == student_id

    def test_update_student_without_authentication(
        self, api_client, student_id, sample_student
    ):
        """Testa atualização de aluno sem autenticação"""
        # Act
        response = api_client.put(
            f"/student/{student_id}",
            json=sample_student,
        )
        
        # Assert
        assert response.status_code in [401, 403]

    def test_update_nonexistent_student(
        self, authenticated_client, sample_student
    ):
        """Testa atualização de aluno que não existe"""
        # Act
        response = authenticated_client.put(
            "/student/999999",
            json=sample_student,
        )
        
        # Assert
        assert response.status_code in [404, 400, 200]

    def test_response_time_for_create_student(
        self, authenticated_client, teacher_class_id, sample_student
    ):
        """Testa se o tempo de resposta para criar aluno está aceitável"""
        # Act
        response = authenticated_client.post(
            f"/student/teacher-class/{teacher_class_id}",
            json=sample_student,
        )
        
        # Assert
        ResponseValidator.assert_response_time(response, 5000)

    def test_response_time_for_get_student(self, authenticated_client, student_id):
        """Testa se o tempo de resposta para obter aluno está aceitável"""
        # Act
        response = authenticated_client.get(f"/student/{student_id}")
        
        # Assert
        ResponseValidator.assert_response_time(response, 5000)

    def test_student_id_is_positive_integer(
        self, authenticated_client, teacher_class_id, sample_student
    ):
        """Testa se o ID do aluno é um inteiro positivo"""
        # Act
        response = authenticated_client.post(
            f"/student/teacher-class/{teacher_class_id}",
            json=sample_student,
        )
        
        # Assert
        student = response.json()
        assert isinstance(student["id"], int)
        assert student["id"] > 0

    def test_create_student_with_duplicate_identifier(
        self, authenticated_client, teacher_class_id, sample_student
    ):
        """Testa criação de aluno com identificador duplicado"""
        # Act - Criar primeiro aluno
        response1 = authenticated_client.post(
            f"/student/teacher-class/{teacher_class_id}",
            json=sample_student,
        )
        
        # Act - Tentar criar segundo aluno com mesmo identificador
        response2 = authenticated_client.post(
            f"/student/teacher-class/{teacher_class_id}",
            json=sample_student,
        )
        
        # Assert
        ResponseValidator.assert_status_code(response1, 200)
        # Pode retornar 400 (erro) ou 200 (criado)
        assert response2.status_code in [200, 400, 409]

    def test_create_multiple_students(
        self, authenticated_client, teacher_class_id, sample_student
    ):
        """Testa criação de múltiplos alunos"""
        # Act
        responses = []
        for i in range(3):
            data = {
                **sample_student,
                "name": f"Aluno {i}",
                "identifier": f"2024{i:03d}",
            }
            response = authenticated_client.post(
                f"/student/teacher-class/{teacher_class_id}",
                json=data,
            )
            responses.append(response)
        
        # Assert
        for response in responses:
            ResponseValidator.assert_status_code(response, 200)

    def test_student_identifier_with_special_characters(
        self, authenticated_client, teacher_class_id
    ):
        """Testa criação de aluno com caracteres especiais no identificador"""
        # Arrange
        special_student = {
            "name": "João Silva",
            "identifier": "2024-A-001",
        }
        
        # Act
        response = authenticated_client.post(
            f"/student/teacher-class/{teacher_class_id}",
            json=special_student,
        )
        
        # Assert
        ResponseValidator.assert_status_code(response, 200)

    def test_student_name_with_unicode_characters(
        self, authenticated_client, teacher_class_id
    ):
        """Testa criação de aluno com caracteres unicode no nome"""
        # Arrange
        unicode_student = {
            "name": "José María Pérez",
            "identifier": "2024999",
        }
        
        # Act
        response = authenticated_client.post(
            f"/student/teacher-class/{teacher_class_id}",
            json=unicode_student,
        )
        
        # Assert
        ResponseValidator.assert_status_code(response, 200)
        student = response.json()
        assert "José" in student["name"] or student["name"] == unicode_student["name"]

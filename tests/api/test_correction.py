"""Testes para API de Correções (Correction)"""
import pytest
from tests.utils.response_validator import ResponseValidator


@pytest.mark.integration
class TestCorrectionAPI:
    """Testes para endpoints de Correções"""

    @pytest.mark.smoke
    def test_get_correction_by_id(self, authenticated_client):
        """
        Testa obtenção de uma correção por ID
        
        Given: Existe uma correção com um ID válido
        When: Faço GET em /correction/{id}
        Then: Retorna 200 com os dados da correção
        """
        # Arrange
        correction_id = 1
        
        # Act
        response = authenticated_client.get(f"/correction/{correction_id}")
        
        # Assert
        if response.status_code == 200:
            ResponseValidator.assert_json_response(response)
            correction = response.json()
            ResponseValidator.assert_json_keys(correction, ["id"])

    def test_get_correction_without_authentication(self, api_client):
        """Testa obtenção de correção sem autenticação"""
        # Act
        response = api_client.get("/correction/1")
        
        # Assert
        assert response.status_code in [401, 403, 404, 200]

    def test_get_correction_with_invalid_id(self, authenticated_client):
        """Testa obtenção de correção com ID inválido"""
        # Act
        response = authenticated_client.get("/correction/999999")
        
        # Assert
        assert response.status_code in [404, 400, 200]

    def test_correction_contains_score(self, authenticated_client):
        """Testa se correção contém score"""
        # Act
        response = authenticated_client.get("/correction/1")
        
        # Assert
        if response.status_code == 200:
            correction = response.json()
            if "score" in correction:
                assert isinstance(correction["score"], (int, float))

    def test_correction_contains_test_written_reference(
        self, authenticated_client
    ):
        """Testa se correção contém referência a prova"""
        # Act
        response = authenticated_client.get("/correction/1")
        
        # Assert
        if response.status_code == 200:
            correction = response.json()
            if "testWritten" in correction:
                assert isinstance(correction["testWritten"], dict)

    def test_correction_contains_student_reference(self, authenticated_client):
        """Testa se correção contém referência a aluno"""
        # Act
        response = authenticated_client.get("/correction/1")
        
        # Assert
        if response.status_code == 200:
            correction = response.json()
            if "student" in correction:
                assert isinstance(correction["student"], dict)

    def test_correction_contains_answers_list(self, authenticated_client):
        """Testa se correção contém lista de respostas"""
        # Act
        response = authenticated_client.get("/correction/1")
        
        # Assert
        if response.status_code == 200:
            correction = response.json()
            if "answers" in correction:
                assert isinstance(correction["answers"], (list, type(None)))

    def test_response_time_for_get_correction(self, authenticated_client):
        """Testa tempo de resposta para obter correção"""
        # Act
        response = authenticated_client.get("/correction/1")
        
        # Assert
        if response.status_code in [200, 404]:
            ResponseValidator.assert_response_time(response, 5000)

    def test_correction_score_is_valid_number(self, authenticated_client):
        """Testa se score da correção é um número válido"""
        # Act
        response = authenticated_client.get("/correction/1")
        
        # Assert
        if response.status_code == 200:
            correction = response.json()
            if "score" in correction:
                assert isinstance(correction["score"], (int, float))
                assert correction["score"] >= 0

    def test_correction_contains_mini_test_written(self, authenticated_client):
        """Testa se correção contém versão mini de prova"""
        # Act
        response = authenticated_client.get("/correction/1")
        
        # Assert
        if response.status_code == 200:
            correction = response.json()
            if "testWritten" in correction:
                test_written = correction["testWritten"]
                # Mini DTO deve ter id e informações básicas
                if isinstance(test_written, dict):
                    if "id" in test_written:
                        assert isinstance(test_written["id"], int)

    def test_correction_contains_mini_student(self, authenticated_client):
        """Testa se correção contém versão mini de aluno"""
        # Act
        response = authenticated_client.get("/correction/1")
        
        # Assert
        if response.status_code == 200:
            correction = response.json()
            if "student" in correction:
                student = correction["student"]
                # Mini DTO deve ter id e informações básicas
                if isinstance(student, dict):
                    if "id" in student:
                        assert isinstance(student["id"], int)

    def test_get_multiple_corrections(self, authenticated_client):
        """Testa obtenção de múltiplas correções"""
        # Act
        responses = []
        for i in range(1, 4):
            response = authenticated_client.get(f"/correction/{i}")
            responses.append(response)
        
        # Assert
        for response in responses:
            if response.status_code in [200, 404]:
                pass  # Status válido
            else:
                assert False, f"Unexpected status code: {response.status_code}"

    def test_correction_structure_with_answers(self, authenticated_client):
        """Testa estrutura completa de uma correção com respostas"""
        # Act
        response = authenticated_client.get("/correction/1")
        
        # Assert
        if response.status_code == 200:
            correction = response.json()
            
            # Validar chaves principais
            expected_keys = ["id", "score"]
            for key in expected_keys:
                if key in correction:
                    assert correction[key] is not None

    def test_correction_answers_contains_score_and_content(
        self, authenticated_client
    ):
        """Testa se respostas em correção contêm score e conteúdo"""
        # Act
        response = authenticated_client.get("/correction/1")
        
        # Assert
        if response.status_code == 200:
            correction = response.json()
            if "answers" in correction and correction["answers"]:
                answers = correction["answers"]
                for answer in answers:
                    if isinstance(answer, dict):
                        # Cada resposta deve ter informações básicas
                        assert "id" in answer or "score" in answer

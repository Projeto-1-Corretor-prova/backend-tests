"""Utilitários para validação de respostas"""
from typing import Any, Dict, List


class ResponseValidator:
    """Validador de respostas HTTP"""

    @staticmethod
    def assert_status_code(response, expected: int):
        """Valida código de status HTTP"""
        assert response.status_code == expected, (
            f"Expected status code {expected}, "
            f"got {response.status_code}. Response: {response.text}"
        )

    @staticmethod
    def assert_json_response(response):
        """Valida se a resposta é JSON válida"""
        try:
            response.json()
        except Exception as e:
            raise AssertionError(f"Response is not valid JSON: {e}")

    @staticmethod
    def assert_json_keys(response_json: Dict, keys: List[str]):
        """Valida se a resposta JSON contém as chaves esperadas"""
        response_data = response_json if isinstance(response_json, dict) else response_json[0]
        missing_keys = set(keys) - set(response_data.keys())
        assert not missing_keys, f"Missing keys in response: {missing_keys}"

    @staticmethod
    def assert_json_structure(response_json: Dict, structure: Dict):
        """Valida a estrutura aninhada da resposta JSON"""
        for key, value_type in structure.items():
            assert key in response_json, f"Key '{key}' not found in response"
            if isinstance(value_type, dict):
                ResponseValidator.assert_json_structure(response_json[key], value_type)
            else:
                assert isinstance(
                    response_json[key], value_type
                ), f"Key '{key}' should be {value_type}, got {type(response_json[key])}"

    @staticmethod
    def assert_header_present(response, header: str):
        """Valida se a resposta contém um header específico"""
        assert header in response.headers, f"Header '{header}' not found in response"

    @staticmethod
    def assert_response_time(response, max_time_ms: int):
        """Valida se o tempo de resposta está dentro do esperado"""
        elapsed_ms = response.elapsed.total_seconds() * 1000
        assert (
            elapsed_ms <= max_time_ms
        ), f"Response time {elapsed_ms}ms exceeds max {max_time_ms}ms"

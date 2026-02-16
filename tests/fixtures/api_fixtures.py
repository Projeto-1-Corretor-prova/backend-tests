import pytest
from tests.utils.api_client import APIClient
from config.settings import TEACHER_EMAIL, TEACHER_PASSWORD, TEACHER_NAME


@pytest.fixture
def api_client():
    """Fixture para cliente API"""
    client = APIClient()
    yield client
    client.close()


@pytest.fixture
def authenticated_client():
    """Fixture para cliente API autenticado"""
    client = APIClient()
    # Fazer login
    login_data = {
        "email": TEACHER_EMAIL,
        "password": TEACHER_PASSWORD,
        "name": TEACHER_NAME,
    }
    response = client.post("/teacher/login", json=login_data)
    if response.status_code == 200:
        token = response.json().get("acessToken")
        if token:
            client.session.headers.update({"Authorization": f"Bearer {token}"})
    yield client
    client.close()


# ============================================================================
# Teacher Fixtures
# ============================================================================


@pytest.fixture
def sample_login_data():
    """Fixture com dados de login"""
    return {
        "email": TEACHER_EMAIL,
        "password": TEACHER_PASSWORD,
        "name": TEACHER_NAME,
    }


# ============================================================================
# TeacherClass Fixtures
# ============================================================================


@pytest.fixture
def sample_teacher_class():
    """Fixture com dados de uma classe de professor"""
    return {
        "title": "Matemática - Turma A",
    }


@pytest.fixture
def teacher_class_id(authenticated_client, sample_teacher_class):
    """Fixture que cria e retorna um ID de classe"""
    response = authenticated_client.post("/teacher-class", json=sample_teacher_class)
    if response.status_code == 200:
        return response.json().get("id")
    return 1  # Fallback


# ============================================================================
# QuestionBank Fixtures
# ============================================================================


@pytest.fixture
def sample_question_bank():
    """Fixture com dados de um banco de questões"""
    return {
        "title": "Banco de Questões - Álgebra",
    }


@pytest.fixture
def question_bank_id(authenticated_client, sample_question_bank):
    """Fixture que cria e retorna um ID de banco de questões"""
    response = authenticated_client.post("/question-bank", json=sample_question_bank)
    if response.status_code == 200:
        return response.json().get("id")
    return 1  # Fallback


# ============================================================================
# Question Fixtures
# ============================================================================


@pytest.fixture
def sample_question():
    """Fixture com dados de uma questão"""
    return {
        "statement": "O que é álgebra?",
        "questionCriterias": [
            {
                "type": "KEYWORD",
                "criteria": "equação",
            },
            {
                "type": "SEMANTIC",
                "criteria": "estudo de operações matemáticas",
            },
        ],
    }


@pytest.fixture
def question_id(authenticated_client, question_bank_id, sample_question):
    """Fixture que cria e retorna um ID de questão"""
    response = authenticated_client.post(
        f"/question/question-bank/{question_bank_id}",
        json=sample_question,
    )
    if response.status_code == 200:
        return response.json().get("id")
    return 1  # Fallback


# ============================================================================
# QuestionCriteria Fixtures
# ============================================================================


@pytest.fixture
def sample_question_criteria():
    """Fixture com dados de um critério de questão"""
    return {
        "type": "KEYWORD",
        "criteria": "novo critério",
    }


# ============================================================================
# TestWritten Fixtures
# ============================================================================


@pytest.fixture
def sample_test_written():
    """Fixture com dados de uma prova escrita"""
    return {
        "title": "Avaliação 1 - Álgebra",
        "regexQuestionIdentifier": "^Q[0-9]{3}$",
    }


@pytest.fixture
def test_written_id(authenticated_client, teacher_class_id, sample_test_written):
    """Fixture que cria e retorna um ID de prova"""
    response = authenticated_client.post(
        f"/test-written/teacher-class/{teacher_class_id}",
        json=sample_test_written,
    )
    if response.status_code == 200:
        return response.json().get("id")
    return 1  # Fallback


# ============================================================================
# QuestionTestWritten Fixtures
# ============================================================================


@pytest.fixture
def sample_question_test_written():
    """Fixture com dados de uma questão em uma prova"""
    return {
        "weight": 2.5,
        "lines": 10,
    }


# ============================================================================
# Student Fixtures
# ============================================================================


@pytest.fixture
def sample_student():
    """Fixture com dados de um aluno"""
    return {
        "name": "João Silva",
        "identifier": "2024001",
    }


@pytest.fixture
def student_id(authenticated_client, teacher_class_id, sample_student):
    """Fixture que cria e retorna um ID de aluno"""
    response = authenticated_client.post(
        f"/student/teacher-class/{teacher_class_id}",
        json=sample_student,
    )
    if response.status_code == 200:
        return response.json().get("id")
    return 1  # Fallback


# ============================================================================
# Comment Fixtures
# ============================================================================


@pytest.fixture
def sample_comment():
    """Fixture com dados de um comentário"""
    return {
        "content": "Excelente resposta!",
    }


# ============================================================================
# Answer Fixtures
# ============================================================================


@pytest.fixture
def sample_answer():
    """Fixture com dados de uma resposta"""
    return {
        "studentAnswer": "A resposta do aluno para a questão",
        "score": 8.5,
    }


# ============================================================================
# Antigos Fixtures (mantendo compatibilidade)
# ============================================================================


@pytest.fixture
def sample_user():
    """Fixture com dados de exemplo de usuário"""
    return {
        "name": "João Silva",
        "email": "joao@example.com",
        "age": 30,
        "active": True,
    }


@pytest.fixture
def sample_product():
    """Fixture com dados de exemplo de produto"""
    return {
        "name": "Produto Exemplo",
        "price": 99.99,
        "description": "Descrição do produto",
        "stock": 100,
    }


@pytest.fixture
def sample_order():
    """Fixture com dados de exemplo de pedido"""
    return {
        "user_id": 1,
        "items": [
            {"product_id": 1, "quantity": 2},
            {"product_id": 2, "quantity": 1},
        ],
        "total": 199.98,
        "status": "pending",
    }

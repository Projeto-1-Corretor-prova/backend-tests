# Testes de API em Python com Requests

Estrutura profissional para testes de API em Python usando a biblioteca `requests` com `pytest`.

## 📋 Estrutura do Projeto

```
backend-tests/
├── config/
│   ├── __init__.py
│   └── settings.py          # Configurações globais
├── tests/
│   ├── __init__.py
│   ├── api/                 # Testes de endpoints
│   │   ├── __init__.py
│   │   ├── test_users.py
│   │   ├── test_products.py
│   │   └── test_orders.py
│   ├── fixtures/            # Dados para testes
│   │   ├── __init__.py
│   │   └── api_fixtures.py
│   └── utils/               # Utilitários
│       ├── __init__.py
│       ├── api_client.py    # Cliente HTTP
│       └── response_validator.py  # Validadores
├── conftest.py              # Configuração pytest
├── requirements.txt         # Dependências
├── .env.example             # Exemplo de variáveis
├── .gitignore
└── README.md
```

## 🚀 Instalação

### 1. Clone ou navegue até o repositório
```bash
cd backend-tests
```

### 2. Crie um ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente
```bash
cp .env.example .env
# Edite .env com suas configurações
```

## ⚙️ Configuração

Edite o arquivo `.env` com as configurações da sua API:

```env
# API Configuration
API_BASE_URL=http://localhost:3000
API_TIMEOUT=30

# Authentication
API_TOKEN=seu_token_aqui
API_KEY=sua_chave_aqui

# Environment
ENVIRONMENT=development
DEBUG=True
```

## 🧪 Executando os Testes

### Executar todos os testes
```bash
pytest
```

### Executar com verbosidade
```bash
pytest -v
```

### Executar apenas testes de smoke
```bash
pytest -m smoke
```

### Executar apenas testes de integração
```bash
pytest -m integration
```

### Executar um arquivo específico
```bash
pytest tests/api/test_users.py
```

### Executar uma classe específica
```bash
pytest tests/api/test_users.py::TestUsersAPI
```

### Executar um teste específico
```bash
pytest tests/api/test_users.py::TestUsersAPI::test_get_users_success
```

### Gerar relatório de cobertura
```bash
pytest --cov=tests
```

### Gerar relatório HTML de cobertura
```bash
pytest --cov=tests --cov-report=html
```

## 📚 Usando o Cliente API

### Exemplo básico
```python
from tests.utils.api_client import APIClient

client = APIClient()

# GET request
response = client.get("/users")

# POST request
response = client.post("/users", json={"name": "João", "email": "joao@example.com"})

# PUT request
response = client.put("/users/1", json={"name": "Novo Nome"})

# PATCH request
response = client.patch("/users/1", json={"name": "Atualizado"})

# DELETE request
response = client.delete("/users/1")

client.close()
```

### Usando como context manager
```python
from tests.utils.api_client import APIClient

with APIClient() as client:
    response = client.get("/users")
    print(response.json())
```

## ✅ Validadores de Resposta

```python
from tests.utils.response_validator import ResponseValidator

# Validar código de status
ResponseValidator.assert_status_code(response, 200)

# Validar JSON válido
ResponseValidator.assert_json_response(response)

# Validar chaves presentes
ResponseValidator.assert_json_keys(response.json(), ["id", "name", "email"])

# Validar estrutura aninhada
ResponseValidator.assert_json_structure(response.json(), {
    "id": int,
    "user": {
        "name": str,
        "email": str
    }
})

# Validar header presente
ResponseValidator.assert_header_present(response, "Content-Type")

# Validar tempo de resposta
ResponseValidator.assert_response_time(response, 2000)  # 2 segundos
```

## 📦 Fixtures Disponíveis

```python
def test_example(api_client, sample_user, sample_product, sample_order):
    # api_client: Cliente API pré-configurado
    # sample_user: Dados de teste de usuário
    # sample_product: Dados de teste de produto
    # sample_order: Dados de teste de pedido
    pass
```

## 🏷️ Marcadores de Teste

- `@pytest.mark.smoke` - Testes básicos de funcionalidade
- `@pytest.mark.integration` - Testes de integração
- `@pytest.mark.unit` - Testes unitários
- `@pytest.mark.regression` - Testes de regressão
- `@pytest.mark.slow` - Testes lentos

## 📝 Escrevendo Novos Testes

### Exemplo de teste bem estruturado
```python
import pytest
from tests.utils.response_validator import ResponseValidator

@pytest.mark.integration
class TestMyAPI:
    """Testes para meu endpoint"""

    @pytest.mark.smoke
    def test_get_data_success(self, api_client):
        """Testa obtenção de dados com sucesso"""
        # Arrange
        expected_status = 200
        
        # Act
        response = api_client.get("/data")
        
        # Assert
        ResponseValidator.assert_status_code(response, expected_status)
        ResponseValidator.assert_json_response(response)
        
        data = response.json()
        assert len(data) > 0
        assert "id" in data[0]
```

## 🔍 Dicas de Uso

1. **Organização**: Mantenha um arquivo de teste por endpoint principal
2. **Fixtures**: Use fixtures para dados reutilizáveis
3. **Validação**: Sempre valide status code e estrutura JSON
4. **Nomes descritivos**: Use nomes de testes que descrevam claramente o que testam
5. **AAA Pattern**: Organize testes em Arrange, Act, Assert
6. **Marcadores**: Use marcadores para categorizar testes

## 🛠️ Troubleshooting

### Erro: "ConnectionError"
Verifique se a API está rodando no endereço configurado em `.env`

### Erro: "CORS"
Verifique se a API permite requisições do seu cliente

### Erro: "Authentication Failed"
Verifique se o token em `.env` é válido

## 📖 Referências

- [Requests Documentation](https://docs.python-requests.org/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Python Dotenv](https://github.com/theskimmingstone/python-dotenv)

## 📄 Licença

MIT

---

**Criado em**: 16 de fevereiro de 2026

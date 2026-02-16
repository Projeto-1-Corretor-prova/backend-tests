# 📋 Sumário de Testes da API - Backend Tests

Estrutura completa de testes gerada a partir da API em `http://localhost:7999/swagger/index.html`

---

## ✅ Testes Criados por Endpoint

### 🧑‍🏫 Teacher (Autenticação)
**Arquivo**: `tests/api/test_teacher.py`

| Endpoint | Método | Testes |
|----------|--------|--------|
| `/teacher/login` | POST | Login sucesso, falha, dados incompletos |
| `/teacher/profile` | GET | Obtenção de perfil, autenticação obrigatória |

**Casos**: 10 testes incluindo validação de tokens, tempo de resposta, dados válidos

---

### 👥 Student (Alunos)
**Arquivo**: `tests/api/test_student.py`

| Endpoint | Método | Testes |
|----------|--------|--------|
| `/student/teacher-class/{id}` | POST | Criar aluno em classe |
| `/student/{id}` | GET | Obter dados do aluno |
| `/student/{id}` | PUT | Atualizar dados do aluno |

**Casos**: 17 testes incluindo validação de nomes unicode, identificadores únicos, duplicação

---

### 🏫 TeacherClass (Classes)
**Arquivo**: `tests/api/test_teacher_class.py`

| Endpoint | Método | Testes |
|----------|--------|--------|
| `/teacher-class` | POST | Criar classe |
| `/teacher-class/{id}` | GET | Obter dados da classe |
| `/teacher-class/{id}` | PUT | Atualizar dados da classe |

**Casos**: 14 testes incluindo validação de listas (alunos, provas), tempo de resposta

---

### 📚 QuestionBank (Banco de Questões)
**Arquivo**: `tests/api/test_question_bank.py`

| Endpoint | Método | Testes |
|----------|--------|--------|
| `/question-bank` | POST | Criar banco |
| `/question-bank/{id}` | GET | Obter dados do banco |
| `/question-bank/{id}` | PUT | Atualizar dados do banco |

**Casos**: 11 testes incluindo caracteres especiais, múltiplos bancos, validação de questões

---

### ❓ Question (Questões)
**Arquivo**: `tests/api/test_question.py`

| Endpoint | Método | Testes |
|----------|--------|--------|
| `/question/question-bank/{questionBankId}` | POST | Criar questão em banco |
| `/question/{id}` | GET | Obter dados da questão |
| `/question/{id}` | PUT | Atualizar dados da questão |

**Casos**: 15 testes incluindo múltiplos critérios, caracteres especiais, validação de enunciado

---

### ✔️ QuestionCriteria (Critérios de Questões)
**Arquivo**: `tests/api/test_question_criteria.py`

| Endpoint | Método | Testes |
|----------|--------|--------|
| `/question-criteria/question/{questionId}` | POST | Criar critério |
| `/question-criteria/{id}` | PUT | Atualizar critério |

**Casos**: 9 testes incluindo validação de enum (KEYWORD, SEMANTIC, EXAMPLE), limites de tamanho

---

### 📝 TestWritten (Provas Escritas)
**Arquivo**: `tests/api/test_test_written.py`

| Endpoint | Método | Testes |
|----------|--------|--------|
| `/test-written/teacher-class/{teacherClassId}` | POST | Criar prova |
| `/test-written/{id}` | GET | Obter dados da prova |
| `/test-written/{id}` | PUT | Atualizar dados da prova |

**Casos**: 13 testes incluindo weight total, regex identifier, listas de questões e correções

---

### 🔗 QuestionTestWritten (Questões em Provas)
**Arquivo**: `tests/api/test_question_test_written.py`

| Endpoint | Método | Testes |
|----------|--------|--------|
| `/question-test-written/question/{questionId}/test-written/{testWrittenId}` | POST | Associar questão a prova |
| `/question-test-written/{id}` | PUT | Atualizar associação |

**Casos**: 9 testes incluindo validação de peso e linhas, múltiplas questões, referências

---

### 💬 Comment (Comentários)
**Arquivo**: `tests/api/test_comment.py`

| Endpoint | Método | Testes |
|----------|--------|--------|
| `/comment/answers/{answerId}` | POST | Criar comentário em resposta |
| `/comment/{commentId}` | PUT | Atualizar comentário |

**Casos**: 9 testes incluindo caracteres especiais, conteúdo vazio, limites de tamanho

---

### 📋 Answer (Respostas)
**Arquivo**: `tests/api/test_answer.py`

| Endpoint | Método | Testes |
|----------|--------|--------|
| `/answer/{id}` | PUT | Atualizar resposta e pontuação |

**Casos**: 11 testes incluindo validação de score (0-100, negativo), respostas vazias, listas de comentários

---

### ✏️ Correction (Correções)
**Arquivo**: `tests/api/test_correction.py`

| Endpoint | Método | Testes |
|----------|--------|--------|
| `/correction/{id}` | GET | Obter dados da correção |

**Casos**: 12 testes incluindo validação de estrutura completa, referências mini DTOs, respostas

---

## 📊 Resumo Geral

| Recurso | Arquivo | Total de Testes |
|---------|---------|-----------------|
| Teacher | test_teacher.py | 10 |
| TeacherClass | test_teacher_class.py | 14 |
| QuestionBank | test_question_bank.py | 11 |
| Question | test_question.py | 15 |
| QuestionCriteria | test_question_criteria.py | 9 |
| TestWritten | test_test_written.py | 13 |
| QuestionTestWritten | test_question_test_written.py | 9 |
| Student | test_student.py | 17 |
| Comment | test_comment.py | 9 |
| Answer | test_answer.py | 11 |
| Correction | test_correction.py | 12 |
| **TOTAL** | **11 arquivos** | **130+ testes** |

---

## 🏷️ Marcadores Utilizados

- `@pytest.mark.smoke` - Testes rápidos e essenciais (17 testes)
- `@pytest.mark.integration` - Testes de integração com a API (120+ testes)

---

## 🔐 Autenticação

Todos os endpoints exceto `/teacher/login` exigem autenticação:
- Use a fixture `authenticated_client` para testes autenticados
- Use `api_client` para testar falhas de autenticação

**Credenciais configuradas em `.env`**:
```
TEACHER_EMAIL=teacher@example.com
TEACHER_PASSWORD=password123
TEACHER_NAME=Teacher
```

---

## 🛠️ Como Executar

### Executar todos os testes
```bash
pytest
```

### Executar apenas testes de smoke
```bash
pytest -m smoke
```

### Executar testes de um recurso específico
```bash
pytest tests/api/test_teacher.py -v
```

### Executar com cobertura
```bash
pytest --cov=tests
```

### Usar Makefile
```bash
make test              # Todos os testes
make test-smoke        # Apenas smoke
make test-integration  # Apenas integration
make coverage          # Com cobertura
```

---

## ✨ Padrões Aplicados

✅ **Padrão AAA** - Arrange, Act, Assert em todos os testes
✅ **Nomes Descritivos** - Cada teste descreve claramente o que testam
✅ **Fixtures Reutilizáveis** - Dados compartilhados entre testes
✅ **Validação Completa** - Status code, JSON, chaves, tipos, tempo de resposta
✅ **Casos Positivos e Negativos** - Testes de sucesso e falha
✅ **Parametrização** - Testes repetitivos com `@pytest.mark.parametrize`
✅ **Organizados por Recursos** - Um arquivo por entidade principal
✅ **Tratamento de Erros** - Validação de 401, 403, 404, 400, 500

---

## 📋 Verificações Incluídas

Por padrão, cada teste valida:

1. **Status HTTP** - Códigos de resposta apropriados
2. **JSON Válido** - Resposta em formato JSON correto
3. **Estrutura de Dados** - Chaves esperadas presentes
4. **Tipos de Dados** - Campos com tipos corretos (int, string, bool, etc)
5. **Valores de Negócio** - Dados correspondem ao esperado
6. **Tempo de Resposta** - Performance dentro de limite (5s por padrão)
7. **Autenticação** - Endpoints protegidos rejeitam requisições não autenticadas
8. **Validação de Entrada** - Rejeição de dados inválidos

---

## 🔍 Casos de Teste Adicionais

Além dos testes CRUD básicos, foram incluídos:

- ✅ Validação de enums (CriteriaEnum: KEYWORD, SEMANTIC, EXAMPLE)
- ✅ Caracteres especiais e unicode em nomes
- ✅ Valores extremos (strings muito longas, números negativos)
- ✅ Identificadores únicos e duplicação
- ✅ Referências entre entidades (mini DTOs)
- ✅ Listas e arrays aninhadas
- ✅ Peso e linhas em questões
- ✅ Pontuação de respostas (0-100)
- ✅ Regex identifier para provas
- ✅ Comentários de IA vs. professor

---

## 📚 Estrutura de Fixtures

Disponíveis em `tests/fixtures/api_fixtures.py`:

- `api_client` - Cliente HTTP não autenticado
- `authenticated_client` - Cliente com token de autenticação
- `sample_login_data` - Credenciais de teste
- `sample_teacher_class` - Dados de classe
- `sample_question_bank` - Dados de banco de questões
- `sample_question` - Dados de questão com critérios
- `sample_question_criteria` - Dados de critério
- `sample_test_written` - Dados de prova
- `sample_student` - Dados de aluno
- `sample_comment` - Dados de comentário
- `sample_answer` - Dados de resposta
- IDs dinâmicos (teacher_class_id, question_bank_id, etc)

---

## 🎯 Próximos Passos

1. **Executar testes localmente**
   ```bash
   make setup
   pytest tests/api/test_teacher.py::TestTeacherAPI::test_teacher_login_success
   ```

2. **Adaptar credenciais** - Configure `.env` com suas credenciais reais

3. **Executar suite completa** - `pytest tests/`

4. **Gerar relatório** - `pytest --cov=tests --cov-report=html`

5. **Adicionar novos testes** - Use os templates em `TEMPLATE_NOVO_ENDPOINT.md`

---

## 📞 Suporte

Para entender melhor os testes:
- Veja `BEST_PRACTICES.md` para padrões Python
- Veja `TEMPLATE_NOVO_ENDPOINT.md` para adicionar novos
- Veja `README.md` para uso geral

**Gerado em**: 16 de fevereiro de 2026  
**API**: http://localhost:7999  
**Total de Testes**: 130+

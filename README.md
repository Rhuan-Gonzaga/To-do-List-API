# To-Do List API com Flask

Esta é uma API RESTful desenvolvida com **Python (Flask)** que permite gerenciamento de tarefas (To-Do) com autenticação JWT. Usuários podem se cadastrar, fazer login e realizar operações de CRUD em tarefas associadas a suas contas.

---

## 🚀 Tecnologias Utilizadas

- Python 
- Flask
- Flask-JWT-Extended
- Flask-SQLAlchemy
- Marshmallow
- MySQL
- Werkzeug

---

## 📦 Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/Rhuan-Gonzaga/To-do-List-API.git
cd To-do-List-API
```

### 2. Crie e ative o ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\\Scripts\\activate   # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure o banco de dados

Edite o arquivo `config.py` com as seguintes configurações:

```python
SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
SECRET_KEY = 'sua_chave_secreta'
JWT_SECRET_KEY = 'sua_chave_jwt'
```

Crie o banco:

```bash
flask db init
flask db migrate
flask db upgrade
```

---

## 🧪 Rodando a API

```bash
flask run
```

A API estará disponível em:  
`http://localhost:5000/`

---

## 🔐 Autenticação JWT

Após o login, envie o token no header:

```http
Authorization: Bearer <seu_token>
```

---

## 📘 Endpoints

### 🧑 Usuário

- `POST /signup` – Criar um novo usuário  
  **Body JSON:**
  ```json
  {
    "username": "usuario",
    "password": "senha"
  }
  ```

- `POST /login` – Login do usuário  
  **Body JSON:**
  ```json
  {
    "username": "usuario",
    "password": "senha"
  }
  ```

---

### ✅ Tarefas

**Todos os endpoints abaixo requerem token JWT no header.**

- `GET /tasks/` – Retorna todas as tarefas do usuário logado
- `GET /tasks/<id>` – Retorna uma tarefa específica do usuário
- `GET /tasks/status/<status>` – Retorna tarefas por status (`pendente`, `em andamento`, `concluída`)
- `POST /tasks/create` – Criar uma nova tarefa  
  **Body JSON:**
  ```json
  {
    "title": "Estudar Flask",
    "description": "Ler a documentação oficial",
    "status": "pendente"
  }
  ```
- `PUT /tasks/update/<id>` – Atualizar uma tarefa  
  **Body JSON:**
  ```json
  {
    "title": "Estudar JWT",
    "status": "em andamento"
  }
  ```
- `DELETE /tasks/delete/<id>` – Deletar uma tarefa

---


## 🧪 Testes

Você pode criar testes automatizados com `pytest`:

```bash
pip install pytest
PYTHONPATH=. pytest tests/
```

---

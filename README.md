# 🏢 SalaFácil API

API REST para gerenciamento de salas de reunião e reservas. Permite cadastrar salas, filtrar por capacidade, desativar salas e fazer reservas por dia, com validação de regras de negócio. Construída com FastAPI, SQLAlchemy e PostgreSQL.

---

## ⚙️ Funcionalidades

- Cadastro, listagem, busca e remoção de salas
- Filtro de salas por capacidade mínima
- Desativação de salas (uma sala desativada não aceita novas reservas)
- Reservas de sala por data, com validação de regras de negócio
- Cancelamento de reservas
- Consulta de uma sala com todas as suas reservas aninhadas
- Documentação interativa automática via Swagger

---

## 📐 Regras de negócio

Ao criar uma reserva, a API valida, nesta ordem:

| Regra | Status |
|---|:---:|
| A sala precisa existir | `404` |
| A sala precisa estar ativa | `400` |
| A quantidade de pessoas não pode ultrapassar a capacidade da sala | `400` |
| A sala não pode ter outra reserva na mesma data | `400` |

Além disso:
- Toda sala é criada como ativa; o status é controlado pela API, não pelo cliente
- Uma sala já desativada não pode ser desativada novamente (`400`)
- Ao remover uma sala, suas reservas são removidas junto (cascade)

---

## 🗂️ Entidades

- **Sala:** id, nome, capacidade, ativa
- **Reserva:** id, sala_id (FK), responsavel, data, quantidade_pessoas

```
Sala ──1:N── Reserva
```

---

## 🔌 Endpoints

| Método | Rota | Descrição |
|---|---|---|
| POST | `/salas/` | Cadastra uma sala |
| GET | `/salas/` | Lista as salas |
| GET | `/salas/?capacidade_minima=10` | Lista salas com capacidade mínima |
| GET | `/salas/{id}` | Busca uma sala |
| PUT | `/salas/{id}/desativar` | Desativa uma sala |
| DELETE | `/salas/{id}` | Remove uma sala e suas reservas |
| POST | `/reservas/` | Cria uma reserva |
| GET | `/reservas/` | Lista as reservas |
| DELETE | `/reservas/{id}` | Cancela uma reserva |
| GET | `/salas/{id}/reservas` | Retorna a sala com suas reservas |

---

## 🛠️ Tecnologias

- Python
- FastAPI
- SQLAlchemy (ORM)
- Pydantic
- PostgreSQL
- Uvicorn

---

## 🚀 Como executar

Pré-requisitos: Python 3 e PostgreSQL instalados.

**1. Clone o repositório:**
```bash
git clone https://github.com/guiamorim0/salafacil.git
cd salafacil
```

**2. Instale as dependências:**
```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary pydantic python-dotenv
```

**3. Crie o banco no PostgreSQL:**
```sql
CREATE DATABASE salafacil;
```

**4. Crie um arquivo `.env` na raiz:**
```
DATABASE_URL=postgresql://usuario:senha@localhost/salafacil
```

**5. Suba a API:**
```bash
uvicorn main:app --reload
```

**6. Acesse a documentação:**
```
http://localhost:8000/docs
```

---

## 📂 Estrutura

```
salafacil/
├── database.py   # Conexão com o banco
├── models.py     # Modelos SQLAlchemy (Sala, Reserva)
├── schemas.py    # Schemas Pydantic
├── main.py       # Endpoints
├── .env          # Variáveis de ambiente (não versionado)
└── .gitignore
```

---

## 🧠 Conceitos aplicados

- Arquitetura em camadas (conexão, models, schemas, rotas)
- Relacionamento 1:N com cascade delete
- Filtro dinâmico por query parameter opcional
- Validação de duplicidade com consulta de múltiplas condições
- Diferenciação entre `404` (recurso inexistente) e `400` (operação inválida)
- Campos controlados pelo servidor, fora do schema de criação
- Carregamento otimizado de dados relacionados com `joinedload`

---

## 👤 Autor

**Guilherme Zanchetti Amorim** — Estudante de Engenharia de Software (FIAP)

- GitHub: [github.com/guiamorim0](https://github.com/guiamorim0)
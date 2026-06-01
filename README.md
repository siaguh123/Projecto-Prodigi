# SIAGUH — Sistema Integrado de Apoio à Gestão de Urgências Hospitalares

Aplicação web desenvolvida em **FastAPI** com base de dados **PostgreSQL**, containerizada com **Podman**.

---

## Pré-requisitos

Instalar apenas uma ferramenta:

- **Podman Desktop** — [https://podman.io/getting-started/installation](https://podman.io/getting-started/installation)

> Se preferir Docker, o `docker-compose` também é compatível — substitua `podman-compose` por `docker-compose` nos comandos abaixo.

---

## Instalação e arranque

### 1. Clonar o repositório

```bash
git clone <URL_DO_REPOSITORIO>
cd Project_final
```

### 2. Arrancar os contentores

```bash
podman-compose up -d
```

Isto inicia dois contentores:
- `hospital_db_container` — PostgreSQL na porta **5433**
- `hospital_app_container` — Aplicação FastAPI na porta **8000**

### 3. Carregar a base de dados

Aguardar ~5 segundos para o PostgreSQL estar pronto e depois executar:

```bash
podman exec -i hospital_db_container psql -U user_admin -d hospital_db < hospital_db_dump.sql
```

### 4. Aceder à aplicação

Abrir o browser em: **http://localhost:8000**

---

## Credenciais de acesso

| Perfil          | Username    | Password       |
|-----------------|-------------|----------------|
| Administrador   | `admin`     | `admin123`     |
| Médico          | `dr.silva`  | `medico123`    |
| Enfermeiro      | `enf.ana`   | `enfermeiro123`|
| Rececionista    | `rec.joao`  | `rececao123`   |

---

## Parar a aplicação

```bash
podman-compose down
```

---

## Estrutura do projeto

```
Project_final/
├── main.py               # Aplicação FastAPI (rotas e lógica)
├── models.py             # Modelos da base de dados (SQLAlchemy)
├── schemas.py            # Schemas de validação (Pydantic)
├── crud.py               # Operações CRUD
├── auth.py               # Autenticação e passwords
├── database.py           # Ligação à base de dados
├── anonimizacao.py       # Exportação de dados anonimizados
├── seed.py               # Dados de teste
├── ia/                   # Módulo de inteligência artificial
├── templates/            # Interface web (HTML/Jinja2)
├── hospital_db_dump.sql  # Dump da base de dados com dados de teste
├── podman-compose.yml    # Configuração dos contentores
└── dockerfile            # Imagem da aplicação
```

---

## Tecnologias utilizadas

| Componente | Tecnologia |
|------------|------------|
| Backend | FastAPI (Python 3.13) |
| Base de dados | PostgreSQL 15 |
| ORM | SQLAlchemy |
| Autenticação | bcrypt + JWT |
| Interface | Jinja2 Templates |
| IA | scikit-learn |
| Containerização | Podman / Docker |

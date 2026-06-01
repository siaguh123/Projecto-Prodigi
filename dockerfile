# 1. Usar a imagem oficial do Python 3.13 (versão slim para ser mais leve)
FROM python:3.13-slim

# 2. Instalar o gestor 'uv' que já está a usar no seu projeto
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# 3. Definir a pasta de trabalho dentro do contentor
WORKDIR /app

# 4. Copiar os ficheiros de dependências (que já tem na sua pasta)
COPY pyproject.toml uv.lock ./

# 5. Instalar as dependências (FastAPI, SQLAlchemy, etc.) de forma rápida
RUN uv sync --frozen --no-install-project

# 6. Copiar todo o código do projeto (incluindo as pastas templates e static)
COPY . .

# 7. Expor a porta 8000 (onde o FastAPI vai rodar)
EXPOSE 8000

# 8. Comando para iniciar o servidor uvicorn através do uv
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]









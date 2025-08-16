# Python slim para imagem leve
FROM python:3.11-slim

# Dependências do sistema mínimas (gcc/headers só se precisar compilar bcrypt)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libffi-dev && \
    rm -rf /var/lib/apt/lists/*

# Workdir
WORKDIR /app

# Copiar somente requirements primeiro (melhor cache)
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copiar restante do projeto
COPY . /app

# Variáveis padrão (override em produção)
ENV FLASK_APP=wsgi.py \
    FLASK_ENV=development \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Expor porta
EXPOSE 5000

# Comando: preparar DB (se não existir) e subir
# Obs: se 'migrations/' não existir, roda init+migrate+upgrade
CMD bash -lc '\
if [ ! -d "migrations" ]; then \
  flask db init && flask db migrate -m "init: users"; \
fi; \
flask db upgrade && flask run --host=0.0.0.0 --port=5000'

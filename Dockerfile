FROM python:3.10-slim

WORKDIR /app

COPY . .

# Instala apenas o necessário para compilar se precisar
RUN apt-get update && \
    apt-get install -y gcc g++ cmake && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get remove -y gcc g++ cmake && \
    apt-get autoremove -y && \
    apt-get clean

# Garante a pasta do modelo
RUN mkdir -p modelo

# Gera base de conhecimento
RUN python3 app/gerar_conhecimento.py

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Usa imagem leve com Python
FROM python:3.10-slim

# Define diretório de trabalho
WORKDIR /app

# Copia arquivos do projeto (inclusive a pasta app/conhecimento)
COPY . .

# Instala dependências do sistema e pacotes Python
RUN apt-get update && \
    apt-get install -y wget gcc g++ cmake && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get remove -y gcc g++ cmake && \
    apt-get autoremove -y && \
    apt-get clean

# Expõe porta da API
EXPOSE 8000

# Inicia a API FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

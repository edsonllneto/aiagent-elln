# Usa imagem leve com Python
FROM python:3.10-slim

# Define diretório de trabalho
WORKDIR /app

# Copia todos os arquivos do projeto para o container
COPY . .

# Copia a pasta de conhecimento do GitHub para um diretório seguro (não sobrescrito pelo volume)
COPY app/backup_conhecimento /app/app/conhecimento

# Instala dependências do sistema e pacotes Python
RUN apt-get update && \
    apt-get install -y wget gcc g++ cmake && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get remove -y gcc g++ cmake && \
    apt-get autoremove -y && \
    apt-get clean

# Expõe a porta da API
EXPOSE 8000

# Inicia a aplicação FastAPI com Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

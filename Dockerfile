# Usa imagem base leve com Python
FROM python:3.10-slim

# Define diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos do projeto para o container
COPY . .

# Instala dependências do sistema e Python
RUN apt-get update && \
    apt-get install -y wget gcc g++ cmake && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Garante que a pasta do modelo existe (modelo será enviado manualmente)
RUN mkdir -p modelo

# Gera a base de conhecimento
RUN python3 app/gerar_conhecimento.py

# Expõe a porta da API
EXPOSE 8000

# Inicia a API FastAPI com Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

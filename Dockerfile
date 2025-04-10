# Usa imagem leve com Python
FROM python:3.10-slim

# Define diretório de trabalho
WORKDIR /app

# Copia arquivos do projeto
COPY . .

# Instala dependências do sistema e Python
RUN apt-get update && \
    apt-get install -y wget gcc g++ cmake && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir gdown && \
    apt-get remove -y gcc g++ cmake && \
    apt-get autoremove -y && \
    apt-get clean

# Cria diretório do modelo e baixa o arquivo via Google Drive
RUN mkdir -p modelo && \
    gdown https://drive.google.com/uc?id=1lhxoUMyKeOkpvchbjihIGTCEbV3x_Bt9 -O modelo/phi2.gguf

# Gera a base de conhecimento
RUN python3 app/gerar_conhecimento.py

# Expõe porta da API
EXPOSE 8000

# Inicia a API FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

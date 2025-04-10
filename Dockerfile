FROM python:3.10-slim

WORKDIR /app

COPY . .

# Instala somente utilitário para baixar o modelo
RUN apt-get update && \
    apt-get install -y wget && \
    pip install --no-cache-dir gdown && \
    apt-get clean

# Cria diretório do modelo e baixa o arquivo via Google Drive
RUN mkdir -p modelo && \
    gdown https://drive.google.com/uc?id=1lhxoUMyKeOkpvchbjihIGTCEbV3x_Bt9 -O modelo/phi2.gguf

# Gera a base de conhecimento
RUN python3 app/gerar_conhecimento.py

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

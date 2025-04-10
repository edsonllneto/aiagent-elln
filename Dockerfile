# Usa imagem leve com Python
FROM python:3.10-slim

# Define diretório de trabalho
WORKDIR /app

# Copia arquivos do projeto
COPY . .

# Instala dependências do sistema
RUN apt-get update && \
    apt-get install -y wget gcc g++ cmake

# Instala pacotes Python
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir gdown

# Remove ferramentas de build para deixar imagem mais leve
RUN apt-get remove -y gcc g++ cmake && \
    apt-get autoremove -y && \
    apt-get clean

# Baixa o modelo Phi-2
RUN mkdir -p modelo && \
    gdown https://drive.google.com/uc?id=1lhxoUMyKeOkpvchbjihIGTCEbV3x_Bt9 -O modelo/phi2.gguf

# Expõe porta da API
EXPOSE 8000

# Inicia a API FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Usar imagem oficial leve com Python
FROM python:3.10-slim

# Diretório de trabalho no container
WORKDIR /app

# Copia todos os arquivos do projeto para dentro do container
COPY . .

# Instala pacotes necessários do sistema e Python
RUN apt-get update && apt-get install -y wget && \
    pip install --no-cache-dir -r requirements.txt

# Baixa automaticamente o modelo GGUF
RUN mkdir -p modelo && \
    wget https://huggingface.co/TheBloke/gemma-2b-it-GGUF/resolve/main/gemma-2b-it.Q4_K_M.gguf -O modelo/gemma.gguf

# Gera a base FAISS a partir dos documentos
RUN python3 app/gerar_base.py

# Expor a porta da API
EXPOSE 8000

# Comando para iniciar a API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

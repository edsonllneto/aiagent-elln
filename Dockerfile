FROM python:3.10-slim

WORKDIR /app

# Copia tudo antes da instalação
COPY . .

# Instala compiladores e dependências para build do llama-cpp-python
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc g++ cmake wget && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get purge -y --auto-remove gcc g++ cmake wget && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /root/.cache/pip

# Cria pasta do modelo
RUN mkdir -p modelo

# Gera a base de conhecimento (ajuste o script se necessário)
RUN python3 app/gerar_conhecimento.py

EXPOSE 8000

# Inicia a API com Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

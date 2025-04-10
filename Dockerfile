FROM python:3.10-slim

WORKDIR /app

COPY . .

# Instala apenas o gdown e baixa o modelo
RUN pip install gdown && \
    mkdir -p modelo && \
    gdown https://drive.google.com/uc?id=1lhxoUMyKeOkpvchbjihIGTCEbV3x_Bt9 -O modelo/phi2.gguf

# Gera a base de conhecimento
RUN python3 app/gerar_conhecimento.py

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

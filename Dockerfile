FROM python:3.10-slim

WORKDIR /app

COPY . .

# Instala dependências Python (sem precisar gcc/g++/cmake)
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

RUN mkdir -p modelo

RUN python3 app/gerar_conhecimento.py

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

FROM python:3.10-slim

WORKDIR /app

COPY . .

# Dependências já instaladas no container anterior, então você pode manter comentado:
# RUN pip install --upgrade pip && \
#     pip install --no-cache-dir -r requirements.txt

# Não roda o script aqui, pois ele falhou no último build
# RUN python3 app/gerar_conhecimento.py

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

FROM python:3.10-slim

# Define diretório de trabalho
WORKDIR /app

# Copia tudo para dentro da imagem
COPY . /app

# Instala dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Comando padrão do container
CMD ["sleep", "infinity"]

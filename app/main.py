from fastapi import FastAPI, Query
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.llms import LlamaCpp
import os
import subprocess
import shutil

app = FastAPI()

# Caminho e ID do modelo
modelo_path = "modelo/phi2.gguf"
modelo_drive_id = "1lhxoUMyKeOkpvchbjihIGTCEbV3x_Bt9"

# Cria a pasta do modelo se não existir
os.makedirs(os.path.dirname(modelo_path), exist_ok=True)

# Baixa o modelo do Google Drive com gdown (se não existir)
if not os.path.exists(modelo_path):
    print("🔽 Baixando modelo phi2.gguf do Google Drive...")
    subprocess.run([
        "gdown",
        f"https://drive.google.com/uc?id={modelo_drive_id}",
        "-O", modelo_path
    ])
    print("✅ Modelo baixado com sucesso!")

# Caminhos para conhecimento
origem_backup = "/app/backup_conhecimento"
destino_conhecimento = "/app/conhecimento"

# Garante que a pasta de destino exista
os.makedirs(destino_conhecimento, exist_ok=True)

# Copia os arquivos de conhecimento para o volume, se estiver vazio
try:
    if os.path.exists(origem_backup) and not os.listdir(destino_conhecimento):
        print("📁 Volume de conhecimento está vazio. Copiando arquivos iniciais...")
        shutil.copytree(origem_backup, destino_conhecimento, dirs_exist_ok=True)
        print("✅ Arquivos de conhecimento copiados.")
except Exception as e:
    print(f"❌ Erro ao copiar conhecimento: {e}")

# Carrega modelo de embeddings e FAISS index
embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = FAISS.load_local(os.path.join(destino_conhecimento, "embeddings"), embedding, allow_dangerous_deserialization=True)

# Cria o wrapper para LlamaCpp
llm = LlamaCpp(
    model_path=modelo_path,
    n_ctx=1024,
    n_batch=128,
    n_threads=1,
    temperature=0.7,
    max_tokens=300,
    verbose=False
)

# QA com base vetorial
qa = RetrievalQA.from_chain_type(llm=llm, retriever=db.as_retriever())

@app.get("/")
def root():
    return {"status": "online"}

@app.get("/chat")
def chat(q: str = Query(..., description="Pergunta do usuário")):
    resposta = qa.run(q)
    return {"resposta": resposta}

from fastapi import FastAPI, Query
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.llms import LlamaCpp
import os
import subprocess
import shutil

app = FastAPI()

# === MODELO ===
modelo_path = "modelo/phi2.gguf"
modelo_drive_id = "1lhxoUMyKeOkpvchbjihIGTCEbV3x_Bt9"
os.makedirs(os.path.dirname(modelo_path), exist_ok=True)

if not os.path.exists(modelo_path):
    print("🔽 Baixando modelo phi2.gguf do Google Drive...")
    subprocess.run([
        "gdown",
        f"https://drive.google.com/uc?id={modelo_drive_id}",
        "-O", modelo_path
    ])
    print("✅ Modelo baixado com sucesso!")

# === CONHECIMENTO ===
volume_conhecimento = "/app/conhecimento"
repositorio_conhecimento = "/app/app/conhecimento"  # <- pasta vinda do GitHub

# Se o volume estiver vazio, copia os arquivos do repositório
if os.path.exists(repositorio_conhecimento) and not os.listdir(volume_conhecimento):
    print("📁 Volume de conhecimento está vazio. Copiando arquivos iniciais...")
    shutil.copytree(repositorio_conhecimento, volume_conhecimento, dirs_exist_ok=True)
    print("✅ Arquivos de conhecimento copiados com sucesso!")

# === VETORES E EMBEDDINGS ===
embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
caminho_embeddings = os.path.join(volume_conhecimento, "embeddings")
db = FAISS.load_local(caminho_embeddings, embedding, allow_dangerous_deserialization=True)

# === LLM ===
llm = LlamaCpp(
    model_path=modelo_path,
    n_ctx=1024,
    n_batch=128,
    n_threads=1,
    temperature=0.7,
    max_tokens=300,
    verbose=False
)

qa = RetrievalQA.from_chain_type(llm=llm, retriever=db.as_retriever())

# === ROTAS ===
@app.get("/")
def root():
    return {"status": "online"}

@app.get("/chat")
def chat(q: str = Query(..., description="Pergunta do usuário")):
    resposta = qa.run(q)
    return {"resposta": resposta}

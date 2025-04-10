from fastapi import FastAPI, Query
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.llms import LlamaCpp
import os
import subprocess
import shutil

app = FastAPI()

# Caminhos importantes
modelo_path = "modelo/phi2.gguf"
modelo_drive_id = "1lhxoUMyKeOkpvchbjihIGTCEbV3x_Bt9"
origem_backup = "/app/backup_conhecimento"
destino_conhecimento = "/app/conhecimento"
caminho_embeddings = os.path.join(destino_conhecimento, "embeddings")
index_faiss_path = os.path.join(caminho_embeddings, "index.faiss")

# Cria a pasta do modelo se não existir
os.makedirs(os.path.dirname(modelo_path), exist_ok=True)

# Baixa o modelo se não existir
if not os.path.exists(modelo_path):
    print("🔽 Baixando modelo phi2.gguf do Google Drive...")
    subprocess.run([
        "gdown",
        f"https://drive.google.com/uc?id={modelo_drive_id}",
        "-O", modelo_path
    ])
    print("✅ Modelo baixado com sucesso!")

# Cria pasta do volume conhecimento, se não existir
os.makedirs(destino_conhecimento, exist_ok=True)

# Só copia do backup se o index ainda não existe
if os.path.exists(origem_backup) and not os.path.exists(index_faiss_path):
    print("📁 Nenhuma base de conhecimento encontrada. Copiando arquivos de exemplo...")
    shutil.copytree(origem_backup, destino_conhecimento, dirs_exist_ok=True)
    print("✅ Arquivos padrão copiados para o volume.")

# Carrega modelo de embeddings e FAISS index
embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = FAISS.load_local(caminho_embeddings, embedding, allow_dangerous_deserialization=True)

# Configura modelo LlamaCpp (Phi-2)
llm = LlamaCpp(
    model_path=modelo_path,
    n_ctx=1024,
    n_batch=128,
    n_threads=1,
    temperature=0.7,
    max_tokens=300,
    verbose=False
)

# Cria chain de QA
qa = RetrievalQA.from_chain_type(llm=llm, retriever=db.as_retriever())

@app.get("/")
def root():
    return {"status": "online"}

@app.get("/chat")
def chat(q: str = Query(..., description="Pergunta do usuário")):
    resposta = qa.run(q)
    return {"resposta": resposta}

from fastapi import FastAPI, Query
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.llms import LlamaCpp
import os
import subprocess

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

# Load embedding model and FAISS index
embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = FAISS.load_local("conhecimento/embeddings", embedding, allow_dangerous_deserialization=True)

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

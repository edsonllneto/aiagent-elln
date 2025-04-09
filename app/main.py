from fastapi import FastAPI, Query
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.llms import LlamaCpp
import os

app = FastAPI()

# Load embedding model and FAISS index
embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = FAISS.load_local("app/embeddings", embedding)

# Caminho do modelo Phi-2 GGUF (já deve estar no servidor)
modelo_path = "modelo/phi2.gguf"

# Cria o wrapper para LlamaCpp
llm = LlamaCpp(
    model_path=modelo_path,
    n_ctx=1024,
    n_batch=128,
    n_threads=2,
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

from fastapi import FastAPI, Query
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.llms import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch

app = FastAPI()

# Load embedding model and FAISS index
embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = FAISS.load_local("app/embeddings", embedding)

# Load LLM (Gemma 2B quantizado via llama.cpp não entra aqui; isso é pra modelo local via transformers)
model_id = "google/gemma-2b-it"  # caso use Transformers
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.float16, device_map="auto")

pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, max_new_tokens=300)
llm = HuggingFacePipeline(pipeline=pipe)

qa = RetrievalQA.from_chain_type(llm=llm, retriever=db.as_retriever())

@app.get("/")
def root():
    return {"status": "online"}

@app.get("/chat")
def chat(q: str = Query(..., description="Pergunta do usuário")):
    resposta = qa.run(q)
    return {"resposta": resposta}

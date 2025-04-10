from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
import os

print("📄 [1] Lendo arquivo de conhecimento...")
try:
    with open("conhecimento/conhecimento.txt", "r", encoding="utf-8") as f:
        conteudo = f.read()
except FileNotFoundError:
    print("❌ Arquivo 'conhecimento/conhecimento.txt' não encontrado.")
    exit(1)

print("🔪 [2] Dividindo texto em chunks...")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = text_splitter.split_text(conteudo)
print(f"🧩 Total de chunks gerados: {len(chunks)}")

if not chunks:
    print("⚠️ Nenhum chunk foi gerado. Verifique o conteúdo do arquivo.")
    exit(1)

print("📚 [3] Convertendo chunks em documentos...")
docs = [Document(page_content=chunk) for chunk in chunks]

print("🧠 [4] Gerando embeddings...")
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

print("📦 [5] Criando base vetorial FAISS...")
db = FAISS.from_documents(docs, embedding_model)

print("💾 [6] Salvando base em conhecimento/embeddings...")
save_path = "conhecimento/embeddings"
os.makedirs(save_path, exist_ok=True)
db.save_local(save_path)

print("✅ Base de conhecimento gerada e salva com sucesso!")

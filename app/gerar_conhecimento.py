from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.docstore.document import Document

# 1. Carrega o conteúdo do arquivo
with open("app/conhecimento.txt", "r", encoding="utf-8") as f:
    conteudo = f.read()

# 2. Divide em chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = text_splitter.split_text(conteudo)

# 3. Transforma em documentos
docs = [Document(page_content=chunk) for chunk in chunks]

# 4. Embeddings
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# 5. Cria base FAISS
db = FAISS.from_documents(docs, embedding_model)

# 6. Salva localmente
db.save_local("app/embeddings")

print("✅ Base de conhecimento gerada com sucesso!")

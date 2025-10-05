# FILE: ingest.py

import os
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

CORPUS_PATH = "corpus"
FAISS_INDEX_PATH = "faiss_index"

def main():
    print("🚀 Starting document ingestion process...")
    print(f"📂 Loading documents from '{CORPUS_PATH}'...")
    loader = PyPDFDirectoryLoader(CORPUS_PATH)
    documents = loader.load()
    if not documents:
        print(f"⚠️ No documents found in '{CORPUS_PATH}'. Please add some PDFs.")
        return
    print(f"✅ Loaded {len(documents)} documents.")

    print("쪼개기 Splitting documents into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    docs = text_splitter.split_documents(documents)
    print(f"✅ Split into {len(docs)} chunks.")

    print("🧠 Initializing embedding model...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    print("✅ Embedding model initialized.")

    print("💾 Creating FAISS vector store...")
    db = FAISS.from_documents(docs, embeddings)
    print("✅ FAISS vector store created.")

    print(f"Saving FAISS index to '{FAISS_INDEX_PATH}'...")
    db.save_local(FAISS_INDEX_PATH)
    print(f"🎉 Ingestion complete! FAISS index saved successfully.")

if __name__ == "__main__":
    main()
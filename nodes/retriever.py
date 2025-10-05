# FILE: nodes/retriever.py

import os
from typing import Dict, Any
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

FAISS_INDEX_PATH = "faiss_index"

def retriever_node(state: Dict[str, Any]) -> Dict[str, Any]:
    print("---NODE: RETRIEVER---")
    topic = state.get("topic", "")
    if not topic: raise ValueError("Topic not set.")

    print(f"🔎 Retrieving documents for topic: '{topic}'")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    if not os.path.exists(FAISS_INDEX_PATH):
        raise FileNotFoundError(f"FAISS index not found. Please run ingest.py first.")

    db = FAISS.load_local(FAISS_INDEX_PATH, embeddings, allow_dangerous_deserialization=True)
    retriever = db.as_retriever(search_kwargs={'k': 5})
    retrieved_docs = retriever.invoke(topic)
    documents = [doc.page_content for doc in retrieved_docs]
    
    print(f"✅ Retrieved {len(documents)} documents.")
    return {"documents": documents}
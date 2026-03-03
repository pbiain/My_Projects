import os
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

PINECONE_INDEX_NAME = "n8n"
EMBEDDING_MODEL = "text-embedding-3-large"

embeddings = OpenAIEmbeddings(
    model=EMBEDDING_MODEL,
    dimensions=1024
)

vectorstore = PineconeVectorStore(
    index_name=PINECONE_INDEX_NAME,
    embedding=embeddings,
)

def retrieve_context(state):
    docs = vectorstore.similarity_search(state["user_message"], k=4)
    parts = []
    for i, doc in enumerate(docs):
        source = doc.metadata.get("source", "unknown")
        parts.append(f"[Chunk {i+1} - {source}]\n{doc.page_content}")
    state["retrieved_context"] = "\n\n".join(parts)
    state["actions_taken"].append("rag_retrieval")
    return state
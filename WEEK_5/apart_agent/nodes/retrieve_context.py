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
    user_msg = state["user_message"]

    # For short/vague messages, prepend last assistant reply to give RAG context
    words = user_msg.strip().split()
    if len(words) <= 6 and state.get("chat_history"):
        last_turn = state["chat_history"][-1]
        rag_query = f"{last_turn['assistant']} {user_msg}"
    else:
        rag_query = user_msg

    results = vectorstore.similarity_search_with_score(rag_query, k=4)
    parts = []
    for i, (doc, score) in enumerate(results):
        if score < 0.35:          # cosine distance — lower = more similar
            continue
        source = doc.metadata.get("source", "unknown")
        parts.append(f"[Chunk {i+1} - {source}]\n{doc.page_content}")
    state["retrieved_context"] = "\n\n".join(parts) if parts else ""
    state["actions_taken"].append("rag_retrieval")
    return state
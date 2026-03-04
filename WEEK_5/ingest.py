"""
ingest.py — Load PDFs from docs/ into Pinecone index.

Usage:
    python ingest.py              # ingest all PDFs in docs/
    python ingest.py --clear      # delete all existing vectors first, then ingest

Drop new or updated PDFs into WEEK_5/docs/ and re-run.
"""

import os
import sys
import argparse
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone

PINECONE_INDEX_NAME = "n8n"
EMBEDDING_MODEL     = "text-embedding-3-large"
EMBEDDING_DIMS      = 1024
CHUNK_SIZE          = 800
CHUNK_OVERLAP       = 100
DOCS_DIR            = Path(__file__).parent / "pinecone_docs"


def load_pdfs(docs_dir: Path):
    docs = []
    pdf_files = list(docs_dir.glob("*.pdf"))
    if not pdf_files:
        print(f"No PDFs found in {docs_dir}. Add files and re-run.")
        sys.exit(1)

    for pdf_path in pdf_files:
        print(f"  Loading: {pdf_path.name}")
        loader = PyPDFLoader(str(pdf_path))
        pages = loader.load()
        # Tag each chunk with the source filename
        for page in pages:
            page.metadata["source"] = pdf_path.name
        docs.extend(pages)

    print(f"  Loaded {len(docs)} pages from {len(pdf_files)} PDF(s)")
    return docs


def chunk_docs(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    chunks = splitter.split_documents(docs)
    print(f"  Split into {len(chunks)} chunks")
    return chunks


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--clear", action="store_true", help="Delete existing vectors before ingesting")
    args = parser.parse_args()

    print(f"\n=== Apart Club — Pinecone Ingest ===")
    print(f"Index: {PINECONE_INDEX_NAME}  |  Docs: {DOCS_DIR}\n")

    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL, dimensions=EMBEDDING_DIMS)

    if args.clear:
        print("Clearing existing vectors...")
        pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        index = pc.Index(PINECONE_INDEX_NAME)
        index.delete(delete_all=True)
        print("  Done.\n")

    print("Loading PDFs...")
    docs = load_pdfs(DOCS_DIR)

    print("Chunking...")
    chunks = chunk_docs(docs)

    print("Embedding and upserting to Pinecone...")
    PineconeVectorStore.from_documents(
        documents=chunks,
        embedding=embeddings,
        index_name=PINECONE_INDEX_NAME,
    )
    print(f"\nDone! {len(chunks)} chunks upserted to '{PINECONE_INDEX_NAME}'.")


if __name__ == "__main__":
    main()

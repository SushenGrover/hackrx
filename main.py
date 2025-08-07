# main.py
from fastapi import FastAPI
from pydantic import BaseModel
import tempfile
import requests
import os
import asyncio

from utils.document_parser import extract_text_from_pdf
from utils.embedding import get_embeddings
from utils.faiss_index import build_faiss_index, search_faiss_index
from utils.openai_qa import ask_gpt_async  # async version using GPT-4o

app = FastAPI()

class QueryRequest(BaseModel):
    documents: str  # URL or local path
    questions: list[str]

# Improved chunking: smaller size + overlap
def chunk_text(text, max_length=160, overlap=40):
    paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
    chunks = []
    current = ""

    for para in paragraphs:
        if len(current) + len(para) < max_length:
            current += " " + para
        else:
            chunks.append(current.strip())
            overlap_text = current[-overlap:] if overlap < len(current) else current
            current = overlap_text + " " + para

    if current:
        chunks.append(current.strip())

    return chunks

def download_file(url: str) -> str:
    response = requests.get(url)
    response.raise_for_status()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(response.content)
        return tmp.name

@app.post("/hackrx/run")
async def run_submission(request: QueryRequest):
    # Extract text from PDF (URL or local)
    if request.documents.startswith("http"):
        pdf_path = download_file(request.documents)
        try:
            text = extract_text_from_pdf(pdf_path)
        finally:
            os.unlink(pdf_path)
    else:
        text = extract_text_from_pdf(request.documents)

    # Chunking and embeddings
    clauses = chunk_text(text)
    clause_embeddings = get_embeddings(clauses)
    faiss_index = build_faiss_index(clause_embeddings)

    # Process each question asynchronously
    async def process_question(q: str):
        query_emb = get_embeddings([q])[0]
        top_idx = search_faiss_index(faiss_index, query_emb)
        top_clauses = [clauses[i] for i in top_idx]
        answer = await ask_gpt_async(top_clauses, q)
        return answer

    # Run all questions concurrently
    answers = await asyncio.gather(*[process_question(q) for q in request.questions])
    return {"answers": answers}

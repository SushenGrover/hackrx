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
from utils.openai_qa import ask_gpt_async  # new async version

app = FastAPI()

class QueryRequest(BaseModel):
    documents: str
    questions: list

def chunk_text(text, max_length=300):
    paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
    chunks = []
    current = ""
    for para in paragraphs:
        if len(current) + len(para) < max_length:
            current += " " + para
        else:
            chunks.append(current.strip())
            current = para
    if current:
        chunks.append(current.strip())
    return chunks

def download_file(url):
    response = requests.get(url)
    response.raise_for_status()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(response.content)
        return tmp.name

@app.post("/hackrx/run")
async def run_submission(request: QueryRequest):
    if request.documents.startswith("http"):
        pdf_path = download_file(request.documents)
        try:
            text = extract_text_from_pdf(pdf_path)
        finally:
            os.unlink(pdf_path)
    else:
        text = extract_text_from_pdf(request.documents)

    clauses = chunk_text(text)
    clause_embeddings = get_embeddings(clauses)
    faiss_index = build_faiss_index(clause_embeddings)

    async def process_question(q):
        query_emb = get_embeddings([q])[0]
        top_idx = search_faiss_index(faiss_index, query_emb)
        retrieved = [clauses[i] for i in top_idx]
        answer = await ask_gpt_async(retrieved, q)
        return answer

    answers = await asyncio.gather(*[process_question(q) for q in request.questions])
    return {"answers": answers}

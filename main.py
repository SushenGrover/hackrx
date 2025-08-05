# main.py
from fastapi import FastAPI
from pydantic import BaseModel
import tempfile
import requests
import os

# Import your functions from utils
from utils.document_parser import extract_text_from_pdf  # and others as needed
from utils.embedding import get_embeddings
from utils.faiss_index import build_faiss_index, search_faiss_index
from utils.openai_qa import ask_gpt

app = FastAPI()

class QueryRequest(BaseModel):
    documents: str  # URL or local file path
    questions: list

def chunk_text(text, max_length=300):
    # Split the document into "clauses" (basic: by paragraph or line)
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
    # Check if documents field is a URL or a local file path
    if request.documents.startswith("http"):
        pdf_path = download_file(request.documents)
        try:
            text = extract_text_from_pdf(pdf_path)
        finally:
            os.unlink(pdf_path)  # Clean up temp file
    else:
        text = extract_text_from_pdf(request.documents)
    
    clauses = chunk_text(text)

    # Get clause embeddings and build FAISS index
    clause_embeddings = get_embeddings(clauses)
    faiss_index = build_faiss_index(clause_embeddings)

    detailed_answers = []
    for q in request.questions:
        query_emb = get_embeddings([q])[0]
        top_idx = search_faiss_index(faiss_index, query_emb)
        retrieved_clauses = [clauses[i] for i in top_idx]
        answer = ask_gpt(retrieved_clauses, q)

        rationale = f"Matched clauses: {[int(i) for i in top_idx]}. Clause excerpts: {' | '.join(retrieved_clauses)}"

        detailed_answers.append({
            "question": q,
            "answer": answer,
            "matched_clauses_indices": [int(i) for i in top_idx],
            "matched_clauses_text": retrieved_clauses,
            "rationale": rationale
        })
    # Return answers list to match sample API response format
    return {"answers": [item['answer'] for item in detailed_answers]}

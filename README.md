IntelliClause: AI-Powered Insurance Policy Q&A
IntelliClause is an intelligent Q&A system designed to provide precise and context-aware answers from complex insurance policy documents. This project was developed as a submission for the HackRx 6.0 Hackathon by Bajaj Finserv.

It leverages a Retrieval-Augmented Generation (RAG) pipeline to understand user questions, retrieve the most relevant clauses from a given policy document, and generate accurate answers using state-of-the-art language models like GPT-4o.

✨ Key Features
Dynamic Document Processing: Ingests insurance policies directly from URLs or local PDF files.

Advanced Text Extraction: Reliably extracts text from PDF documents.

Intelligent Text Chunking: Breaks down long documents into small, overlapping chunks to preserve semantic context.

High-Speed Similarity Search: Uses FAISS (Facebook AI Similarity Search) for blazingly fast retrieval of relevant document clauses.

State-of-the-Art Q&A: Employs OpenAI's GPT-4o model for generating highly accurate, context-aware answers.

Asynchronous API: Built with FastAPI to handle multiple questions concurrently, ensuring low latency.

Specialized Prompting: The model is prompted to act as a legal assistant, ensuring answers are precise, factual, and in the style of official policy summaries.

⚙️ How It Works: The RAG Pipeline
The project is built around a Retrieval-Augmented Generation (RAG) architecture. This approach enhances the capabilities of Large Language Models (LLMs) by grounding them with information from a specific knowledge base.

Here's a step-by-step breakdown of the process:

Document Ingestion: The system accepts a PDF document via a URL or a local file path.

Text Extraction & Chunking: The text is extracted from the document. To handle long texts, it's segmented into smaller, overlapping chunks of 160 characters with a 40-character overlap. This ensures that the semantic meaning is not lost at the boundaries of chunks.

Vector Embedding: Each text chunk is converted into a numerical vector representation (embedding) using OpenAI's text-embedding-ada-002 model.

FAISS Indexing: The generated embeddings are stored in a FAISS index. FAISS allows for highly efficient similarity searches, enabling us to quickly find the chunks most relevant to a user's query.

Query Processing: When a user asks a question, it is also converted into an embedding using the same model.

Context Retrieval: The FAISS index is searched to retrieve the top 15 text chunks whose embeddings are most similar to the question's embedding.

Answer Generation: These retrieved chunks are passed as context to the GPT-4o model along with the original question. A carefully crafted prompt instructs the model to act as a legal assistant and generate a concise, factual answer based only on the provided context.

Concurrent Responses: The entire process is wrapped in an asynchronous FastAPI endpoint, allowing multiple questions to be processed in parallel for maximum efficiency.

📂 Project Structure
.
├── data/
│   └── *.pdf               # Example insurance policy documents
├── utils/
│   ├── __pycache__/
│   ├── document_parser.py  # Extracts text from PDF and DOCX files
│   ├── embedding.py        # Generates embeddings using OpenAI API
│   ├── faiss_index.py      # Builds and searches the FAISS index
│   └── openai_qa.py        # Generates answers using GPT-4o
├── .http                   # HTTP request examples
├── main.py                 # FastAPI application and main logic
├── Procfile                # Deployment configuration
├── requirements.txt        # Python dependencies
└── test.py                 # Test scripts

🚀 Getting Started
Prerequisites
Python 3.9 or higher

An OpenAI API Key

1. Clone the Repository
git clone https://github.com/your-username/intelliclause.git
cd intelliclause

2. Create a Virtual Environment
It's recommended to use a virtual environment to manage dependencies.

python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

3. Install Dependencies
pip install -r requirements.txt

4. Set Up Environment Variables
Create a .env file in the root directory and add your OpenAI API key:

OPENAI_API_KEY="sk-..."

The application uses python-dotenv to load this key automatically.

5. Run the Application
uvicorn main:app --reload

The API will be available at http://127.0.0.1:8000.

🤖 API Usage
Endpoint: /hackrx/run
Method: POST

Description: Submits a document and a list of questions for processing.

Request Body
{
  "documents": "https://url.to/your/policy.pdf",
  "questions": [
    "What is the grace period for premium payment?",
    "Are maternity expenses covered?",
    "What is the room rent limit?"
  ]
}

documents (string): A URL to a PDF file or a local path to the file.

questions (list[string]): A list of questions to ask about the document.

Example cURL Request
curl -X POST "http://127.0.0.1:8000/hackrx/run" \
-H "Content-Type: application/json" \
-d '{
    "documents": "https://www.bajajallianz.com/content/dam/bagic/health-insurance/sales-brochure-global-health-care.pdf",
    "questions": [
        "What is the grace period?",
        "Is dental treatment covered?"
    ]
}'

Success Response (200 OK)
{
  "answers": [
    "A grace period of 30 days is provided for yearly premium payments and 15 days for all other payment modes.",
    "Yes, emergency dental treatment required due to an accident is covered."
  ]
}

🛠️ Technologies Used
Backend Framework: FastAPI

LLM & Embeddings: OpenAI (GPT-4o, text-embedding-ada-002)

Vector Database: FAISS (Facebook AI Similarity Search)

PDF Parsing: pdfplumber

Async Operations: asyncio

Data Validation: Pydantic

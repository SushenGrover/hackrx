# IntelliClause: AI-Powered Insurance Policy Q&A

IntelliClause is an intelligent Q&A system designed to provide precise and context-aware answers from complex insurance policy documents.  
This project was developed as a submission for the **HackRx 6.0 Hackathon by Bajaj Finserv**.  

It leverages a Retrieval-Augmented Generation (RAG) pipeline to understand user questions, retrieve the most relevant clauses from a given policy document, and generate accurate answers using state-of-the-art language models like GPT-4o.

---

## Key Features

- **Dynamic Document Processing**: Ingests insurance policies directly from URLs or local PDF files.  
- **Advanced Text Extraction**: Reliably extracts text from PDF documents.  
- **Intelligent Text Chunking**: Breaks down long documents into small, overlapping chunks to preserve semantic context.  
- **High-Speed Similarity Search**: Uses FAISS (Facebook AI Similarity Search) for efficient retrieval of relevant clauses.  
- **State-of-the-Art Q&A**: Employs OpenAI's GPT-4o model for generating accurate, context-aware answers.  
- **Asynchronous API**: Built with FastAPI to handle multiple questions concurrently with low latency.  
- **Specialized Prompting**: Ensures responses are concise, factual, and in the style of official policy summaries.  

---

## How It Works: The RAG Pipeline

The project is built around a Retrieval-Augmented Generation (RAG) architecture. This enhances the capabilities of Large Language Models (LLMs) by grounding them with information from a specific knowledge base.

**Step-by-step process:**

1. **Document Ingestion** – The system accepts a PDF document via a URL or a local file path.  
2. **Text Extraction & Chunking** – Extracted text is segmented into overlapping chunks (160 characters with 40-character overlap) to preserve semantics.  
3. **Vector Embedding** – Each chunk is embedded using OpenAI's `text-embedding-ada-002` model.  
4. **FAISS Indexing** – Embeddings are stored in a FAISS index for efficient similarity search.  
5. **Query Processing** – User questions are also converted into embeddings.  
6. **Context Retrieval** – The FAISS index retrieves the top 15 most relevant chunks.  
7. **Answer Generation** – GPT-4o uses retrieved context and the question to generate precise, legal-style answers.  
8. **Concurrent Responses** – FastAPI enables handling multiple queries asynchronously.  

---

## Project Structure

```
├── data/
│ └── *.pdf # Example insurance policy documents
├── utils/
│ ├── pycache/
│ ├── document_parser.py # Extracts text from PDF and DOCX files
│ ├── embedding.py # Generates embeddings using OpenAI API
│ ├── faiss_index.py # Builds and searches the FAISS index
│ └── openai_qa.py # Generates answers using GPT-4o
├── .http # HTTP request examples
├── main.py # FastAPI application and main logic
├── Procfile # Deployment configuration
├── requirements.txt # Python dependencies
└── test.py # Test scripts
```


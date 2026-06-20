# python-native-rag-pipeline

A lightweight Retrieval-Augmented Generation (RAG) pipeline built entirely in native Python.

This project demonstrates how to:

* Extract text from a PDF
* Split the text into chunks
* Generate embeddings using OpenAI
* Store vector embeddings in ChromaDB
* Retrieve relevant document context
* Answer questions using Anthropic Claude

The goal of this repository is educational simplicity: showing the core mechanics behind a RAG system without heavy frameworks or orchestration layers.

---

# What is RAG?

RAG (Retrieval-Augmented Generation) is a technique that allows Large Language Models (LLMs) to answer questions using external knowledge sources.

Instead of relying only on model training data, the system:

1. Retrieves relevant information from documents
2. Injects that information into the prompt
3. Generates a grounded answer based on the retrieved context

This repository demonstrates a minimal end-to-end implementation of that workflow.

---

# Features

* PDF document ingestion
* Automatic text chunking
* OpenAI embedding generation
* ChromaDB vector storage
* Semantic similarity search
* Claude-powered question answering
* Pure Python implementation
* Beginner-friendly architecture

---

# Project Architecture

The pipeline follows this flow:

```text
PDF File
   ↓
Text Extraction
   ↓
Chunking
   ↓
OpenAI Embeddings
   ↓
ChromaDB Vector Store
   ↓
Similarity Search
   ↓
Context Injection
   ↓
Claude Response
```

---

# Technologies Used

## OpenAI

Used for generating embeddings with:

```python
text-embedding-3-small
```

Embeddings convert text into numerical vectors that can be searched semantically.

---

## Anthropic Claude

Used for final answer generation.

The retrieved chunks are passed into Claude as context so responses are grounded in the uploaded document.

---

## ChromaDB

Acts as the vector database.

Stores:

* embeddings
* text chunks
* metadata
* chunk IDs

Then performs nearest-neighbor semantic search.

---

## PyPDF

Used to extract text from PDF files page by page.

---

# Installation

## Clone the repository

```bash
git clone https://github.com/yourusername/python-native-rag-pipeline.git
cd python-native-rag-pipeline
```

## Install dependencies

```bash
pip install openai anthropic chromadb pypdf
```

---

# Environment Variables

Set your API keys before running the script.

## Linux / macOS

```bash
export OPENAI_API_KEY="your_openai_key"
export ANTHROPIC_API_KEY="your_anthropic_key"
```

## Windows (PowerShell)

```powershell
setx OPENAI_API_KEY "your_openai_key"
setx ANTHROPIC_API_KEY "your_anthropic_key"
```

---

# How It Works

## 1. PDF Extraction

The script reads the PDF and extracts text page-by-page.

```python
reader = PdfReader(path)
```

Each page is stored with:

* page number
* extracted content

---

## 2. Text Chunking

Large documents are split into overlapping chunks.

```python
chunk_text(text, size=500, overlap=100)
```

Why overlap matters:

* prevents context loss between chunks
* improves retrieval quality
* helps preserve sentence continuity

---

## 3. Embedding Generation

Each chunk is converted into a vector embedding.

```python
openai_client.embeddings.create(
    model='text-embedding-3-small',
    input=text
)
```

These vectors represent semantic meaning rather than keywords.

---

## 4. Vector Storage

Chunks and embeddings are stored in ChromaDB.

Each stored item contains:

* chunk text
* embedding vector
* page metadata
* source file name

---

## 5. Semantic Retrieval

When a question is asked:

* the question is embedded
* ChromaDB searches for similar chunks
* the most relevant results are returned

```python
collection.query(
    query_embeddings=[query_embedding],
    n_results=3
)
```

---

## 6. Response Generation

Relevant chunks are injected into a prompt and sent to Claude.

```python
response = anth_client.messages.create(
    model='claude-haiku-4-5',
    ...
)
```

Claude then answers using the retrieved document context.

---

# Example Usage

## Input Question

```python
question = 'How to multiply matrices?'
```

## Example Output

```text
QUESTION: How to multiply matrices?
ANSWER: Matrix multiplication is performed by taking the dot product...
```

---

# File Structure

```text
python-native-rag-pipeline/
│
├── main.py
├── linearalgebra.pdf
├── README.md
└── requirements.txt
```

---

# Why This Project Exists

Many RAG tutorials rely on:

* LangChain
* LlamaIndex
* large abstractions
* hidden orchestration layers

This project intentionally avoids those tools to show:

* what embeddings actually do
* how retrieval works internally
* how vector databases integrate with LLMs
* how prompts are constructed

The repository is designed for learning and experimentation.

---

# Limitations

This is a minimal educational implementation and does not yet include:

* streaming responses
* persistent vector storage
* batch embedding optimization
* async processing
* metadata filtering
* citation generation
* advanced chunking strategies
* reranking
* multi-document ingestion
* production-grade error handling

---

# Potential Improvements

Ideas for extending the project:

* Add a CLI interface
* Support multiple PDFs
* Add a web UI with Streamlit or FastAPI
* Persist ChromaDB locally
* Add source citations
* Implement hybrid search
* Add reranking models
* Support conversation memory
* Add OCR support for scanned PDFs

---

# Example Use Cases

* Chat with textbooks
* Internal company documentation search
* Research paper assistants
* Personal knowledge bases
* PDF question answering
* Educational AI tools

---

# License

MIT License

---

# Educational Purpose

This repository is primarily intended as a learning resource for developers who want to understand the foundations of Retrieval-Augmented Generation systems from first principles.

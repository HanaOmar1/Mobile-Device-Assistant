# Mobile Device Assistant API

A modular FastAPI service that provides two capabilities:

1. **Mobile Device Specification Extraction** — uses an LLM to extract structured device information from messy text and validates the result using Pydantic.
2. **Hybrid Document Search** — combines BM25 sparse retrieval and dense embedding retrieval using Reciprocal Rank Fusion (RRF).

## Features

* Structured device extraction with Pydantic
* RFTC-based prompt design
* JSON-mode LLM responses
* Automatic validation and retry on invalid extraction
* Prompt-injection protection
* BM25 sparse retrieval
* Dense retrieval using SentenceTransformer
* Reciprocal Rank Fusion (RRF)
* FastAPI endpoints for extraction and search
* Input length validation

## Project Structure

```text
mobile-device-assistant/
├── .env
├── .env.example
├── .gitignore
├── README.md
└── app/
    ├── __init__.py
    ├── main.py
    ├── schema/
    │   ├── __init__.py
    │   └── device.py
    ├── services/
    │   ├── __init__.py
    │   ├── extraction.py
    │   └── search.py
    ├── prompts/
    │   ├── __init__.py
    │   └── templates.py
    ├── data/
    │   ├── __init__.py
    │   └── devices.py
    └── utils/
        ├── __init__.py
        ├── embeddings.py
        └── bm25_index.py
```

## Setup

Create and activate a virtual environment:

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Install the required dependencies:

```bash
pip install fastapi uvicorn python-dotenv openai pydantic rank-bm25 sentence-transformers numpy
```

Create a `.env` file:

```env
OPENAI_API_KEY=your_openai_api_key
MODEL_NAME=gpt-4o-mini
```

Never commit the `.env` file or a real API key to GitHub.

## Running the API

From the project root:

```bash
uvicorn app.main:app --reload
```

The API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

## API Endpoints

### POST `/extract`

Extract structured information from a mobile-device description.

Example request:

```json
{
  "text": "Samsung Galaxy S24 Ultra is a flagship from 2024 with a 6.8 inch dynamic AMOLED display, 5000 mAh battery and 200MP camera."
}
```

### POST `/search`

Search the device catalog using hybrid retrieval.

Example request:

```json
{
  "q": "best phone for low light photography"
}
```

The search combines BM25 and dense retrieval using Reciprocal Rank Fusion and returns the top-k documents with their fused scores.

## Prompt Injection Protection

The extraction endpoint checks input for suspicious instruction-like phrases before making an LLM call.

Raw device text is also wrapped in `<external_data>` tags, and the system prompt explicitly instructs the model to treat the content as untrusted data rather than instructions.

## Validation

Requests longer than 500 characters are rejected.

Invalid LLM outputs are validated using the Pydantic `Device` model. Validation failures trigger a retry, with a maximum of two retries.

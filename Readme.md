# 📘 AI Student Helper

An end-to-end AI-powered learning assistant that extracts knowledge from handwritten notes, PDFs, images, and URLs, then provides topic-wise explanations, semantic search, test generation, and mistake evaluation.  
Built with FastAPI, OCR, Embeddings, Vector Search, and RAG (Retrieval-Augmented Generation).

---

## 🚀 Features

### 🔍 Input Processing

- Upload PDFs, images (JPG/PNG), URLs
- OCR for handwritten and printed text (PaddleOCR)
- PDF text extraction (PyPDF / pdfminer)
- Smart text chunking & metadata tagging

### 🧠 Core AI Capabilities

- Semantic Search (Qdrant / Chroma)
- RAG-based chatbot using Llama 3.1 (Groq API)
- Topic-wise explanations
- Test generation (MCQ, short questions, fill-in-the-blanks)
- Mistake evaluation: compare student answers to source notes

### 📦 Storage & Databases

- MinIO / S3 (file storage)
- PostgreSQL (metadata & user management)
- Qdrant (vector embeddings)

### 🌐 Backend

- FastAPI + Uvicorn
- JWT-based authentication
- Background processing for OCR/embedding

### 🖥️ Frontend

- React / Next.js / Vercel
- Chat UI
- File upload dashboard
- History viewer

---

## 🏛️ System Architecture

                  Frontend (React)
                        │
                        ▼
                FastAPI Backend
       ┌───────────────┼────────────────┐
       ▼               ▼                ▼

OCR / Parser RAG Engine Authentication
│ │
▼ ▼
MinIO Storage Qdrant Vector DB
│
▼
PostgreSQL DB

---

## 📁 Project Structure

/app
├── api
│ ├── upload.py
│ ├── chat.py
│ ├── test_generator.py
│ ├── evaluate.py
│ └── auth.py
├── services
│ ├── ocr_service.py
│ ├── pdf_parser.py
│ ├── embeddings.py
│ ├── rag_engine.py
│ ├── test_service.py
│ └── evaluation_service.py
├── core
│ ├── config.py
│ └── logging.py
├── db
│ ├── postgres.py
│ ├── vector_db.py
│ └── storage.py
└── main.py

---

## ⚙️ Technologies Used

| Component  | Technology            |
| ---------- | --------------------- |
| Backend    | FastAPI, Python       |
| OCR        | PaddleOCR             |
| Embeddings | Sentence Transformers |
| LLM        | Groq (Llama 3.1)      |
| Vector DB  | Qdrant                |
| Storage    | MinIO / S3            |
| Database   | PostgreSQL            |
| Frontend   | React / Next.js       |
| DevOps     | Docker, Nginx         |

---

## 🧭 API Endpoints (Overview)

### Upload

- `POST /upload` — Upload PDF/Image
- `POST /url-process` — Parse webpage content
- `GET /file/{id}/status` — Processing status

### Chat + RAG

- `POST /chat` — Ask questions
- `POST /semantic-search` — Direct search

### Tests

- `POST /generate-test`
- `POST /evaluate-answer`

### Auth

- `POST /register`
- `POST /login`

---

## 🐳 Deployment (Docker Compose)

Example stack:

```yaml
version: '3.8'

services:
  api:
    build: ./backend
    ports:
      - "8000:8000"
    depends_on:
      - postgres
      - qdrant
      - minio

  postgres:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: your_password

  qdrant:
    image: qdrant/qdrant

  minio:
    image: minio/minio
    command: server /data
    ports:
      - "9000:9000"

🔧 Local Development
git clone <repo>
cd backend
uvicorn main:app --reload


Frontend:

npm install
npm run dev

🧪 Testing (SQA Coverage)

The project includes test cases for:

File uploads

OCR extraction

PDF parsing

Embedding generation

Vector search accuracy

RAG pipeline correctness

Test generator output

Mistake evaluation logic

Load testing

Security (SQL injection, SSRF, file traversal)

Full test document is available in /docs/tests.md

📊 Maintenance Plan
Monthly:

Update dependencies

Clean storage/logs

Evaluate OCR/embedding accuracy

Monitor CPU/RAM/disk

Quarterly:

Update LLM models

Recompute embeddings

Security audit

Improve RAG prompts

💰 Cost Estimate
Usage Level	Monthly Cost
Low (20–50 users)	$7–10
Medium (100–300 users)	$10–15
High (1,000+ users)	$20–25


🧑‍💻 Team Roles (Recommended):

Backend Developer

ML Engineer

Frontend Developer

DevOps

SQA Engineer



🤝 Contributing

Pull requests are welcome.
For major changes, open an issue first.

📬 Contact

For questions or support, contact the development team.


---

If you want, I can also generate:

✅ A `docs/` folder
✅ API documentation (`OPENAPI.md`)
✅ Sequence diagrams
✅ A PDF export of the README
✅ UML diagrams (Class + Activity + Deployment)

Just tell me.
```

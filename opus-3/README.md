# 🇸🇬 Singapore SMB Customer Support AI Agent

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com/)
[![React 18](https://img.shields.io/badge/React-18+-blue.svg)](https://react.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A production-ready, context-aware customer enquiry support AI Agent designed specifically for Singapore Small and Medium Businesses (SMBs). Built with advanced RAG (Retrieval Augmented Generation), hierarchical memory, and PDPA-compliant data handling.

## ✨ Features

- **🧠 Advanced RAG Pipeline**: Multi-stage retrieval with query transformation, hybrid search, and cross-encoder reranking
- **💾 Hierarchical Memory**: Short-term (Redis) + Long-term (PostgreSQL) + Working memory management
- **🔒 PDPA Compliant**: Built-in consent tracking, data minimization, and auto-expiry
- **🌏 Singapore Context**: Timezone-aware, bilingual-ready (English/Mandarin)
- **⚡ Real-time Chat**: WebSocket-based streaming responses
- **📊 Evaluation Ready**: RAGAS metrics integration for continuous quality monitoring

## 🏗️ Architecture

```text
┌─────────────────┐ ┌─────────────────────────────────────────────┐
│ React Chat │────▶│ FastAPI Backend │
│ Widget │◀────│ ┌─────────────────────────────────────┐ │
└─────────────────┘ │ │ Pydantic AI Agent │ │
│ │ ┌─────────┐ ┌─────────┐ ┌───────┐ │ │
│ │ │ RAG │ │ Memory │ │ Tools │ │ │
│ │ │Pipeline │ │ Manager │ │ │ │ │
│ │ └────┬────┘ └────┬────┘ └───────┘ │ │
│ └───────┼───────────┼──────────────────┘ │
│ │ │ │
│ ┌───────▼───┐ ┌─────▼─────┐ ┌───────────┐ │
│ │ Qdrant │ │ Redis │ │PostgreSQL │ │
│ │ (Vectors) │ │(Sessions) │ │ (Long) │ │
│ └───────────┘ └───────────┘ └───────────┘ │
└─────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- OpenAI API Key
- Cohere API Key (optional, for reranking)

### 1. Clone and Setup

```bash
git clone https://github.com/yourusername/singapore-smb-support-agent.git
cd singapore-smb-support-agent

# Copy environment configuration
cp .env.example .env

# Edit .env with your API keys
nano .env
```

### 2. Start Infrastructure

```bash
# Start all services with Docker Compose
docker-compose up -d

# Or use Make
make up
```

### 3. Start Development Servers

```bash
# Terminal 1: Backend
cd backend
pip install -e ".[dev]"
python -m app.main

# Terminal 2: Frontend
cd frontend
npm install
npm run dev
```

### 4. Seed Knowledge Base

```bash
cd backend
python scripts/seed_knowledge.py
```

### 5. Access the Application

- Frontend: http://localhost:3000
- API Docs: http://localhost:8000/docs
- Qdrant Dashboard: http://localhost:6333/dashboard

📁 **Project Structure**
```text
singapore-smb-support-agent/
├── backend/                 # FastAPI + Pydantic AI backend
│   ├── app/
│   │   ├── agent/          # AI agent with tools
│   │   ├── api/            # REST & WebSocket endpoints
│   │   ├── ingestion/      # Document processing pipeline
│   │   ├── memory/         # Hierarchical memory system
│   │   ├── models/         # Pydantic & SQLAlchemy models
│   │   ├── rag/            # RAG pipeline components
│   │   └── services/       # Business logic services
│   ├── tests/              # Unit & integration tests
│   └── scripts/            # Utility scripts
├── frontend/               # React + TypeScript frontend
│   ├── src/
│   │   ├── components/     # UI components (Shadcn/UI)
│   │   ├── hooks/          # Custom React hooks
│   │   ├── stores/         # Zustand state management
│   │   └── lib/            # Utilities & API client
├── infrastructure/         # Docker & deployment configs
└── docs/                   # Documentation
```

🧪 **Testing**
```bash
# Run backend tests
cd backend
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run RAG evaluation
python scripts/evaluate_rag.py
```

<img width="794" height="844" alt="image" src="https://github.com/user-attachments/assets/be5393ff-cea9-4648-9e6a-5a98c0632c73" />

📊 RAG Quality Metrics
Metric	Target	Current
Faithfulness	> 0.90	-
Answer Relevancy	> 0.85	-
Context Precision	> 0.80	-
Context Recall	> 0.85	-
🔐 PDPA Compliance
This system is designed with Singapore's Personal Data Protection Act in mind:

✅ Consent tracking for data collection
✅ Purpose limitation (support only)
✅ Configurable data retention (default: 30 days)
✅ Anonymization for analytics
✅ No cross-border data transfer (SG-hosted)
🤝 Contributing
Contributions are welcome! Please read our Contributing Guide for details.

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

🙏 Acknowledgments
Built with Pydantic AI
RAG powered by LangChain
Vector search by Qdrant
UI components from Shadcn/UI

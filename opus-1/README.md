# Singapore SMB Customer Support AI Agent

A production-ready, context-aware AI customer support agent built for Singapore SMBs.

## Features

- 🤖 **Intelligent Responses**: Powered by GPT-4o-mini with RAG-grounded answers
- 🧠 **Memory System**: Short-term (Redis) + Long-term (PostgreSQL) memory
- 🔍 **Advanced RAG**: Multi-stage retrieval with hybrid search and reranking
- 🌏 **Multilingual**: English and Mandarin support
- 🔒 **PDPA Compliant**: Singapore data protection compliance built-in
- ⚡ **Real-time**: WebSocket-based streaming responses
- 📱 **Responsive UI**: Modern React chatbox interface

## Tech Stack

### Backend
- Python 3.11+
- FastAPI
- Pydantic AI
- LangChain 0.3.x
- Qdrant (Vector Database)
- Redis (Session Memory)
- PostgreSQL (Long-term Storage)

### Frontend
- React 18 + TypeScript
- Tailwind CSS
- Shadcn/UI Components
- Zustand (State Management)

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.11+
- Node.js 20+

### Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd singapore-smb-support-agent

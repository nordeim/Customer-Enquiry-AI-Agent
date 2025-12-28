Deep Analysis: Customer Enquiry Support AI Agent for Singapore SMB
Executive Summary
This document presents a comprehensive architectural design and implementation plan for a production-ready Customer Enquiry Support AI Agent tailored for Singapore SMBs. The system integrates LangChain 1.0, Pydantic AI, Advanced RAG, and a hierarchical memory architecture to deliver context-aware, intelligent customer conversations through a React frontend interface.

Phase 1: Deep Requirement Analysis
1.1 Stakeholder & Context Analysis
text

┌─────────────────────────────────────────────────────────────────────────────┐
│                     SINGAPORE SMB CONTEXT MAP                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  BUSINESS REALITY                    REGULATORY ENVIRONMENT                 │
│  ┌─────────────────────────┐         ┌─────────────────────────┐           │
│  │ • Limited IT resources  │         │ • PDPA Compliance       │           │
│  │ • Cost-sensitive        │         │ • Data localization     │           │
│  │ • Need 24/7 coverage    │         │ • Consent management    │           │
│  │ • High staff turnover   │         │ • Audit trail required  │           │
│  │ • Domain expertise loss │         │ • Right to deletion     │           │
│  └─────────────────────────┘         └─────────────────────────┘           │
│                                                                             │
│  LINGUISTIC LANDSCAPE                TECHNICAL CONSTRAINTS                  │
│  ┌─────────────────────────┐         ┌─────────────────────────┐           │
│  │ • English (primary)     │         │ • Moderate scale        │           │
│  │ • Mandarin (secondary)  │         │ • Cloud-first           │           │
│  │ • Singlish patterns     │         │ • API integrations      │           │
│  │ • Code-switching        │         │ • Mobile-critical       │           │
│  └─────────────────────────┘         └─────────────────────────┘           │
│                                                                             │
│  USER PSYCHOLOGY                                                            │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │ Enquiry State: Frustrated → Seeking Clarity → Need Resolution        │  │
│  │ Trust Threshold: Low for AI → Must prove competence quickly          │  │
│  │ Expectation: Fast, accurate, escalation path visible                 │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
1.2 Multi-Dimensional Requirements Analysis
Dimension	Deep Analysis	Design Implication
Psychological	Users in support context exhibit heightened anxiety, reduced patience. Cognitive load must be minimized. Trust is earned through competence demonstration within first 2 exchanges.	Interface must feel effortless. Agent must acknowledge, validate, then resolve. Never defensive. Transparency about AI nature with graceful human escalation.
Technical	LangChain 1.0 introduced breaking changes—LCEL (LangChain Expression Language) is now primary. Pydantic AI provides structured outputs with validation. RAG quality directly proportional to chunking strategy.	Use LangGraph for stateful agents. Pydantic models for all agent I/O. Semantic chunking with overlap. Cross-encoder reranking mandatory.
Accessibility	WCAG AAA requires 7:1 contrast, keyboard-only navigation, screen reader semantics, reduced motion options. Singapore population aging—accessibility is business-critical.	Shadcn UI primitives provide ARIA compliance. Custom focus management. Announce messages to screen readers. Respect prefers-reduced-motion.
Scalability	SMB today, potential multi-tenant tomorrow. Knowledge base will grow. Conversation history accumulates. Token costs compound.	Modular architecture. Tenant isolation in database design. Aggressive context compression. Tiered LLM usage (cheaper model for routing).
Security	PDPA mandates consent, purpose limitation, data retention policies. Customer data in conversations is PII.	Encryption at rest/transit. Consent checkpoints. Configurable retention. Audit logging. No PII in logs.
Phase 2: System Architecture Design
2.1 High-Level Architecture
text

┌─────────────────────────────────────────────────────────────────────────────────────┐
│                           CUSTOMER ENQUIRY SUPPORT AI AGENT                         │
│                              SYSTEM ARCHITECTURE                                     │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                      │
│  ┌─────────────────────────────────────────────────────────────────────────────┐    │
│  │                         PRESENTATION LAYER                                   │    │
│  │  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐          │    │
│  │  │   React Chat     │  │   Admin Portal   │  │  Webhook APIs    │          │    │
│  │  │   Interface      │  │   (KB Mgmt)      │  │  (WhatsApp/FB)   │          │    │
│  │  │                  │  │                  │  │                  │          │    │
│  │  │  • Tailwind CSS  │  │  • Document      │  │  • Channel       │          │    │
│  │  │  • Shadcn UI     │  │    Upload        │  │    Abstraction   │          │    │
│  │  │  • WebSocket     │  │  • Analytics     │  │  • Message       │          │    │
│  │  │  • Streaming     │  │  • Config        │  │    Normalization │          │    │
│  │  └────────┬─────────┘  └────────┬─────────┘  └────────┬─────────┘          │    │
│  └───────────┼──────────────────────┼──────────────────────┼────────────────────┘    │
│              │                      │                      │                         │
│              └──────────────────────┼──────────────────────┘                         │
│                                     ▼                                                │
│  ┌─────────────────────────────────────────────────────────────────────────────┐    │
│  │                           API GATEWAY LAYER                                  │    │
│  │  ┌────────────────────────────────────────────────────────────────────┐    │    │
│  │  │  FastAPI Application                                                │    │    │
│  │  │  ├── REST Endpoints (Admin, Config, History)                       │    │    │
│  │  │  ├── WebSocket Handler (Real-time Chat)                            │    │    │
│  │  │  ├── Rate Limiting & Auth Middleware                               │    │    │
│  │  │  └── Request Validation (Pydantic Models)                          │    │    │
│  │  └────────────────────────────────────────────────────────────────────┘    │    │
│  └──────────────────────────────────┬──────────────────────────────────────────┘    │
│                                     │                                                │
│                                     ▼                                                │
│  ┌─────────────────────────────────────────────────────────────────────────────┐    │
│  │                          AGENT ORCHESTRATION LAYER                           │    │
│  │                                                                              │    │
│  │  ┌─────────────────────────────────────────────────────────────────────┐   │    │
│  │  │                    LangGraph State Machine                          │   │    │
│  │  │  ┌───────────┐    ┌───────────┐    ┌───────────┐    ┌───────────┐ │   │    │
│  │  │  │  INTAKE   │───▶│  ROUTER   │───▶│ EXECUTOR  │───▶│ RESPONDER │ │   │    │
│  │  │  │           │    │           │    │           │    │           │ │   │    │
│  │  │  │ • Parse   │    │ • Classify│    │ • RAG     │    │ • Format  │ │   │    │
│  │  │  │ • Intent  │    │ • Route   │    │ • Tools   │    │ • Validate│ │   │    │
│  │  │  │ • Context │    │ • Decide  │    │ • Actions │    │ • Stream  │ │   │    │
│  │  │  └───────────┘    └───────────┘    └───────────┘    └───────────┘ │   │    │
│  │  │                          │                                         │   │    │
│  │  │                          ▼                                         │   │    │
│  │  │  ┌─────────────────────────────────────────────────────────────┐  │   │    │
│  │  │  │                   TOOL REGISTRY                              │  │   │    │
│  │  │  │  • rag_search      • order_lookup      • appointment_book   │  │   │    │
│  │  │  │  • human_escalate  • faq_retrieval     • feedback_collect   │  │   │    │
│  │  │  └─────────────────────────────────────────────────────────────┘  │   │    │
│  │  └─────────────────────────────────────────────────────────────────────┘   │    │
│  │                                                                              │    │
│  │  ┌─────────────────────────────────────────────────────────────────────┐   │    │
│  │  │                    Pydantic AI Validation Layer                     │   │    │
│  │  │  • Input schemas     • Output schemas     • Tool call validation   │   │    │
│  │  └─────────────────────────────────────────────────────────────────────┘   │    │
│  └──────────────────────────────────┬──────────────────────────────────────────┘    │
│                                     │                                                │
│              ┌──────────────────────┼──────────────────────┐                        │
│              ▼                      ▼                      ▼                        │
│  ┌───────────────────┐  ┌───────────────────┐  ┌───────────────────┐               │
│  │   RAG PIPELINE    │  │  MEMORY SYSTEM    │  │  EXTERNAL APIs    │               │
│  │                   │  │                   │  │                   │               │
│  │ ┌───────────────┐ │  │ ┌───────────────┐ │  │ • CRM Systems     │               │
│  │ │ Query         │ │  │ │ Short-Term    │ │  │ • Order Systems   │               │
│  │ │ Transformer   │ │  │ │ (Redis)       │ │  │ • Booking APIs    │               │
│  │ └───────┬───────┘ │  │ └───────────────┘ │  │ • Payment Status  │               │
│  │         ▼         │  │ ┌───────────────┐ │  │                   │               │
│  │ ┌───────────────┐ │  │ │ Long-Term     │ │  └───────────────────┘               │
│  │ │ Hybrid Search │ │  │ │ (PostgreSQL + │ │                                      │
│  │ │ (BM25+Vector) │ │  │ │  Vector)      │ │                                      │
│  │ └───────┬───────┘ │  │ └───────────────┘ │                                      │
│  │         ▼         │  │ ┌───────────────┐ │                                      │
│  │ ┌───────────────┐ │  │ │ Working       │ │                                      │
│  │ │ Cross-Encoder │ │  │ │ Memory        │ │                                      │
│  │ │ Reranker      │ │  │ │ (Per-Request) │ │                                      │
│  │ └───────┬───────┘ │  │ └───────────────┘ │                                      │
│  │         ▼         │  │                   │                                      │
│  │ ┌───────────────┐ │  └───────────────────┘                                      │
│  │ │ Context       │ │                                                             │
│  │ │ Compressor    │ │                                                             │
│  │ └───────────────┘ │                                                             │
│  └───────────────────┘                                                             │
│                                                                                      │
│  ┌─────────────────────────────────────────────────────────────────────────────┐    │
│  │                           DATA PERSISTENCE LAYER                            │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │    │
│  │  │  PostgreSQL  │  │    Qdrant    │  │    Redis     │  │  S3/MinIO    │    │    │
│  │  │              │  │              │  │              │  │              │    │    │
│  │  │ • Users      │  │ • Document   │  │ • Sessions   │  │ • Documents  │    │    │
│  │  │ • Sessions   │  │   Chunks     │  │ • Short-term │  │ • Exports    │    │    │
│  │  │ • History    │  │ • Memory     │  │   Memory     │  │ • Backups    │    │    │
│  │  │ • Summaries  │  │   Embeddings │  │ • Pub/Sub    │  │              │    │    │
│  │  │ • Audit Logs │  │ • Metadata   │  │ • Rate Limit │  │              │    │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘    │    │
│  └─────────────────────────────────────────────────────────────────────────────┘    │
│                                                                                      │
└─────────────────────────────────────────────────────────────────────────────────────┘
2.2 Memory Architecture (Critical for Context-Awareness)
text

┌─────────────────────────────────────────────────────────────────────────────────────┐
│                        HIERARCHICAL MEMORY ARCHITECTURE                              │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                      │
│  ┌─────────────────────────────────────────────────────────────────────────────┐    │
│  │                         LONG-TERM MEMORY                                     │    │
│  │                     (Persistent Across Sessions)                             │    │
│  │  ┌─────────────────────────────────────────────────────────────────────┐    │    │
│  │  │  CUSTOMER PROFILE STORE                                              │    │    │
│  │  │  ┌─────────────────────────────────────────────────────────────┐    │    │    │
│  │  │  │  {                                                           │    │    │    │
│  │  │  │    "customer_id": "cust_sg_12345",                          │    │    │    │
│  │  │  │    "preferences": {                                          │    │    │    │
│  │  │  │      "language": "en",                                       │    │    │    │
│  │  │  │      "communication_style": "formal",                        │    │    │    │
│  │  │  │      "timezone": "Asia/Singapore"                            │    │    │    │
│  │  │  │    },                                                        │    │    │    │
│  │  │  │    "history_summary": "Frequent buyer, 3 previous support   │    │    │    │
│  │  │  │                        tickets about delivery. Prefers       │    │    │    │
│  │  │  │                        email follow-up.",                    │    │    │    │
│  │  │  │    "key_entities": ["Order #A1234", "Product SKU-789"],      │    │    │    │
│  │  │  │    "sentiment_trend": "neutral_improving",                   │    │    │    │
│  │  │  │    "last_interaction": "2025-01-10T14:30:00+08:00"          │    │    │    │
│  │  │  │  }                                                           │    │    │    │
│  │  │  └─────────────────────────────────────────────────────────────┘    │    │    │
│  │  └─────────────────────────────────────────────────────────────────────┘    │    │
│  │  ┌─────────────────────────────────────────────────────────────────────┐    │    │
│  │  │  CONVERSATION SUMMARIES (Vector-Indexed for Retrieval)            │    │    │
│  │  │  ┌─────────────────────────────────────────────────────────────┐    │    │    │
│  │  │  │  Session: sess_abc123 | Date: 2025-01-08                    │    │    │    │
│  │  │  │  Summary: "Customer inquired about return policy for        │    │    │    │
│  │  │  │           electronics. Explained 14-day policy. Customer    │    │    │    │
│  │  │  │           satisfied. Mentioned they might return headphones │    │    │    │
│  │  │  │           purchased last week."                             │    │    │    │
│  │  │  │  Resolution: RESOLVED | Entities: [headphones, return]      │    │    │    │
│  │  │  └─────────────────────────────────────────────────────────────┘    │    │    │
│  │  └─────────────────────────────────────────────────────────────────────┘    │    │
│  │  Storage: PostgreSQL (structured) + Qdrant (embeddings)                    │    │
│  │  Retention: Configurable (default 365 days, PDPA compliant)                │    │
│  └─────────────────────────────────────────────────────────────────────────────┘    │
│                                      │                                               │
│                                      │ Retrieved on session start                    │
│                                      ▼                                               │
│  ┌─────────────────────────────────────────────────────────────────────────────┐    │
│  │                         SHORT-TERM MEMORY                                    │    │
│  │                      (Active Conversation Session)                           │    │
│  │  ┌─────────────────────────────────────────────────────────────────────┐    │    │
│  │  │  CONVERSATION BUFFER                                                 │    │    │
│  │  │  ┌─────────────────────────────────────────────────────────────┐    │    │    │
│  │  │  │  [                                                           │    │    │    │
│  │  │  │    {"role": "user", "content": "Hi, I have a question..."},  │    │    │    │
│  │  │  │    {"role": "assistant", "content": "Hello! I'd be happy..."}, │    │    │    │
│  │  │  │    {"role": "user", "content": "It's about my order..."},    │    │    │    │
│  │  │  │    {"role": "assistant", "content": "I can help with that..."},│    │    │    │
│  │  │  │    // ... rolling window, max 20 turns                       │    │    │    │
│  │  │  │  ]                                                           │    │    │    │
│  │  │  └─────────────────────────────────────────────────────────────┘    │    │    │
│  │  └─────────────────────────────────────────────────────────────────────┘    │    │
│  │  ┌─────────────────────────────────────────────────────────────────────┐    │    │
│  │  │  SESSION STATE                                                       │    │    │
│  │  │  ┌─────────────────────────────────────────────────────────────┐    │    │    │
│  │  │  │  {                                                           │    │    │    │
│  │  │  │    "current_intent": "order_tracking",                       │    │    │    │
│  │  │  │    "extracted_entities": {"order_id": "ORD-12345"},         │    │    │    │
│  │  │  │    "conversation_stage": "information_gathering",            │    │    │    │
│  │  │  │    "pending_actions": [],                                    │    │    │    │
│  │  │  │    "escalation_flag": false                                  │    │    │    │
│  │  │  │  }                                                           │    │    │    │
│  │  │  └─────────────────────────────────────────────────────────────┘    │    │    │
│  │  └─────────────────────────────────────────────────────────────────────┘    │    │
│  │  Storage: Redis (TTL: 2 hours of inactivity)                               │    │
│  │  Overflow Strategy: Summarize oldest turns when buffer exceeds limit       │    │
│  └─────────────────────────────────────────────────────────────────────────────┘    │
│                                      │                                               │
│                                      │ Assembled per-request                         │
│                                      ▼                                               │
│  ┌─────────────────────────────────────────────────────────────────────────────┐    │
│  │                         WORKING MEMORY                                       │    │
│  │                    (Optimized Context for LLM Call)                          │    │
│  │  ┌─────────────────────────────────────────────────────────────────────┐    │    │
│  │  │  ASSEMBLED CONTEXT (Max ~6000 tokens for GPT-4o-mini)               │    │    │
│  │  │  ┌─────────────────────────────────────────────────────────────┐    │    │    │
│  │  │  │  1. SYSTEM PROMPT (500 tokens)                               │    │    │    │
│  │  │  │     - Role definition, company context, tone guidelines     │    │    │    │
│  │  │  │                                                              │    │    │    │
│  │  │  │  2. CUSTOMER CONTEXT (300 tokens)                            │    │    │    │
│  │  │  │     - Profile summary, relevant history, preferences        │    │    │    │
│  │  │  │                                                              │    │    │    │
│  │  │  │  3. RETRIEVED KNOWLEDGE (2000 tokens)                        │    │    │    │
│  │  │  │     - Reranked, compressed RAG results with citations       │    │    │    │
│  │  │  │                                                              │    │    │    │
│  │  │  │  4. RECENT CONVERSATION (2500 tokens)                        │    │    │    │
│  │  │  │     - Last N turns from short-term buffer                   │    │    │    │
│  │  │  │                                                              │    │    │    │
│  │  │  │  5. CURRENT QUERY + INSTRUCTIONS (700 tokens)                │    │    │    │
│  │  │  │     - User message, output format requirements              │    │    │    │
│  │  │  └─────────────────────────────────────────────────────────────┘    │    │    │
│  │  └─────────────────────────────────────────────────────────────────────┘    │    │
│  │  Storage: In-memory (request lifecycle only)                               │    │
│  │  Optimization: Dynamic token allocation based on query complexity          │    │
│  └─────────────────────────────────────────────────────────────────────────────┘    │
│                                                                                      │
└─────────────────────────────────────────────────────────────────────────────────────┘
2.3 RAG Pipeline Architecture (Following Guide Best Practices)
text

┌─────────────────────────────────────────────────────────────────────────────────────┐
│                          ADVANCED RAG PIPELINE                                       │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                      │
│  ═══════════════════════════════════════════════════════════════════════════════    │
│  ║                        OFFLINE INDEXING PIPELINE                            ║    │
│  ═══════════════════════════════════════════════════════════════════════════════    │
│                                                                                      │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │   SOURCES    │    │    PARSE     │    │    CLEAN     │    │    CHUNK     │      │
│  │              │───▶│              │───▶│              │───▶│              │      │
│  │ • PDFs       │    │ Unstructured │    │ • Noise      │    │ Semantic +   │      │
│  │ • DOCX       │    │    .io       │    │   removal    │    │ Recursive    │      │
│  │ • HTML       │    │              │    │ • Unicode    │    │              │      │
│  │ • Markdown   │    │ LlamaParse   │    │   normalize  │    │ Chunk Size:  │      │
│  │ • Notion     │    │ (for tables) │    │ • Header/    │    │ 512-768 tok  │      │
│  │              │    │              │    │   footer rm  │    │ Overlap: 64  │      │
│  └──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘      │
│                                                                    │                 │
│                                                                    ▼                 │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │   QDRANT     │◀───│    INDEX     │◀───│   ENRICH     │◀───│   EMBED      │      │
│  │              │    │              │    │              │    │              │      │
│  │ Collection:  │    │ • Vector     │    │ • Source     │    │ text-embed-  │      │
│  │ smb_kb       │    │   index      │    │ • Category   │    │ ding-3-small │      │
│  │              │    │ • BM25       │    │ • Date       │    │              │      │
│  │ Metadata:    │    │   index      │    │ • Summary    │    │ Dimension:   │      │
│  │ • source     │    │              │    │   (LLM)      │    │ 1536         │      │
│  │ • category   │    │ HNSW config  │    │ • Keywords   │    │              │      │
│  │ • chunk_id   │    │              │    │   (LLM)      │    │ Batch: 100   │      │
│  └──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘      │
│                                                                                      │
│  ═══════════════════════════════════════════════════════════════════════════════    │
│  ║                        ONLINE RETRIEVAL PIPELINE                            ║    │
│  ═══════════════════════════════════════════════════════════════════════════════    │
│                                                                                      │
│  ┌──────────────────────────────────────────────────────────────────────────────┐   │
│  │  USER QUERY: "What's your return policy for electronics bought last week?"  │   │
│  └──────────────────────────────────────────────────────────────────────────────┘   │
│                                          │                                           │
│                                          ▼                                           │
│  ┌─────────────────────────────────────────────────────────────────────────────┐    │
│  │                    STAGE 1: QUERY TRANSFORMATION                            │    │
│  │  ┌────────────────────────────────────────────────────────────────────┐    │    │
│  │  │  Query Analyzer (LLM)                                               │    │    │
│  │  │  ┌────────────────────────────────────────────────────────────┐    │    │    │
│  │  │  │  Input: Original query + conversation context               │    │    │    │
│  │  │  │                                                             │    │    │    │
│  │  │  │  Techniques Applied:                                        │    │    │    │
│  │  │  │  1. Query Expansion:                                        │    │    │    │
│  │  │  │     → "return policy electronics" + "refund" + "exchange"  │    │    │    │
│  │  │  │                                                             │    │    │    │
│  │  │  │  2. Sub-Question Decomposition:                             │    │    │    │
│  │  │  │     → Q1: "What is the return policy for electronics?"     │    │    │    │
│  │  │  │     → Q2: "What is the return window timeframe?"           │    │    │    │
│  │  │  │     → Q3: "Are there conditions for electronics returns?"  │    │    │    │
│  │  │  │                                                             │    │    │    │
│  │  │  │  3. Metadata Filter Extraction:                             │    │    │    │
│  │  │  │     → category: ["returns", "policy", "electronics"]       │    │    │    │
│  │  │  └────────────────────────────────────────────────────────────┘    │    │    │
│  │  └────────────────────────────────────────────────────────────────────┘    │    │
│  └─────────────────────────────────────────────────────────────────────────────┘    │
│                                          │                                           │
│                                          ▼                                           │
│  ┌─────────────────────────────────────────────────────────────────────────────┐    │
│  │                    STAGE 2: HYBRID RETRIEVAL                                │    │
│  │  ┌──────────────────────────────┐    ┌──────────────────────────────┐      │    │
│  │  │  SEMANTIC SEARCH (Dense)     │    │  KEYWORD SEARCH (Sparse)     │      │    │
│  │  │  ┌─────────────────────────┐ │    │  ┌─────────────────────────┐ │      │    │
│  │  │  │  Qdrant Vector Search   │ │    │  │  BM25 over Qdrant       │ │      │    │
│  │  │  │                         │ │    │  │                         │ │      │    │
│  │  │  │  • Embed transformed    │ │    │  │  • Exact keyword match  │ │      │    │
│  │  │  │    queries              │ │    │  │  • TF-IDF scoring       │ │      │    │
│  │  │  │  • Cosine similarity    │ │    │  │                         │ │      │    │
│  │  │  │  • Top-K: 30            │ │    │  │  • Top-K: 30            │ │      │    │
│  │  │  │  • Metadata filter      │ │    │  │  • Same filters         │ │      │    │
│  │  │  └─────────────────────────┘ │    │  └─────────────────────────┘ │      │    │
│  │  └──────────────────────────────┘    └──────────────────────────────┘      │    │
│  │                    │                              │                         │    │
│  │                    └──────────────┬───────────────┘                         │    │
│  │                                   ▼                                         │    │
│  │                    ┌──────────────────────────────┐                         │    │
│  │                    │  RECIPROCAL RANK FUSION      │                         │    │
│  │                    │  ┌─────────────────────────┐ │                         │    │
│  │                    │  │  RRF(d) = Σ 1/(k + r_i) │ │                         │    │
│  │                    │  │  k = 60 (constant)      │ │                         │    │
│  │                    │  │  Output: Top 50 fused   │ │                         │    │
│  │                    │  └─────────────────────────┘ │                         │    │
│  │                    └──────────────────────────────┘                         │    │
│  └─────────────────────────────────────────────────────────────────────────────┘    │
│                                          │                                           │
│                                          ▼                                           │
│  ┌─────────────────────────────────────────────────────────────────────────────┐    │
│  │                    STAGE 3: RERANKING                                       │    │
│  │  ┌────────────────────────────────────────────────────────────────────┐    │    │
│  │  │  Cross-Encoder Reranker (ms-marco-MiniLM-L-12-v2)                  │    │    │
│  │  │  ┌────────────────────────────────────────────────────────────┐    │    │    │
│  │  │  │  • Input: (query, document) pairs                          │    │    │    │
│  │  │  │  • Deep token-level interaction analysis                   │    │    │    │
│  │  │  │  • Output: Relevance score [0, 1]                          │    │    │    │
│  │  │  │  • Select: Top 5-8 for final context                       │    │    │    │
│  │  │  │  • Processing: ~100ms for 50 candidates                    │    │    │    │
│  │  │  └────────────────────────────────────────────────────────────┘    │    │    │
│  │  └────────────────────────────────────────────────────────────────────┘    │    │
│  └─────────────────────────────────────────────────────────────────────────────┘    │
│                                          │                                           │
│                                          ▼                                           │
│  ┌─────────────────────────────────────────────────────────────────────────────┐    │
│  │                    STAGE 4: CONTEXT COMPRESSION                             │    │
│  │  ┌────────────────────────────────────────────────────────────────────┐    │    │
│  │  │  Extractive Compression                                             │    │    │
│  │  │  ┌────────────────────────────────────────────────────────────┐    │    │    │
│  │  │  │  • Sentence-level relevance scoring                        │    │    │    │
│  │  │  │  • Remove redundant information across chunks              │    │    │    │
│  │  │  │  • Preserve citation metadata                               │    │    │    │
│  │  │  │  • Target: ~2000 tokens final context                       │    │    │    │
│  │  │  └────────────────────────────────────────────────────────────┘    │    │    │
│  │  └────────────────────────────────────────────────────────────────────┘    │    │
│  └─────────────────────────────────────────────────────────────────────────────┘    │
│                                          │                                           │
│                                          ▼                                           │
│  ┌─────────────────────────────────────────────────────────────────────────────┐    │
│  │                    STAGE 5: GENERATION                                      │    │
│  │  ┌────────────────────────────────────────────────────────────────────┐    │    │
│  │  │  Final Context Assembly → LLM (GPT-4o-mini) → Validated Response   │    │    │
│  │  │  ┌────────────────────────────────────────────────────────────┐    │    │    │
│  │  │  │  [System Prompt]                                           │    │    │    │
│  │  │  │  [Customer Context from Long-Term Memory]                  │    │    │    │
│  │  │  │  [Retrieved Knowledge with Citations]                      │    │    │    │
│  │  │  │  [Conversation History from Short-Term Memory]             │    │    │    │
│  │  │  │  [Current Query]                                           │    │    │    │
│  │  │  │  [Response Format Instructions]                            │    │    │    │
│  │  │  └────────────────────────────────────────────────────────────┘    │    │    │
│  │  └────────────────────────────────────────────────────────────────────┘    │    │
│  └─────────────────────────────────────────────────────────────────────────────┘    │
│                                                                                      │
└─────────────────────────────────────────────────────────────────────────────────────┘
2.4 LangGraph Agent State Machine
text

┌─────────────────────────────────────────────────────────────────────────────────────┐
│                       LANGGRAPH AGENT STATE MACHINE                                  │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                      │
│                              ┌─────────────────┐                                     │
│                              │     START       │                                     │
│                              └────────┬────────┘                                     │
│                                       │                                              │
│                                       ▼                                              │
│  ┌────────────────────────────────────────────────────────────────────────────┐     │
│  │                           INTAKE NODE                                       │     │
│  │  ┌────────────────────────────────────────────────────────────────────┐    │     │
│  │  │  Functions:                                                         │    │     │
│  │  │  • Parse incoming message                                          │    │     │
│  │  │  • Load customer context from long-term memory                     │    │     │
│  │  │  • Load conversation buffer from short-term memory                 │    │     │
│  │  │  • Extract initial entities (order IDs, product names, dates)      │    │     │
│  │  │  • Detect language (for multilingual support)                      │    │     │
│  │  │                                                                     │    │     │
│  │  │  Output → AgentState:                                              │    │     │
│  │  │  {                                                                  │    │     │
│  │  │    "messages": [...],                                              │    │     │
│  │  │    "customer_context": {...},                                      │    │     │
│  │  │    "extracted_entities": {...},                                    │    │     │
│  │  │    "language": "en"                                                │    │     │
│  │  │  }                                                                  │    │     │
│  │  └────────────────────────────────────────────────────────────────────┘    │     │
│  └────────────────────────────────────────────────────────────────────────────┘     │
│                                       │                                              │
│                                       ▼                                              │
│  ┌────────────────────────────────────────────────────────────────────────────┐     │
│  │                           ROUTER NODE                                       │     │
│  │  ┌────────────────────────────────────────────────────────────────────┐    │     │
│  │  │  Intent Classification (LLM with Pydantic output schema):          │    │     │
│  │  │                                                                     │    │     │
│  │  │  class IntentClassification(BaseModel):                            │    │     │
│  │  │      intent: Literal[                                              │    │     │
│  │  │          "general_inquiry",      # → RAG path                      │    │     │
│  │  │          "order_status",         # → Tool path (order lookup)      │    │     │
│  │  │          "appointment_booking",  # → Tool path (booking)           │    │     │
│  │  │          "complaint",            # → Escalation consideration      │    │     │
│  │  │          "feedback",             # → Feedback collection           │    │     │
│  │  │          "greeting",             # → Quick response                │    │     │
│  │  │          "unclear"               # → Clarification request         │    │     │
│  │  │      ]                                                             │    │     │
│  │  │      confidence: float                                             │    │     │
│  │  │      requires_rag: bool                                            │    │     │
│  │  │      requires_tool: Optional[str]                                  │    │     │
│  │  │      escalation_risk: Literal["low", "medium", "high"]             │    │     │
│  │  └────────────────────────────────────────────────────────────────────┘    │     │
│  └────────────────────────────────────────────────────────────────────────────┘     │
│                                       │                                              │
│           ┌───────────────────────────┼───────────────────────────┐                  │
│           │                           │                           │                  │
│           ▼                           ▼                           ▼                  │
│  ┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐            │
│  │   RAG NODE      │       │   TOOL NODE     │       │ ESCALATION NODE │            │
│  │                 │       │                 │       │                 │            │
│  │ • Query         │       │ • Determine     │       │ • Log issue     │            │
│  │   transform     │       │   which tool    │       │ • Create ticket │            │
│  │ • Hybrid search │       │ • Execute tool  │       │ • Notify human  │            │
│  │ • Rerank        │       │ • Parse result  │       │ • Graceful msg  │            │
│  │ • Compress      │       │                 │       │                 │            │
│  │ • Cite sources  │       │ Tools:          │       │ Triggers:       │            │
│  │                 │       │ • order_lookup  │       │ • High frustrat │            │
│  │                 │       │ • booking_check │       │ • Complex issue │            │
│  │                 │       │ • payment_status│       │ • Explicit req  │            │
│  │                 │       │ • faq_search    │       │ • 3+ failed att │            │
│  └────────┬────────┘       └────────┬────────┘       └────────┬────────┘            │
│           │                         │                         │                      │
│           │                         │                         │                      │
│           └─────────────────────────┼─────────────────────────┘                      │
│                                     │                                                │
│                                     ▼                                                │
│  ┌────────────────────────────────────────────────────────────────────────────┐     │
│  │                        RESPONSE GENERATOR NODE                              │     │
│  │  ┌────────────────────────────────────────────────────────────────────┐    │     │
│  │  │  Pydantic Output Schema:                                            │    │     │
│  │  │                                                                     │    │     │
│  │  │  class AgentResponse(BaseModel):                                   │    │     │
│  │  │      message: str                    # Main response                │    │     │
│  │  │      citations: List[Citation]       # Source references           │    │     │
│  │  │      suggested_actions: List[str]    # Follow-up suggestions       │    │     │
│  │  │      confidence: float               # Response confidence         │    │     │
│  │  │      requires_followup: bool         # Does agent need more info?  │    │     │
│  │  │      sentiment: Literal["positive", "neutral", "negative"]         │    │     │
│  │  │                                                                     │    │     │
│  │  │  Generation Guidelines:                                             │    │     │
│  │  │  • Tone: Professional but warm (Singaporean business context)     │    │     │
│  │  │  • Length: Concise (2-4 sentences default)                        │    │     │
│  │  │  • Structure: Answer first, then details if needed                │    │     │
│  │  │  • Always offer next steps                                         │    │     │
│  │  └────────────────────────────────────────────────────────────────────┘    │     │
│  └────────────────────────────────────────────────────────────────────────────┘     │
│                                       │                                              │
│                                       ▼                                              │
│  ┌────────────────────────────────────────────────────────────────────────────┐     │
│  │                        MEMORY UPDATE NODE                                   │     │
│  │  ┌────────────────────────────────────────────────────────────────────┐    │     │
│  │  │  Operations:                                                        │    │     │
│  │  │  1. Append to short-term conversation buffer                       │    │     │
│  │  │  2. Update session state (entities, intent tracking)               │    │     │
│  │  │  3. Check if buffer exceeds limit → trigger summarization          │    │     │
│  │  │  4. If conversation ends → store summary in long-term memory       │    │     │
│  │  │  5. Update customer profile if new preferences detected            │    │     │
│  │  └────────────────────────────────────────────────────────────────────┘    │     │
│  └────────────────────────────────────────────────────────────────────────────┘     │
│                                       │                                              │
│                                       ▼                                              │
│  ┌────────────────────────────────────────────────────────────────────────────┐     │
│  │                         CONDITIONAL EDGE                                    │     │
│  │  ┌────────────────────────────────────────────────────────────────────┐    │     │
│  │  │  if requires_followup or tool_needs_confirmation:                  │    │     │
│  │  │      → LOOP BACK to appropriate node (Router or Tool)              │    │     │
│  │  │  else:                                                              │    │     │
│  │  │      → END (stream response to user)                               │    │     │
│  │  └────────────────────────────────────────────────────────────────────┘    │     │
│  └────────────────────────────────────────────────────────────────────────────┘     │
│                                       │                                              │
│                              ┌────────┴────────┐                                     │
│                              │      END        │                                     │
│                              └─────────────────┘                                     │
│                                                                                      │
└─────────────────────────────────────────────────────────────────────────────────────┘
Phase 3: Technology Stack Validation
3.1 Stack Selection Matrix
Component	Selection	Rationale	Alternatives Considered
Frontend	React 18 + Tailwind 4.0 + Shadcn UI	Type-safe, accessible primitives, modern DX	Vue (less React ecosystem), plain HTML (less maintainable)
API Layer	FastAPI (Python 3.11+)	Async native, Pydantic integration, WebSocket support	Django (heavier), Flask (no native async)
Agent Framework	LangChain 1.0 + LangGraph	Stateful agents, LCEL composition, production-ready	LlamaIndex (more RAG-focused), CrewAI (overkill for single agent)
Structured Output	Pydantic AI	Type validation, schema enforcement, LLM output parsing	Instructor (similar but less integrated)
Vector DB	Qdrant	Rust performance, metadata filtering, hybrid search native, affordable	Milvus (overkill for SMB), Chroma (less production-ready), Weaviate (heavier)
Cache/Session	Redis 7+	Sub-ms latency, pub/sub for real-time, TTL support	Memcached (no persistence), DragonflyDB (newer, less tested)
Primary DB	PostgreSQL 16	JSONB for flexible schemas, full-text search, reliability	MySQL (less JSON support), MongoDB (unnecessary here)
Embedding	OpenAI text-embedding-3-small	Cost-effective ($0.02/1M tokens), 1536 dim, strong performance	Cohere (similar), local models (infra overhead for SMB)
LLM	GPT-4o-mini (primary), GPT-4o (complex)	Best cost/quality ratio, structured output support	Claude (similar), local LLM (latency, cost for SMB)
Reranker	ms-marco-MiniLM-L-12-v2	Open-source, fast, effective	Cohere Rerank (paid), ColBERT (more complex)
Document Processing	Unstructured.io	Multi-format, metadata extraction, production-ready	LlamaParse (for complex only), custom parsers (maintenance burden)
Evaluation	RAGAs + Custom	Standard metrics, LLM-as-judge, integrates with LangChain	TruLens (similar), custom only (reinventing wheel)
3.2 Validation Checklist
Requirement	Validated	Notes
LangChain 1.0 compatibility	✅	Using LCEL, LangGraph for state management
Pydantic AI integration	✅	All agent I/O through Pydantic models
RAG with multi-stage retrieval	✅	Query transform → Hybrid search → Rerank → Compress
Short-term memory	✅	Redis with conversation buffer, rolling window
Long-term memory	✅	PostgreSQL + Qdrant for customer profiles and summaries
Context-aware conversations	✅	Hierarchical memory assembly per request
PDPA compliance	✅	Encryption, consent, retention policies, audit logs
Singapore multilingual	✅	Language detection, English primary, Mandarin support
SMB cost-effectiveness	✅	Tiered LLM usage, efficient embeddings, Qdrant (free tier)
Phase 4: Detailed Implementation Plan
4.1 Project Timeline Overview
text

┌─────────────────────────────────────────────────────────────────────────────────────┐
│                          IMPLEMENTATION TIMELINE                                     │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                      │
│  WEEK 1          WEEK 2          WEEK 3          WEEK 4          WEEK 5-6           │
│  ┌──────┐        ┌──────┐        ┌──────┐        ┌──────┐        ┌────────────┐     │
│  │FOUND-│        │ RAG  │        │AGENT │        │ ADV  │        │  FRONTEND  │     │
│  │ATION │───────▶│PIPE- │───────▶│ CORE │───────▶│FEAT- │───────▶│  + DEPLOY  │     │
│  │      │        │ LINE │        │      │        │ URES │        │            │     │
│  └──────┘        └──────┘        └──────┘        └──────┘        └────────────┘     │
│                                                                                      │
│  • Project       • Ingestion     • LangGraph    • Multi-stage   • React chat       │
│    setup         • Chunking        state          retrieval     • Accessibility    │
│  • Infra         • Embedding       machine      • Reranking     • Real-time        │
│    (Docker)      • Qdrant        • Pydantic     • Compression   • Testing          │
│  • DB schemas      setup           models       • Memory        • CI/CD            │
│  • Basic API     • Basic         • Tools          refinement    • Production       │
│                    retrieval                                       deploy          │
│                                                                                      │
│  ════════════════════════════════════════════════════════════════════════════════   │
│  │ MILESTONE 1   │ MILESTONE 2   │ MILESTONE 3   │ MILESTONE 4   │ MILESTONE 5 │   │
│  │ Infra Ready   │ RAG Works     │ Agent Responds│ Quality Good  │ Production  │   │
│  ════════════════════════════════════════════════════════════════════════════════   │
│                                                                                      │
└─────────────────────────────────────────────────────────────────────────────────────┘
4.2 Phase 1: Foundation (Days 1-5)
Objectives
Establish project structure and development environment
Deploy core infrastructure (databases, cache)
Implement basic API scaffolding with authentication
Detailed Tasks
text

┌─────────────────────────────────────────────────────────────────────────────────────┐
│  PHASE 1 CHECKLIST                                                                   │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                      │
│  □ 1.1 PROJECT SETUP                                                                │
│    □ Initialize monorepo structure (backend/, frontend/, infra/)                    │
│    □ Configure Python 3.11+ environment with Poetry                                 │
│    □ Configure Node.js 20+ with pnpm for frontend                                   │
│    □ Setup pre-commit hooks (ruff, black, prettier, eslint)                         │
│    □ Configure VS Code workspace settings                                           │
│                                                                                      │
│  □ 1.2 INFRASTRUCTURE SETUP                                                         │
│    □ Create Docker Compose for local development:                                   │
│      □ PostgreSQL 16 container                                                      │
│      □ Redis 7 container                                                            │
│      □ Qdrant container (latest)                                                    │
│    □ Create .env.example with all required variables                                │
│    □ Setup docker-compose.override.yml for local volumes                            │
│                                                                                      │
│  □ 1.3 DATABASE SCHEMA                                                              │
│    □ Design and create PostgreSQL tables:                                           │
│      □ customers (id, external_id, preferences JSONB, created_at, updated_at)      │
│      □ conversations (id, customer_id, started_at, ended_at, status, summary)      │
│      □ messages (id, conversation_id, role, content, metadata JSONB, created_at)   │
│      □ conversation_summaries (id, conversation_id, summary_text, embedding_id)    │
│      □ knowledge_documents (id, filename, source_url, category, processed_at)      │
│      □ audit_logs (id, action, entity_type, entity_id, changes JSONB, timestamp)   │
│    □ Create Alembic migration scripts                                               │
│    □ Setup Qdrant collections:                                                      │
│      □ knowledge_base (1536 dim, HNSW index, metadata payload)                     │
│      □ memory_embeddings (1536 dim, for long-term memory retrieval)                │
│                                                                                      │
│  □ 1.4 FASTAPI SCAFFOLDING                                                          │
│    □ Create FastAPI application structure:                                          │
│      □ app/main.py (app factory, lifespan events)                                  │
│      □ app/api/ (routers)                                                          │
│      □ app/core/ (config, security, dependencies)                                  │
│      □ app/models/ (SQLAlchemy models)                                             │
│      □ app/schemas/ (Pydantic schemas)                                             │
│      □ app/services/ (business logic)                                              │
│    □ Implement health check endpoint                                                │
│    □ Setup CORS middleware                                                          │
│    □ Implement basic JWT authentication                                             │
│    □ Create WebSocket endpoint skeleton for chat                                    │
│                                                                                      │
│  □ 1.5 INITIAL PYDANTIC MODELS                                                      │
│    □ Define core schemas:                                                           │
│      □ ChatMessage (role, content, timestamp, metadata)                            │
│      □ CustomerContext (id, preferences, history_summary)                          │
│      □ ConversationState (messages, entities, intent, stage)                       │
│      □ AgentResponse (message, citations, actions, confidence)                     │
│                                                                                      │
│  SUCCESS CRITERIA:                                                                   │
│  ✓ Docker compose up brings all services online                                     │
│  ✓ API health check returns 200                                                     │
│  ✓ Database migrations run successfully                                             │
│  ✓ WebSocket connection can be established                                          │
│                                                                                      │
└─────────────────────────────────────────────────────────────────────────────────────┘
Key Code Structures
Project Structure:

text

smb-support-agent/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── deps.py
│   │   │   ├── v1/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── chat.py
│   │   │   │   ├── admin.py
│   │   │   │   └── health.py
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   └── logging.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── customer.py
│   │   │   ├── conversation.py
│   │   │   └── document.py
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── chat.py
│   │   │   ├── agent.py
│   │   │   └── memory.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── agent/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── graph.py
│   │   │   │   ├── nodes.py
│   │   │   │   └── tools.py
│   │   │   ├── rag/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── indexer.py
│   │   │   │   ├── retriever.py
│   │   │   │   └── reranker.py
│   │   │   ├── memory/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── short_term.py
│   │   │   │   └── long_term.py
│   │   │   └── llm/
│   │   │       ├── __init__.py
│   │   │       └── clients.py
│   │   └── db/
│   │       ├── __init__.py
│   │       ├── session.py
│   │       └── migrations/
│   ├── tests/
│   ├── pyproject.toml
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   ├── components/
│   │   │   ├── ui/  (shadcn)
│   │   │   └── chat/
│   │   ├── hooks/
│   │   ├── lib/
│   │   └── styles/
│   ├── package.json
│   └── Dockerfile
├── infra/
│   ├── docker-compose.yml
│   ├── docker-compose.override.yml
│   └── k8s/  (optional)
├── docs/
├── scripts/
└── README.md
4.3 Phase 2: RAG Pipeline (Days 6-12)
Objectives
Implement complete document ingestion pipeline
Configure chunking with semantic awareness
Setup Qdrant with hybrid search
Implement basic retrieval with quality validation
Detailed Tasks
text

┌─────────────────────────────────────────────────────────────────────────────────────┐
│  PHASE 2 CHECKLIST                                                                   │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                      │
│  □ 2.1 DOCUMENT INGESTION                                                           │
│    □ Install and configure Unstructured.io                                          │
│    □ Create document processor service:                                             │
│      □ PDF parsing with layout preservation                                         │
│      □ DOCX extraction                                                              │
│      □ HTML/Markdown parsing                                                        │
│      □ Metadata extraction (title, author, date, source)                           │
│    □ Implement cleaning pipeline:                                                   │
│      □ Remove headers/footers                                                       │
│      □ Normalize unicode                                                            │
│      □ Remove excessive whitespace                                                  │
│      □ Handle tables (convert to structured text)                                  │
│    □ Create admin endpoint for document upload                                      │
│    □ Store original documents in S3/MinIO                                          │
│                                                                                      │
│  □ 2.2 CHUNKING STRATEGY                                                            │
│    □ Implement RecursiveCharacterTextSplitter as baseline:                          │
│      □ chunk_size: 600 tokens                                                       │
│      □ chunk_overlap: 60 tokens                                                     │
│      □ separators: ["\n\n", "\n", ". ", " "]                                       │
│    □ Implement SemanticChunker for comparison:                                      │
│      □ Use embedding model to detect semantic boundaries                           │
│      □ Configure breakpoint_threshold                                              │
│    □ Create chunking configuration per document type                                │
│    □ Preserve section headers in chunks                                             │
│    □ Add parent document reference to each chunk                                    │
│                                                                                      │
│  □ 2.3 EMBEDDING PIPELINE                                                           │
│    □ Setup OpenAI embedding client:                                                 │
│      □ Model: text-embedding-3-small                                               │
│      □ Batch size: 100 (rate limit aware)                                          │
│      □ Retry logic with exponential backoff                                        │
│    □ Create embedding cache (Redis) for repeated queries                           │
│    □ Implement async batch embedding for large documents                            │
│                                                                                      │
│  □ 2.4 QDRANT CONFIGURATION                                                         │
│    □ Create knowledge_base collection:                                              │
│      □ Vector dimension: 1536                                                       │
│      □ Distance: Cosine                                                             │
│      □ Index: HNSW (m=16, ef_construct=100)                                        │
│    □ Configure payload schema:                                                      │
│      □ chunk_id: keyword                                                            │
│      □ document_id: keyword                                                         │
│      □ source: keyword                                                              │
│      □ category: keyword (indexed for filtering)                                   │
│      □ created_at: datetime                                                         │
│      □ content: text (for BM25)                                                    │
│    □ Enable BM25 index for hybrid search                                            │
│    □ Create indexing service with upsert logic                                      │
│                                                                                      │
│  □ 2.5 BASIC RETRIEVAL                                                              │
│    □ Implement semantic search:                                                     │
│      □ Embed query                                                                  │
│      □ Search with top_k=30                                                         │
│      □ Apply metadata filters                                                       │
│    □ Implement keyword search (BM25):                                               │
│      □ Qdrant's built-in sparse vector search                                      │
│      □ Same top_k=30                                                                │
│    □ Implement Reciprocal Rank Fusion:                                              │
│      □ Combine semantic + keyword results                                          │
│      □ k=60 constant                                                                │
│      □ Return top 50 merged results                                                │
│    □ Create retriever interface for LangChain integration                           │
│                                                                                      │
│  □ 2.6 RETRIEVAL VALIDATION                                                         │
│    □ Create test knowledge base with known Q&A pairs                                │
│    □ Implement retrieval evaluation:                                                │
│      □ Hit rate @ k                                                                 │
│      □ MRR (Mean Reciprocal Rank)                                                  │
│      □ NDCG                                                                         │
│    □ Tune parameters based on results                                               │
│    □ Document baseline metrics                                                      │
│                                                                                      │
│  SUCCESS CRITERIA:                                                                   │
│  ✓ Documents can be uploaded and processed                                          │
│  ✓ Chunks appear in Qdrant with correct metadata                                    │
│  ✓ Semantic search returns relevant results                                         │
│  ✓ Hybrid search outperforms semantic-only                                          │
│  ✓ Retrieval metrics meet baseline (Hit Rate > 0.8 @ k=10)                          │
│                                                                                      │
└─────────────────────────────────────────────────────────────────────────────────────┘
4.4 Phase 3: Agent Core (Days 13-19)
Objectives
Implement LangGraph state machine
Define Pydantic models for all agent I/O
Create core tools (RAG search, order lookup, escalation)
Implement basic short-term memory
Detailed Tasks
text

┌─────────────────────────────────────────────────────────────────────────────────────┐
│  PHASE 3 CHECKLIST                                                                   │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                      │
│  □ 3.1 LANGGRAPH STATE DEFINITION                                                   │
│    □ Define AgentState TypedDict:                                                   │
│      □ messages: List[BaseMessage]                                                  │
│      □ customer_context: CustomerContext                                           │
│      □ extracted_entities: Dict[str, Any]                                          │
│      □ current_intent: Optional[IntentClassification]                              │
│      □ retrieved_context: Optional[List[RetrievedChunk]]                           │
│      □ tool_results: Optional[Dict[str, Any]]                                      │
│      □ response: Optional[AgentResponse]                                           │
│      □ should_escalate: bool                                                        │
│      □ loop_count: int (prevent infinite loops)                                    │
│                                                                                      │
│  □ 3.2 PYDANTIC AI SCHEMAS                                                          │
│    □ Define all agent I/O models:                                                   │
│      □ IntentClassification                                                         │
│      □ QueryTransformation                                                          │
│      □ RetrievedChunk                                                               │
│      □ ToolCallRequest                                                              │
│      □ ToolCallResult                                                               │
│      □ AgentResponse                                                                │
│      □ Citation                                                                     │
│    □ Configure LLM output parsing with Pydantic                                     │
│    □ Add validation and error handling                                              │
│                                                                                      │
│  □ 3.3 GRAPH NODES IMPLEMENTATION                                                   │
│    □ Intake Node:                                                                   │
│      □ Parse incoming WebSocket message                                             │
│      □ Load customer context from DB                                               │
│      □ Load conversation buffer from Redis                                         │
│      □ Simple entity extraction (regex for order IDs, etc.)                        │
│      □ Language detection                                                          │
│                                                                                      │
│    □ Router Node:                                                                   │
│      □ Configure GPT-4o-mini with structured output                                │
│      □ Intent classification prompt                                                 │
│      □ Return IntentClassification                                                  │
│      □ Decision logic for next node                                                 │
│                                                                                      │
│    □ RAG Node:                                                                      │
│      □ Query transformation (expand, decompose)                                    │
│      □ Call retriever service                                                      │
│      □ Store results in state                                                      │
│                                                                                      │
│    □ Tool Node:                                                                     │
│      □ Tool selection based on intent                                              │
│      □ Tool execution with error handling                                          │
│      □ Result parsing                                                               │
│                                                                                      │
│    □ Response Generator Node:                                                       │
│      □ Assemble final context (system + customer + RAG + history)                 │
│      □ Generate response with structured output                                    │
│      □ Include citations                                                            │
│      □ Streaming support                                                            │
│                                                                                      │
│    □ Memory Update Node:                                                            │
│      □ Append to conversation buffer                                               │
│      □ Update session state                                                        │
│      □ Trigger summarization if needed                                             │
│                                                                                      │
│    □ Escalation Node:                                                               │
│      □ Create support ticket                                                        │
│      □ Prepare handoff context                                                      │
│      □ Generate graceful message                                                    │
│                                                                                      │
│  □ 3.4 GRAPH EDGES                                                                  │
│    □ Define conditional edges:                                                      │
│      □ Router → RAG (if requires_rag)                                              │
│      □ Router → Tool (if requires_tool)                                            │
│      □ Router → Escalation (if high risk)                                          │
│      □ Router → Response (if simple greeting)                                      │
│    □ Define standard edges:                                                         │
│      □ Intake → Router                                                              │
│      □ RAG → Response Generator                                                     │
│      □ Tool → Response Generator                                                    │
│      □ Response Generator → Memory Update                                           │
│      □ Memory Update → END (or loop if clarification needed)                       │
│                                                                                      │
│  □ 3.5 TOOL IMPLEMENTATIONS                                                         │
│    □ rag_search tool:                                                               │
│      □ Wrapper around retrieval service                                            │
│      □ Returns top-k chunks with citations                                         │
│    □ order_lookup tool 
Som

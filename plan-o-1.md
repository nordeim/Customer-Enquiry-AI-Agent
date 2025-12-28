Deep Analysis: Customer Enquiry Support AI Agent for Singapore SMBs
Executive Summary
This document presents a comprehensive, production-ready architecture for a Customer Enquiry Support AI Agent tailored for Singapore Small-Medium Businesses. The system integrates LangChain 1.0, Pydantic AI, and advanced RAG methodologies with hierarchical memory layers to deliver context-aware, multi-turn conversations.

Phase 1: Multi-Dimensional Requirement Analysis
1.1 Stakeholder & Context Analysis
text

┌─────────────────────────────────────────────────────────────────────────────┐
│                        SINGAPORE SMB CONTEXT MAPPING                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  BUSINESS PROFILE                    CUSTOMER EXPECTATIONS                  │
│  ─────────────────                   ────────────────────                   │
│  • 10-200 employees                  • 24/7 availability                    │
│  • Limited IT resources              • Sub-5 second responses               │
│  • Cost-conscious operations         • Accurate, consistent answers         │
│  • Multi-channel presence            • Seamless escalation to humans        │
│  • PDPA compliance mandatory         • Multi-lingual support (EN/ZH/MS/TA)  │
│                                                                              │
│  TECHNICAL CONSTRAINTS               SUCCESS METRICS                         │
│  ────────────────────                ───────────────                         │
│  • Cloud-first deployment            • >85% query resolution rate           │
│  • Moderate concurrent load          • <3s average response time            │
│  • Integration with existing CRM     • >90% user satisfaction               │
│  • Mobile-first user base            • <5% escalation rate for FAQ          │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
1.2 Psychological Analysis
Dimension	User Need	System Response
Cognitive Load	Customers seek quick answers without complexity	Concise, actionable responses with optional depth
Trust Building	Skepticism toward bots; fear of loops	Transparent capability disclosure; clear escalation paths
Emotional State	Often frustrated when reaching support	Empathetic tone detection; appropriate response calibration
Cultural Context	Singapore's efficiency-oriented, polite culture	Direct yet courteous responses; respect for formality
1.3 Technical Feasibility Analysis
text

┌─────────────────────────────────────────────────────────────────────────────┐
│                      TECHNOLOGY STACK VALIDATION                             │
├──────────────────┬──────────────────────────────────────────────────────────┤
│ Component        │ Selection Rationale                                       │
├──────────────────┼──────────────────────────────────────────────────────────┤
│ LangChain 1.0    │ ✓ LCEL composition for flexible pipelines                │
│                  │ ✓ Native LangGraph integration for stateful agents       │
│                  │ ✓ Extensive retriever ecosystem                          │
│                  │ ⚠ Breaking changes from 0.x require careful migration   │
├──────────────────┼──────────────────────────────────────────────────────────┤
│ Pydantic AI      │ ✓ Type-safe structured outputs                           │
│                  │ ✓ Runtime validation prevents hallucination propagation  │
│                  │ ✓ Seamless FastAPI integration                           │
├──────────────────┼──────────────────────────────────────────────────────────┤
│ Qdrant           │ ✓ Hybrid search native support                           │
│                  │ ✓ Rich metadata filtering                                │
│                  │ ✓ Rust performance for low-latency retrieval             │
│                  │ ✓ Self-hosted or cloud options (SMB flexibility)         │
├──────────────────┼──────────────────────────────────────────────────────────┤
│ Redis            │ ✓ Sub-millisecond short-term memory access               │
│                  │ ✓ Native TTL for session expiration                      │
│                  │ ✓ Pub/Sub for real-time streaming                        │
├──────────────────┼──────────────────────────────────────────────────────────┤
│ React + Tailwind │ ✓ Component-based chatbox architecture                   │
│                  │ ✓ Real-time streaming via SSE/WebSocket                  │
│                  │ ✓ Accessibility primitives available                     │
└──────────────────┴──────────────────────────────────────────────────────────┘
Phase 2: System Architecture Design
2.1 High-Level Architecture
text

┌─────────────────────────────────────────────────────────────────────────────────────┐
│                                                                                      │
│                        CUSTOMER ENQUIRY AI AGENT - SYSTEM ARCHITECTURE              │
│                                                                                      │
│  ┌────────────────────────────────────────────────────────────────────────────────┐ │
│  │                              PRESENTATION LAYER                                 │ │
│  │                                                                                 │ │
│  │    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐          │ │
│  │    │   React Chat    │    │   Mobile Web    │    │  Widget Embed   │          │ │
│  │    │   Interface     │    │   Responsive    │    │   (iframe/SDK)  │          │ │
│  │    └────────┬────────┘    └────────┬────────┘    └────────┬────────┘          │ │
│  │             │                      │                      │                    │ │
│  │             └──────────────────────┼──────────────────────┘                    │ │
│  │                                    │                                           │ │
│  │                          ┌─────────▼─────────┐                                 │ │
│  │                          │   WebSocket/SSE   │                                 │ │
│  │                          │   Streaming Layer │                                 │ │
│  │                          └─────────┬─────────┘                                 │ │
│  └────────────────────────────────────┼───────────────────────────────────────────┘ │
│                                       │                                              │
│  ┌────────────────────────────────────┼───────────────────────────────────────────┐ │
│  │                              API GATEWAY                                        │ │
│  │                                    │                                            │ │
│  │    ┌───────────────────────────────▼───────────────────────────────────┐       │ │
│  │    │                         FastAPI Server                             │       │ │
│  │    │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────────┐  │       │ │
│  │    │  │   Auth   │  │   Rate   │  │  Request │  │   Response       │  │       │ │
│  │    │  │  (JWT)   │  │  Limiter │  │  Valid.  │  │   Streaming      │  │       │ │
│  │    │  └──────────┘  └──────────┘  └──────────┘  └──────────────────┘  │       │ │
│  │    └───────────────────────────────┬───────────────────────────────────┘       │ │
│  └────────────────────────────────────┼───────────────────────────────────────────┘ │
│                                       │                                              │
│  ┌────────────────────────────────────┼───────────────────────────────────────────┐ │
│  │                           AGENT ORCHESTRATION LAYER                             │ │
│  │                                    │                                            │ │
│  │    ┌───────────────────────────────▼───────────────────────────────────┐       │ │
│  │    │                    LangGraph State Machine                         │       │ │
│  │    │                                                                    │       │ │
│  │    │   ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐       │       │ │
│  │    │   │ INTAKE  │───▶│ REASON  │───▶│  ACT    │───▶│ RESPOND │       │       │ │
│  │    │   │  Node   │    │  Node   │    │  Node   │    │  Node   │       │       │ │
│  │    │   └─────────┘    └────┬────┘    └────┬────┘    └─────────┘       │       │ │
│  │    │                       │              │                            │       │ │
│  │    │                       ▼              ▼                            │       │ │
│  │    │              ┌────────────────────────────────┐                  │       │ │
│  │    │              │         TOOL REGISTRY          │                  │       │ │
│  │    │              │  ┌──────┐ ┌──────┐ ┌────────┐ │                  │       │ │
│  │    │              │  │ RAG  │ │ FAQ  │ │Escalate│ │                  │       │ │
│  │    │              │  │Search│ │Lookup│ │ Human  │ │                  │       │ │
│  │    │              │  └──────┘ └──────┘ └────────┘ │                  │       │ │
│  │    │              └────────────────────────────────┘                  │       │ │
│  │    └───────────────────────────────────────────────────────────────────┘       │ │
│  └────────────────────────────────────────────────────────────────────────────────┘ │
│                                       │                                              │
│  ┌────────────────────────────────────┼───────────────────────────────────────────┐ │
│  │                           MEMORY MANAGEMENT LAYER                               │ │
│  │                                    │                                            │ │
│  │    ┌───────────────────────────────┴───────────────────────────────────┐       │ │
│  │    │                                                                    │       │ │
│  │    │   ┌──────────────────┐  ┌──────────────────┐  ┌────────────────┐ │       │ │
│  │    │   │   SHORT-TERM     │  │    LONG-TERM     │  │    WORKING     │ │       │ │
│  │    │   │     MEMORY       │  │     MEMORY       │  │    MEMORY      │ │       │ │
│  │    │   │                  │  │                  │  │                │ │       │ │
│  │    │   │ ┌──────────────┐ │  │ ┌──────────────┐ │  │ ┌────────────┐ │ │       │ │
│  │    │   │ │    Redis     │ │  │ │    Qdrant    │ │  │ │  Context   │ │ │       │ │
│  │    │   │ │  Conversation│ │  │ │   User       │ │  │ │  Window    │ │ │       │ │
│  │    │   │ │    Buffer    │ │  │ │   History    │ │  │ │  Assembly  │ │ │       │ │
│  │    │   │ └──────────────┘ │  │ └──────────────┘ │  │ └────────────┘ │ │       │ │
│  │    │   │                  │  │                  │  │                │ │       │ │
│  │    │   │ • Last N turns   │  │ • Semantic index │  │ • Compressed   │ │       │ │
│  │    │   │ • Session state  │  │ • User profiles  │  │   context      │ │       │ │
│  │    │   │ • Auto-summarize │  │ • Past issues    │  │ • Ready for    │ │       │ │
│  │    │   │   on overflow    │  │ • Preferences    │  │   LLM prompt   │ │       │ │
│  │    │   └──────────────────┘  └──────────────────┘  └────────────────┘ │       │ │
│  │    │                                                                    │       │ │
│  │    └────────────────────────────────────────────────────────────────────┘       │ │
│  └────────────────────────────────────────────────────────────────────────────────┘ │
│                                       │                                              │
│  ┌────────────────────────────────────┼───────────────────────────────────────────┐ │
│  │                          RAG PIPELINE LAYER                                     │ │
│  │                                    │                                            │ │
│  │    ┌───────────────────────────────┴───────────────────────────────────┐       │ │
│  │    │                     MULTI-STAGE RETRIEVAL                          │       │ │
│  │    │                                                                    │       │ │
│  │    │   ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────────┐   │       │ │
│  │    │   │  QUERY  │───▶│ HYBRID  │───▶│ RERANK  │───▶│  COMPRESS   │   │       │ │
│  │    │   │TRANSFORM│    │ SEARCH  │    │         │    │             │   │       │ │
│  │    │   └─────────┘    └─────────┘    └─────────┘    └─────────────┘   │       │ │
│  │    │                                                                    │       │ │
│  │    │   • Rewrite       • BM25+Dense   • Cross-encoder  • Extract key   │       │ │
│  │    │   • Expand        • RRF fusion   • Top-K select   • Summarize     │       │ │
│  │    │   • Decompose     • Metadata     • Score filter   • Token limit   │       │ │
│  │    │                     filtering                                      │       │ │
│  │    └────────────────────────────────────────────────────────────────────┘       │ │
│  └────────────────────────────────────────────────────────────────────────────────┘ │
│                                       │                                              │
│  ┌────────────────────────────────────┼───────────────────────────────────────────┐ │
│  │                          KNOWLEDGE LAYER                                        │ │
│  │                                    │                                            │ │
│  │    ┌───────────────────────────────┴───────────────────────────────────┐       │ │
│  │    │                                                                    │       │ │
│  │    │   ┌──────────────────┐  ┌──────────────────┐  ┌────────────────┐ │       │ │
│  │    │   │   VECTOR STORE   │  │   DOCUMENT DB    │  │   METADATA     │ │       │ │
│  │    │   │     (Qdrant)     │  │   (PostgreSQL)   │  │    STORE       │ │       │ │
│  │    │   │                  │  │                  │  │                │ │       │ │
│  │    │   │ • Company FAQs   │  │ • Raw documents  │  │ • Categories   │ │       │ │
│  │    │   │ • Product docs   │  │ • Version history│  │ • Tags         │ │       │ │
│  │    │   │ • Policy guides  │  │ • Audit trail    │  │ • Timestamps   │ │       │ │
│  │    │   │ • Past tickets   │  │                  │  │ • Sources      │ │       │ │
│  │    │   └──────────────────┘  └──────────────────┘  └────────────────┘ │       │ │
│  │    │                                                                    │       │ │
│  │    └────────────────────────────────────────────────────────────────────┘       │ │
│  └────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                      │
└─────────────────────────────────────────────────────────────────────────────────────┘
2.2 Data Flow Architecture
text

┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              CONVERSATION FLOW SEQUENCE                              │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                      │
│   CUSTOMER                    SYSTEM                         KNOWLEDGE              │
│      │                          │                                │                  │
│      │  1. Send Message         │                                │                  │
│      │─────────────────────────▶│                                │                  │
│      │                          │                                │                  │
│      │                          │  2. Load Session Memory        │                  │
│      │                          │◀───────────────────────────────│                  │
│      │                          │     (Redis: short-term)        │                  │
│      │                          │                                │                  │
│      │                          │  3. Load User History          │                  │
│      │                          │◀───────────────────────────────│                  │
│      │                          │     (Qdrant: long-term)        │                  │
│      │                          │                                │                  │
│      │                          │  4. Transform Query            │                  │
│      │                          │──────────┐                     │                  │
│      │                          │          │ (LLM rewrite)       │                  │
│      │                          │◀─────────┘                     │                  │
│      │                          │                                │                  │
│      │                          │  5. Hybrid Search              │                  │
│      │                          │───────────────────────────────▶│                  │
│      │                          │     (BM25 + Vector)            │                  │
│      │                          │                                │                  │
│      │                          │  6. Retrieved Chunks           │                  │
│      │                          │◀───────────────────────────────│                  │
│      │                          │                                │                  │
│      │                          │  7. Cross-Encoder Rerank       │                  │
│      │                          │──────────┐                     │                  │
│      │                          │          │                     │                  │
│      │                          │◀─────────┘                     │                  │
│      │                          │                                │                  │
│      │                          │  8. Context Compression        │                  │
│      │                          │──────────┐                     │                  │
│      │                          │          │                     │                  │
│      │                          │◀─────────┘                     │                  │
│      │                          │                                │                  │
│      │                          │  9. Assemble Working Memory    │                  │
│      │                          │  ┌─────────────────────────┐   │                  │
│      │                          │  │ System Prompt           │   │                  │
│      │                          │  │ + User Profile          │   │                  │
│      │                          │  │ + Conversation History  │   │                  │
│      │                          │  │ + Retrieved Context     │   │                  │
│      │                          │  │ + Current Query         │   │                  │
│      │                          │  └─────────────────────────┘   │                  │
│      │                          │                                │                  │
│      │                          │  10. LLM Generation            │                  │
│      │                          │──────────┐                     │                  │
│      │                          │          │ (Streaming)         │                  │
│      │                          │◀─────────┘                     │                  │
│      │                          │                                │                  │
│      │  11. Stream Response     │                                │                  │
│      │◀─────────────────────────│                                │                  │
│      │     (Token by token)     │                                │                  │
│      │                          │                                │                  │
│      │                          │  12. Update Memories           │                  │
│      │                          │───────────────────────────────▶│                  │
│      │                          │     (Async background)         │                  │
│      │                          │                                │                  │
│      ▼                          ▼                                ▼                  │
│                                                                                      │
└─────────────────────────────────────────────────────────────────────────────────────┘
2.3 Memory Architecture Deep Dive
text

┌─────────────────────────────────────────────────────────────────────────────────────┐
│                         HIERARCHICAL MEMORY SYSTEM                                   │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                      │
│  ╔═══════════════════════════════════════════════════════════════════════════════╗ │
│  ║                          SHORT-TERM MEMORY (Redis)                             ║ │
│  ╠═══════════════════════════════════════════════════════════════════════════════╣ │
│  ║                                                                                ║ │
│  ║  Purpose: Maintain current conversation state within session                  ║ │
│  ║                                                                                ║ │
│  ║  ┌─────────────────────────────────────────────────────────────────────────┐ ║ │
│  ║  │  session:{session_id}:messages                                          │ ║ │
│  ║  │  ┌───────────────────────────────────────────────────────────────────┐  │ ║ │
│  ║  │  │ [                                                                  │  │ ║ │
│  ║  │  │   { role: "user", content: "...", timestamp: "..." },             │  │ ║ │
│  ║  │  │   { role: "assistant", content: "...", timestamp: "..." },        │  │ ║ │
│  ║  │  │   ...                                                              │  │ ║ │
│  ║  │  │ ]                                                                  │  │ ║ │
│  ║  │  └───────────────────────────────────────────────────────────────────┘  │ ║ │
│  ║  └─────────────────────────────────────────────────────────────────────────┘ ║ │
│  ║                                                                                ║ │
│  ║  Configuration:                                                               ║ │
│  ║  • Window size: 10 messages (configurable)                                   ║ │
│  ║  • TTL: 30 minutes of inactivity                                             ║ │
│  ║  • Overflow strategy: Summarize oldest messages via LLM                      ║ │
│  ║                                                                                ║ │
│  ╚═══════════════════════════════════════════════════════════════════════════════╝ │
│                                       │                                              │
│                                       │ Summarize & Archive                          │
│                                       ▼                                              │
│  ╔═══════════════════════════════════════════════════════════════════════════════╗ │
│  ║                          LONG-TERM MEMORY (Qdrant)                             ║ │
│  ╠═══════════════════════════════════════════════════════════════════════════════╣ │
│  ║                                                                                ║ │
│  ║  Purpose: Persistent user history & semantic search across sessions          ║ │
│  ║                                                                                ║ │
│  ║  Collection: user_memories                                                    ║ │
│  ║  ┌─────────────────────────────────────────────────────────────────────────┐ ║ │
│  ║  │  {                                                                       │ ║ │
│  ║  │    id: "mem_abc123",                                                     │ ║ │
│  ║  │    vector: [0.123, 0.456, ...],  // Semantic embedding                  │ ║ │
│  ║  │    payload: {                                                            │ ║ │
│  ║  │      user_id: "user_123",                                                │ ║ │
│  ║  │      type: "conversation_summary",                                       │ ║ │
│  ║  │      content: "User inquired about refund policy for...",               │ ║ │
│  ║  │      outcome: "resolved",                                                │ ║ │
│  ║  │      sentiment: "satisfied",                                             │ ║ │
│  ║  │      topics: ["refund", "shipping", "product_A"],                       │ ║ │
│  ║  │      timestamp: "2025-01-15T10:30:00Z"                                  │ ║ │
│  ║  │    }                                                                      │ ║ │
│  ║  │  }                                                                        │ ║ │
│  ║  └─────────────────────────────────────────────────────────────────────────┘ ║ │
│  ║                                                                                ║ │
│  ║  Collection: user_profiles                                                    ║ │
│  ║  ┌─────────────────────────────────────────────────────────────────────────┐ ║ │
│  ║  │  {                                                                       │ ║ │
│  ║  │    user_id: "user_123",                                                  │ ║ │
│  ║  │    preferences: { language: "en", tone: "formal" },                     │ ║ │
│  ║  │    known_issues: ["order_456 delayed"],                                 │ ║ │
│  ║  │    loyalty_tier: "gold",                                                 │ ║ │
│  ║  │    last_interaction: "2025-01-15T10:30:00Z"                             │ ║ │
│  ║  │  }                                                                        │ ║ │
│  ║  └─────────────────────────────────────────────────────────────────────────┘ ║ │
│  ║                                                                                ║ │
│  ╚═══════════════════════════════════════════════════════════════════════════════╝ │
│                                       │                                              │
│                                       │ Assemble for LLM                             │
│                                       ▼                                              │
│  ╔═══════════════════════════════════════════════════════════════════════════════╗ │
│  ║                          WORKING MEMORY (In-Request)                           ║ │
│  ╠═══════════════════════════════════════════════════════════════════════════════╣ │
│  ║                                                                                ║ │
│  ║  Purpose: Optimized context package for single LLM call                       ║ │
│  ║                                                                                ║ │
│  ║  ┌─────────────────────────────────────────────────────────────────────────┐ ║ │
│  ║  │  SYSTEM PROMPT                                           ~500 tokens    │ ║ │
│  ║  │  ├── Agent persona & capabilities                                       │ ║ │
│  ║  │  ├── Company context (Singapore SMB specifics)                          │ ║ │
│  ║  │  └── Response guidelines & constraints                                  │ ║ │
│  ║  │                                                                          │ ║ │
│  ║  │  USER PROFILE CONTEXT                                    ~200 tokens    │ ║ │
│  ║  │  ├── Retrieved user preferences                                         │ ║ │
│  ║  │  └── Relevant past interaction summaries                                │ ║ │
│  ║  │                                                                          │ ║ │
│  ║  │  CONVERSATION HISTORY                                    ~800 tokens    │ ║ │
│  ║  │  ├── Recent messages (last 10 or summarized)                            │ ║ │
│  ║  │  └── Previous summary if window overflow                                │ ║ │
│  ║  │                                                                          │ ║ │
│  ║  │  RETRIEVED KNOWLEDGE                                     ~1500 tokens   │ ║ │
│  ║  │  ├── Top-K reranked & compressed chunks                                 │ ║ │
│  ║  │  └── Source attributions                                                │ ║ │
│  ║  │                                                                          │ ║ │
│  ║  │  CURRENT QUERY                                           ~100 tokens    │ ║ │
│  ║  │  └── User's latest message                                              │ ║ │
│  ║  │                                                                          │ ║ │
│  ║  │  ─────────────────────────────────────────────────────────────────────  │ ║ │
│  ║  │  TOTAL WORKING MEMORY                                    ~3100 tokens   │ ║ │
│  ║  │  (Leaves ~5000 tokens for response in 8K context model)                 │ ║ │
│  ║  └─────────────────────────────────────────────────────────────────────────┘ ║ │
│  ║                                                                                ║ │
│  ╚═══════════════════════════════════════════════════════════════════════════════╝ │
│                                                                                      │
└─────────────────────────────────────────────────────────────────────────────────────┘
2.4 RAG Pipeline Detail
text

┌─────────────────────────────────────────────────────────────────────────────────────┐
│                          ADVANCED RAG PIPELINE                                       │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                      │
│  STAGE 1: QUERY TRANSFORMATION                                                      │
│  ════════════════════════════════                                                   │
│                                                                                      │
│  ┌─────────────────────────────────────────────────────────────────────────────┐   │
│  │  Original Query: "what's ur return policy for stuff bought last week"       │   │
│  │                                      │                                       │   │
│  │                    ┌─────────────────┼─────────────────┐                    │   │
│  │                    ▼                 ▼                 ▼                    │   │
│  │           ┌────────────────┐ ┌────────────────┐ ┌────────────────┐         │   │
│  │           │    REWRITE     │ │    EXPAND      │ │   DECOMPOSE    │         │   │
│  │           │   (Formalize)  │ │  (Synonyms)    │ │ (Sub-queries)  │         │   │
│  │           └───────┬────────┘ └───────┬────────┘ └───────┬────────┘         │   │
│  │                   │                  │                  │                   │   │
│  │                   ▼                  ▼                  ▼                   │   │
│  │  "What is the    "return policy     "1. Return policy   │                   │   │
│  │   return policy   refund policy      2. Time limits      │                   │   │
│  │   for items       exchange policy    3. Purchase date    │                   │   │
│  │   purchased       product return     eligibility"        │                   │   │
│  │   within the      within 7 days"                         │                   │   │
│  │   last 7 days?"                                          │                   │   │
│  └─────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                      │
│  STAGE 2: HYBRID SEARCH                                                             │
│  ══════════════════════                                                             │
│                                                                                      │
│  ┌─────────────────────────────────────────────────────────────────────────────┐   │
│  │                                                                              │   │
│  │     Transformed Query                                                        │   │
│  │           │                                                                  │   │
│  │     ┌─────┴─────┐                                                           │   │
│  │     ▼           ▼                                                           │   │
│  │  ┌──────────┐  ┌──────────┐                                                 │   │
│  │  │   BM25   │  │  VECTOR  │                                                 │   │
│  │  │ (Sparse) │  │ (Dense)  │                                                 │   │
│  │  └────┬─────┘  └────┬─────┘                                                 │   │
│  │       │             │                                                        │   │
│  │       │  Results    │  Results                                               │   │
│  │       │  ┌──────┐   │  ┌──────┐                                             │   │
│  │       │  │Doc A │   │  │Doc C │                                             │   │
│  │       │  │Doc B │   │  │Doc A │                                             │   │
│  │       │  │Doc E │   │  │Doc D │                                             │   │
│  │       │  └──────┘   │  └──────┘                                             │   │
│  │       │             │                                                        │   │
│  │       └──────┬──────┘                                                        │   │
│  │              ▼                                                               │   │
│  │     ┌────────────────┐                                                       │   │
│  │     │   RRF FUSION   │                                                       │   │
│  │     │                │                                                       │   │
│  │     │ score = Σ 1/(k+rank)                                                  │   │
│  │     │ k = 60 (smoothing)                                                    │   │
│  │     └───────┬────────┘                                                       │   │
│  │             ▼                                                                │   │
│  │     Fused Results: [Doc A, Doc C, Doc B, Doc D, Doc E, ...]                 │   │
│  │     (Top 20-50 candidates)                                                   │   │
│  │                                                                              │   │
│  └─────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                      │
│  STAGE 3: CROSS-ENCODER RERANKING                                                   │
│  ══════════════════════════════════                                                 │
│                                                                                      │
│  ┌─────────────────────────────────────────────────────────────────────────────┐   │
│  │                                                                              │   │
│  │     ┌──────────────────────────────────────────────────────────────────┐    │   │
│  │     │  Cross-Encoder Model (e.g., ms-marco-MiniLM-L-12-v2)             │    │   │
│  │     │                                                                   │    │   │
│  │     │  For each (query, document) pair:                                │    │   │
│  │     │  ┌─────────────────────────────────────────────────────────────┐ │    │   │
│  │     │  │ [CLS] query tokens [SEP] document tokens [SEP]              │ │    │   │
│  │     │  │                          ↓                                   │ │    │   │
│  │     │  │              Relevance Score: 0.0 - 1.0                     │ │    │   │
│  │     │  └─────────────────────────────────────────────────────────────┘ │    │   │
│  │     └──────────────────────────────────────────────────────────────────┘    │   │
│  │                                                                              │   │
│  │     Input:  20 candidates                                                    │   │
│  │     Output: Top 5 with scores > 0.7                                         │   │
│  │                                                                              │   │
│  │     Reranked: [Doc A (0.94), Doc D (0.89), Doc C (0.82), Doc B (0.75), ...]  │   │
│  │                                                                              │   │
│  └─────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                      │
│  STAGE 4: CONTEXT COMPRESSION                                                       │
│  ════════════════════════════                                                       │
│                                                                                      │
│  ┌─────────────────────────────────────────────────────────────────────────────┐   │
│  │                                                                              │   │
│  │     Top-K Chunks (~2000 tokens each × 5 = ~10,000 tokens)                   │   │
│  │                          │                                                   │   │
│  │                          ▼                                                   │   │
│  │     ┌────────────────────────────────────────────────────────────────────┐  │   │
│  │     │              EXTRACTIVE COMPRESSION                                 │  │   │
│  │     │                                                                     │  │   │
│  │     │  • Remove sentences not directly relevant to query                 │  │   │
│  │     │  • Keep only key facts and direct answers                          │  │   │
│  │     │  • Preserve source attribution markers                             │  │   │
│  │     └────────────────────────────────────────────────────────────────────┘  │   │
│  │                          │                                                   │   │
│  │                          ▼                                                   │   │
│  │     Compressed Context (~1500 tokens total)                                 │   │
│  │                                                                              │   │
│  │     ┌────────────────────────────────────────────────────────────────────┐  │   │
│  │     │ [Source: Return Policy v2.1]                                        │  │   │
│  │     │ Items purchased within 14 days may be returned for full refund.    │  │   │
│  │     │ Electronics have a 7-day return window. Receipt required.          │  │   │
│  │     │                                                                     │  │   │
│  │     │ [Source: FAQ - Returns]                                             │  │   │
│  │     │ To initiate a return, visit our website or contact support...      │  │   │
│  │     └────────────────────────────────────────────────────────────────────┘  │   │
│  │                                                                              │   │
│  └─────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                      │
└─────────────────────────────────────────────────────────────────────────────────────┘
Phase 3: Pydantic AI Schema Design
3.1 Core Data Models
Python

"""
Pydantic AI Schema Definitions for Customer Enquiry Agent
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, field_validator
from pydantic_ai import Agent, RunContext


# ═══════════════════════════════════════════════════════════════════════════════
# ENUMERATIONS
# ═══════════════════════════════════════════════════════════════════════════════

class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class EscalationReason(str, Enum):
    COMPLEX_ISSUE = "complex_issue"
    CUSTOMER_REQUEST = "customer_request"
    NEGATIVE_SENTIMENT = "negative_sentiment"
    OUT_OF_SCOPE = "out_of_scope"
    BILLING_DISPUTE = "billing_dispute"
    TECHNICAL_ERROR = "technical_error"


class ConversationStatus(str, Enum):
    ACTIVE = "active"
    RESOLVED = "resolved"
    ESCALATED = "escalated"
    ABANDONED = "abandoned"


class ConfidenceLevel(str, Enum):
    HIGH = "high"        # > 0.85
    MEDIUM = "medium"    # 0.6 - 0.85
    LOW = "low"          # < 0.6


# ═══════════════════════════════════════════════════════════════════════════════
# INPUT SCHEMAS
# ═══════════════════════════════════════════════════════════════════════════════

class CustomerMessage(BaseModel):
    """Incoming customer message with context"""
    
    content: str = Field(
        ..., 
        min_length=1, 
        max_length=4000,
        description="The customer's message content"
    )
    session_id: str = Field(
        ..., 
        pattern=r"^[a-zA-Z0-9-]{36}$",
        description="UUID v4 session identifier"
    )
    user_id: Optional[str] = Field(
        None, 
        description="Authenticated user ID if available"
    )
    language: str = Field(
        default="en",
        pattern=r"^(en|zh|ms|ta)$",
        description="Preferred language code (Singapore context)"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Additional context (device, location, etc.)"
    )
    
    @field_validator('content')
    @classmethod
    def sanitize_content(cls, v: str) -> str:
        """Remove potentially harmful content"""
        # Basic sanitization - extend as needed
        return v.strip()


class ConversationContext(BaseModel):
    """Full context for agent reasoning"""
    
    session_id: str
    user_id: Optional[str]
    messages: List["ChatMessage"]
    user_profile: Optional["UserProfile"]
    retrieved_context: List["RetrievedChunk"]
    current_query: str
    transformed_query: Optional[str] = None


# ═══════════════════════════════════════════════════════════════════════════════
# MEMORY SCHEMAS
# ═══════════════════════════════════════════════════════════════════════════════

class ChatMessage(BaseModel):
    """Single conversation message"""
    
    role: MessageRole
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Optional[Dict[str, Any]] = None


class UserProfile(BaseModel):
    """Long-term user profile from memory"""
    
    user_id: str
    display_name: Optional[str] = None
    preferred_language: str = "en"
    preferred_tone: str = "professional"  # professional, casual, formal
    loyalty_tier: Optional[str] = None
    known_issues: List[str] = Field(default_factory=list)
    interaction_count: int = 0
    last_interaction: Optional[datetime] = None
    notes: Optional[str] = None


class ConversationSummary(BaseModel):
    """Summarized past conversation for long-term storage"""
    
    session_id: str
    user_id: Optional[str]
    summary: str
    topics: List[str]
    outcome: ConversationStatus
    sentiment: str  # positive, neutral, negative
    resolution: Optional[str] = None
    timestamp: datetime
    message_count: int


# ═══════════════════════════════════════════════════════════════════════════════
# RAG SCHEMAS
# ═══════════════════════════════════════════════════════════════════════════════

class RetrievedChunk(BaseModel):
    """Single retrieved document chunk"""
    
    id: str
    content: str
    source: str = Field(..., description="Document source identifier")
    page: Optional[int] = None
    section: Optional[str] = None
    relevance_score: float = Field(..., ge=0.0, le=1.0)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class TransformedQuery(BaseModel):
    """Result of query transformation"""
    
    original: str
    rewritten: str
    expanded_terms: List[str] = Field(default_factory=list)
    sub_queries: List[str] = Field(default_factory=list)
    intent: str = Field(..., description="Detected user intent")
    entities: Dict[str, str] = Field(
        default_factory=dict,
        description="Extracted entities (product, order_id, etc.)"
    )


# ═══════════════════════════════════════════════════════════════════════════════
# OUTPUT SCHEMAS
# ═══════════════════════════════════════════════════════════════════════════════

class AgentResponse(BaseModel):
    """Structured agent response"""
    
    content: str = Field(
        ..., 
        description="The response message to display to customer"
    )
    confidence: float = Field(
        ..., 
        ge=0.0, 
        le=1.0,
        description="Confidence score for this response"
    )
    confidence_level: ConfidenceLevel = Field(
        ...,
        description="Categorized confidence level"
    )
    sources: List[str] = Field(
        default_factory=list,
        description="Source documents used for this response"
    )
    needs_escalation: bool = Field(
        default=False,
        description="Whether this should be escalated to human"
    )
    escalation_reason: Optional[EscalationReason] = None
    suggested_actions: List[str] = Field(
        default_factory=list,
        description="Suggested follow-up actions for customer"
    )
    internal_notes: Optional[str] = Field(
        None,
        description="Internal notes for logging (not shown to customer)"
    )
    
    @field_validator('confidence_level', mode='before')
    @classmethod
    def derive_confidence_level(cls, v, info):
        """Auto-derive confidence level from score if not provided"""
        if v is None and 'confidence' in info.data:
            score = info.data['confidence']
            if score > 0.85:
                return ConfidenceLevel.HIGH
            elif score > 0.6:
                return ConfidenceLevel.MEDIUM
            else:
                return ConfidenceLevel.LOW
        return v


class StreamingChunk(BaseModel):
    """Single chunk in streaming response"""
    
    type: str = Field(..., pattern=r"^(token|metadata|done|error)$")
    content: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


# ═══════════════════════════════════════════════════════════════════════════════
# TOOL SCHEMAS
# ═══════════════════════════════════════════════════════════════════════════════

class SearchToolInput(BaseModel):
    """Input for RAG search tool"""
    
    query: str
    filters: Optional[Dict[str, Any]] = None
    top_k: int = Field(default=10, ge=1, le=50)


class SearchToolOutput(BaseModel):
    """Output from RAG search tool"""
    
    chunks: List[RetrievedChunk]
    total_found: int
    search_time_ms: float


class EscalationToolInput(BaseModel):
    """Input for escalation tool"""
    
    reason: EscalationReason
    priority: str = Field(default="normal", pattern=r"^(low|normal|high|urgent)$")
    summary: str
    conversation_id: str


class EscalationToolOutput(BaseModel):
    """Output from escalation tool"""
    
    ticket_id: str
    estimated_response_time: str
    assigned_team: Optional[str] = None


# ═══════════════════════════════════════════════════════════════════════════════
# AGENT STATE (for LangGraph)
# ═══════════════════════════════════════════════════════════════════════════════

class AgentState(BaseModel):
    """LangGraph agent state"""
    
    session_id: str
    messages: List[ChatMessage]
    user_profile: Optional[UserProfile] = None
    current_query: str
    transformed_query: Optional[TransformedQuery] = None
    retrieved_chunks: List[RetrievedChunk] = Field(default_factory=list)
    working_memory: Optional[str] = None
    response: Optional[AgentResponse] = None
    step_count: int = 0
    max_steps: int = 5
    error: Optional[str] = None


# Forward reference resolution
ConversationContext.model_rebuild()
Phase 4: LangGraph Agent Architecture
text

┌─────────────────────────────────────────────────────────────────────────────────────┐
│                          LANGGRAPH STATE MACHINE                                     │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                      │
│                                 ┌─────────────┐                                     │
│                                 │    START    │                                     │
│                                 └──────┬──────┘                                     │
│                                        │                                            │
│                                        ▼                                            │
│  ┌─────────────────────────────────────────────────────────────────────────────┐   │
│  │                              INTAKE NODE                                     │   │
│  │                                                                              │   │
│  │  • Validate input message                                                   │   │
│  │  • Load session from Redis (short-term memory)                              │   │
│  │  • Retrieve user profile from Qdrant (long-term memory)                     │   │
│  │  • Check for ongoing escalations                                            │   │
│  │                                                                              │   │
│  └─────────────────────────────────┬───────────────────────────────────────────┘   │
│                                    │                                                │
│                                    ▼                                                │
│  ┌─────────────────────────────────────────────────────────────────────────────┐   │
│  │                         QUERY TRANSFORM NODE                                 │   │
│  │                                                                              │   │
│  │  • Rewrite query for clarity                                                │   │
│  │  • Expand with synonyms                                                     │   │
│  │  • Extract entities (order IDs, product names, etc.)                        │   │
│  │  • Classify intent                                                          │   │
│  │                                                                              │   │
│  └─────────────────────────────────┬───────────────────────────────────────────┘   │
│                                    │                                                │
│                                    ▼                                                │
│  ┌─────────────────────────────────────────────────────────────────────────────┐   │
│  │                           RETRIEVE NODE                                      │   │
│  │                                                                              │   │
│  │  • Execute hybrid search (BM25 + Vector)                                    │   │
│  │  • Apply metadata filters based on intent                                   │   │
│  │  • Retrieve relevant user history                                           │   │
│  │                                                                              │   │
│  └─────────────────────────────────┬───────────────────────────────────────────┘   │
│                                    │                                                │
│                                    ▼                                                │
│  ┌─────────────────────────────────────────────────────────────────────────────┐   │
│  │                            RERANK NODE                                       │   │
│  │                                                                              │   │
│  │  • Cross-encoder reranking                                                  │   │
│  │  • Filter by score threshold (> 0.7)                                        │   │
│  │  • Select top-K chunks                                                      │   │
│  │  • Apply context compression                                                │   │
│  │                                                                              │   │
│  └─────────────────────────────────┬───────────────────────────────────────────┘   │
│                                    │                                                │
│                                    ▼                                                │
│  ┌─────────────────────────────────────────────────────────────────────────────┐   │
│  │                           REASON NODE                                        │   │
│  │                                                                              │   │
│  │  • Assemble working memory                                                  │   │
│  │  • Evaluate if escalation is needed                                         │   │
│  │  • Decide on response strategy                                              │   │
│  │                                                                              │   │
│  │  ┌─────────────────────────────────────────────────────────────────────┐    │   │
│  │  │  Decision Logic:                                                     │    │   │
│  │  │  IF retrieval_confidence < 0.5 AND intent == "complaint":           │    │   │
│  │  │      → ESCALATE                                                      │    │   │
│  │  │  ELIF needs_external_api (order_lookup, etc.):                      │    │   │
│  │  │      → TOOL_CALL                                                     │    │   │
│  │  │  ELSE:                                                               │    │   │
│  │  │      → GENERATE                                                      │    │   │
│  │  └─────────────────────────────────────────────────────────────────────┘    │   │
│  │                                                                              │   │
│  └───────────┬──────────────────────┬──────────────────────┬───────────────────┘   │
│              │                      │                      │                        │
│              ▼                      ▼                      ▼                        │
│   ┌──────────────────┐   ┌──────────────────┐   ┌──────────────────┐               │
│   │  ESCALATE NODE   │   │  TOOL CALL NODE  │   │  GENERATE NODE   │               │
│   │                  │   │                  │   │                  │               │
│   │ • Create ticket  │   │ • Call external  │   │ • LLM generation │               │
│   │ • Notify human   │   │   APIs           │   │ • Structured     │               │
│   │ • Set response   │   │ • Update state   │   │   output via     │               │
│   │                  │   │ • Loop back to   │   │   Pydantic       │               │
│   │                  │   │   REASON         │   │                  │               │
│   └────────┬─────────┘   └────────┬─────────┘   └────────┬─────────┘               │
│            │                      │                      │                          │
│            │                      │ (may loop)           │                          │
│            │                      ▲                      │                          │
│            │                      │                      │                          │
│            └──────────────────────┼──────────────────────┘                          │
│                                   │                                                 │
│                                   ▼                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────────┐   │
│  │                           RESPOND NODE                                       │   │
│  │                                                                              │   │
│  │  • Format response for display                                              │   │
│  │  • Attach sources and suggested actions                                     │   │
│  │  • Update short-term memory (Redis)                                         │   │
│  │  • Queue long-term memory update (async)                                    │   │
│  │                                                                              │   │
│  └─────────────────────────────────┬───────────────────────────────────────────┘   │
│                                    │                                                │
│                                    ▼                                                │
│                              ┌─────────────┐                                        │
│                              │     END     │                                        │
│                              └─────────────┘                                        │
│                                                                                      │
└─────────────────────────────────────────────────────────────────────────────────────┘
Phase 5: Implementation Plan
5.1 Project Structure
text

customer-enquiry-agent/
├── 📁 backend/
│   ├── 📁 app/
│   │   ├── 📄 __init__.py
│   │   ├── 📄 main.py                    # FastAPI application entry
│   │   ├── 📄 config.py                  # Environment configuration
│   │   │
│   │   ├── 📁 api/
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 routes.py              # API route definitions
│   │   │   ├── 📄 websocket.py           # WebSocket handlers
│   │   │   └── 📄 middleware.py          # Auth, rate limiting
│   │   │
│   │   ├── 📁 agent/
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 graph.py               # LangGraph state machine
│   │   │   ├── 📄 nodes.py               # Individual node implementations
│   │   │   ├── 📄 tools.py               # Agent tools (search, escalate)
│   │   │   ├── 📄 prompts.py             # System prompts and templates
│   │   │   └── 📄 state.py               # State management
│   │   │
│   │   ├── 📁 memory/
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 short_term.py          # Redis-based session memory
│   │   │   ├── 📄 long_term.py           # Qdrant-based persistent memory
│   │   │   └── 📄 working.py             # Working memory assembly
│   │   │
│   │   ├── 📁 rag/
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 ingestion.py           # Document processing pipeline
│   │   │   ├── 📄 chunking.py            # Chunking strategies
│   │   │   ├── 📄 embeddings.py          # Embedding generation
│   │   │   ├── 📄 retrieval.py           # Hybrid search implementation
│   │   │   ├── 📄 reranking.py           # Cross-encoder reranking
│   │   │   └── 📄 compression.py         # Context compression
│   │   │
│   │   ├── 📁 schemas/
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 inputs.py              # Input validation schemas
│   │   │   ├── 📄 outputs.py             # Response schemas
│   │   │   ├── 📄 memory.py              # Memory data schemas
│   │   │   └── 📄 rag.py                 # RAG-related schemas
│   │   │
│   │   ├── 📁 services/
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 llm.py                 # LLM client abstraction
│   │   │   ├── 📄 vector_store.py        # Qdrant client
│   │   │   ├── 📄 cache.py               # Redis client
│   │   │   └── 📄 escalation.py          # Escalation/ticketing service
│   │   │
│   │   └── 📁 utils/
│   │       ├── 📄 __init__.py
│   │       ├── 📄 logging.py             # Structured logging
│   │       └── 📄 metrics.py             # Observability metrics
│   │
│   ├── 📁 tests/
│   │   ├── 📄 conftest.py
│   │   ├── 📁 unit/
│   │   ├── 📁 integration/
│   │   └── 📁 evaluation/                # RAGAs evaluation tests
│   │
│   ├── 📁 scripts/
│   │   ├── 📄 ingest_documents.py        # Knowledge base ingestion
│   │   ├── 📄 seed_data.py               # Sample data seeding
│   │   └── 📄 evaluate_rag.py            # RAG evaluation runner
│   │
│   ├── 📁 knowledge/                     # Source documents for RAG
│   │   ├── 📁 faqs/
│   │   ├── 📁 policies/
│   │   └── 📁 products/
│   │
│   ├── 📄 pyproject.toml
│   ├── 📄 Dockerfile
│   └── 📄 docker-compose.yml
│
├── 📁 frontend/
│   ├── 📁 src/
│   │   ├── 📁 components/
│   │   │   ├── 📁 chat/
│   │   │   │   ├── 📄 ChatContainer.tsx
│   │   │   │   ├── 📄 MessageList.tsx
│   │   │   │   ├── 📄 MessageBubble.tsx
│   │   │   │   ├── 📄 InputArea.tsx
│   │   │   │   ├── 📄 TypingIndicator.tsx
│   │   │   │   └── 📄 SourcesPanel.tsx
│   │   │   │
│   │   │   └── 📁 ui/                    # Shadcn UI components
│   │   │       ├── 📄 button.tsx
│   │   │       ├── 📄 input.tsx
│   │   │       ├── 📄 scroll-area.tsx
│   │   │       └── 📄 ...
│   │   │
│   │   ├── 📁 hooks/
│   │   │   ├── 📄 useChat.ts             # Chat state management
│   │   │   ├── 📄 useStreaming.ts        # SSE/WebSocket handling
│   │   │   └── 📄 useSession.ts          # Session management
│   │   │
│   │   ├── 📁 lib/
│   │   │   ├── 📄 api.ts                 # API client
│   │   │   └── 📄 utils.ts               # Utility functions
│   │   │
│   │   ├── 📁 styles/
│   │   │   └── 📄 globals.css            # Tailwind + custom styles
│   │   │
│   │   ├── 📄 App.tsx
│   │   └── 📄 main.tsx
│   │
│   ├── 📄 package.json
│   ├── 📄 tailwind.config.ts
│   ├── 📄 tsconfig.json
│   └── 📄 vite.config.ts
│
├── 📁 infra/
│   ├── 📄 docker-compose.yml             # Full stack compose
│   ├── 📁 kubernetes/                    # K8s manifests (optional)
│   └── 📁 terraform/                     # Cloud provisioning (optional)
│
├── 📄 README.md
└── 📄 Makefile                           # Common commands
5.2 Phased Implementation Checklist
text

┌─────────────────────────────────────────────────────────────────────────────────────┐
│                      IMPLEMENTATION PHASES & CHECKLIST                               │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                      │
│  ╔═══════════════════════════════════════════════════════════════════════════════╗ │
│  ║  PHASE 1: FOUNDATION (Week 1-2)                                                ║ │
│  ╠═══════════════════════════════════════════════════════════════════════════════╣ │
│  ║                                                                                ║ │
│  ║  □ 1.1 Project Setup                                                          ║ │
│  ║      □ Initialize Python project with uv/poetry                               ║ │
│  ║      □ Configure pyproject.toml with dependencies:                            ║ │
│  ║          - langchain-core >= 0.3.0                                            ║ │
│  ║          - langchain-openai >= 0.2.0                                          ║ │
│  ║          - langchain-community >= 0.3.0                                       ║ │
│  ║          - langgraph >= 0.2.0                                                 ║ │
│  ║          - pydantic >= 2.0                                                    ║ │
│  ║          - pydantic-ai >= 0.1.0                                               ║ │
│  ║          - qdrant-client >= 1.12.0                                            ║ │
│  ║          - redis >= 5.0                                                       ║ │
│  ║          - fastapi >= 0.115.0                                                 ║ │
│  ║          - sentence-transformers >= 3.0                                       ║ │
│  ║      □ Set up environment configuration (pydantic-settings)                   ║ │
│  ║      □ Configure structured logging                                           ║ │
│  ║                                                                                ║ │
│  ║  □ 1.2 Infrastructure Setup                                                   ║ │
│  ║      □ Docker Compose for local development:                                  ║ │
│  ║          - Qdrant (vector store)                                              ║ │
│  ║          - Redis (session/cache)                                              ║ │
│  ║          - PostgreSQL (optional: document metadata)                           ║ │
│  ║      □ Verify connectivity to all services                                    ║ │
│  ║      □ Create health check endpoints                                          ║ │
│  ║                                                                                ║ │
│  ║  □ 1.3 LLM Integration                                                        ║ │
│  ║      □ Create LLM client abstraction layer                                    ║ │
│  ║      □ Implement OpenAI/Azure OpenAI provider                                 ║ │
│  ║      □ Add fallback provider support                                          ║ │
│  ║      □ Implement streaming response handling                                  ║ │
│  ║      □ Add token counting utilities                                           ║ │
│  ║                                                                                ║ │
│  ║  Success Criteria:                                                            ║ │
│  ║  ✓ All services running in Docker                                            ║ │
│  ║  ✓ Health checks passing                                                      ║ │
│  ║  ✓ LLM can generate simple responses                                         ║ │
│  ║                                                                                ║ │
│  ╚═══════════════════════════════════════════════════════════════════════════════╝ │
│                                                                                      │
│  ╔═══════════════════════════════════════════════════════════════════════════════╗ │
│  ║  PHASE 2: RAG PIPELINE (Week 2-3)                                              ║ │
│  ╠═══════════════════════════════════════════════════════════════════════════════╣ │
│  ║                                                                                ║ │
│  ║  □ 2.1 Document Ingestion                                                     ║ │
│  ║      □ Implement document loaders (PDF, DOCX, Markdown, HTML)                 ║ │
│  ║      □ Create cleaning pipeline (remove headers, normalize text)              ║ │
│  ║      □ Implement recursive text chunking:                                     ║ │
│  ║          - Chunk size: 500 tokens                                             ║ │
│  ║          - Overlap: 50 tokens                                                 ║ │
│  ║          - Separators: ["\n\n", "\n", ". ", " "]                             ║ │
│  ║      □ Create metadata schema:                                                ║ │
│  ║          - source, page, section, category, timestamp                         ║ │
│  ║      □ Build ingestion CLI script                                             ║ │
│  ║                                                                                ║ │
│  ║  □ 2.2 Embedding & Storage                                                    ║ │
│  ║      □ Select embedding model:                                                ║ │
│  ║          - sentence-transformers/all-mpnet-base-v2 (768 dim)                  ║ │
│  ║          - OR text-embedding-3-small (1536 dim)                               ║ │
│  ║      □ Configure Qdrant collection with:                                      ║ │
│  ║          - Vector config (size, distance: Cosine)                             ║ │
│  ║          - Payload indexing for metadata fields                               ║ │
│  ║      □ Implement batch embedding with progress tracking                       ║ │
│  ║      □ Add deduplication logic                                                ║ │
│  ║                                                                                ║ │
│  ║  □ 2.3 Basic Retrieval                                                        ║ │
│  ║      □ Implement semantic search                                              ║ │
│  ║      □ Add BM25 sparse search (via Qdrant or separate index)                  ║ │
│  ║      □ Implement RRF fusion                                                   ║ │
│  ║      □ Add metadata filtering                                                 ║ │
│  ║      □ Create retrieval unit tests                                            ║ │
│  ║                                                                                ║ │
│  ║  □ 2.4 Advanced Retrieval                                                     ║ │
│  ║      □ Implement query rewriting (LLM-based)                                  ║ │
│  ║      □ Add query expansion                                                    ║ │
│  ║      □ Implement cross-encoder reranking:                                     ║ │
│  ║          - Model: cross-encoder/ms-marco-MiniLM-L-6-v2                        ║ │
│  ║          - Rerank top 20 → select top 5                                       ║ │
│  ║      □ Implement context compression:                                         ║ │
│  ║          - Extractive (LLMChainExtractor)                                     ║ │
│  ║          - Token limit: 1500 tokens                                           ║ │
│  ║                                                                                ║ │
│  ║  Success Criteria:                                                            ║ │
│  ║  ✓ Documents ingested and searchable                                         ║ │
│  ║  ✓ Hybrid search returning relevant results                                  ║ │
│  ║  ✓ Reranking improving precision                                             ║ │
│  ║  ✓ Context fits within token budget                                          ║ │
│  ║                                                                                ║ │
│  ╚═══════════════════════════════════════════════════════════════════════════════╝ │
│                                                                                      │
│  ╔═══════════════════════════════════════════════════════════════════════════════╗ │
│  ║  PHASE 3: MEMORY SYSTEM (Week 3-4)                                             ║ │
│  ╠═══════════════════════════════════════════════════════════════════════════════╣ │
│  ║                                                                                ║ │
│  ║  □ 3.1 Short-Term Memory (Redis)                                              ║ │
│  ║      □ Design Redis key structure:                                            ║ │
│  ║          - session:{id}:messages → List of messages                          ║ │
│  ║          - session:{id}:summary → Overflow summary                           ║ │
│  ║          - session:{id}:meta → Session metadata                              ║ │
│  ║      □ Implement message buffer (max 10 turns)                                ║ │
│  ║      □ Create overflow summarization:                                         ║ │
│  ║          - When buffer > 10, summarize oldest 5                               ║ │
│  ║          - Store summary, keep recent 5                                       ║ │
│  ║      □ Implement TTL (30 min inactivity)                                      ║ │
│  ║      □ Add session persistence/recovery                                       ║ │
│  ║                                                                                ║ │
│  ║  □ 3.2 Long-Term Memory (Qdrant)                                              ║ │
│  ║      □ Create user_memories collection:                                       ║ │
│  ║          - Conversation summaries (vectorized)                                ║ │
│  ║          - Issue resolutions                                                  ║ │
│  ║          - Preferences                                                        ║ │
│  ║      □ Create user_profiles collection:                                       ║ │
│  ║          - Static user data (non-vectorized)                                  ║ │
│  ║      □ Implement memory retrieval by user_id                                  ║ │
│  ║      □ Add semantic search over past conversations                            ║ │
│  ║      □ Create async background memory update                                  ║ │
│  ║                                                                                ║ │
│  ║  □ 3.3 Working Memory Assembly                                                ║ │
│  ║      □ Create context assembly pipeline:                                      ║ │
│  ║          1. System prompt (~500 tokens)                                       ║ │
│  ║          2. User profile context (~200 tokens)                                ║ │
│  ║          3. Conversation history (~800 tokens)                                ║ │
│  ║          4. Retrieved knowledge (~1500 tokens)                                ║ │
│  ║          5. Current query                                                     ║ │
│  ║      □ Implement token counting and budget allocation                         ║ │
│  ║      □ Add context prioritization logic                                       ║ │
│  ║                                                                                ║ │
│  ║  Success Criteria:                                                            ║ │
│  ║  ✓ Multi-turn conversations maintain context                                 ║ │
│  ║  ✓ Sessions persist across reconnections                                     ║ │
│  ║  ✓ Past user interactions influence responses                                ║ │
│  ║  ✓ Working memory stays within token budget                                  ║ │
│  ║                                                                                ║ │
│  ╚═══════════════════════════════════════════════════════════════════════════════╝ │
│                                                                                      │
│  ╔═══════════════════════════════════════════════════════════════════════════════╗ │
│  ║  PHASE 4: AGENT ORCHESTRATION (Week 4-5)                                       ║ │
│  ╠═══════════════════════════════════════════════════════════════════════════════╣ │
│  ║                                                                                ║ │
│  ║  □ 4.1 LangGraph State Machine                                                ║ │
│  ║      □ Define AgentState TypedDict/Pydantic model                             ║ │
│  ║      □ Implement state graph structure:                                       ║ │
│  ║          - Nodes: intake, transform, retrieve, rerank, reason, respond        ║ │
│  ║          - Conditional edges for branching logic                              ║ │
│  ║      □ Add checkpointing for state persistence                                ║ │
│  ║      □ Implement error handling and recovery                                  ║ │
│  ║                                                                                ║ │
│  ║  □ 4.2 Node Implementations                                                   ║ │
│  ║      □ Intake Node:                                                           ║ │
│  ║          - Load memories                                                      ║ │
│  ║          - Validate input                                                     ║ │
│  ║          - Initialize state                                                   ║ │
│  ║      □ Query Transform Node:                                                  ║ │
│  ║          - Intent classification                                              ║ │
│  ║          - Entity extraction                                                  ║ │
│  ║          - Query rewriting                                                    ║ │
│  ║      □ Retrieve Node:                                                         ║ │
│  ║          - Execute hybrid search                                              ║ │
│  ║          - Retrieve user history                                              ║ │
│  ║      □ Rerank Node:                                                           ║ │
│  ║          - Cross-encoder scoring                                              ║ │
│  ║          - Context compression                                                ║ │
│  ║      □ Reason Node:                                                           ║ │
│  ║          - Confidence evaluation                                              ║ │
│  ║          - Escalation decision                                                ║ │
│  ║          - Response strategy selection                                        ║ │
│  ║      □ Respond Node:                                                          ║ │
│  ║          - LLM generation with Pydantic structured output                     ║ │
│  ║          - Memory updates                                                     ║ │
│  ║                                                                                ║ │
│  ║  □ 4.3 Tool Integration                                                       ║ │
│  ║      □ Implement search tool (exposed RAG pipeline)                           ║ │
│  ║      □ Implement escalation tool                                              ║ │
│  ║      □ 

Deep Analysis: Singapore SMB Customer Enquiry Support AI Agent
Executive Summary
text

╔══════════════════════════════════════════════════════════════════════════════════╗
║                                                                                  ║
║   PROJECT: Customer Enquiry Support AI Agent                                     ║
║   TARGET: Singapore Small-Medium Businesses                                      ║
║   CORE STACK: React + Pydantic AI + LangChain 1.0 + RAG + Memory Systems        ║
║                                                                                  ║
║   ┌─────────────────────────────────────────────────────────────────────────┐   ║
║   │  This analysis excavates requirements across 7 dimensions:              │   ║
║   │                                                                         │   ║
║   │  1. Business Context (Singapore SMB landscape)                          │   ║
║   │  2. User Psychology (Customer expectations & friction points)           │   ║
║   │  3. Technical Architecture (Agent + RAG + Memory integration)           │   ║
║   │  4. Regulatory Compliance (PDPA, data sovereignty)                      │   ║
║   │  5. Scalability Patterns (SMB today, growth tomorrow)                   │   ║
║   │  6. Cost Engineering (LLM economics for budget-conscious SMBs)          │   ║
║   │  7. UX/UI Excellence (Frontend that earns trust)                        │   ║
║   └─────────────────────────────────────────────────────────────────────────┘   ║
║                                                                                  ║
╚══════════════════════════════════════════════════════════════════════════════════╝
I will now present my comprehensive analysis and implementation plan. No code will be written until you validate and approve this plan.

Phase 1: Deep Requirements Analysis
1.1 Understanding Singapore SMB Context
text

┌─────────────────────────────────────────────────────────────────────────────────┐
│                     SINGAPORE SMB LANDSCAPE ANALYSIS                            │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  TYPICAL SECTORS                    COMMON ENQUIRY PATTERNS                     │
│  ─────────────────                  ───────────────────────                     │
│  ├── Retail/E-commerce              ├── Product availability & specs           │
│  ├── F&B Services                   ├── Order status & tracking                │
│  ├── Professional Services          ├── Pricing & quotations                   │
│  ├── Healthcare/Wellness            ├── Appointment booking                    │
│  ├── Education/Tuition              ├── Service hours & locations              │
│  ├── Property/Real Estate           ├── Complaint resolution                   │
│  └── Logistics/Trading              └── Account & billing queries              │
│                                                                                 │
│  LANGUAGE CONSIDERATIONS            OPERATIONAL CONSTRAINTS                     │
│  ─────────────────────              ────────────────────────                    │
│  ├── English (Primary)              ├── Limited IT resources                   │
│  ├── Singlish (Colloquial)          ├── Budget-conscious                       │
│  ├── Mandarin (Secondary)           ├── Need quick deployment                  │
│  ├── Malay (Tertiary)               ├── Minimal maintenance overhead           │
│  └── Tamil (Tertiary)               └── PDPA compliance mandatory              │
│                                                                                 │
│  TIMEZONE: SGT (UTC+8)              PEAK HOURS: 10am-9pm SGT                   │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
1.2 Psychological Analysis: Customer Expectations
Dimension	Customer Expectation	Design Implication
Response Time	Instant acknowledgment, answer within 3-5 seconds	Streaming responses, typing indicators
Accuracy	Correct information or honest "I don't know"	RAG with faithfulness validation, graceful fallback
Continuity	Remember previous conversations	Long-term memory with customer profile linking
Escalation	Seamless handoff to human when needed	Clear escalation triggers, context preservation
Trust	Data handled responsibly	PDPA compliance, transparent data usage
Accessibility	Works on mobile, any browser	Responsive design, progressive enhancement
1.3 Technical Requirements Matrix
text

┌────────────────────────────────────────────────────────────────────────────────┐
│                        TECHNICAL REQUIREMENTS MATRIX                           │
├────────────────────────────────────────────────────────────────────────────────┤
│                                                                                │
│  REQUIREMENT              PRIORITY    COMPLEXITY    FRAMEWORK ALIGNMENT        │
│  ───────────────────────  ────────    ──────────    ─────────────────────      │
│                                                                                │
│  RAG Knowledge Base       Critical    High          LangChain + Vector DB      │
│  Short-term Memory        Critical    Medium        LangGraph State            │
│  Long-term Memory         Critical    High          PostgreSQL + Vector DB     │
│  Agent Reasoning          Critical    High          Pydantic AI                │
│  Streaming Responses      High        Medium        FastAPI + SSE              │
│  Multi-turn Context       Critical    High          Conversation Buffer        │
│  Human Escalation         High        Low           State Machine              │
│  Analytics/Logging        Medium      Medium        Structured Logging         │
│  Multilingual Support     Medium      High          Embedding Model Choice     │
│  Cost Optimization        High        Medium        Caching + Model Routing    │
│                                                                                │
└────────────────────────────────────────────────────────────────────────────────┘
Phase 2: Architecture Design
2.1 High-Level System Architecture
text

┌──────────────────────────────────────────────────────────────────────────────────────┐
│                                                                                      │
│                        CUSTOMER ENQUIRY SUPPORT AI AGENT                             │
│                              SYSTEM ARCHITECTURE                                     │
│                                                                                      │
│  ┌─────────────────────────────────────────────────────────────────────────────┐    │
│  │                           PRESENTATION LAYER                                 │    │
│  │  ┌─────────────────────────────────────────────────────────────────────┐    │    │
│  │  │                     React Chatbox Interface                          │    │    │
│  │  │   ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────────┐   │    │    │
│  │  │   │ Message  │  │ Input    │  │ Typing   │  │ Escalation       │   │    │    │
│  │  │   │ History  │  │ Composer │  │ Indicator│  │ Request Panel    │   │    │    │
│  │  │   └──────────┘  └──────────┘  └──────────┘  └──────────────────┘   │    │    │
│  │  │   Shadcn UI Components + Tailwind CSS 4.0 + Framer Motion          │    │    │
│  │  └─────────────────────────────────────────────────────────────────────┘    │    │
│  └─────────────────────────────────────────────────────────────────────────────┘    │
│                                        │                                             │
│                                        │ WebSocket / SSE                             │
│                                        ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────┐    │
│  │                              API LAYER                                       │    │
│  │  ┌─────────────────────────────────────────────────────────────────────┐    │    │
│  │  │                     FastAPI Application                              │    │    │
│  │  │   ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐   │    │    │
│  │  │   │ Chat       │  │ Session    │  │ Health     │  │ Admin      │   │    │    │
│  │  │   │ Endpoints  │  │ Management │  │ Checks     │  │ Endpoints  │   │    │    │
│  │  │   └────────────┘  └────────────┘  └────────────┘  └────────────┘   │    │    │
│  │  └─────────────────────────────────────────────────────────────────────┘    │    │
│  └─────────────────────────────────────────────────────────────────────────────┘    │
│                                        │                                             │
│                                        ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────┐    │
│  │                           AGENT ORCHESTRATION LAYER                          │    │
│  │                                                                              │    │
│  │  ┌─────────────────────────────┐    ┌─────────────────────────────────┐     │    │
│  │  │      PYDANTIC AI AGENT      │    │       LANGCHAIN RAG SYSTEM      │     │    │
│  │  │  ┌───────────────────────┐  │    │  ┌─────────────────────────┐   │     │    │
│  │  │  │   Agent Definition    │  │    │  │   Query Transformer     │   │     │    │
│  │  │  │   - System Prompt     │  │    │  │   - Rewriting           │   │     │    │
│  │  │  │   - Tool Bindings     │  │    │  │   - Decomposition       │   │     │    │
│  │  │  │   - Output Schemas    │  │    │  └─────────────────────────┘   │     │    │
│  │  │  └───────────────────────┘  │    │  ┌─────────────────────────┐   │     │    │
│  │  │  ┌───────────────────────┐  │◄───┼──│   Hybrid Retriever      │   │     │    │
│  │  │  │   Tool Definitions    │  │    │  │   - Semantic Search     │   │     │    │
│  │  │  │   - rag_search        │  │    │  │   - BM25 Keyword        │   │     │    │
│  │  │  │   - order_lookup      │  │────┼──►   - RRF Fusion          │   │     │    │
│  │  │  │   - escalate_human    │  │    │  └─────────────────────────┘   │     │    │
│  │  │  │   - book_appointment  │  │    │  ┌─────────────────────────┐   │     │    │
│  │  │  └───────────────────────┘  │    │  │   Cross-Encoder         │   │     │    │
│  │  │  ┌───────────────────────┐  │    │  │   Reranker              │   │     │    │
│  │  │  │   Dependency Inject.  │  │    │  └─────────────────────────┘   │     │    │
│  │  │  │   - LLM Client        │  │    │  ┌─────────────────────────┐   │     │    │
│  │  │  │   - RAG Retriever     │  │    │  │   Context Compressor    │   │     │    │
│  │  │  │   - Memory Store      │  │    │  └─────────────────────────┘   │     │    │
│  │  │  └───────────────────────┘  │    └─────────────────────────────────┘     │    │
│  │  └─────────────────────────────┘                                            │    │
│  └─────────────────────────────────────────────────────────────────────────────┘    │
│                                        │                                             │
│                                        ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────┐    │
│  │                            MEMORY LAYER                                      │    │
│  │                                                                              │    │
│  │  ┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐  │    │
│  │  │   WORKING MEMORY    │  │   SHORT-TERM MEMORY │  │   LONG-TERM MEMORY  │  │    │
│  │  │                     │  │                     │  │                     │  │    │
│  │  │  Current context    │  │  Conversation       │  │  ┌───────────────┐  │  │    │
│  │  │  window for LLM     │  │  history buffer     │  │  │ Knowledge Base│  │  │    │
│  │  │  - Retrieved docs   │  │  (rolling window)   │  │  │ (Qdrant)      │  │  │    │
│  │  │  - Recent messages  │  │  - Last N turns     │  │  └───────────────┘  │  │    │
│  │  │  - Active entities  │  │  - Summarized if    │  │  ┌───────────────┐  │  │    │
│  │  │                     │  │    exceeds limit    │  │  │ Customer      │  │  │    │
│  │  │  Token Budget:      │  │                     │  │  │ Profiles      │  │  │    │
│  │  │  ~4000 tokens       │  │  Managed by:        │  │  │ (PostgreSQL)  │  │  │    │
│  │  │                     │  │  LangGraph State    │  │  └───────────────┘  │  │    │
│  │  │                     │  │                     │  │  ┌───────────────┐  │  │    │
│  │  │                     │  │                     │  │  │ Conversation  │  │  │    │
│  │  │                     │  │                     │  │  │ History Store │  │  │    │
│  │  │                     │  │                     │  │  │ (PostgreSQL)  │  │  │    │
│  │  │                     │  │                     │  │  └───────────────┘  │  │    │
│  │  └─────────────────────┘  └─────────────────────┘  └─────────────────────┘  │    │
│  └─────────────────────────────────────────────────────────────────────────────┘    │
│                                        │                                             │
│                                        ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────┐    │
│  │                          DATA PERSISTENCE LAYER                              │    │
│  │                                                                              │    │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────────────────┐  │    │
│  │  │     QDRANT      │  │   POSTGRESQL    │  │          REDIS              │  │    │
│  │  │  Vector Store   │  │   Relational    │  │      Cache & Sessions       │  │    │
│  │  │                 │  │                 │  │                             │  │    │
│  │  │  - Documents    │  │  - Customers    │  │  - Session state            │  │    │
│  │  │  - Embeddings   │  │  - Conversations│  │  - Response cache           │  │    │
│  │  │  - Metadata     │  │  - Feedback     │  │  - Rate limiting            │  │    │
│  │  │  - BM25 Index   │  │  - Analytics    │  │                             │  │    │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────────────────┘  │    │
│  └─────────────────────────────────────────────────────────────────────────────┘    │
│                                                                                      │
└──────────────────────────────────────────────────────────────────────────────────────┘
2.2 Agent Reasoning Flow (Pydantic AI + LangChain Integration)
text

┌──────────────────────────────────────────────────────────────────────────────────────┐
│                                                                                      │
│                         AGENT REASONING FLOW (ReAct Pattern)                         │
│                                                                                      │
│  ┌────────────────────────────────────────────────────────────────────────────────┐ │
│  │                                                                                │ │
│  │   Customer        ┌──────────────────────────────────────────────────────┐    │ │
│  │   Message    ───► │              PYDANTIC AI AGENT CORE                  │    │ │
│  │                   │                                                      │    │ │
│  │                   │  1. OBSERVE                                          │    │ │
│  │                   │     ├── Parse incoming message                       │    │ │
│  │                   │     ├── Load short-term memory (conversation)        │    │ │
│  │                   │     └── Identify customer context from long-term     │    │ │
│  │                   │                                                      │    │ │
│  │                   │  2. THINK (Internal Reasoning)                       │    │ │
│  │                   │     ├── Classify intent                              │    │ │
│  │                   │     ├── Extract entities                             │    │ │
│  │                   │     ├── Determine required actions                   │    │ │
│  │                   │     └── Plan tool usage                              │    │ │
│  │                   │                         │                            │    │ │
│  │                   │                         ▼                            │    │ │
│  │                   │  3. ACT (Tool Execution Loop)                        │    │ │
│  │                   │     ┌─────────────────────────────────────────┐      │    │ │
│  │                   │     │                                         │      │    │ │
│  │                   │     │  ┌─────────────┐    ┌─────────────┐    │      │    │ │
│  │                   │     │  │ rag_search  │    │order_lookup │    │      │    │ │
│  │                   │     │  │             │    │             │    │      │    │ │
│  │                   │     │  │ LangChain   │    │ Direct DB   │    │      │    │ │
│  │                   │     │  │ Retriever   │    │ Query       │    │      │    │ │
│  │                   │     │  └─────────────┘    └─────────────┘    │      │    │ │
│  │                   │     │                                         │      │    │ │
│  │                   │     │  ┌─────────────┐    ┌─────────────┐    │      │    │ │
│  │                   │     │  │book_appt    │    │escalate_    │    │      │    │ │
│  │                   │     │  │             │    │human        │    │      │    │ │
│  │                   │     │  │ Calendar    │    │ State       │    │      │    │ │
│  │                   │     │  │ Integration │    │ Transition  │    │      │    │ │
│  │                   │     │  └─────────────┘    └─────────────┘    │      │    │ │
│  │                   │     │                                         │      │    │ │
│  │                   │     └─────────────────────────────────────────┘      │    │ │
│  │                   │                         │                            │    │ │
│  │                   │                         ▼                            │    │ │
│  │                   │  4. SYNTHESIZE                                       │    │ │
│  │                   │     ├── Combine tool results                         │    │ │
│  │                   │     ├── Generate contextual response                 │    │ │
│  │                   │     ├── Validate faithfulness (hallucination check)  │    │ │
│  │                   │     └── Format for delivery                          │    │ │
│  │                   │                                                      │    │ │
│  │                   │  5. UPDATE MEMORY                                    │    │ │
│  │                   │     ├── Append to short-term (conversation)          │    │ │
│  │                   │     ├── Update customer profile if new info          │    │ │
│  │                   │     └── Log for analytics                            │    │ │
│  │                   │                                                      │    │ │
│  │                   └──────────────────────────────────────────────────────┘    │ │
│  │                                            │                                   │ │
│  │                                            ▼                                   │ │
│  │                                   Response (Streamed)                          │ │
│  │                                                                                │ │
│  └────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                      │
└──────────────────────────────────────────────────────────────────────────────────────┘
2.3 Memory Architecture Deep Dive
text

┌──────────────────────────────────────────────────────────────────────────────────────┐
│                                                                                      │
│                         HIERARCHICAL MEMORY ARCHITECTURE                             │
│                                                                                      │
│  ┌────────────────────────────────────────────────────────────────────────────────┐ │
│  │                                                                                │ │
│  │                          LONG-TERM MEMORY (Persistent)                         │ │
│  │                                                                                │ │
│  │   ┌─────────────────────────────────────────────────────────────────────────┐ │ │
│  │   │                     KNOWLEDGE BASE (Qdrant)                             │ │ │
│  │   │                                                                         │ │ │
│  │   │   Collection: business_knowledge                                        │ │ │
│  │   │   ├── Products/Services catalog                                         │ │ │
│  │   │   ├── Pricing information                                               │ │ │
│  │   │   ├── Company policies (refunds, warranties)                            │ │ │
│  │   │   ├── FAQ content                                                       │ │ │
│  │   │   ├── Process documentation                                             │ │ │
│  │   │   └── Location/contact information                                      │ │ │
│  │   │                                                                         │ │ │
│  │   │   Indexing Strategy:                                                    │ │ │
│  │   │   ├── Dense: text-embedding-3-small (1536d)                             │ │ │
│  │   │   ├── Sparse: BM25 via Qdrant's built-in                                │ │ │
│  │   │   └── Metadata: source, category, date_updated, language                │ │ │
│  │   │                                                                         │ │ │
│  │   └─────────────────────────────────────────────────────────────────────────┘ │ │
│  │                                                                                │ │
│  │   ┌─────────────────────────────────────────────────────────────────────────┐ │ │
│  │   │                   CUSTOMER PROFILES (PostgreSQL)                        │ │ │
│  │   │                                                                         │ │ │
│  │   │   Table: customers                                                      │ │ │
│  │   │   ├── id (UUID)                                                         │ │ │
│  │   │   ├── identifier (email/phone - hashed for PDPA)                        │ │ │
│  │   │   ├── preferences (JSONB)                                               │ │ │
│  │   │   ├── summary (LLM-generated profile summary)                           │ │ │
│  │   │   ├── last_interaction (timestamp)                                      │ │ │
│  │   │   └── total_conversations (int)                                         │ │ │
│  │   │                                                                         │ │ │
│  │   └─────────────────────────────────────────────────────────────────────────┘ │ │
│  │                                                                                │ │
│  │   ┌─────────────────────────────────────────────────────────────────────────┐ │ │
│  │   │                CONVERSATION HISTORY (PostgreSQL)                        │ │ │
│  │   │                                                                         │ │ │
│  │   │   Table: conversations                                                  │ │ │
│  │   │   ├── id (UUID)                                                         │ │ │
│  │   │   ├── customer_id (FK)                                                  │ │ │
│  │   │   ├── session_id (UUID)                                                 │ │ │
│  │   │   ├── started_at, ended_at (timestamps)                                 │ │ │
│  │   │   ├── summary (LLM-generated when session ends)                         │ │ │
│  │   │   └── escalated (boolean)                                               │ │ │
│  │   │                                                                         │ │ │
│  │   │   Table: messages                                                       │ │ │
│  │   │   ├── id (UUID)                                                         │ │ │
│  │   │   ├── conversation_id (FK)                                              │ │ │
│  │   │   ├── role (user/assistant/system/tool)                                 │ │ │
│  │   │   ├── content (text)                                                    │ │ │
│  │   │   ├── metadata (JSONB - tool calls, retrieved docs)                     │ │ │
│  │   │   └── created_at (timestamp)                                            │ │ │
│  │   │                                                                         │ │ │
│  │   └─────────────────────────────────────────────────────────────────────────┘ │ │
│  │                                                                                │ │
│  └────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                      │
│  ┌────────────────────────────────────────────────────────────────────────────────┐ │
│  │                                                                                │ │
│  │                          SHORT-TERM MEMORY (Session)                           │ │
│  │                                                                                │ │
│  │   Managed by: LangGraph Checkpointer + Redis                                   │ │
│  │                                                                                │ │
│  │   ┌─────────────────────────────────────────────────────────────────────────┐ │ │
│  │   │                    CONVERSATION BUFFER                                  │ │ │
│  │   │                                                                         │ │ │
│  │   │   Strategy: Sliding Window with Summarization                           │ │ │
│  │   │                                                                         │ │ │
│  │   │   ┌───────────────────────────────────────────────────────────────┐    │ │ │
│  │   │   │                                                               │    │ │ │
│  │   │   │   IF messages.count <= 10:                                    │    │ │ │
│  │   │   │       Include all messages verbatim                           │    │ │ │
│  │   │   │                                                               │    │ │ │
│  │   │   │   ELSE:                                                       │    │ │ │
│  │   │   │       ┌─────────────────────────────────────────────────┐    │    │ │ │
│  │   │   │       │ SUMMARY of older messages (LLM-generated)       │    │    │ │ │
│  │   │   │       │ "Customer asked about product X, was quoted     │    │    │ │ │
│  │   │   │       │  $50, expressed concern about delivery time..." │    │    │ │ │
│  │   │   │       └─────────────────────────────────────────────────┘    │    │ │ │
│  │   │   │       +                                                       │    │ │ │
│  │   │   │       ┌─────────────────────────────────────────────────┐    │    │ │ │
│  │   │   │       │ RECENT 6 messages (verbatim)                    │    │    │ │ │
│  │   │   │       └─────────────────────────────────────────────────┘    │    │ │ │
│  │   │   │                                                               │    │ │ │
│  │   │   └───────────────────────────────────────────────────────────────┘    │ │ │
│  │   │                                                                         │ │ │
│  │   └─────────────────────────────────────────────────────────────────────────┘ │ │
│  │                                                                                │ │
│  │   ┌─────────────────────────────────────────────────────────────────────────┐ │ │
│  │   │                      ACTIVE ENTITIES                                    │ │ │
│  │   │                                                                         │ │ │
│  │   │   Tracked within session:                                               │ │ │
│  │   │   ├── current_product: "Widget Pro X"                                   │ │ │
│  │   │   ├── current_order_id: "ORD-12345"                                     │ │ │
│  │   │   ├── pending_action: "awaiting_confirmation"                           │ │ │
│  │   │   └── sentiment: "frustrated" (for escalation logic)                    │ │ │
│  │   │                                                                         │ │ │
│  │   └─────────────────────────────────────────────────────────────────────────┘ │ │
│  │                                                                                │ │
│  └────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                      │
│  ┌────────────────────────────────────────────────────────────────────────────────┐ │
│  │                                                                                │ │
│  │                          WORKING MEMORY (Per-Request)                          │ │
│  │                                                                                │ │
│  │   Assembled fresh for each LLM call:                                           │ │
│  │                                                                                │ │
│  │   ┌─────────────────────────────────────────────────────────────────────────┐ │ │
│  │   │                    CONTEXT WINDOW BUDGET (~4000 tokens)                 │ │ │
│  │   │                                                                         │ │ │
│  │   │   ┌─────────────────────────────────────────────────────────────────┐  │ │ │
│  │   │   │ SYSTEM PROMPT (~400 tokens)                                     │  │ │ │
│  │   │   │ Agent identity, capabilities, guidelines, tone                  │  │ │ │
│  │   │   └─────────────────────────────────────────────────────────────────┘  │ │ │
│  │   │   ┌─────────────────────────────────────────────────────────────────┐  │ │ │
│  │   │   │ CUSTOMER PROFILE SUMMARY (~200 tokens)                          │  │ │ │
│  │   │   │ "Returning customer, prefers quick responses, past orders..."   │  │ │ │
│  │   │   └─────────────────────────────────────────────────────────────────┘  │ │ │
│  │   │   ┌─────────────────────────────────────────────────────────────────┐  │ │ │
│  │   │   │ RETRIEVED CONTEXT (~1500 tokens)                                │  │ │ │
│  │   │   │ RAG results, compressed and reranked                            │  │ │ │
│  │   │   └─────────────────────────────────────────────────────────────────┘  │ │ │
│  │   │   ┌─────────────────────────────────────────────────────────────────┐  │ │ │
│  │   │   │ CONVERSATION CONTEXT (~1400 tokens)                             │  │ │ │
│  │   │   │ Summary of older + recent messages verbatim                     │  │ │ │
│  │   │   └─────────────────────────────────────────────────────────────────┘  │ │ │
│  │   │   ┌─────────────────────────────────────────────────────────────────┐  │ │ │
│  │   │   │ CURRENT USER MESSAGE (~100 tokens)                              │  │ │ │
│  │   │   └─────────────────────────────────────────────────────────────────┘  │ │ │
│  │   │   ┌─────────────────────────────────────────────────────────────────┐  │ │ │
│  │   │   │ BUFFER FOR RESPONSE (~400 tokens reserved)                      │  │ │ │
│  │   │   └─────────────────────────────────────────────────────────────────┘  │ │ │
│  │   │                                                                         │ │ │
│  │   └─────────────────────────────────────────────────────────────────────────┘ │ │
│  │                                                                                │ │
│  └────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                      │
└──────────────────────────────────────────────────────────────────────────────────────┘
2.4 RAG Pipeline Deep Architecture
text

┌──────────────────────────────────────────────────────────────────────────────────────┐
│                                                                                      │
│                              RAG PIPELINE ARCHITECTURE                               │
│                         (Multi-Stage Retrieval System)                               │
│                                                                                      │
│  ┌────────────────────────────────────────────────────────────────────────────────┐ │
│  │                                                                                │ │
│  │                      STAGE 1: OFFLINE INDEXING                                 │ │
│  │                                                                                │ │
│  │   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    │ │
│  │   │   SOURCE    │    │   LOADER    │    │   CLEANER   │    │   CHUNKER   │    │ │
│  │   │   FILES     │───►│ Unstructured│───►│  Custom     │───►│  Semantic   │    │ │
│  │   │             │    │    .io      │    │  Pipeline   │    │  + Overlap  │    │ │
│  │   │ PDF, DOCX,  │    │             │    │             │    │             │    │ │
│  │   │ HTML, MD    │    │ Extract     │    │ Remove      │    │ Chunk Size: │    │ │
│  │   │             │    │ text +      │    │ noise,      │    │ 512 tokens  │    │ │
│  │   │             │    │ metadata    │    │ normalize   │    │ Overlap: 50 │    │ │
│  │   └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘    │ │
│  │                                                                 │              │ │
│  │                                                                 ▼              │ │
│  │   ┌─────────────────────────────────────────────────────────────────────────┐ │ │
│  │   │                         EMBEDDING & STORAGE                             │ │ │
│  │   │                                                                         │ │ │
│  │   │   ┌─────────────────────┐         ┌─────────────────────────────────┐  │ │ │
│  │   │   │   Dense Embedding   │         │            QDRANT               │  │ │ │
│  │   │   │   text-embedding-   │────────►│                                 │  │ │ │
│  │   │   │   3-small (OpenAI)  │         │  Collection: business_knowledge │  │ │ │
│  │   │   │   1536 dimensions   │         │                                 │  │ │ │
│  │   │   └─────────────────────┘         │  Stored per chunk:              │  │ │ │
│  │   │                                   │  ├── id (UUID)                  │  │ │ │
│  │   │   ┌─────────────────────┐         │  ├── dense_vector (1536d)       │  │ │ │
│  │   │   │   Sparse Embedding  │────────►│  ├── sparse_vector (BM25)       │  │ │ │
│  │   │   │   BM25 (Qdrant      │         │  ├── text (original chunk)      │  │ │ │
│  │   │   │   built-in)         │         │  └── metadata:                  │  │ │ │
│  │   │   └─────────────────────┘         │      ├── source                 │  │ │ │
│  │   │                                   │      ├── category               │  │ │ │
│  │   │   ┌─────────────────────┐         │      ├── language               │  │ │ │
│  │   │   │   Metadata          │────────►│      ├── date_updated           │  │ │ │
│  │   │   │   Enrichment        │         │      └── parent_doc_id          │  │ │ │
│  │   │   │   (LLM-generated)   │         │                                 │  │ │ │
│  │   │   └─────────────────────┘         └─────────────────────────────────┘  │ │ │
│  │   │                                                                         │ │ │
│  │   └─────────────────────────────────────────────────────────────────────────┘ │ │
│  │                                                                                │ │
│  └────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                      │
│  ┌────────────────────────────────────────────────────────────────────────────────┐ │
│  │                                                                                │ │
│  │                     STAGE 2: ONLINE RETRIEVAL                                  │ │
│  │                                                                                │ │
│  │   ┌─────────────────────────────────────────────────────────────────────────┐ │ │
│  │   │                   STEP 1: QUERY TRANSFORMATION                          │ │ │
│  │   │                                                                         │ │ │
│  │   │   User Query: "can I return this if don't like?"                        │ │ │
│  │   │                        │                                                │ │ │
│  │   │                        ▼                                                │ │ │
│  │   │   ┌─────────────────────────────────────────────────────────────────┐  │ │ │
│  │   │   │   LLM Query Rewriter                                            │  │ │ │
│  │   │   │                                                                 │  │ │ │
│  │   │   │   Input: Raw query + conversation context                       │  │ │ │
│  │   │   │   Output: Optimized search queries                              │  │ │ │
│  │   │   │                                                                 │  │ │ │
│  │   │   │   Generated Queries:                                            │  │ │ │
│  │   │   │   1. "return policy dissatisfied product"                       │  │ │ │
│  │   │   │   2. "refund conditions customer not satisfied"                 │  │ │ │
│  │   │   │   3. "exchange policy product return requirements"              │  │ │ │
│  │   │   │                                                                 │  │ │ │
│  │   │   └─────────────────────────────────────────────────────────────────┘  │ │ │
│  │   │                                                                         │ │ │
│  │   └─────────────────────────────────────────────────────────────────────────┘ │ │
│  │                                          │                                     │ │
│  │                                          ▼                                     │ │
│  │   ┌─────────────────────────────────────────────────────────────────────────┐ │ │
│  │   │                   STEP 2: HYBRID RETRIEVAL                              │ │ │
│  │   │                                                                         │ │ │
│  │   │   For each transformed query:                                           │ │ │
│  │   │                                                                         │ │ │
│  │   │   ┌─────────────────────┐    ┌─────────────────────┐                   │ │ │
│  │   │   │   DENSE SEARCH      │    │   SPARSE SEARCH     │                   │ │ │
│  │   │   │   (Semantic)        │    │   (BM25 Keyword)    │                   │ │ │
│  │   │   │                     │    │                     │                   │ │ │
│  │   │   │   Embed query with  │    │   Match exact       │                   │ │ │
│  │   │   │   same model        │    │   keywords          │                   │ │ │
│  │   │   │   Cosine similarity │    │   TF-IDF scoring    │                   │ │ │
│  │   │   │                     │    │                     │                   │ │ │
│  │   │   │   Top 30 results    │    │   Top 30 results    │                   │ │ │
│  │   │   └─────────────────────┘    └─────────────────────┘                   │ │ │
│  │   │              │                         │                                │ │ │
│  │   │              └────────────┬────────────┘                                │ │ │
│  │   │                           ▼                                             │ │ │
│  │   │              ┌─────────────────────────────────────┐                   │ │ │
│  │   │              │   RECIPROCAL RANK FUSION (RRF)      │                   │ │ │
│  │   │              │                                     │                   │ │ │
│  │   │              │   RRF_score(d) = Σ 1/(k + rank(d))  │                   │ │ │
│  │   │              │   where k = 60 (constant)           │                   │ │ │
│  │   │              │                                     │                   │ │ │
│  │   │              │   Merged result: Top 20 candidates  │                   │ │ │
│  │   │              └─────────────────────────────────────┘                   │ │ │
│  │   │                                                                         │ │ │
│  │   └─────────────────────────────────────────────────────────────────────────┘ │ │
│  │                                          │                                     │ │
│  │                                          ▼                                     │ │
│  │   ┌─────────────────────────────────────────────────────────────────────────┐ │ │
│  │   │                   STEP 3: RERANKING                                     │ │ │
│  │   │                                                                         │ │ │
│  │   │   ┌─────────────────────────────────────────────────────────────────┐  │ │ │
│  │   │   │   CROSS-ENCODER RERANKER                                        │  │ │ │
│  │   │   │   Model: ms-marco-MiniLM-L-12-v2 (or Cohere Rerank)             │  │ │ │
│  │   │   │                                                                 │  │ │ │
│  │   │   │   Input: (query, document) pairs                                │  │ │ │
│  │   │   │   Output: Relevance score [0, 1]                                │  │ │ │
│  │   │   │                                                                 │  │ │ │
│  │   │   │   Process: Token-level attention between query and doc          │  │ │ │
│  │   │   │   Result: Top 5 most relevant chunks                            │  │ │ │
│  │   │   │                                                                 │  │ │ │
│  │   │   └─────────────────────────────────────────────────────────────────┘  │ │ │
│  │   │                                                                         │ │ │
│  │   └─────────────────────────────────────────────────────────────────────────┘ │ │
│  │                                          │                                     │ │
│  │                                          ▼                                     │ │
│  │   ┌─────────────────────────────────────────────────────────────────────────┐ │ │
│  │   │                   STEP 4: CONTEXT COMPRESSION                           │ │ │
│  │   │                                                                         │ │ │
│  │   │   ┌─────────────────────────────────────────────────────────────────┐  │ │ │
│  │   │   │   EXTRACTIVE COMPRESSOR                                         │  │ │ │
│  │   │   │                                                                 │  │ │ │
│  │   │   │   For each reranked chunk:                                      │  │ │ │
│  │   │   │   1. Identify sentences most relevant to query                  │  │ │ │
│  │   │   │   2. Remove redundant/overlapping information                   │  │ │ │
│  │   │   │   3. Preserve source attribution                                │  │ │ │
│  │   │   │                                                                 │  │ │ │
│  │   │   │   Token budget: 1500 tokens for retrieved context               │  │ │ │
│  │   │   │                                                                 │  │ │ │
│  │   │   └─────────────────────────────────────────────────────────────────┘  │ │ │
│  │   │                                                                         │ │ │
│  │   └─────────────────────────────────────────────────────────────────────────┘ │ │
│  │                                          │                                     │ │
│  │                                          ▼                                     │ │
│  │                              FINAL RETRIEVED CONTEXT                           │ │
│  │                        (Ready for injection into prompt)                       │ │
│  │                                                                                │ │
│  └────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                      │
└──────────────────────────────────────────────────────────────────────────────────────┘
2.5 Technology Stack Decision Matrix
text

┌──────────────────────────────────────────────────────────────────────────────────────┐
│                                                                                      │
│                          TECHNOLOGY STACK DECISIONS                                  │
│                                                                                      │
├──────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                      │
│  CATEGORY          CHOSEN             ALTERNATIVES        RATIONALE                  │
│  ─────────────     ───────────────    ───────────────     ─────────────────────────  │
│                                                                                      │
│  AGENT             Pydantic AI        LangChain Agents    - Type-safe agent defs     │
│  FRAMEWORK         v0.0.x             CrewAI              - Dependency injection     │
│                                                           - Structured outputs       │
│                                                           - Modern Python patterns   │
│                                                                                      │
│  RAG               LangChain 1.0      LlamaIndex          - Mature ecosystem         │
│  ORCHESTRATION     + LangGraph        Haystack            - Excellent integrations   │
│                                                           - LCEL for composability   │
│                                                           - LangGraph for state      │
│                                                                                      │
│  VECTOR            Qdrant             Weaviate            - Hybrid search native     │
│  DATABASE          (Cloud or          Milvus              - Excellent metadata       │
│                    Self-hosted)       Chroma              - Production-ready         │
│                                                           - Cost-effective for SMB   │
│                                                           - Fast (Rust-based)        │
│                                                                                      │
│  EMBEDDING         OpenAI             Cohere              - Excellent quality        │
│  MODEL             text-embedding-    voyage-lite-02      - Cost-effective           │
│                    3-small            BGE-M3              - Good multilingual        │
│                                                           - 1536 dimensions          │
│                                                                                      │
│  LLM               GPT-4o-mini        GPT-4o              - Best cost/quality ratio  │
│  (Primary)         (OpenAI)           Claude 3.5 Sonnet   - Fast responses           │
│                                       Llama 3.1           - Excellent instruction    │
│                                                             following               │
│                                                                                      │
│  LLM               GPT-4o             Claude 3.5 Opus     - Complex reasoning        │
│  (Escalated)       (OpenAI)                               - Multi-step tasks         │
│                                                                                      │
│  RERANKER          Cohere Rerank      Cross-encoder       - Production quality       │
│                    v3                 (local)             - API simplicity           │
│                                       Jina Reranker       - Good accuracy            │
│                                                                                      │
│  RELATIONAL        PostgreSQL 16      MySQL               - JSONB support            │
│  DATABASE                             SQLite              - Full-text search         │
│                                                           - Scalable                 │
│                                                           - Industry standard        │
│                                                                                      │
│  CACHE/            Redis 7            Memcached           - Session management       │
│  SESSION                              DragonflyDB         - Pub/sub for real-time    │
│                                                           - Rate limiting            │
│                                                                                      │
│  API               FastAPI            Flask               - Async native             │
│  FRAMEWORK         (Python 3.12)      Django              - OpenAPI auto-gen         │
│                                       Litestar            - Pydantic integration     │
│                                                           - WebSocket support        │
│                                                                                      │
│  FRONTEND          React 18+          Vue 3               - Ecosystem maturity       │
│  FRAMEWORK         + TypeScript       Svelte              - Component libraries      │
│                                       Next.js             - Team familiarity         │
│                                                                                      │
│  UI                Shadcn UI          Radix               - Accessible primitives    │
│  COMPONENTS        + Tailwind 4       Headless UI         - Customizable styling     │
│                    + Framer Motion    Chakra UI           - Modern aesthetic         │
│                                                                                      │
│  DOCUMENT          Unstructured.io    LlamaParse          - Wide format support      │
│  PARSING           (Open Source)      Docling             - Production-ready         │
│                                       PyMuPDF             - Good metadata extraction │
│                                                                                      │
│  EVALUATION        RAGAs +            TruLens             - RAG-specific metrics     │
│  FRAMEWORK         DeepEval           Evidently AI        - LLM-as-judge             │
│                                                           - CI/CD integration        │
│                                                                                      │
│  DEPLOYMENT        Docker +           Kubernetes          - SMB-appropriate          │
│                    Docker Compose     AWS ECS             - Easy local dev           │
│                    (Dev/Small Prod)   Railway             - Scalable path forward    │
│                                                                                      │
└──────────────────────────────────────────────────────────────────────────────────────┘
Phase 3: Implementation Plan
3.1 Project Structure
text

singapore-smb-support-agent/
│
├── 📁 backend/
│   ├── 📁 app/
│   │   ├── 📄 __init__.py
│   │   ├── 📄 main.py                    # FastAPI application entry
│   │   ├── 📄 config.py                  # Configuration management
│   │   │
│   │   ├── 📁 agent/
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 core.py                # Pydantic AI Agent definition
│   │   │   ├── 📄 tools.py               # Agent tools (RAG, order lookup, etc.)
│   │   │   ├── 📄 prompts.py             # System prompts and templates
│   │   │   └── 📄 schemas.py             # Pydantic models for agent I/O
│   │   │
│   │   ├── 📁 rag/
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 indexer.py             # Document ingestion pipeline
│   │   │   ├── 📄 retriever.py           # Hybrid retrieval logic
│   │   │   ├── 📄 reranker.py            # Cross-encoder reranking
│   │   │   ├── 📄 compressor.py          # Context compression
│   │   │   └── 📄 query_transformer.py   # Query rewriting/expansion
│   │   │
│   │   ├── 📁 memory/
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 short_term.py          # Conversation buffer management
│   │   │   ├── 📄 long_term.py           # Customer profile & history
│   │   │   ├── 📄 working.py             # Context window assembly
│   │   │   └── 📄 summarizer.py          # Conversation summarization
│   │   │
│   │   ├── 📁 api/
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 routes/
│   │   │   │   ├── 📄 chat.py            # Chat endpoints (WebSocket + REST)
│   │   │   │   ├── 📄 admin.py           # Knowledge base management
│   │   │   │   ├── 📄 health.py          # Health checks
│   │   │   │   └── 📄 analytics.py       # Usage analytics
│   │   │   ├── 📄 middleware.py          # Auth, rate limiting, logging
│   │   │   └── 📄 dependencies.py        # FastAPI dependencies
│   │   │
│   │   ├── 📁 db/
│   │   │   ├── 📄 __init__.py
│   │   │   ├── 📄 postgres.py            # PostgreSQL connection & models
│   │   │   ├── 📄 qdrant.py              # Qdrant client wrapper
│   │   │   ├── 📄 redis.py               # Redis connection
│   │   │   └── 📄 models/
│   │   │       ├── 📄 customer.py        # Customer SQLAlchemy model
│   │   │       ├── 📄 conversation.py    # Conversation models
│   │   │       └── 📄 message.py         # Message models
│   │   │
│   │   └── 📁 utils/
│   │       ├── 📄 __init__.py
│   │       ├── 📄 logging.py             # Structured logging
│   │       ├── 📄 tokens.py              # Token counting utilities
│   │       └── 📄 pdpa.py                # PDPA compliance helpers
│   │
│   ├── 📁 scripts/
│   │   ├── 📄 ingest_documents.py        # Bulk document ingestion
│   │   ├── 📄 evaluate_rag.py            # RAG evaluation with RAGAs
│   │   └── 📄 migrate_db.py              # Database migrations
│   │
│   ├── 📁 tests/
│   │   ├── 📄 test_agent.py
│   │   ├── 📄 test_rag.py
│   │   ├── 📄 test_memory.py
│   │   └── 📄 test_api.py
│   │
│   ├── 📄 requirements.txt
│   ├── 📄 pyproject.toml
│   └── 📄 Dockerfile
│
├── 📁 frontend/
│   ├── 📁 src/
│   │   ├── 📁 components/
│   │   │   ├── 📁 chat/
│   │   │   │   ├── 📄 ChatContainer.tsx      # Main chat wrapper
│   │   │   │   ├── 📄 MessageList.tsx        # Message display
│   │   │   │   ├── 📄 MessageBubble.tsx      # Individual message
│   │   │   │   ├── 📄 InputComposer.tsx      # Message input
│   │   │   │   ├── 📄 TypingIndicator.tsx    # Agent typing animation
│   │   │   │   ├── 📄 EscalationPanel.tsx    # Human handoff UI
│   │   │   │   └── 📄 FeedbackButtons.tsx    # Thumbs up/down
│   │   │   │
│   │   │   └── 📁 ui/                        # Shadcn UI components
│   │   │       ├── 📄 button.tsx
│   │   │       ├── 📄 input.tsx
│   │   │       ├── 📄 card.tsx
│   │   │       ├── 📄 scroll-area.tsx
│   │   │       └── 📄 avatar.tsx
│   │   │
│   │   ├── 📁 hooks/
│   │   │   ├── 📄 useChat.ts                 # Chat state management
│   │   │   ├── 📄 useWebSocket.ts            # WebSocket connection
│   │   │   └── 📄 useSession.ts              # Session management
│   │   │
│   │   ├── 📁 lib/
│   │   │   ├── 📄 api.ts                     # API client
│   │   │   └── 📄 utils.ts                   # Utility functions
│   │   │
│   │   ├── 📁 styles/
│   │   │   └── 📄 globals.css                # Tailwind + custom styles
│   │   │
│   │   ├── 📄 App.tsx
│   │   └── 📄 main.tsx
│   │
│   ├── 📄 package.json
│   ├── 📄 tailwind.config.js
│   ├── 📄 tsconfig.json
│   ├── 📄 vite.config.ts
│   └── 📄 Dockerfile
│
├── 📁 docs/
│   ├── 📄 ARCHITECTURE.md
│   ├── 📄 DEPLOYMENT.md
│   ├── 📄 API.md
│   └── 📄 KNOWLEDGE_BASE_GUIDE.md
│
├── 📁 data/
│   └── 📁 sample_documents/                  # Example documents for testing
│
├── 📄 docker-compose.yml
├── 📄 docker-compose.dev.yml
├── 📄 .env.example
└── 📄 README.md
3.2 Implementation Phases
text

┌──────────────────────────────────────────────────────────────────────────────────────┐
│                                                                                      │
│                          IMPLEMENTATION ROADMAP                                      │
│                                                                                      │
├──────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                      │
│  PHASE 1: FOUNDATION (Week 1-2)                                                      │
│  ═══════════════════════════════                                                     │
│                                                                                      │
│  ┌────────────────────────────────────────────────────────────────────────────────┐ │
│  │  1.1 Project Setup & Infrastructure                                            │ │
│  │      □ Initialize Python project with pyproject.toml                           │ │
│  │      □ Set up Docker Compose for Qdrant, PostgreSQL, Redis                     │ │
│  │      □ Configure environment management (.env, pydantic-settings)              │ │
│  │      □ Set up structured logging (structlog)                                   │ │
│  │      □ Create database schemas and migrations (Alembic)                        │ │
│  │      Validation: All services start, connections verified                      │ │
│  │      ────────────────────────────────────────────────────────────────────────  │ │
│  │  1.2 Core RAG Pipeline - Indexing                                              │ │
│  │      □ Implement document loader (Unstructured.io integration)                 │ │
│  │      □ Build semantic chunking pipeline                                        │ │
│  │      □ Create embedding generation (OpenAI text-embedding-3-small)             │ │
│  │      □ Set up Qdrant collection with hybrid indexing                           │ │
│  │      □ Implement metadata enrichment                                           │ │
│  │      □ Create bulk ingestion script                                            │ │
│  │      Validation: Sample documents indexed, basic search works                  │ │
│  │      ────────────────────────────────────────────────────────────────────────  │ │
│  │  1.3 Core RAG Pipeline - Retrieval                                             │ │
│  │      □ Implement hybrid search (dense + sparse)                                │ │
│  │      □ Add RRF fusion logic                                                    │ │
│  │      □ Integrate Cohere reranker                                               │ │
│  │      □ Build query transformer (rewriting/expansion)                           │ │
│  │      □ Implement context compressor                                            │ │
│  │      Validation: RAG pipeline returns relevant, compressed results             │ │
│  └────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                      │
│  PHASE 2: AGENT CORE (Week 3-4)                                                      │
│  ═══════════════════════════════                                                     │
│                                                                                      │
│  ┌────────────────────────────────────────────────────────────────────────────────┐ │
│  │  2.1 Pydantic AI Agent Setup                                                   │ │
│  │      □ Define agent with system prompt                                         │ │
│  │      □ Create tool definitions (rag_search, escalate_human)                    │ │
│  │      □ Implement structured output schemas                                     │ │
│  │      □ Set up dependency injection for LLM, retriever                          │ │
│  │      Validation: Agent can answer basic questions using RAG                    │ │
│  │      ────────────────────────────────────────────────────────────────────────  │ │
│  │  2.2 Memory System - Short-Term                                                │ │
│  │      □ Implement conversation buffer with sliding window                       │ │
│  │      □ Create summarization logic for long conversations                       │ │
│  │      □ Integrate LangGraph for state management                                │ │
│  │      □ Add entity tracking (current product, order, etc.)                      │ │
│  │      Validation: Multi-turn conversations maintain context                     │ │
│  │      ────────────────────────────────────────────────────────────────────────  │ │
│  │  2.3 Memory System - Long-Term                                                 │ │
│  │      □ Create customer profile model and CRUD                                  │ │
│  │      □ Implement conversation history storage                                  │ │
│  │      □ Build customer profile summarization                                    │ │
│  │      □ Add session-to-long-term memory transfer                                │ │
│  │      Validation: Returning customer context is retrieved                       │ │
│  │      ────────────────────────────────────────────────────────────────────────  │ │
│  │  2.4 Working Memory Assembly                                                   │ │
│  │      □ Implement context window budget management                              │ │
│  │      □ Create optimal prompt assembly logic                                    │ │
│  │      □ Add token counting and truncation                                       │ │
│  │      Validation: Context stays within token limits                             │ │
│  └────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                      │
│  PHASE 3: API & INTEGRATION (Week 5)                                                 │
│  ═══════════════════════════════════                                                 │
│                                                                                      │
│  ┌────────────────────────────────────────────────────────────────────────────────┐ │
│  │  3.1 FastAPI Application                                                       │ │
│  │      □ Set up FastAPI with proper structure                                    │ │
│  │      □ Implement chat endpoint (POST /api/chat)                                │ │
│  │      □ Add WebSocket endpoint for streaming                                    │ │
│  │      □ Create session management endpoints                                     │ │
│  │      □ Implement health checks                                                 │ │
│  │      Validation: API endpoints functional via curl/Postman                     │ │
│  │      ────────────────────────────────────────────────────────────────────────  │ │
│  │  3.2 Streaming Implementation                                                  │ │
│  │      □ Configure LLM for streaming responses                                   │ │
│  │      □ Implement SSE endpoint                                                  │ │
│  │      □ Handle partial token streaming                                          │ │
│  │      □ Add error handling for stream interruption                              │ │
│  │      Validation: Responses stream token-by-token                               │ │
│  │      ────────────────────────────────────────────────────────────────────────  │ │
│  │  3.3 Admin Endpoints                                                           │ │
│  │      □ Document upload and indexing API                                        │ │
│  │      □ Knowledge base management (list, delete)                                │ │
│  │      □ Analytics endpoints (usage stats)                                       │ │
│  │      Validation: Admin can manage knowledge base via API                       │ │
│  └────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                      │
│  PHASE 4: FRONTEND (Week 6-7)                                                        │
│  ═══════════════════════════════                                                     │
│                                                                                      │
│  ┌────────────────────────────────────────────────────────────────────────────────┐ │
│  │  4.1 React Project Setup                                                       │ │
│  │      □ Initialize Vite + React + TypeScript                                    │ │
│  │      □ Configure Tailwind CSS 4.0                                              │ │
│  │      □ Set up Shadcn UI components                                             │ │
│  │      □ Create project structure                                                │ │
│  │      Validation: Dev server runs, components render                            │ │
│  │      ────────────────────────────────────────────────────────────────────────  │ │
│  │  4.2 Chat Interface Components                                                 │ │
│  │      □ Build ChatContainer with layout                                         │ │
│  │      □ Create MessageList with virtualization                                  │ │
│  │      □ Implement MessageBubble (user/assistant variants)                       │ │
│  │      □ Build InputComposer with send functionality                             │ │
│  │      □ Add TypingIndicator animation                                           │ │
│  │      Validation: Chat UI renders, messages display correctly                   │ │
│  │      ────────────────────────────────────────────────────────────────────────  │ │
│  │  4.3 Real-time Communication                                                   │ │
│  │      □ Implement useWebSocket hook                                             │ │
│  │      □ Handle connection lifecycle                                             │ │
│  │      □ Process streaming responses                                             │ │
│  │      □ Add reconnection logic                                                  │ │
│  │      Validation: Messages send/receive in real-time                            │ │
│  │      ────────────────────────────────────────────────────────────────────────  │ │
│  │  4.4 Polish & UX                                                               │ │
│  │      □ Add loading states and transitions                                      │ │
│  │      □ Implement error handling UI                                             │ │
│  │      □ Create escalation request panel                                         │ │
│  │      □ Add feedback buttons (thumbs up/down)                                   │ │
│  │      □ Mobile responsiveness                                                   │ │
│  │      □ Accessibility audit (WCAG AA)                                           │ │
│  │      Validation: Smooth UX, accessible, mobile-friendly                        │ │
│  └────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                      │
│  PHASE 5: QUALITY & DEPLOYMENT (Week 8)                                              │
│  ═══════════════════════════════════════                                             │
│                                                                                      │
│  ┌────────────────────────────────────────────────────────────────────────────────┐ │
│  │  5.1 Testing                                                                   │ │
│  │      □ Unit tests for RAG components                                           │ │
│  │      □ Integration tests for agent                                             │ │
│  │      □ API endpoint tests                                                      │ │
│  │      □ Frontend component tests                                                │ │
│  │      □ End-to-end tests (Playwright)                                           │ │
│  │      Validation: >80% coverage, all tests pass                                 │ │
│  │      ────────────────────────────────────────────────────────────────────────  │ │
│  │  5.2 RAG Evaluation                                                            │ │
│  │      □ Create evaluation dataset                                               │ │
│  │      □ Run RAGAs evaluation (faithfulness, relevancy)                          │ │
│  │      □ Benchmark retrieval (NDCG, Hit Rate)                                    │ │
│  │      □ Tune parameters based on results                                        │ │
│  │      Validation: Faithfulness >0.9, Answer Relevancy >0.85                     │ │
│  │      ────────────────────────────────────────────────────────────────────────  │ │
│  │  5.3 Security & Compliance                                                     │ │
│  │      □ API key management (secrets)                                            │ │
│  │      □ Rate limiting implementation                                            │ │
│  │      □ Input sanitization                                                      │ │
│  │      □ PDPA compliance review                                                  │ │
│  │      □ Security audit (OWASP basics)                                           │ │
│  │      Validation: No critical vulnerabilities                                   │ │
│  │      ────────────────────────────────────────────────────────────────────────  │ │
│  │  5.4 Deployment                                                                │ │
│  │      □ Production Docker Compose configuration                                 │ │
│  │      □ Environment variable documentation                                      │ │
│  │      □ Deployment runbook                                                      │ │
│  │      □ Monitoring setup (basic)                                                │ │
│  │      □ Backup procedures                                                       │ │
│  │      Validation: System runs in production-like environment                    │ │
│  └────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                      │
│  PHASE 6: DOCUMENTATION & HANDOFF (Week 8)                                           │ │
│  ═════════════════════════════════════════                                           │ │
│                                                                                      │
│  ┌────────────────────────────────────────────────────────────────────────────────┐ │
│  │  6.1 Documentation                                                             │ │
│  │      □ Architecture documentation                                              │ │
│  │      □ API documentation (OpenAPI)                                             │ │
│  │      □ Knowledge base management guide                                         │ │
│  │      □ Deployment guide                                                        │ │
│  │      □ Troubleshooting runbook                                                 │ │
│  │      Validation: Non-technical user can manage system                          │ │
│  └────────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                      │
└──────────────────────────────────────────────────────────────────────────────────────┘
3.3 Key Implementation Details
3.3.1 Pydantic AI Agent Definition (Core Pattern)
Python

# Conceptual structure - actual implementation in Phase 2

from pydantic_ai import Agent, RunContext
from pydantic import BaseModel
from typing import Literal

class CustomerSupportDeps(BaseModel):
    """Dependencies injected into the agent"""
    customer_id: str | None
    session_id: str
    rag_retriever: RAGRetriever
    memory_store: MemoryStore
    
class SupportResponse(BaseModel):
    """Structured output from agent"""
    message: str
    confidence: float
    sources: list[str]
    requires_escalation: bool
    suggested_actions: list[str]

support_agent = Agent(
    'openai:gpt-4o-mini',
    deps_type=CustomerSupportDeps,
    result_type=SupportResponse,
    system_prompt="""You are a helpful customer support agent for {business_name}, 
    a Singapore-based business. You assist customers with enquiries about products, 
    services, orders, and general information.
    
    Guidelines:
    - Be warm, professional, and efficient
    - Use information from the provided context only
    - If uncertain, acknowledge it honestly
    - Escalate to human support when appropriate
    - Respect Singapore business customs and language nuances
    """
)

@support_agent.tool
async def search_knowledge_base(
    ctx: RunContext[CustomerSupportDeps],
    query: str
) -> str:
    """Search the business knowledge base for relevant information."""
    results = await ctx.deps.rag_retriever.retrieve(query)
    return format_retrieved_context(results)

@support_agent.tool
async def escalate_to_human(
    ctx: RunContext[CustomerSupportDeps],
    reason: str
) -> str:
    """Escalate the conversation to a human support agent."""
    await ctx.deps.memory_store.flag_for_escalation(
        session_id=ctx.deps.session_id,
        reason=reason
    )
    return "Escalation request submitted. A human agent will assist shortly."
3.3.2 Memory Integration Pattern
Python

# Conceptual structure - actual implementation in Phase 2

class ConversationMemory:
    """Manages the three-tier memory system"""
    
    def __init__(
        self,
        postgres: PostgresClient,
        redis: RedisClient,
        summarizer: ConversationSummarizer
    ):
        self.postgres = postgres
        self.redis = redis
        self.summarizer = summarizer
        
    async def build_working_memory(
        self,
        session_id: str,
        customer_id: str | None,
        retrieved_context: str,
        current_message: str
    ) -> WorkingMemory:
        """Assemble the optimal context for the current LLM call"""
        
        # 1. Get customer profile (long-term)
        customer_summary = ""
        if customer_id:
            profile = await self.postgres.get_customer_profile(customer_id)
            customer_summary = profile.summary if profile else ""
        
        # 2. Get conversation history (short-term)
        messages = await self.redis.get_session_messages(session_id)
        
        # 3. Apply sliding window with summarization
        if len(messages) > 10:
            older_messages = messages[:-6]
            recent_messages = messages[-6:]
            conversation_summary = await self.summarizer.summarize(older_messages)
            conversation_context = format_with_summary(
                summary=conversation_summary,
                recent=recent_messages
            )
        else:
            conversation_context = format_messages(messages)
        
        # 4. Assemble within token budget
        return WorkingMemory(
            customer_context=customer_summary,      # ~200 tokens
            retrieved_context=retrieved_context,    # ~1500 tokens
            conversation_context=conversation_context,  # ~1400 tokens
            current_message=current_message,        # ~100 tokens
        )
3.3.3 Frontend Chat Component (Aesthetic Direction)
text

┌──────────────────────────────────────────────────────────────────────────────────────┐
│                                                                                      │
│                        FRONTEND AESTHETIC DIRECTION                                  │
│                                                                                      │
│  ┌────────────────────────────────────────────────────────────────────────────────┐ │
│  │                                                                                │ │
│  │   CONCEPT: "Trusted Advisor"                                                   │ │
│  │   ───────────────────────────                                                  │ │
│  │                                                                                │ │
│  │   A chat interface that feels like speaking with a knowledgeable,              │ │
│  │   composed professional - not a gimmicky chatbot.                              │ │
│  │                                                                                │ │
│  │   VISUAL LANGUAGE:                                                             │ │
│  │   ├── Clean, editorial typography (Inter or Source Sans)                       │ │
│  │   ├── Generous whitespace (breathing room signals competence)                  │ │
│  │   ├── Subtle, non-intrusive animations                                         │ │
│  │   ├── Monochromatic base with single accent color                              │ │
│  │   └── No gradients, no unnecessary ornamentation                               │ │
│  │                                                

# Phase 1: Deep Analysis & Strategic Design

## Executive Summary

I'll design a **production-grade, context-aware AI customer support agent** for Singapore SMBs that synthesizes advanced RAG methodologies with agentic workflows. This system will move beyond simple Q&A to deliver intelligent, multi-turn conversations with genuine business understanding.

---

## 1. DEEP REQUIREMENT ANALYSIS

### A. Business Context: Singapore SMB Landscape

**Critical Insights:**
- **Market Reality**: Singapore SMBs (≤200 employees) face resource constraints but demand enterprise-grade customer experience
- **Multilingual Necessity**: English + Singlish colloquialisms, potential Mandarin/Malay support
- **Regulatory Compliance**: PDPA (Personal Data Protection Act) compliance mandatory
- **Operating Hours**: 24/7 support expectations despite small teams
- **Cost Sensitivity**: Must justify ROI through measurable efficiency gains

**User Personas:**
1. **Customer-facing staff** (primary users): Need quick, accurate information retrieval
2. **Business owners**: Require analytics, cost monitoring, quality assurance
3. **End customers**: Expect natural, helpful interactions via chat

### B. Technical Requirements Matrix

| Dimension | Requirement | Rationale |
|-----------|-------------|-----------|
| **Latency** | <3s first response, <1.5s subsequent | Attention span threshold for chat |
| **Accuracy** | >90% faithfulness, >85% answer relevance | Trust threshold for business use |
| **Scalability** | Handle 100-500 concurrent conversations | Typical SMB peak traffic |
| **Memory** | 2-hour short-term window, indefinite long-term | Balance context vs. cost |
| **Observability** | Full conversation tracing, metric dashboards | Required for continuous improvement |
| **Security** | End-to-end encryption, PII detection/masking | PDPA compliance |

### C. Multi-Dimensional Analysis

#### **1. Psychological Dimension**
- **User Sentiment**: Customers arrive frustrated; agent must de-escalate through empathetic tone
- **Cognitive Load**: Minimize decision fatigue with clear, structured responses
- **Trust Building**: Cite sources, admit uncertainty, escalate gracefully to humans

#### **2. Technical Dimension**
- **Rendering Performance**: React frontend must maintain 60fps during streaming responses
- **State Complexity**: Managing conversation history, user preferences, business context simultaneously
- **Repaint/Reflow Costs**: Optimize DOM updates for message rendering

#### **3. Accessibility Dimension**
- **WCAG AAA Compliance**: Keyboard navigation, screen reader support, color contrast
- **Multilingual UI**: RTL support for potential Arabic customers
- **Mobile-First**: 70% of Singapore users on mobile devices

#### **4. Scalability Dimension**
- **Horizontal Scaling**: Stateless agent design for load balancing
- **Database Sharding**: Vector DB partitioning by business unit
- **Cache Strategy**: Redis for frequently accessed knowledge chunks

---

## 2. ARCHITECTURAL DESIGN

### A. System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    CUSTOMER ENQUIRY AI AGENT                    │
│                  (Singapore SMB Context-Aware)                  │
└─────────────────────────────────────────────────────────────────┘
                              │
            ┌─────────────────┼─────────────────┐
            │                 │                 │
    ┌───────▼───────┐ ┌──────▼──────┐ ┌───────▼───────┐
    │   Frontend    │ │   Backend   │ │   AI Engine   │
    │  React + WS   │ │  FastAPI    │ │  LangGraph    │
    └───────────────┘ └─────────────┘ └───────────────┘
            │                 │                 │
    ┌───────▼───────┐ ┌──────▼──────┐ ┌───────▼───────┐
    │  UI Layer     │ │  API Layer  │ │ Agent Layer   │
    │  - Chat Box   │ │  - REST     │ │ - Orchestrator│
    │  - Typing     │ │  - WebSocket│ │ - RAG Tools   │
    │  - History    │ │  - Auth     │ │ - Memory Mgmt │
    └───────────────┘ └─────────────┘ └───────────────┘
                              │
            ┌─────────────────┼─────────────────┐
            │                 │                 │
    ┌───────▼───────┐ ┌──────▼──────┐ ┌───────▼───────┐
    │  Vector DB    │ │  SQL DB     │ │  Cache Layer  │
    │  (Qdrant)     │ │  (Postgres) │ │  (Redis)      │
    │  - Embeddings │ │  - Users    │ │  - Sessions   │
    │  - Metadata   │ │  - Logs     │ │  - Hot Chunks │
    └───────────────┘ └─────────────┘ └───────────────┘
```

### B. Core Component Design

#### **1. Frontend Layer (React + TypeScript)**

**Design Philosophy**: "Intentional Minimalism" with "Conversational Clarity"

```typescript
// Architectural Decisions:
// 1. WebSocket for real-time streaming (no polling)
// 2. Optimistic UI updates for perceived speed
// 3. Virtual scrolling for long conversation histories
// 4. IndexedDB for offline conversation caching

interface ChatMessage {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: Date;
  metadata?: {
    sources?: Source[];
    confidence?: number;
    reasoning?: string;
  };
  status: 'sending' | 'sent' | 'error';
}

// Component Hierarchy:
<ChatContainer>
  <ConversationHeader /> {/* Business context, session info */}
  <MessageList>         {/* Virtualized for performance */}
    <MessageBubble />   {/* User/Assistant with citations */}
    <TypingIndicator /> {/* Animated during agent thinking */}
  </MessageList>
  <InputComposer />     {/* Multi-line, attachment support */}
  <QuickActions />      {/* Suggested responses, escalation */}
</ChatContainer>
```

**Aesthetic Direction**: 
- **Tone**: "Refined Digital Banking" - trust through clarity
- **Typography**: Inter for UI, system fonts for messages (legibility)
- **Color**: Deep navy primary (#1a2332), teal accent (#14b8a6), warm grays
- **Spacing**: Generous whitespace (1.5rem base unit) for breathing room
- **Animation**: Subtle micro-interactions (200ms spring easing)

#### **2. Backend API Layer (FastAPI + Python 3.11+)**

```python
# Architecture Pattern: Hexagonal (Ports & Adapters)
# - Domain logic isolated from infrastructure
# - Easy testing, framework-agnostic core

from fastapi import FastAPI, WebSocket
from pydantic import BaseModel, Field
from contextlib import asynccontextmanager

class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=2000)
    session_id: str
    metadata: dict[str, Any] = Field(default_factory=dict)
    
class StreamingResponse(BaseModel):
    type: Literal['chunk', 'complete', 'error']
    content: str
    sources: list[Source] = []
    
# Critical Endpoints:
# POST /api/v1/chat/query - Initiate conversation
# WS   /api/v1/chat/stream - Bidirectional streaming
# GET  /api/v1/chat/history/{session_id} - Retrieve context
# POST /api/v1/feedback - User satisfaction scoring
```

#### **3. AI Agent Layer (LangGraph + Pydantic AI)**

**Core Innovation**: Multi-stage reasoning with explicit memory management

```python
from langgraph.graph import StateGraph, END
from pydantic_ai import Agent, RunContext
from typing import Annotated, TypedDict

class AgentState(TypedDict):
    # Conversation Context
    messages: list[Message]
    session_id: str
    
    # Memory Layers (Hierarchical)
    long_term_facts: list[str]      # Company knowledge base
    short_term_context: list[str]   # Last 10 turns, summarized
    working_memory: str              # Current retrieval context
    
    # Reasoning Trace
    current_step: str
    reasoning_chain: list[str]
    confidence_score: float
    
    # Metadata
    user_profile: UserProfile
    retrieved_chunks: list[Chunk]
    
# Graph Structure:
graph = StateGraph(AgentState)

# Nodes (Processing Steps):
graph.add_node("query_analysis", analyze_user_intent)
graph.add_node("memory_retrieval", retrieve_relevant_context)
graph.add_node("rag_search", execute_hybrid_search)
graph.add_node("rerank", cross_encoder_rerank)
graph.add_node("response_generation", generate_response)
graph.add_node("quality_check", verify_faithfulness)

# Edges (Control Flow):
graph.add_edge("query_analysis", "memory_retrieval")
graph.add_conditional_edges(
    "memory_retrieval",
    route_search_strategy,  # Decides: memory_only vs. RAG needed
    {
        "sufficient": "response_generation",
        "needs_rag": "rag_search"
    }
)
graph.add_edge("rag_search", "rerank")
graph.add_edge("rerank", "response_generation")
graph.add_edge("response_generation", "quality_check")
graph.add_conditional_edges(
    "quality_check",
    check_quality,
    {
        "pass": END,
        "retry": "response_generation",  # Loop if hallucination detected
        "escalate": "human_handoff"
    }
)
```

**Key Design Decisions:**

1. **Why LangGraph over LangChain Chains?**
   - **Cyclical Reasoning**: Allows self-correction loops (quality_check → retry)
   - **State Persistence**: Built-in checkpointing for long conversations
   - **Observability**: Graph structure visualizable for debugging

2. **Why Pydantic AI Integration?**
   - **Type Safety**: Structured outputs prevent hallucinated JSON
   - **Validation**: Automatic checking of agent tool calls
   - **Dependencies**: Inject context (DB connections, API keys) cleanly

3. **Memory Architecture Rationale:**
   ```
   Long-Term Memory (Vector DB)
   ↓ [Retrieval based on query similarity]
   Short-Term Memory (Redis + Summarization)
   ↓ [Sliding window of last 10 turns, compressed]
   Working Memory (LLM Context Window)
   ↓ [Final, optimized prompt with top-k chunks]
   ```

---

## 3. ADVANCED RAG PIPELINE DESIGN

### A. Indexing Pipeline (Offline Preprocessing)

```python
# Stage 1: Data Ingestion
from unstructured.partition.auto import partition

documents = partition(
    filename="company_kb.pdf",
    strategy="hi_res",  # OCR + layout analysis
    extract_images_in_pdf=True,
    infer_table_structure=True
)

# Stage 2: Intelligent Chunking
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Decision: Semantic Chunking for SMB knowledge base
# - Average doc: 5-20 pages product manuals
# - Optimal chunk: 512 tokens (~380 words) with 50 token overlap
# - Preserves context across paragraph boundaries

splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,
    chunk_overlap=50,
    separators=["\n\n", "\n", ". ", " ", ""],
    length_function=tiktoken_len
)

# Stage 3: Metadata Enrichment
for chunk in chunks:
    chunk.metadata = {
        "source": "product_manual_v2.pdf",
        "page": chunk.page_number,
        "section": extract_section_title(chunk),  # LLM-generated
        "keywords": extract_keywords(chunk),       # KeyBERT
        "category": classify_content(chunk),       # Zero-shot
        "created_at": datetime.utcnow(),
        "version": "2.1.0"
    }

# Stage 4: Embedding Generation
from sentence_transformers import SentenceTransformer

# Decision: bge-large-en-v1.5 (1024 dims)
# - SOTA for retrieval (MTEB benchmark)
# - Better than OpenAI ada-002 for domain-specific knowledge
# - Self-hosted = no API costs, data privacy

embedder = SentenceTransformer('BAAI/bge-large-en-v1.5')
embeddings = embedder.encode(
    [chunk.content for chunk in chunks],
    normalize_embeddings=True  # Cosine similarity
)

# Stage 5: Vector Storage (Qdrant)
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

client = QdrantClient(url="http://localhost:6333")

client.create_collection(
    collection_name="smb_knowledge_base",
    vectors_config=VectorParams(
        size=1024,
        distance=Distance.COSINE
    )
)

points = [
    PointStruct(
        id=idx,
        vector=embedding.tolist(),
        payload={
            "content": chunk.content,
            **chunk.metadata
        }
    )
    for idx, (chunk, embedding) in enumerate(zip(chunks, embeddings))
]

client.upsert(collection_name="smb_knowledge_base", points=points)
```

### B. Retrieval Pipeline (Online Query Processing)

```python
# Multi-Stage Retrieval Implementation

class HybridRetriever:
    def __init__(self, vector_db, bm25_index):
        self.vector_db = vector_db
        self.bm25_index = bm25_index
        self.reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')
        
    async def retrieve(
        self, 
        query: str, 
        top_k: int = 50,
        final_k: int = 5
    ) -> list[Chunk]:
        
        # Stage 1: Query Transformation
        transformed_queries = await self.transform_query(query)
        # - Original query
        # - Rephrased version (LLM)
        # - Sub-questions (if complex)
        
        # Stage 2: Hybrid Search
        dense_results = await self.dense_search(
            transformed_queries, 
            top_k=top_k
        )
        sparse_results = await self.sparse_search(
            transformed_queries,
            top_k=top_k
        )
        
        # Stage 3: Fusion (RRF)
        fused_results = self.reciprocal_rank_fusion(
            [dense_results, sparse_results],
            k=60  # RRF parameter
        )
        
        # Stage 4: Cross-Encoder Reranking
        pairs = [(query, chunk.content) for chunk in fused_results[:top_k]]
        scores = self.reranker.predict(pairs)
        
        reranked = sorted(
            zip(fused_results[:top_k], scores),
            key=lambda x: x[1],
            reverse=True
        )
        
        # Stage 5: Context Compression
        final_chunks = reranked[:final_k]
        compressed = await self.compress_context(query, final_chunks)
        
        return compressed
    
    async def transform_query(self, query: str) -> list[str]:
        """Query expansion using LLM"""
        prompt = f"""
        Original query: {query}
        
        Generate 2 alternative phrasings that might improve retrieval:
        1. A more specific version
        2. A broader, conceptual version
        
        Return as JSON array of strings.
        """
        # Use structured output (Pydantic AI)
        result = await llm.generate(prompt, response_model=QueryVariants)
        return [query] + result.variants
    
    async def dense_search(self, queries: list[str], top_k: int):
        """Vector similarity search"""
        query_embeddings = self.embedder.encode(queries)
        
        results = []
        for emb in query_embeddings:
            hits = self.vector_db.search(
                collection_name="smb_knowledge_base",
                query_vector=emb.tolist(),
                limit=top_k,
                with_payload=True
            )
            results.extend(hits)
        
        return self.deduplicate(results)
    
    async def sparse_search(self, queries: list[str], top_k: int):
        """BM25 keyword search"""
        results = []
        for query in queries:
            hits = self.bm25_index.get_top_n(
                query, 
                self.corpus, 
                n=top_k
            )
            results.extend(hits)
        
        return results
    
    def reciprocal_rank_fusion(
        self, 
        result_lists: list[list[Chunk]], 
        k: int = 60
    ) -> list[Chunk]:
        """Merge multiple ranked lists"""
        scores = defaultdict(float)
        
        for result_list in result_lists:
            for rank, chunk in enumerate(result_list):
                scores[chunk.id] += 1 / (k + rank + 1)
        
        return sorted(scores.items(), key=lambda x: x[1], reverse=True)
    
    async def compress_context(
        self, 
        query: str, 
        chunks: list[tuple[Chunk, float]]
    ) -> list[Chunk]:
        """Extractive compression to reduce token count"""
        compressed_chunks = []
        
        for chunk, score in chunks:
            # Keep only sentences highly relevant to query
            relevant_sentences = await self.extract_relevant_sentences(
                query, 
                chunk.content
            )
            
            compressed_chunks.append(
                Chunk(
                    content=" ".join(relevant_sentences),
                    metadata={
                        **chunk.metadata,
                        "compression_ratio": len(relevant_sentences) / len(chunk.sentences),
                        "relevance_score": score
                    }
                )
            )
        
        return compressed_chunks
```

---

## 4. MEMORY MANAGEMENT ARCHITECTURE

### A. Three-Layer Memory System

```python
class MemoryManager:
    """
    Hierarchical memory inspired by human cognition:
    - Long-term: Entire knowledge base (Vector DB)
    - Short-term: Conversation history (Redis + Summarization)
    - Working: Current context (LLM prompt)
    """
    
    def __init__(
        self,
        vector_db: QdrantClient,
        cache: Redis,
        summarizer: LLM
    ):
        self.long_term = LongTermMemory(vector_db)
        self.short_term = ShortTermMemory(cache, summarizer)
        self.working = WorkingMemory(max_tokens=4000)
    
    async def prepare_context(
        self,
        session_id: str,
        current_query: str
    ) -> str:
        """
        Optimized context assembly for LLM input
        
        Process:
        1. Retrieve conversation summary from short-term
        2. Semantic search in long-term based on query + summary
        3. Compress and structure for working memory
        """
        
        # Short-term: Last 10 turns, rolling summary
        conversation_summary = await self.short_term.get_summary(session_id)
        recent_turns = await self.short_term.get_recent(session_id, n=3)
        
        # Long-term: RAG retrieval
        rag_context = await self.long_term.retrieve(
            query=current_query,
            context=conversation_summary,  # Contextualized search
            top_k=5
        )
        
        # Working memory assembly
        context = self.working.assemble({
            "system_prompt": AGENT_INSTRUCTIONS,
            "conversation_summary": conversation_summary,
            "recent_history": recent_turns,
            "retrieved_knowledge": rag_context,
            "current_query": current_query
        })
        
        return context

class ShortTermMemory:
    """
    Manages conversation state with automatic summarization
    """
    
    def __init__(self, cache: Redis, summarizer: LLM):
        self.cache = cache
        self.summarizer = summarizer
        self.window_size = 10  # turns
        self.summarization_threshold = 2000  # tokens
    
    async def add_turn(
        self, 
        session_id: str, 
        role: str, 
        content: str
    ):
        """Add message and trigger summarization if needed"""
        key = f"conversation:{session_id}"
        
        # Append to conversation
        await self.cache.rpush(key, json.dumps({
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow().isoformat()
        }))
        
        # Sliding window: keep only last N turns
        await self.cache.ltrim(key, -self.window_size, -1)
        
        # Check if summarization needed
        conversation = await self.cache.lrange(key, 0, -1)
        total_tokens = sum(count_tokens(msg['content']) for msg in conversation)
        
        if total_tokens > self.summarization_threshold:
            await self.create_summary(session_id, conversation)
    
    async def create_summary(
        self, 
        session_id: str, 
        conversation: list[dict]
    ):
        """
        Progressive summarization strategy:
        - Compress older messages more aggressively
        - Keep recent exchanges verbatim
        """
        
        # Split: old (to summarize) vs recent (keep detailed)
        old_messages = conversation[:-3]
        recent_messages = conversation[-3:]
        
        # Summarize old messages
        summary_prompt = f"""
        Summarize the following conversation, focusing on:
        1. Key facts established
        2. Customer's main concerns/questions
        3. Product/service details discussed
        4. Any unresolved issues
        
        Conversation:
        {json.dumps(old_messages, indent=2)}
        
        Provide a concise summary (max 200 words).
        """
        
        summary = await self.summarizer.generate(summary_prompt)
        
        # Store summary
        summary_key = f"summary:{session_id}"
        await self.cache.set(
            summary_key, 
            summary,
            ex=7200  # 2 hour expiry
        )
        
        # Update conversation to include summary + recent
        compressed_key = f"conversation:{session_id}"
        await self.cache.delete(compressed_key)
        await self.cache.rpush(compressed_key, json.dumps({
            "role": "system",
            "content": f"Conversation summary: {summary}",
            "timestamp": datetime.utcnow().isoformat()
        }))
        
        for msg in recent_messages:
            await self.cache.rpush(compressed_key, json.dumps(msg))
```

---

## 5. IMPLEMENTATION PLAN (VALIDATED)

### Phase Breakdown

```
┌─────────────────────────────────────────────────────────────────┐
│ IMPLEMENTATION TIMELINE: 8-10 Weeks (SMB-Optimized Sprints)    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Week 1-2: Foundation & Data Pipeline                          │
│  ├─ Set up development environment (Docker Compose)            │
│  ├─ Implement indexing pipeline (Unstructured.io → Qdrant)     │
│  ├─ Build evaluation dataset (50 question-answer pairs)        │
│  └─ Establish baseline metrics (latency, accuracy)             │
│                                                                 │
│  Week 3-4: Core RAG Implementation                             │
│  ├─ Develop hybrid retriever (vector + BM25)                   │
│  ├─ Integrate cross-encoder reranking                          │
│  ├─ Implement query transformation module                      │
│  └─ Unit test each retrieval stage (pytest)                    │
│                                                                 │
│  Week 5-6: Agent & Memory Systems                              │
│  ├─ Build LangGraph agent workflow                             │
│  ├─ Implement three-layer memory architecture                  │
│  ├─ Develop conversation state management (Redis)              │
│  └─ Add quality assurance node (faithfulness check)            │
│                                                                 │
│  Week 7-8: Frontend & API Integration                          │
│  ├─ Create React chat interface (WebSocket streaming)          │
│  ├─ Build FastAPI backend (REST + WS endpoints)                │
│  ├─ Implement authentication & session management              │
│  └─ Add observability (LangSmith/LangFuse tracing)             │
│                                                                 │
│  Week 9-10: Testing, Optimization & Deployment                 │
│  ├─ Load testing (Locust: 100 concurrent users)                │
│  ├─ Security audit (OWASP checklist, PII detection)            │
│  ├─ Performance tuning (query latency optimization)            │
│  └─ Deploy to staging (AWS ECS / GCP Cloud Run)                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Detailed Task Checklist

#### **Phase 1: Foundation (Week 1-2)**
- [ ] **Environment Setup**
  - [ ] Docker Compose with services: FastAPI, Qdrant, Redis, PostgreSQL
  - [ ] Python 3.11+ with poetry for dependency management
  - [ ] Pre-commit hooks: black, ruff, mypy for code quality
  
- [ ] **Data Pipeline**
  - [ ] Install & configure Unstructured.io for document parsing
  - [ ] Implement chunking strategies (recursive, semantic comparison)
  - [ ] Set up embedding pipeline (bge-large-en-v1.5)
  - [ ] Initialize Qdrant collection with metadata schema
  - [ ] Create ingestion scripts for PDF, DOCX, CSV
  
- [ ] **Evaluation Framework**
  - [ ] Curate 50 Singapore SMB-specific Q&A pairs
  - [ ] Set up RAGAs for automated evaluation
  - [ ] Define success metrics:
    - Faithfulness: >0.9
    - Answer Relevance: >0.85
    - Context Precision: >0.8
    - Latency P95: <3s

#### **Phase 2: Core RAG (Week 3-4)**
- [ ] **Retrieval Components**
  - [ ] Implement dense vector search (Qdrant client)
  - [ ] Build BM25 sparse retrieval (rank-bm25 library)
  - [ ] Create RRF fusion algorithm
  - [ ] Integrate cross-encoder reranking (ms-marco model)
  - [ ] Add metadata filtering (date ranges, categories)
  
- [ ] **Query Processing**
  - [ ] Build query transformation module:
    - [ ] Query rewriting (GPT-4o-mini for cost)
    - [ ] Sub-question decomposition
    - [ ] Step-back prompting for context
  - [ ] Implement intent classification (product vs. policy vs. troubleshooting)
  
- [ ] **Testing**
  - [ ] Write pytest suite for each retrieval stage
  - [ ] Benchmark retrieval quality (NDCG@5, MRR)
  - [ ] Profile latency bottlenecks (cProfile)

#### **Phase 3: Agent Architecture (Week 5-6)**
- [ ] **LangGraph Agent**
  - [ ] Define AgentState schema (Pydantic models)
  - [ ] Implement graph nodes:
    - [ ] Query analysis node
    - [ ] Memory retrieval node
    - [ ] RAG search node
    - [ ] Reranking node
    - [ ] Response generation node
    - [ ] Quality check node (hallucination detection)
  - [ ] Configure conditional edges for routing logic
  - [ ] Add human-in-the-loop escalation path
  
- [ ] **Memory Management**
  - [ ] Build LongTermMemory (vector DB wrapper)
  - [ ] Implement ShortTermMemory (Redis + summarization)
  - [ ] Create WorkingMemory (context assembly)
  - [ ] Develop conversation summarization with GPT-4o-mini
  - [ ] Add memory pruning strategies (token limits)
  
- [ ] **Pydantic AI Integration**
  - [ ] Define structured output models for agent responses
  - [ ] Implement validation for tool calls
  - [ ] Add dependency injection for DB connections

#### **Phase 4: API & Frontend (Week 7-8)**
- [ ] **Backend API (FastAPI)**
  - [ ] REST endpoints:
    - [ ] `POST /api/v1/chat/query` - Initiate conversation
    - [ ] `GET /api/v1/chat/history/{session_id}` - Retrieve history
    - [ ] `POST /api/v1/feedback` - User satisfaction
    - [ ] `GET /api/v1/health` - Readiness probe
  - [ ] WebSocket endpoint: `/api/v1/chat/stream`
  - [ ] Implement JWT authentication (singapore-ic + OTP)
  - [ ] Add rate limiting (100 req/min per user)
  - [ ] Set up CORS for frontend domain
  
- [ ] **Frontend (React + TypeScript)**
  - [ ] Component structure:
    - [ ] `<ChatContainer />` - Main layout
    - [ ] `<MessageList />` - Virtualized conversation
    - [ ] `<MessageBubble />` - User/assistant messages with citations
    - [ ] `<InputComposer />` - Multi-line text input
    - [ ] `<TypingIndicator />` - Animated thinking state
    - [ ] `<QuickActions />` - Suggested replies, escalation
  - [ ] WebSocket integration for streaming responses
  - [ ] IndexedDB for offline conversation caching
  - [ ] Implement optimistic UI updates
  - [ ] Add keyboard shortcuts (Ctrl+Enter to send)
  
- [ ] **Observability**
  - [ ] Integrate LangSmith for trace visualization
  - [ ] Add custom metrics to Prometheus:
    - [ ] Queries per second
    - [ ] Average retrieval latency
    - [ ] LLM token usage
    - [ ] User satisfaction scores
  - [ ] Set up Grafana dashboards

#### **Phase 5: Testing & Deployment (Week 9-10)**
- [ ] **Testing Suite**
  - [ ] Unit tests: >80% coverage (pytest-cov)
  - [ ] Integration tests: End-to-end conversation flows
  - [ ] Load testing: Locust for 100 concurrent users
  - [ ] Security testing:
    - [ ] PII detection & masking (presidio)
    - [ ] Prompt injection prevention
    - [ ] SQL injection prevention (parameterized queries)
  
- [ ] **Performance Optimization**
  - [ ] Query latency profiling (aim for P95 <3s)
  - [ ] Implement Redis caching for frequent queries
  - [ ] Optimize embedding batch sizes
  - [ ] Configure Qdrant HNSW parameters (ef=128, M=16)
  
- [ ] **Deployment**
  - [ ] Containerize all services (multi-stage Docker builds)
  - [ ] Set up CI/CD pipeline (GitHub Actions):
    - [ ] Automated testing on PR
    - [ ] Container scanning (Trivy)
    - [ ] Deploy to staging on merge
    - [ ] Deploy to AWS/GCP:
    - [ ] ECS/Cloud Run for stateless services
    - [ ] Managed Postgres (RDS/Cloud SQL)
    - [ ] Managed Redis (ElastiCache/Memorystore)
    - [ ] Qdrant Cloud or self-hosted on EC2/GCE
  - [ ] Configure monitoring alerts (PagerDuty)

---

## 6. RISK ASSESSMENT & MITIGATION

| Risk | Probability | Impact | Mitigation Strategy |
|------|-------------|--------|---------------------|
| **Hallucination in Responses** | High | Critical | 1. Quality check node in agent graph<br>2. Faithfulness metric (RAGAs) >0.9 threshold<br>3. Cite sources for every claim<br>4. Fallback to "I don't know" if confidence <0.7 |
| **Context Window Overflow** | Medium | High | 1. Aggressive summarization of old messages<br>2. Context compression via extractive method<br>3. Monitor token usage per request<br>4. Implement sliding window (10 turns max) |
| **Latency Exceeds 3s** | Medium | High | 1. Cache frequent queries (Redis)<br>2. Asynchronous retrieval (concurrent searches)<br>3. Use smaller reranker model<br>4. Implement request queuing with priority |
| **PII Leakage** | Low | Critical | 1. Presidio for PII detection/masking<br>2. PDPA compliance audit<br>3. Encrypt all data at rest & in transit<br>4. Regular security penetration testing |
| **Vector DB Scaling Issues** | Low | Medium | 1. Start with Qdrant Cloud (auto-scaling)<br>2. Partition by business unit if needed<br>3. Monitor query latency (P95, P99)<br>4. HNSW index optimization |

---

## 7. VALIDATION CHECKPOINT

### A. Design Correctness Review

**✅ Alignment with Research Document:**
- [x] Multi-stage retrieval (query transform → hybrid search → rerank)
- [x] Hierarchical memory (long-term, short-term, working)
- [x] Agentic workflow with LangGraph (stateful, cyclical)
- [x] Context engineering (compression, summarization)
- [x] Open-source stack (LangChain, Qdrant, RAGAs)

**✅ Singapore SMB Requirements:**
- [x] Cost-effective (self-hosted embedding model, GPT-4o-mini for cheap operations)
- [x] PDPA compliant (PII detection, encryption)
- [x] Multilingual ready (English/Singlish, extensible to Mandarin)
- [x] 24/7 availability (stateless design for high availability)

**✅ Production-Ready Criteria:**
- [x] Observability (LangSmith traces, Prometheus metrics)
- [x] Testing strategy (unit, integration, load, security)
- [x] Error handling (retry logic, human escalation)
- [x] Performance targets (latency, accuracy, scalability)

### B. Anti-Pattern Checks

**❌ Avoided Mistakes:**
- ❌ Single-stage naive RAG (would fail on complex queries)
- ❌ No memory management (conversations would lose context)
- ❌ Blocking synchronous calls (would cause timeouts)
- ❌ No evaluation metrics (would have no way to measure quality)
- ❌ Over-engineering (didn't add unnecessary complexity like knowledge graphs for SMB use case)

---

## 8. NEXT STEPS

### Immediate Actions:
1. **Review & Approve**: Validate this design aligns with your business constraints
2. **Clarify Unknowns**:
   - What is the typical size of the knowledge base? (# of documents, total tokens)
   - What LLM provider do you prefer? (OpenAI, Anthropic, local Llama?)
   - What is your hosting preference? (AWS, GCP, Azure, on-prem?)
   - Do you have existing customer data to bootstrap memory?

3. **Proceed to Implementation**: Upon approval, I'll begin with **Phase 1: Foundation** and deliver:
   - Working indexing pipeline
   - Qdrant collection populated with sample data
   - Baseline evaluation metrics

**Estimated Time to MVP**: 8 weeks
**Estimated Cost** (AWS, moderate usage):
- Compute: $200-400/month (ECS tasks)
- Storage: $50-100/month (RDS, S3)
- Vector DB: $100-200/month (Qdrant Cloud starter)
- LLM API: $300-600/month (OpenAI GPT-4o-mini at 10k queries/month)
**Total**: ~$650-1,300/month

---

https://claude.ai/share/4bcea268-8b30-4e54-9020-0e7e0048ae6c

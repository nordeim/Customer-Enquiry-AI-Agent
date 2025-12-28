"""
Chat Routes

Handles customer chat interactions with the AI agent.
"""

from datetime import datetime, timezone
from typing import Any
from uuid import UUID, uuid4

import structlog
from fastapi import APIRouter, HTTPException, Query, WebSocket, WebSocketDisconnect, status
from pydantic import BaseModel, Field

from app.dependencies import DbSessionDep, QdrantDep, RedisDep, SettingsDep

router = APIRouter()
logger = structlog.get_logger()


# ─────────────────────────────────────────────────────────────────────────────
# Request/Response Models
# ─────────────────────────────────────────────────────────────────────────────

class ChatMessage(BaseModel):
    """Individual chat message."""
    
    id: UUID = Field(default_factory=uuid4, description="Message unique identifier")
    role: str = Field(..., pattern="^(user|assistant|system)$", description="Message sender role")
    content: str = Field(..., min_length=1, max_length=10000, description="Message content")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: dict[str, Any] = Field(default_factory=dict, description="Additional message metadata")


class ChatRequest(BaseModel):
    """Chat request from client."""
    
    session_id: UUID | None = Field(default=None, description="Existing session ID or None for new")
    message: str = Field(..., min_length=1, max_length=5000, description="User message")
    customer_id: str | None = Field(default=None, description="Optional customer identifier")
    metadata: dict[str, Any] = Field(default_factory=dict, description="Request metadata")


class SourceCitation(BaseModel):
    """Source citation for response grounding."""
    
    source: str = Field(..., description="Source document name")
    chunk_id: str = Field(..., description="Chunk identifier")
    relevance_score: float = Field(..., ge=0, le=1, description="Relevance score")
    text_preview: str = Field(..., description="Preview of cited text")


class SuggestedAction(BaseModel):
    """Suggested follow-up action."""
    
    type: str = Field(..., description="Action type")
    label: str = Field(..., description="Display label")
    payload: dict[str, Any] = Field(default_factory=dict, description="Action payload")


class ChatResponse(BaseModel):
    """Chat response from agent."""
    
    session_id: UUID = Field(..., description="Session identifier")
    message_id: UUID = Field(default_factory=uuid4, description="Response message ID")
    content: str = Field(..., description="Response content")
    confidence: float = Field(..., ge=0, le=1, description="Response confidence score")
    sources: list[SourceCitation] = Field(default_factory=list, description="Source citations")
    suggested_actions: list[SuggestedAction] = Field(default_factory=list)
    requires_followup: bool = Field(default=False, description="Whether human follow-up needed")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    processing_time_ms: float = Field(..., description="Processing time in milliseconds")


class ConversationHistory(BaseModel):
    """Conversation history response."""
    
    session_id: UUID
    messages: list[ChatMessage]
    created_at: datetime
    last_activity: datetime
    message_count: int


# ─────────────────────────────────────────────────────────────────────────────
# REST Endpoints
# ─────────────────────────────────────────────────────────────────────────────

@router.post(
    "/chat",
    response_model=ChatResponse,
    summary="Send Chat Message",
    description="Send a message to the AI support agent and receive a response.",
    responses={
        200: {"description": "Successful response from agent"},
        429: {"description": "Rate limit exceeded"},
        500: {"description": "Internal server error"},
    },
)
async def send_message(
    request: ChatRequest,
    settings: SettingsDep,
    db: DbSessionDep,
    redis: RedisDep,
    qdrant: QdrantDep,
) -> ChatResponse:
    """
    Process a chat message through the AI agent.
    
    This endpoint:
    1. Creates or retrieves a session
    2. Loads conversation history from memory
    3. Processes the message through the RAG pipeline
    4. Generates a response using the AI agent
    5. Stores the conversation in memory
    
    Args:
        request: Chat request containing the user message.
        settings: Application settings.
        db: Database session.
        redis: Redis client for short-term memory.
        qdrant: Qdrant client for vector search.
    
    Returns:
        ChatResponse: AI agent response with sources and metadata.
    """
    import time
    
    start_time = time.perf_counter()
    
    # Generate or use provided session ID
    session_id = request.session_id or uuid4()
    
    logger.info(
        "Processing chat message",
        session_id=str(session_id),
        message_length=len(request.message),
        has_customer_id=request.customer_id is not None,
    )
    
    # TODO: Implement full agent processing in Phase 5
    # For now, return a placeholder response
    
    processing_time = (time.perf_counter() - start_time) * 1000
    
    # Placeholder response (will be replaced with actual agent logic)
    return ChatResponse(
        session_id=session_id,
        content=(
            f"Thank you for your message. I'm {settings.business_name}'s AI assistant. "
            "This is a placeholder response - the full agent implementation is coming in Phase 5. "
            f"You said: '{request.message[:100]}...'" if len(request.message) > 100 
            else f"You said: '{request.message}'"
        ),
        confidence=0.95,
        sources=[],
        suggested_actions=[
            SuggestedAction(
                type="quick_reply",
                label="Tell me more about your services",
                payload={"message": "Tell me more about your services"},
            ),
            SuggestedAction(
                type="quick_reply",
                label="What are your business hours?",
                payload={"message": "What are your business hours?"},
            ),
        ],
        requires_followup=False,
        processing_time_ms=round(processing_time, 2),
    )


@router.get(
    "/chat/history/{session_id}",
    response_model=ConversationHistory,
    summary="Get Conversation History",
    description="Retrieve the conversation history for a session.",
    responses={
        200: {"description": "Conversation history"},
        404: {"description": "Session not found"},
    },
)
async def get_conversation_history(
    session_id: UUID,
    redis: RedisDep,
    limit: int = Query(default=50, ge=1, le=100, description="Maximum messages to return"),
) -> ConversationHistory:
    """
    Retrieve conversation history for a session.
    
    Args:
        session_id: Session identifier.
        redis: Redis client.
        limit: Maximum number of messages to return.
    
    Returns:
        ConversationHistory: Session conversation history.
    """
    # TODO: Implement in Phase 4 with memory system
    
    logger.info("Retrieving conversation history", session_id=str(session_id))
    
    # Placeholder - will be replaced with actual memory retrieval
    return ConversationHistory(
        session_id=session_id,
        messages=[],
        created_at=datetime.now(timezone.utc),
        last_activity=datetime.now(timezone.utc),
        message_count=0,
    )


# ─────────────────────────────────────────────────────────────────────────────
# WebSocket Endpoint
# ─────────────────────────────────────────────────────────────────────────────

class ConnectionManager:
    """Manages WebSocket connections."""
    
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}
    
    async def connect(self, websocket: WebSocket, session_id: str) -> None:
        """Accept and register a new connection."""
        await websocket.accept()
        self.active_connections[session_id] = websocket
        logger.info("WebSocket connected", session_id=session_id)
    
    def disconnect(self, session_id: str) -> None:
        """Remove a connection."""
        if session_id in self.active_connections:
            del self.active_connections[session_id]
            logger.info("WebSocket disconnected", session_id=session_id)
    
    async def send_message(self, session_id: str, message: dict[str, Any]) -> None:
        """Send a message to a specific connection."""
        if session_id in self.active_connections:
            await self.active_connections[session_id].send_json(message)


manager = ConnectionManager()


@router.websocket("/ws/chat/{session_id}")
async def websocket_chat(
    websocket: WebSocket,
    session_id: str,
) -> None:
    """
    WebSocket endpoint for real-time chat.
    
    Enables streaming responses and real-time updates.
    
    Protocol:
    - Client sends: {"type": "message", "content": "..."}
    - Server sends: {"type": "chunk", "content": "..."} for streaming
    - Server sends: {"type": "complete", "response": {...}} when done
    - Server sends: {"type": "error", "error": "..."} on error
    """
    await manager.connect(websocket, session_id)
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_json()
            
            logger.info(
                "WebSocket message received",
                session_id=session_id,
                message_type=data.get("type"),
            )
            
            if data.get("type") == "message":
                content = data.get("content", "")
                
                # TODO: Implement streaming response in Phase 5
                # For now, send a simple response
                
                await manager.send_message(session_id, {
                    "type": "chunk",
                    "content": "Thank you for your message. ",
                })
                
                await manager.send_message(session_id, {
                    "type": "chunk",
                    "content": "I'm processing your request...",
                })
                
                await manager.send_message(session_id, {
                    "type": "complete",
                    "response": {
                        "content": f"This is a placeholder response to: {content}",
                        "confidence": 0.95,
                        "sources": [],
                    },
                })
            
            elif data.get("type") == "ping":
                await manager.send_message(session_id, {"type": "pong"})
    
    except WebSocketDisconnect:
        manager.disconnect(session_id)
    except Exception as e:
        logger.error("WebSocket error", session_id=session_id, error=str(e))
        await manager.send_message(session_id, {
            "type": "error",
            "error": "An error occurred processing your request.",
        })
        manager.disconnect(session_id)

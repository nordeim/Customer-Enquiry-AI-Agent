"""
Chat API Endpoints

Handles customer chat interactions with the AI support agent.
Supports both REST and WebSocket communication.
"""

from datetime import datetime, timezone
from typing import Annotated
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect, status
from pydantic import BaseModel, Field

from app.config import settings
from app.dependencies import SessionDep, RedisDep, ApiKeyDep
from app.logging_config import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/chat")


# =============================================================================
# REQUEST/RESPONSE MODELS
# =============================================================================

class ChatMessage(BaseModel):
    """A single chat message."""
    role: str = Field(..., description="Message role: 'user' or 'assistant'")
    content: str = Field(..., description="Message content")
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class ChatRequest(BaseModel):
    """Chat request from client."""
    message: str = Field(..., min_length=1, max_length=4000, description="User message")
    session_id: str | None = Field(default=None, description="Session ID for conversation continuity")
    customer_id: str | None = Field(default=None, description="Optional customer identifier")
    metadata: dict | None = Field(default=None, description="Additional metadata")
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "What are your business hours?",
                "session_id": "sess_abc123",
                "customer_id": "cust_xyz789",
            }
        }


class SourceCitation(BaseModel):
    """Citation from knowledge base."""
    source: str = Field(..., description="Source document identifier")
    content: str = Field(..., description="Relevant excerpt")
    relevance_score: float = Field(..., ge=0.0, le=1.0, description="Relevance score")


class ChatResponse(BaseModel):
    """Chat response to client."""
    session_id: str = Field(..., description="Session ID for conversation continuity")
    message: str = Field(..., description="Agent response message")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Response confidence score")
    sources: list[SourceCitation] = Field(default_factory=list, description="Knowledge base sources")
    suggested_actions: list[str] = Field(default_factory=list, description="Suggested follow-up actions")
    requires_escalation: bool = Field(default=False, description="Whether human escalation is needed")
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    
    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "sess_abc123",
                "message": "Our business hours are Monday to Friday, 9 AM to 6 PM Singapore Time.",
                "confidence": 0.95,
                "sources": [
                    {
                        "source": "faq_business_hours",
                        "content": "We operate from 9 AM to 6 PM SGT, Monday through Friday.",
                        "relevance_score": 0.92,
                    }
                ],
                "suggested_actions": ["View location", "Contact us"],
                "requires_escalation": False,
            }
        }


class ConversationHistory(BaseModel):
    """Conversation history response."""
    session_id: str
    messages: list[ChatMessage]
    created_at: str
    updated_at: str


# =============================================================================
# ENDPOINTS
# =============================================================================

@router.post(
    "",
    response_model=ChatResponse,
    summary="Send Chat Message",
    description="Send a message to the AI support agent and receive a response",
)
async def send_message(
    request: ChatRequest,
    session: SessionDep,
    redis: RedisDep,
    api_key: ApiKeyDep,
) -> ChatResponse:
    """
    Process a chat message and return AI response.
    
    This endpoint:
    1. Loads or creates a session
    2. Retrieves relevant context from knowledge base
    3. Generates a response using the AI agent
    4. Stores the conversation in memory
    """
    # Generate session ID if not provided
    session_id = request.session_id or f"sess_{uuid4().hex[:12]}"
    
    logger.info(
        "chat_message_received",
        session_id=session_id,
        message_length=len(request.message),
        customer_id=request.customer_id,
    )
    
    # TODO: Implement full agent pipeline in Phase 5
    # For now, return a placeholder response
    
    response = ChatResponse(
        session_id=session_id,
        message=f"Thank you for your message. Our AI agent is being set up and will be fully operational soon. You asked: '{request.message[:100]}...'",
        confidence=0.0,
        sources=[],
        suggested_actions=["Contact support for immediate assistance"],
        requires_escalation=True,
    )
    
    logger.info(
        "chat_response_sent",
        session_id=session_id,
        confidence=response.confidence,
        requires_escalation=response.requires_escalation,
    )
    
    return response


@router.get(
    "/history/{session_id}",
    response_model=ConversationHistory,
    summary="Get Conversation History",
    description="Retrieve the conversation history for a session",
)
async def get_conversation_history(
    session_id: str,
    redis: RedisDep,
    api_key: ApiKeyDep,
) -> ConversationHistory:
    """
    Retrieve conversation history for a session.
    
    Returns all messages exchanged in the specified session.
    """
    # TODO: Implement memory retrieval in Phase 4
    
    # For now, return empty history
    return ConversationHistory(
        session_id=session_id,
        messages=[],
        created_at=datetime.now(timezone.utc).isoformat(),
        updated_at=datetime.now(timezone.utc).isoformat(),
    )


@router.delete(
    "/history/{session_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Conversation History",
    description="Delete conversation history for PDPA compliance",
)
async def delete_conversation_history(
    session_id: str,
    redis: RedisDep,
    api_key: ApiKeyDep,
) -> None:
    """
    Delete conversation history.
    
    Supports PDPA right to erasure requirements.
    """
    # TODO: Implement in Phase 4
    logger.info("conversation_history_deleted", session_id=session_id)


# =============================================================================
# WEBSOCKET ENDPOINT
# =============================================================================

@router.websocket("/ws/{session_id}")
async def websocket_chat(
    websocket: WebSocket,
    session_id: str,
) -> None:
    """
    WebSocket endpoint for real-time chat.
    
    Enables streaming responses for better UX.
    """
    await websocket.accept()
    
    logger.info("websocket_connected", session_id=session_id)
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_json()
            message = data.get("message", "")
            
            logger.debug(
                "websocket_message_received",
                session_id=session_id,
                message_length=len(message),
            )
            
            # TODO: Implement streaming response in Phase 6
            # For now, send placeholder response
            
            await websocket.send_json({
                "type": "response",
                "session_id": session_id,
                "message": f"Received: {message}",
                "confidence": 0.0,
                "done": True,
            })
            
    except WebSocketDisconnect:
        logger.info("websocket_disconnected", session_id=session_id)
    except Exception as e:
        logger.error("websocket_error", session_id=session_id, error=str(e))
        await websocket.close(code=1011, reason=str(e))

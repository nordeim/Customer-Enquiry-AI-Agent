"""
Pydantic Schemas for API Request/Response Validation
═══════════════════════════════════════════════════════════════════════════════════

Defines all data transfer objects (DTOs) for the API layer.
These schemas ensure type safety and validation at API boundaries.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


# ═══════════════════════════════════════════════════════════════════════════════
# ENUMS
# ═══════════════════════════════════════════════════════════════════════════════


class MessageRole(str, Enum):
    """Message sender role."""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class ConversationStatus(str, Enum):
    """Conversation lifecycle status."""
    ACTIVE = "active"
    RESOLVED = "resolved"
    ESCALATED = "escalated"
    EXPIRED = "expired"


class FeedbackType(str, Enum):
    """Type of feedback provided."""
    THUMBS = "thumbs"
    RATING = "rating"
    DETAILED = "detailed"


# ═══════════════════════════════════════════════════════════════════════════════
# BASE SCHEMAS
# ═══════════════════════════════════════════════════════════════════════════════


class BaseSchema(BaseModel):
    """Base schema with common configuration."""
    
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        str_strip_whitespace=True,
    )


class TimestampMixin(BaseModel):
    """Mixin for timestamp fields."""
    
    created_at: datetime
    updated_at: Optional[datetime] = None


# ═══════════════════════════════════════════════════════════════════════════════
# CHAT SCHEMAS
# ═══════════════════════════════════════════════════════════════════════════════


class ChatMessageRequest(BaseSchema):
    """
    Incoming chat message from user.
    
    Attributes:
        message: The user's message content
        session_id: Client-generated session identifier
        customer_id: Optional customer identifier for personalization
        metadata: Optional additional context
    """
    
    message: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="User message content",
        examples=["What are your business hours?"],
    )
    session_id: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Unique session identifier",
        examples=["sess_abc123"],
    )
    customer_id: Optional[str] = Field(
        default=None,
        max_length=255,
        description="Optional customer identifier",
    )
    language: Optional[str] = Field(
        default=None,
        max_length=10,
        description="Preferred response language (ISO 639-1)",
        examples=["en", "zh"],
    )
    metadata: Optional[dict[str, Any]] = Field(
        default=None,
        description="Additional context metadata",
    )
    
    @field_validator("message")
    @classmethod
    def validate_message_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Message cannot be empty or whitespace only")
        return v.strip()


class SourceCitation(BaseSchema):
    """
    Citation for a source used in generating the response.
    """
    
    source_id: str = Field(..., description="Unique identifier for the source")
    title: Optional[str] = Field(default=None, description="Source document title")
    category: Optional[str] = Field(default=None, description="Source category")
    relevance_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Relevance score from retrieval",
    )
    snippet: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Relevant text snippet from source",
    )


class SuggestedAction(BaseSchema):
    """
    Suggested follow-up action for the user.
    """
    
    action_type: str = Field(
        ...,
        description="Type of action: link, button, form",
        examples=["link", "button", "quick_reply"],
    )
    label: str = Field(..., description="Display label for the action")
    value: str = Field(..., description="Action value (URL, intent, etc.)")
    metadata: Optional[dict[str, Any]] = Field(default=None)


class ChatMessageResponse(BaseSchema):
    """
    Response from the AI agent.
    
    Comprehensive response including the message, confidence metrics,
    sources used, and suggested follow-up actions.
    """
    
    message_id: UUID = Field(..., description="Unique message identifier")
    session_id: str = Field(..., description="Session identifier")
    
    # Response Content
    content: str = Field(..., description="AI response content")
    
    # Confidence & Quality
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Agent confidence in the response",
    )
    
    # Sources (if RAG was used)
    sources: list[SourceCitation] = Field(
        default_factory=list,
        description="Sources used to generate response",
    )
    
    # Follow-up Suggestions
    suggested_actions: list[SuggestedAction] = Field(
        default_factory=list,
        description="Suggested follow-up actions",
    )
    quick_replies: list[str] = Field(
        default_factory=list,
        max_length=5,
        description="Quick reply suggestions",
    )
    
    # Status Flags
    requires_followup: bool = Field(
        default=False,
        description="Whether user follow-up is expected",
    )
    escalated: bool = Field(
        default=False,
        description="Whether conversation was escalated to human",
    )
    
    # Metadata
    detected_language: str = Field(
        default="en",
        description="Detected language of user message",
    )
    detected_intent: Optional[str] = Field(
        default=None,
        description="Detected user intent",
    )
    processing_time_ms: int = Field(
        ...,
        ge=0,
        description="Response generation time in milliseconds",
    )
    
    # Timestamps
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Response timestamp (UTC)",
    )


class ConversationHistoryItem(BaseSchema):
    """Single message in conversation history."""
    
    message_id: UUID
    role: MessageRole
    content: str
    timestamp: datetime
    confidence: Optional[float] = None
    sources: Optional[list[SourceCitation]] = None


class ConversationHistory(BaseSchema):
    """Complete conversation history response."""
    
    session_id: str
    status: ConversationStatus
    messages: list[ConversationHistoryItem]
    message_count: int
    started_at: datetime
    last_activity_at: datetime
    detected_language: str = "en"
    topic: Optional[str] = None


# ═══════════════════════════════════════════════════════════════════════════════
# FEEDBACK SCHEMAS
# ═══════════════════════════════════════════════════════════════════════════════


class FeedbackRequest(BaseSchema):
    """
    User feedback submission.
    """
    
    session_id: str = Field(..., description="Session identifier")
    message_id: Optional[UUID] = Field(
        default=None,
        description="Specific message ID if feedback is for a single message",
    )
    feedback_type: FeedbackType = Field(
        default=FeedbackType.THUMBS,
        description="Type of feedback",
    )
    rating: int = Field(
        ...,
        ge=-1,
        le=5,
        description="Rating value: -1/1 for thumbs, 1-5 for rating",
    )
    comment: Optional[str] = Field(
        default=None,
        max_length=2000,
        description="Optional feedback comment",
    )
    categories: Optional[list[str]] = Field(
        default=None,
        description="Feedback categories",
        examples=[["accuracy", "helpfulness", "clarity"]],
    )


class FeedbackResponse(BaseSchema):
    """Feedback submission confirmation."""
    
    feedback_id: UUID
    message: str = "Thank you for your feedback!"
    received_at: datetime = Field(default_factory=datetime.utcnow)


# ═══════════════════════════════════════════════════════════════════════════════
# KNOWLEDGE BASE SCHEMAS
# ═══════════════════════════════════════════════════════════════════════════════


class KnowledgeSearchRequest(BaseSchema):
    """Search request for knowledge base."""
    
    query: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="Search query",
    )
    top_k: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Number of results to return",
    )
    category: Optional[str] = Field(
        default=None,
        description="Filter by category",
    )
    min_score: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="Minimum relevance score",
    )


class KnowledgeSearchResult(BaseSchema):
    """Single search result from knowledge base."""
    
    chunk_id: str
    content: str
    score: float
    source: str
    category: Optional[str] = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class KnowledgeSearchResponse(BaseSchema):
    """Knowledge base search response."""
    
    query: str
    results: list[KnowledgeSearchResult]
    total_results: int
    search_time_ms: int


class DocumentUploadRequest(BaseSchema):
    """Request to upload a document to knowledge base."""
    
    source_type: str = Field(
        ...,
        description="Document type: faq, product, policy, website",
        examples=["faq", "product", "policy"],
    )
    metadata: Optional[dict[str, Any]] = Field(
        default=None,
        description="Additional document metadata",
    )


class DocumentUploadResponse(BaseSchema):
    """Document upload confirmation."""
    
    document_id: UUID
    filename: str
    status: str
    chunk_count: int
    message: str


# ═══════════════════════════════════════════════════════════════════════════════
# HEALTH CHECK SCHEMAS
# ═══════════════════════════════════════════════════════════════════════════════


class HealthStatus(str, Enum):
    """Health check status values."""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"


class ComponentHealth(BaseSchema):
    """Individual component health status."""
    
    name: str
    status: HealthStatus
    latency_ms: Optional[float] = None
    message: Optional[str] = None


class HealthCheckResponse(BaseSchema):
    """Complete health check response."""
    
    status: HealthStatus
    version: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    components: list[ComponentHealth] = Field(default_factory=list)


# ═══════════════════════════════════════════════════════════════════════════════
# WEBSOCKET SCHEMAS
# ═══════════════════════════════════════════════════════════════════════════════


class WebSocketMessageType(str, Enum):
    """WebSocket message types."""
    CHAT = "chat"
    TYPING = "typing"
    PING = "ping"
    PONG = "pong"
    ERROR = "error"
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"


class WebSocketMessage(BaseSchema):
    """WebSocket message envelope."""
    
    type: WebSocketMessageType
    payload: dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class StreamingChunk(BaseSchema):
    """Streaming response chunk for real-time output."""
    
    chunk_index: int
    content: str
    is_final: bool = False
    message_id: Optional[UUID] = None

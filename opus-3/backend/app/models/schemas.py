"""
Pydantic Schemas

API request/response schemas and validation models.
"""

from datetime import datetime
from enum import Enum
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


# ─────────────────────────────────────────────────────────────────────────────
# Enums
# ─────────────────────────────────────────────────────────────────────────────

class MessageRole(str, Enum):
    """Chat message roles."""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class DocumentSource(str, Enum):
    """Knowledge base document sources."""
    FAQ = "faq"
    PRODUCT = "product"
    POLICY = "policy"
    WEBSITE = "website"
    TICKET = "ticket"


class ConsentStatus(str, Enum):
    """PDPA consent status."""
    PENDING = "pending"
    GRANTED = "granted"
    DENIED = "denied"
    WITHDRAWN = "withdrawn"


class EscalationReason(str, Enum):
    """Reasons for escalating to human support."""
    LOW_CONFIDENCE = "low_confidence"
    NEGATIVE_SENTIMENT = "negative_sentiment"
    EXPLICIT_REQUEST = "explicit_request"
    SENSITIVE_TOPIC = "sensitive_topic"
    REPEATED_FAILURE = "repeated_failure"


# ─────────────────────────────────────────────────────────────────────────────
# Base Schemas
# ─────────────────────────────────────────────────────────────────────────────

class TimestampMixin(BaseModel):
    """Mixin for created/updated timestamps."""
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class UUIDMixin(BaseModel):
    """Mixin for UUID primary key."""
    id: UUID = Field(default_factory=uuid4)


# ─────────────────────────────────────────────────────────────────────────────
# Customer Schemas
# ─────────────────────────────────────────────────────────────────────────────

class CustomerBase(BaseModel):
    """Base customer schema."""
    email: str | None = None
    name: str | None = None
    phone: str | None = None
    company: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class CustomerCreate(CustomerBase):
    """Schema for creating a customer."""
    external_id: str | None = Field(None, description="External system customer ID")
    consent_status: ConsentStatus = ConsentStatus.PENDING


class CustomerRead(CustomerBase, UUIDMixin, TimestampMixin):
    """Schema for reading customer data."""
    external_id: str | None = None
    consent_status: ConsentStatus
    total_conversations: int = 0
    last_interaction: datetime | None = None


# ─────────────────────────────────────────────────────────────────────────────
# Conversation Schemas
# ─────────────────────────────────────────────────────────────────────────────

class ConversationSummary(BaseModel):
    """Summarized conversation for long-term storage."""
    session_id: UUID
    customer_id: UUID | None = None
    summary: str
    key_topics: list[str] = Field(default_factory=list)
    sentiment: str | None = None
    resolution_status: str | None = None
    message_count: int = 0


# ─────────────────────────────────────────────────────────────────────────────
# Agent Schemas
# ─────────────────────────────────────────────────────────────────────────────

class AgentContext(BaseModel):
    """Context provided to the agent for processing."""
    session_id: UUID
    customer_id: UUID | None = None
    customer_info: CustomerRead | None = None
    conversation_history: list[dict[str, Any]] = Field(default_factory=list)
    conversation_summary: str | None = None
    retrieved_context: list[dict[str, Any]] = Field(default_factory=list)
    business_context: dict[str, Any] = Field(default_factory=dict)


class AgentResponse(BaseModel):
    """Structured response from the agent."""
    content: str
    confidence: float = Field(ge=0, le=1)
    sources: list[dict[str, Any]] = Field(default_factory=list)
    suggested_actions: list[dict[str, Any]] = Field(default_factory=list)
    escalate: bool = False
    escalation_reason: EscalationReason | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


# ─────────────────────────────────────────────────────────────────────────────
# Feedback Schemas
# ─────────────────────────────────────────────────────────────────────────────

class FeedbackCreate(BaseModel):
    """Schema for creating feedback on a response."""
    session_id: UUID
    message_id: UUID
    rating: int = Field(ge=1, le=5, description="Rating from 1-5")
    feedback_type: str = Field(..., pattern="^(helpful|not_helpful|incorrect|other)$")
    comment: str | None = Field(None, 

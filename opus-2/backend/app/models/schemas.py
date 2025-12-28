"""
Pydantic Schemas for API

Request and response models for the API layer.
Separate from database models for flexibility.
"""

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field


# =============================================================================
# CHAT SCHEMAS
# =============================================================================

class ChatMessage(BaseModel):
    """A single chat message."""
    role: str = Field(..., description="Message role: 'user' or 'assistant'")
    content: str = Field(..., description="Message content")
    timestamp: Optional[str] = Field(default=None, description="ISO timestamp")


class SourceCitation(BaseModel):
    """Citation from knowledge base."""
    source: str = Field(..., description="Source document identifier")
    content: str = Field(..., description="Relevant excerpt")
    relevance_score: float = Field(..., ge=0.0, le=1.0)
    metadata: Optional[dict[str, Any]] = Field(default=None)


class ChatRequest(BaseModel):
    """Chat request from client."""
    message: str = Field(..., min_length=1, max_length=4000)
    session_id: Optional[str] = Field(default=None)
    customer_id: Optional[str] = Field(default=None)
    language: Optional[str] = Field(default="en")
    metadata: Optional[dict[str, Any]] = Field(default=None)


class ChatResponse(BaseModel):
    """Chat response to client."""
    session_id: str
    message: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    sources: list[SourceCitation] = Field(default_factory=list)
    suggested_actions: list[str] = Field(default_factory=list)
    requires_escalation: bool = Field(default=False)
    timestamp: str


# =============================================================================
# KNOWLEDGE BASE SCHEMAS
# =============================================================================

class DocumentMetadata(BaseModel):
    """Metadata for a knowledge base document."""
    source: str
    category: str
    language: str = "en"
    created_at: Optional[str] = None
    custom: Optional[dict[str, Any]] = None


class ChunkMetadata(BaseModel):
    """Metadata for a document chunk."""
    document_id: str
    chunk_index: int
    source: str
    category: str
    language: str
    created_at: str


class SearchResult(BaseModel):
    """A single search result."""
    id: str
    content: str
    score: float
    metadata: ChunkMetadata


# =============================================================================
# CUSTOMER SCHEMAS
# =============================================================================

class CustomerProfile(BaseModel):
    """Customer profile for context."""
    id: str
    name: Optional[str] = None
    email: Optional[str] = None
    language_preference: str = "en"
    previous_topics: list[str] = Field(default_factory=list)
    metadata: Optional[dict[str, Any]] = None


# =============================================================================
# TICKET SCHEMAS
# =============================================================================

class TicketCreate(BaseModel):
    """Request to create a support ticket."""
    subject: str = Field(..., max_length=500)
    description: str
    priority: str = "medium"
    customer_id: Optional[str] = None
    conversation_id: Optional[str] = None


class TicketResponse(BaseModel):
    """Response after ticket creation."""
    ticket_id: str
    ticket_number: str
    status: str
    created_at: str

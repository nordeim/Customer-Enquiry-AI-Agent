"""
SQLAlchemy Database Models
═══════════════════════════════════════════════════════════════════════════════════

Defines the relational database schema for long-term memory storage.
Follows PDPA compliance requirements with data retention tracking.

Tables:
- customers: Customer profiles and preferences
- conversations: Conversation sessions
- messages: Individual messages within conversations
- conversation_summaries: LLM-generated conversation summaries
- feedback: User feedback on responses
- support_tickets: Escalated support tickets
"""

from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID as PGUUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base class for all database models."""
    
    type_annotation_map = {
        dict: JSONB,
    }


class MessageRole(str, Enum):
    """Message sender role enumeration."""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class ConversationStatus(str, Enum):
    """Conversation lifecycle status."""
    ACTIVE = "active"
    RESOLVED = "resolved"
    ESCALATED = "escalated"
    EXPIRED = "expired"


class TicketStatus(str, Enum):
    """Support ticket status."""
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"


class TicketPriority(str, Enum):
    """Support ticket priority level."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class Customer(Base):
    """
    Customer Profile Model
    
    Stores customer information with PDPA-compliant data handling.
    Includes consent tracking and data retention management.
    """
    
    __tablename__ = "customers"
    
    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    
    # Customer Identification
    external_id: Mapped[Optional[str]] = mapped_column(
        String(255),
        unique=True,
        nullable=True,
        index=True,
        comment="External system customer ID",
    )
    email: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        index=True,
    )
    phone: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
    )
    name: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )
    
    # Preferences
    preferred_language: Mapped[str] = mapped_column(
        String(10),
        default="en",
        comment="ISO 639-1 language code",
    )
    timezone: Mapped[str] = mapped_column(
        String(50),
        default="Asia/Singapore",
    )
    
    # PDPA Compliance
    consent_given: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        comment="PDPA consent for data collection",
    )
    consent_date: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    data_retention_until: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        comment="Date until which data can be retained",
    )
    is_anonymized: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )
    
    # Metadata
    metadata: Mapped[dict] = mapped_column(
        JSONB,
        default=dict,
        comment="Additional customer metadata",
    )
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
    
    # Relationships
    conversations: Mapped[list["Conversation"]] = relationship(
        "Conversation",
        back_populates="customer",
        cascade="all, delete-orphan",
    )
    
    __table_args__ = (
        Index("idx_customer_email_active", "email", "is_anonymized"),
    )


class Conversation(Base):
    """
    Conversation Session Model
    
    Tracks conversation sessions between customers and the AI agent.
    Links to messages, summaries, and any escalation tickets.
    """
    
    __tablename__ = "conversations"
    
    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    
    # Foreign Keys
    customer_id: Mapped[Optional[UUID]] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("customers.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    
    # Session Identification
    session_id: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        comment="External session identifier (e.g., from frontend)",
    )
    
    # Status Tracking
    status: Mapped[ConversationStatus] = mapped_column(
        String(50),
        default=ConversationStatus.ACTIVE,
        index=True,
    )
    
    # Context Tracking
    topic: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
        comment="Detected conversation topic",
    )
    intent: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        comment="Primary user intent",
    )
    sentiment_score: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
        comment="Overall conversation sentiment (-1 to 1)",
    )
    
    # Language
    detected_language: Mapped[str] = mapped_column(
        String(10),
        default="en",
    )
    
    # Metrics
    message_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )
    resolution_time_seconds: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
    )
    
    # Metadata
    metadata: Mapped[dict] = mapped_column(
        JSONB,
        default=dict,
    )
    
    # Timestamps
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    last_activity_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
    ended_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    
    # Relationships
    customer: Mapped[Optional["Customer"]] = relationship(
        "Customer",
        back_populates="conversations",
    )
    messages: Mapped[list["Message"]] = relationship(
        "Message",
        back_populates="conversation",
        cascade="all, delete-orphan",
        order_by="Message.created_at",
    )
    summaries: Mapped[list["ConversationSummary"]] = relationship(
        "ConversationSummary",
        back_populates="conversation",
        cascade="all, delete-orphan",
        order_by="ConversationSummary.created_at.desc()",
    )
    feedback: Mapped[list["Feedback"]] = relationship(
        "Feedback",
        back_populates="conversation",
        cascade="all, delete-orphan",
    )
    tickets: Mapped[list["SupportTicket"]] = relationship(
        "SupportTicket",
        back_populates="conversation",
        cascade="all, delete-orphan",
    )
    
    __table_args__ = (
        Index("idx_conversation_status_activity", "status", "last_activity_at"),
    )


class Message(Base):
    """
    Individual Message Model
    
    Stores each message in a conversation with role, content,
    and associated metadata like sources and confidence scores.
    """
    
    __tablename__ = "messages"
    
    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    
    # Foreign Keys
    conversation_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("conversations.id", ondelete="CASCADE"),
        index=True,
    )
    
    # Message Content
    role: Mapped[MessageRole] = mapped_column(
        String(20),
        index=True,
    )
    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    
    # Assistant Response Metadata (only for assistant messages)
    confidence_score: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
        comment="Agent confidence in response (0-1)",
    )
    sources: Mapped[Optional[dict]] = mapped_column(
        JSONB,
        nullable=True,
        comment="RAG sources used for response",
    )
    tools_used: Mapped[Optional[list]] = mapped_column(
        JSONB,
        nullable=True,
        comment="Tools invoked during response generation",
    )
    
    # Token Usage (for cost tracking)
    prompt_tokens: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
    )
    completion_tokens: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
    )
    
    # Processing Metadata
    processing_time_ms: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
    )
    model_used: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
    )
    
    # Metadata
    metadata: Mapped[dict] = mapped_column(
        JSONB,
        default=dict,
    )
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        index=True,
    )
    
    # Relationships
    conversation: Mapped["Conversation"] = relationship(
        "Conversation",
        back_populates="messages",
    )
    
    __table_args__ = (
        Index("idx_message_conversation_created", "conversation_id", "created_at"),
    )


class ConversationSummary(Base):
    """
    Conversation Summary Model
    
    Stores LLM-generated summaries of conversation segments.
    Used for context compression in long conversations.
    """
    
    __tablename__ = "conversation_summaries"
    
    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    
    # Foreign Keys
    conversation_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("conversations.id", ondelete="CASCADE"),
        index=True,
    )
    
    # Summary Content
    summary: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    
    # Coverage
    message_range_start: Mapped[int] = mapped_column(
        Integer,
        comment="First message index covered by this summary",
    )
    message_range_end: Mapped[int] = mapped_column(
        Integer,
        comment="Last message index covered by this summary",
    )
    
    # Key Information Extracted
    key_topics: Mapped[list] = mapped_column(
        JSONB,
        default=list,
    )
    action_items: Mapped[list] = mapped_column(
        JSONB,
        default=list,
    )
    
    # Token Count
    token_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    
    # Relationships
    conversation: Mapped["Conversation"] = relationship(
        "Conversation",
        back_populates="summaries",
    )


class Feedback(Base):
    """
    User Feedback Model
    
    Captures user feedback on AI responses for quality improvement.
    """
    
    __tablename__ = "feedback"
    
    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    
    # Foreign Keys
    conversation_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("conversations.id", ondelete="CASCADE"),
        index=True,
    )
    message_id: Mapped[Optional[UUID]] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("messages.id", ondelete="SET NULL"),
        nullable=True,
    )
    
    # Feedback Content
    rating: Mapped[int] = mapped_column(
        Integer,
        comment="Rating 1-5 or thumbs up (1) / down (-1)",
    )
    feedback_type: Mapped[str] = mapped_column(
        String(50),
        default="rating",
        comment="Type: rating, thumbs, detailed",
    )
    comment: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    
    # Categories
    categories: Mapped[list] = mapped_column(
        JSONB,
        default=list,
        comment="Feedback categories: accuracy, helpfulness, clarity, etc.",
    )
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    
    # Relationships
    conversation: Mapped["Conversation"] = relationship(
        "Conversation",
        back_populates="feedback",
    )


class SupportTicket(Base):
    """
    Support Ticket Model
    
    Created when conversations are escalated to human support.
    """
    
    __tablename__ = "support_tickets"
    
    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    
    # Foreign Keys
    conversation_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("conversations.id", ondelete="CASCADE"),
        index=True,
    )
    customer_id: Mapped[Optional[UUID]] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("customers.id", ondelete="SET NULL"),
        nullable=True,
    )
    
    # Ticket Details
    ticket_number: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True,
    )
    subject: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )
    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    
    # Status & Priority
    status: Mapped[TicketStatus] = mapped_column(
        String(50),
        default=TicketStatus.OPEN,
        index=True,
    )
    priority: Mapped[TicketPriority] = mapped_column(
        String(50),
        default=TicketPriority.MEDIUM,
    )
    
    # Escalation Reason
    escalation_reason: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Why the conversation was escalated",
    )
    
    # AI Summary
    ai_summary: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="AI-generated summary for support agent",
    )
    suggested_resolution: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    
    # Assignment
    assigned_to: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
    resolved_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    
    # Relationships
    conversation: Mapped["Conversation"] = relationship(
        "Conversation",
        back_populates="tickets",
    )


class KnowledgeDocument(Base):
    """
    Knowledge Document Tracking Model
    
    Tracks documents ingested into the knowledge base.
    Used for document management and update tracking.
    """
    
    __tablename__ = "knowledge_documents"
    
    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    
    # Document Identification
    filename: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )
    source_type: Mapped[str] = mapped_column(
        String(50),
        comment="Type: faq, product, policy, website, manual",
    )
    
    # Processing Status
    status: Mapped[str] = mapped_column(
        String(50),
        default="pending",
        comment="Status: pending, processing, completed, failed",
    )
    
    # Chunk Information
    chunk_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )
    vector_ids: Mapped[list] = mapped_column(
        JSONB,
        default=list,
        comment="List of vector IDs in Qdrant",
    )
    
    # Content Hash (for change detection)
    content_hash: Mapped[str] = mapped_column(
        String(64),
        comment="SHA-256 hash of document content",
    )
    
    # Metadata
    metadata: Mapped[dict] = mapped_column(
        JSONB,
        default=dict,
    )
    
    # Error Tracking
    error_message: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
    last_indexed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    
    __table_args__ = (
        Index("idx_knowledge_doc_status", "status", "source_type"),
    )

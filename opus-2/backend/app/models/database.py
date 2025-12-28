"""
SQLAlchemy Database Models

Defines the PostgreSQL schema for long-term persistent storage.
Follows PDPA compliance requirements for data retention.
"""

from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum as SQLEnum,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.domain import (
    ConsentStatus,
    DocumentCategory,
    Language,
    MessageRole,
    TicketPriority,
    TicketStatus,
)


def utc_now() -> datetime:
    """Get current UTC datetime."""
    return datetime.now(timezone.utc)


def generate_uuid() -> str:
    """Generate a new UUID string."""
    return str(uuid4())


class Customer(Base):
    """
    Customer profile for long-term storage.
    
    Stores customer information with PDPA compliance considerations.
    """
    __tablename__ = "customers"
    
    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        primary_key=True,
        default=generate_uuid,
    )
    external_id: Mapped[Optional[str]] = mapped_column(
        String(255),
        unique=True,
        nullable=True,
        index=True,
        comment="External customer ID from client system",
    )
    email: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        index=True,
    )
    name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    language_preference: Mapped[str] = mapped_column(
        SQLEnum(Language),
        default=Language.ENGLISH,
    )
    
    # PDPA Compliance
    consent_status: Mapped[str] = mapped_column(
        SQLEnum(ConsentStatus),
        default=ConsentStatus.PENDING,
    )
    consent_timestamp: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    data_retention_days: Mapped[int] = mapped_column(Integer, default=30)
    
    # Metadata
    metadata: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now,
    )
    
    # Relationships
    conversations: Mapped[list["Conversation"]] = relationship(
        "Conversation",
        back_populates="customer",
        cascade="all, delete-orphan",
    )
    tickets: Mapped[list["SupportTicket"]] = relationship(
        "SupportTicket",
        back_populates="customer",
        cascade="all, delete-orphan",
    )
    
    __table_args__ = (
        Index("ix_customers_consent", "consent_status"),
        Index("ix_customers_created", "created_at"),
    )


class Conversation(Base):
    """
    Conversation record for long-term storage.
    
    Stores conversation metadata and summaries.
    Individual messages are stored separately.
    """
    __tablename__ = "conversations"
    
    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        primary_key=True,
        default=generate_uuid,
    )
    session_id: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        comment="Session ID for linking with Redis short-term memory",
    )
    customer_id: Mapped[Optional[str]] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("customers.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    
    # Conversation metadata
    title: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
        comment="Auto-generated conversation title",
    )
    summary: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="Rolling summary of conversation",
    )
    message_count: Mapped[int] = mapped_column(Integer, default=0)
    
    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_escalated: Mapped[bool] = mapped_column(Boolean, default=False)
    escalation_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Analytics
    avg_confidence: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    topics: Mapped[Optional[list]] = mapped_column(JSONB, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now,
    )
    expires_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        comment="PDPA data retention expiry",
    )
    
    # Relationships
    customer: Mapped[Optional["Customer"]] = relationship(
        "Customer",
        back_populates="conversations",
    )
    messages: Mapped[list["ConversationMessage"]] = relationship(
        "ConversationMessage",
        back_populates="conversation",
        cascade="all, delete-orphan",
        order_by="ConversationMessage.created_at",
    )
    
    __table_args__ = (
        Index("ix_conversations_active", "is_active"),
        Index("ix_conversations_expires", "expires_at"),
    )


class ConversationMessage(Base):
    """
    Individual message in a conversation.
    
    Stored in PostgreSQL for long-term persistence.
    Redis is used for short-term session storage.
    """
    __tablename__ = "conversation_messages"
    
    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        primary_key=True,
        default=generate_uuid,
    )
    conversation_id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("conversations.id", ondelete="CASCADE"),
        index=True,
    )
    
    # Message content
    role: Mapped[str] = mapped_column(SQLEnum(MessageRole))
    content: Mapped[str] = mapped_column(Text)
    
    # AI response metadata (for assistant messages)
    confidence: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    sources: Mapped[Optional[list]] = mapped_column(JSONB, nullable=True)
    model_used: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    token_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        index=True,
    )
    
    # Relationships
    conversation: Mapped["Conversation"] = relationship(
        "Conversation",
        back_populates="messages",
    )
    
    __table_args__ = (
        Index("ix_messages_conversation_created", "conversation_id", "created_at"),
    )


class Document(Base):
    """
    Knowledge base document metadata.
    
    Stores document information; actual embeddings are in Qdrant.
    """
    __tablename__ = "documents"
    
    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        primary_key=True,
        default=generate_uuid,
    )
    
    # Document info
    filename: Mapped[str] = mapped_column(String(500))
    category: Mapped[str] = mapped_column(
        SQLEnum(DocumentCategory),
        index=True,
    )
    language: Mapped[str] = mapped_column(
        SQLEnum(Language),
        default=Language.ENGLISH,
        index=True,
    )
    
    # Processing status
    is_processed: Mapped[bool] = mapped_column(Boolean, default=False)
    chunk_count: Mapped[int] = mapped_column(Integer, default=0)
    processing_error: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Metadata
    file_size_bytes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    content_hash: Mapped[Optional[str]] = mapped_column(
        String(64),
        nullable=True,
        unique=True,
        comment="SHA-256 hash for deduplication",
    )
    metadata: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now,
    )
    
    __table_args__ = (
        Index("ix_documents_category_lang", "category", "language"),
        Index("ix_documents_processed", "is_processed"),
    )


class SupportTicket(Base):
    """
    Support ticket for escalated conversations.
    
    Created when AI agent escalates to human support.
    """
    __tablename__ = "support_tickets"
    
    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        primary_key=True,
        default=generate_uuid,
    )
    ticket_number: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True,
    )
    
    # Relationships
    customer_id: Mapped[Optional[str]] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("customers.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    conversation_id: Mapped[Optional[str]] = mapped_column(
        UUID(as_uuid=False),
        ForeignKey("conversations.id", ondelete="SET NULL"),
        nullable=True,
    )
    
    # Ticket details
    subject: Mapped[str] = mapped_column(String(500))
    description: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(
        SQLEnum(TicketStatus),
        default=TicketStatus.OPEN,
        index=True,
    )
    priority: Mapped[str] = mapped_column(
        SQLEnum(TicketPriority),
        default=TicketPriority.MEDIUM,
        index=True,
    )
    
    # Assignment
    assigned_to: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # Resolution
    resolution: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    resolved_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now,
    )
    
    # Relationships
    customer: Mapped[Optional["Customer"]] = relationship(
        "Customer",
        back_populates="tickets",
    )
    
    __table_args__ = (
        Index("ix_tickets_status_priority", "status", "priority"),
        Index("ix_tickets_created", "created_at"),
    )

"""
Domain Models
═══════════════════════════════════════════════════════════════════════════════════

Core business domain models used internally within the application.
These are distinct from API schemas and database models.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Optional
from uuid import UUID, uuid4


class Intent(str, Enum):
    """Detected user intent categories."""
    
    PRODUCT_INQUIRY = "product_inquiry"
    PRICING = "pricing"
    BUSINESS_HOURS = "business_hours"
    ORDER_STATUS = "order_status"
    COMPLAINT = "complaint"
    TECHNICAL_SUPPORT = "technical_support"
    GENERAL_INQUIRY = "general_inquiry"
    GREETING = "greeting"
    FAREWELL = "farewell"
    UNKNOWN = "unknown"


class Sentiment(str, Enum):
    """Sentiment classification."""
    
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"


@dataclass
class Document:
    """
    Represents a document chunk from the knowledge base.
    """
    
    id: str
    content: str
    metadata: dict[str, Any] = field(default_factory=dict)
    score: float = 0.0
    
    @property
    def source(self) -> str:
        return self.metadata.get("source", "unknown")
    
    @property
    def category(self) -> str:
        return self.metadata.get("category", "general")
    
    @property
    def language(self) -> str:
        return self.metadata.get("language", "en")


@dataclass
class RetrievalResult:
    """
    Result from the RAG retrieval pipeline.
    """
    
    documents: list[Document]
    query_used: str
    retrieval_time_ms: int
    reranking_applied: bool = False
    
    @property
    def top_document(self) -> Optional[Document]:
        return self.documents[0] if self.documents else None
    
    @property
    def average_score(self) -> float:
        if not self.documents:
            return 0.0
        return sum(d.score for d in self.documents) / len(self.documents)


@dataclass
class ConversationContext:
    """
    Current conversation context assembled for the agent.
    """
    
    session_id: str
    messages: list[dict[str, Any]]
    customer_info: Optional[dict[str, Any]] = None
    summary: Optional[str] = None
    retrieved_context: Optional[str] = None
    detected_intent: Intent = Intent.UNKNOWN
    detected_language: str = "en"
    sentiment: Sentiment = Sentiment.NEUTRAL
    
    @property
    def message_count(self) -> int:
        return len(self.messages)
    
    @property
    def last_user_message(self) -> Optional[str]:
        for msg in reversed(self.messages):
            if msg.get("role") == "user":
                return msg.get("content")
        return None


@dataclass
class AgentResponse:
    """
    Complete response from the AI agent.
    """
    
    content: str
    confidence: float
    sources: list[Document] = field(default_factory=list)
    tools_used: list[str] = field(default_factory=list)
    requires_escalation: bool = False
    escalation_reason: Optional[str] = None
    suggested_actions: list[dict[str, Any]] = field(default_factory=list)
    quick_replies: list[str] = field(default_factory=list)
    processing_time_ms: int = 0
    model_used: str = ""
    prompt_tokens: int = 0
    completion_tokens: int = 0
    
    @property
    def total_tokens(self) -> int:
        return self.prompt_tokens + self.completion_tokens


@dataclass
class EscalationRequest:
    """
    Request to escalate conversation to human support.
    """
    
    session_id: str
    reason: str
    priority: str = "medium"
    summary: str = ""
    customer_info: Optional[dict[str, Any]] = None
    conversation_history: list[dict[str, Any]] = field(default_factory=list)
    
    def to_ticket_data(self) -> dict[str, Any]:
        return {
            "ticket_number": f"TKT-{uuid4().hex[:8].upper()}",
            "subject": f"Escalated: {self.reason[:100]}",
            "description": self.summary,
            "priority": self.priority,
            "escalation_reason": self.reason,
            "ai_summary": self.summary,
        }


@dataclass
class BusinessHoursStatus:
    """
    Current business hours status.
    """
    
    is_open: bool
    current_time: datetime
    opens_at: Optional[datetime] = None
    closes_at: Optional[datetime] = None
    next_opening: Optional[datetime] = None
    timezone: str = "Asia/Singapore"
    
    @property
    def status_message(self) -> str:
        if self.is_open:
            return f"We're currently open until {self.closes_at.strftime('%I:%M %p') if self.closes_at else 'later today'}."
        elif self.next_opening:
            return f"We're currently closed. We'll be open again on {self.next_opening.strftime('%A at %I:%M %p')}."
        return "We're currently closed."


@dataclass
class CustomerProfile:
    """
    Customer profile for personalization.
    """
    
    id: UUID
    external_id: Optional[str] = None
    email: Optional[str] = None
    name: Optional[str] = None
    preferred_language: str = "en"
    timezone: str = "Asia/Singapore"
    metadata: dict[str, Any] = field(default_factory=dict)
    interaction_count: int = 0
    last_interaction: Optional[datetime] = None
    
    @property
    def display_name(self) -> str:
        return self.name or self.email or "Valued Customer"


@dataclass
class TokenBudget:
    """
    Token budget tracking for context management.
    """
    
    max_tokens: int = 4000
    system_prompt_tokens: int = 0
    conversation_tokens: int = 0
    retrieved_context_tokens: int = 0
    reserved_for_response: int = 1000
    
    @property
    def used_tokens(self) -> int:
        return (
            self.system_prompt_tokens
            + self.conversation_tokens
            + self.retrieved_context_tokens
        )
    
    @property
    def available_tokens(self) -> int:
        return max(0, self.max_tokens - self.used_tokens - self.reserved_for_response)
    
    @property
    def utilization(self) -> float:
        return self.used_tokens / self.max_tokens if self.max_tokens > 0 else 0.0
    
    def can_add(self, tokens: int) -> bool:
        return (self.used_tokens + tokens + self.reserved_for_response) <= self.max_tokens

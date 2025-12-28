"""
Domain Models and Enums

Core domain types used throughout the application.
"""

from enum import Enum


class MessageRole(str, Enum):
    """Chat message roles."""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class TicketStatus(str, Enum):
    """Support ticket statuses."""
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    WAITING_CUSTOMER = "waiting_customer"
    RESOLVED = "resolved"
    CLOSED = "closed"


class TicketPriority(str, Enum):
    """Support ticket priorities."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class DocumentCategory(str, Enum):
    """Knowledge base document categories."""
    FAQ = "faq"
    PRODUCT = "product"
    POLICY = "policy"
    PRICING = "pricing"
    SUPPORT = "support"
    GENERAL = "general"


class Language(str, Enum):
    """Supported languages."""
    ENGLISH = "en"
    CHINESE = "zh"
    MALAY = "ms"
    TAMIL = "ta"


class ConsentStatus(str, Enum):
    """PDPA consent status."""
    PENDING = "pending"
    GRANTED = "granted"
    REVOKED = "revoked"

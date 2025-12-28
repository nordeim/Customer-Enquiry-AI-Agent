"""
Knowledge Base Routes

Handles knowledge base management including document upload,
search, and administration.
"""

from datetime import datetime, timezone
from typing import Any
from uuid import UUID, uuid4

import structlog
from fastapi import APIRouter, File, HTTPException, Query, UploadFile, status
from pydantic import BaseModel, Field

from app.dependencies import QdrantDep, SettingsDep

router = APIRouter()
logger = structlog.get_logger()


# ─────────────────────────────────────────────────────────────────────────────
# Models
# ─────────────────────────────────────────────────────────────────────────────

class KnowledgeDocument(BaseModel):
    """Knowledge base document."""
    
    id: UUID = Field(default_factory=uuid4)
    title: str = Field(..., min_length=1, max_length=500)
    content: str = Field(..., min_length=1)
    source: str = Field(..., description="Document source (faq, product, policy, etc.)")
    category: str = Field(..., description="Document category")
    metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class DocumentUploadResponse(BaseModel):
    """Response after document upload."""
    
    document_id: UUID
    title: str
    chunks_created: int
    status: str
    message: str


class SearchQuery(BaseModel):
    """Search query for knowledge base."""
    
    query: str = Field(..., min_length=1, max_length=1000)
    top_k: int = Field(default=5, ge=1, le=20)
    filter_source: str | None = None
    filter_category: str | None = None
    min_score: float = Field(default=0.5, ge=0, le=1)


class SearchResult(BaseModel):
    """Individual search result."""
    
    chunk_id: str
    document_id: str
    content: str
    score: float
    metadata: dict[str, Any]


class SearchResponse(BaseModel):
    """Search response."""
    
    query: str
    results: list[SearchResult]
    total_results: int
    search_time_ms: float


class CollectionStats(BaseModel):
    """Knowledge base collection statistics."""
    
    collection_name: str
    total_documents: int
    total_chunks: int
    sources: dict[str, int]
    categories: dict[str, int]
    last_updated: datetime | None


# ─────────────────────────────────────────────────────────────────────────────
# Endpoints
# ─────────────────────────────────────────────────────────────────────────────

@router.post(
    "/knowledge/documents",
    response_model=DocumentUploadResponse,
    summary="Upload Document",
    description="Upload a document to the knowledge base.",
    responses={
        200: {"description": "Document uploaded successfully"},
        400: {"description": "Invalid document format"},
        413: {"description": "Document too large"},
    },
)
async def upload_document(
    file: UploadFile = File(...),
    source: str = Query(..., description="Document source type"),
    category: str = Query(..., description="Document category"),
    settings: SettingsDep = None,
    qdrant: QdrantDep = None,
) -> DocumentUploadResponse:
    """
    Upload a document to the knowledge base.
    
    Supported formats:
    - PDF
    - Markdown (.md)
    - Plain text (.txt)
    - HTML
    
    The document will be:
    1. Parsed and cleaned
    2. Chunked into semantic segments
    3. Embedded using the configured model
    4. Stored in the vector database
    
    Args:
        file: Document file to upload.
        source: Source type (faq, product, policy, website).
        category: Document category for filtering.
    
    Returns:
        DocumentUploadResponse: Upload result with document ID.
    """
    logger.info(
        "Document upload requested",
        filename=file.filename,
        content_type=file.content_type,
        source=source,
        category=category,
    )
    
    # Validate file type
    allowed_types = {
        "application/pdf",
        "text/plain",
        "text/markdown",
        "text/html",
        "application/json",
    }
    
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file type: {file.content_type}. Allowed: {allowed_types}",
        )
    
    # TODO: Implement full ingestion pipeline in Phase 2
    # For now, return a placeholder response
    
    document_id = uuid4()
    
    return DocumentUploadResponse(
        document_id=document_id,
        title=file.filename or "Untitled",
        chunks_created=0,  # Will be populated after actual processing
        status="queued",
        message="Document queued for processing. Full implementation in Phase 2.",
    )


@router.post(
    "/knowledge/search",
    response_model=SearchResponse,
    summary="Search Knowledge Base",
    description="Search the knowledge base using semantic search.",
)
async def search_knowledge(
    query: SearchQuery,
    qdrant: QdrantDep = None,
    settings: SettingsDep = None,
) -> SearchResponse:
    """
    Search the knowledge base.
    
    Uses hybrid search combining:
    - Semantic similarity (dense vectors)
    - Keyword matching (sparse vectors)
    
    Results are reranked for optimal relevance.
    
    Args:
        query: Search query with filters.
    
    Returns:
        SearchResponse: Search results with relevance scores.
    """
    import time
    
    start_time = time.perf_counter()
    
    logger.info(
        "Knowledge search requested",
        query=query.query[:100],
        top_k=query.top_k,
        filter_source=query.filter_source,
    )
    
    # TODO: Implement full search pipeline in Phase 3
    # For now, return placeholder response
    
    search_time = (time.perf_counter() - start_time) * 1000
    
    return SearchResponse(
        query=query.query,
        results=[],  # Will be populated by actual search
        total_results=0,
        search_time_ms=round(search_time, 2),
    )


@router.get(
    "/knowledge/stats",
    response_model=CollectionStats,
    summary="Get Collection Statistics",
    description="Get statistics about the knowledge base.",
)
async def get_collection_stats(
    qdrant: QdrantDep = None,
    settings: SettingsDep = None,
) -> CollectionStats:
    """
    Get knowledge base statistics.
    
    Returns counts of documents, chunks, and breakdowns by source/category.
    
    Returns:
        CollectionStats: Collection statistics.
    """
    logger.info("Collection stats requested")
    
    # TODO: Implement actual stats retrieval
    # For now, return placeholder
    
    return CollectionStats(
        collection_name=settings.qdrant_collection_name if settings else "knowledge_base",
        total_documents=0,
        total_chunks=0,
        sources={},
        categories={},
        last_updated=None,
    )


@router.delete(
    "/knowledge/documents/{document_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Document",
    description="Delete a document from the knowledge base.",
)
async def delete_document(
    document_id: UUID,
    qdrant: QdrantDep = None,
) -> None:
    """
    Delete a document and all its chunks from the knowledge base.
    
    Args:
        document_id: Document UUID to delete.
    """
    logger.info("Document deletion requested", document_id=str(document_id))
    
    # TODO: Implement deletion in Phase 2
    pass

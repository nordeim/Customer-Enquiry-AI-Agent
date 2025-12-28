"""
Knowledge Base API Endpoints

Handles knowledge base management including document upload,
search, and administration.
"""

from datetime import datetime, timezone
from typing import Annotated
from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile, status
from pydantic import BaseModel, Field

from app.config import settings
from app.dependencies import SessionDep, QdrantDep, ApiKeyDep
from app.logging_config import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/knowledge")


# =============================================================================
# REQUEST/RESPONSE MODELS
# =============================================================================

class DocumentMetadata(BaseModel):
    """Metadata for a knowledge base document."""
    source: str = Field(..., description="Source identifier")
    category: str = Field(..., description="Document category")
    language: str = Field(default="en", description="Document language code")
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class SearchResult(BaseModel):
    """A single search result from the knowledge base."""
    id: str = Field(..., description="Document chunk ID")
    content: str = Field(..., description="Document content")
    metadata: DocumentMetadata
    score: float = Field(..., ge=0.0, le=1.0, description="Relevance score")


class SearchRequest(BaseModel):
    """Search request for the knowledge base."""
    query: str = Field(..., min_length=1, max_length=1000, description="Search query")
    top_k: int = Field(default=5, ge=1, le=50, description="Number of results to return")
    category: str | None = Field(default=None, description="Filter by category")
    language: str | None = Field(default=None, description="Filter by language")


class SearchResponse(BaseModel):
    """Search response from the knowledge base."""
    query: str
    results: list[SearchResult]
    total_results: int
    search_time_ms: float


class UploadResponse(BaseModel):
    """Response after document upload."""
    document_id: str
    filename: str
    chunks_created: int
    status: str


class KnowledgeBaseStats(BaseModel):
    """Knowledge base statistics."""
    total_documents: int
    total_chunks: int
    categories: dict[str, int]
    languages: dict[str, int]
    last_updated: str


# =============================================================================
# ENDPOINTS
# =============================================================================

@router.post(
    "/search",
    response_model=SearchResponse,
    summary="Search Knowledge Base",
    description="Search the knowledge base using semantic similarity",
)
async def search_knowledge_base(
    request: SearchRequest,
    qdrant: QdrantDep,
    api_key: ApiKeyDep,
) -> SearchResponse:
    """
    Perform semantic search on the knowledge base.
    
    Uses hybrid search (dense + sparse vectors) with optional
    metadata filtering for category and language.
    """
    import time
    start_time = time.time()
    
    logger.info(
        "knowledge_search_started",
        query_length=len(request.query),
        top_k=request.top_k,
        category=request.category,
    )
    
    # TODO: Implement full RAG retrieval in Phase 3
    # For now, return empty results
    
    search_time_ms = (time.time() - start_time) * 1000
    
    response = SearchResponse(
        query=request.query,
        results=[],
        total_results=0,
        search_time_ms=search_time_ms,
    )
    
    logger.info(
        "knowledge_search_completed",
        total_results=response.total_results,
        search_time_ms=search_time_ms,
    )
    
    return response


@router.post(
    "/upload",
    response_model=UploadResponse,
    summary="Upload Document",
    description="Upload a document to the knowledge base",
)
async def upload_document(
    file: Annotated[UploadFile, File(description="Document file (PDF, DOCX, TXT, MD)")],
    category: Annotated[str, Query(description="Document category")],
    language: Annotated[str, Query(default="en", description="Document language")],
    session: SessionDep,
    qdrant: QdrantDep,
    api_key: ApiKeyDep,
) -> UploadResponse:
    """
    Upload and process a document into the knowledge base.
    
    Supports:
    - PDF files
    - Word documents (.docx)
    - Text files (.txt)
    - Markdown files (.md)
    
    The document will be parsed, chunked, and embedded.
    """
    # Validate file type
    allowed_extensions = {".pdf", ".docx", ".txt", ".md"}
    file_ext = "." + (file.filename or "").split(".")[-1].lower()
    
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type not supported. Allowed types: {allowed_extensions}",
        )
    
    document_id = f"doc_{uuid4().hex[:12]}"
    
    logger.info(
        "document_upload_started",
        document_id=document_id,
        filename=file.filename,
        category=category,
    )
    
    # TODO: Implement document processing in Phase 2
    # For now, return placeholder response
    
    response = UploadResponse(
        document_id=document_id,
        filename=file.filename or "unknown",
        chunks_created=0,
        status="pending",
    )
    
    logger.info(
        "document_upload_completed",
        document_id=document_id,
        chunks_created=response.chunks_created,
    )
    
    return response


@router.get(
    "/stats",
    response_model=KnowledgeBaseStats,
    summary="Get Knowledge Base Statistics",
    description="Get statistics about the knowledge base",
)
async def get_knowledge_base_stats(
    qdrant: QdrantDep,
    api_key: ApiKeyDep,
) -> KnowledgeBaseStats:
    """
    Retrieve statistics about the knowledge base.
    
    Includes document counts, category breakdown,
    and language distribution.
    """
    # TODO: Implement proper stats retrieval
    
    return KnowledgeBaseStats(
        total_documents=0,
        total_chunks=0,
        categories={},
        languages={},
        last_updated=datetime.now(timezone.utc).isoformat(),
    )


@router.delete(
    "/document/{document_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Document",
    description="Delete a document from the knowledge base",
)
async def delete_document(
    document_id: str,
    session: SessionDep,
    qdrant: QdrantDep,
    api_key: ApiKeyDep,
) -> None:
    """
    Delete a document and all its chunks from the knowledge base.
    """
    logger.info("document_delete_started", document_id=document_id)
    
    # TODO: Implement document deletion in Phase 2
    
    logger.info("document_deleted", document_id=document_id)

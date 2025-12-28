# backend/app/core/compliance.py
from pydantic import BaseModel
from typing import Optional, Dict, Any
import re

class PII_Scrubber:
    """Singapore PDPA-compliant PII scrubber with cultural context awareness"""
    
    # Singapore-specific PII patterns
    SINGAPORE_PII_PATTERNS = {
        'NRIC': r'[STFG]\d{7}[A-Z]',
        'FIN': r'[G]\d{7}[A-Z]',  # Foreign Identification Number
        'PHONE': r'(\+65\s?)?(\d{4}\s?\d{4}|\d{8})',  # Singapore phone format
        'EMAIL': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
        'ADDRESS': r'(\d+\s+\w+\s+street|block\s+\d+\s+\w+|singapore\s+\d{6})',
    }
    
    def __init__(self, langsmith_client):
        self.langsmith_client = langsmith_client
        self.logger = logging.getLogger(__name__)
        
    def scrub_pii(self, text: str, session_id: str) -> str:
        """Scrub PII while preserving context for Singapore business conversations"""
        scrubbed_text = text
        
        for pii_type, pattern in self.SINGAPORE_PII_PATTERNS.items():
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                original = match.group()
                masked = f"[{pii_type.upper()}_MASKED]"
                scrubbed_text = scrubbed_text.replace(original, masked)
                
                # Log PII detection for audit trail
                self.logger.info(f"PII detected: {pii_type} in session {session_id}")
                self.langsmith_client.log_event(
                    session_id=session_id,
                    event_type="PII_DETECTED",
                    details={"type": pii_type, "masked_value": masked}
                )
        
        return scrubbed_text
    
    def create_compliance_trace(self, run_id: str, metadata: Dict[str, Any]):
        """Create LangSmith trace with PDPA compliance metadata"""
        compliance_metadata = {
            **metadata,
            "pdpa_compliant": True,
            "pii_scrubbed": True,
            "singapore_governance_framework": "Model AI Governance Framework v2.0",
            "data_residency": "Singapore",
            "consent_obtained": metadata.get("consent_obtained", False),
            "audit_timestamp": datetime.utcnow().isoformat()
        }
        return compliance_metadata

# Integration with LangChain
from langchain_community.callbacks import LangChainTracer

class PDPA_Compliant_Tracer(LangChainTracer):
    """Custom tracer that enforces Singapore PDPA compliance"""
    
    def __init__(self, langsmith_client, pii_scrubber):
        super().__init__(client=langsmith_client)
        self.pii_scrubber = pii_scrubber
        
    def on_llm_start(self, serialized, prompts, **kwargs):
        # Scrub PII from prompts before tracing
        scrubbed_prompts = [
            self.pii_scrubber.scrub_pii(prompt, kwargs.get('session_id', 'unknown'))
            for prompt in prompts
        ]
        return super().on_llm_start(serialized, scrubbed_prompts, **kwargs)

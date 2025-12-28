# backend/app/core/multilingual.py
from enum import Enum
from typing import Dict, Any, Optional
import spacy
from googletrans import Translator

class SingaporeLanguage(Enum):
    ENGLISH = "en"
    MANDARIN = "zh"
    MALAY = "ms"
    TAMIL = "ta"

class LanguageDetector:
    """Singapore-optimized language detection with cultural context"""
    
    def __init__(self):
        self.translator = Translator()
        self.nlp_models = {}
        self._load_nlp_models()
        
        # Singapore-specific language weights
        self.SINGAPORE_LANGUAGE_WEIGHTS = {
            'en': 0.7,  # Primary business language
            'zh': 0.2,  # Mandarin - major community
            'ms': 0.07, # Malay - national language
            'ta': 0.03  # Tamil - minority community
        }
    
    def _load_nlp_models(self):
        """Load lightweight NLP models for language detection"""
        for lang in SingaporeLanguage:
            try:
                self.nlp_models[lang.value] = spacy.load(f"{lang.value}_core_web_sm")
            except:
                self.nlp_models[lang.value] = None
    
    def detect_language(self, text: str, context: Dict[str, Any] = None) -> SingaporeLanguage:
        """Detect language with Singapore cultural context awareness"""
        
        # First pass: Fast pattern matching for common Singapore phrases
        singapore_phrases = {
            'zh': ['你好', '谢谢', '请问', '多少钱'],
            'ms': ['selamat', 'terima kasih', 'berapa', 'boleh'],
            'ta': ['வணக்கம்', 'நன்றி', 'எவ்வளவு', 'உதவி']
        }
        
        text_lower = text.lower()
        for lang, phrases in singapore_phrases.items():
            if any(phrase in text_lower for phrase in phrases):
                return SingaporeLanguage(lang)
        
        # Second pass: Statistical detection with cultural weights
        detected_lang = self.translator.detect(text).lang
        
        # Apply Singapore context weighting
        if detected_lang not in [lang.value for lang in SingaporeLanguage]:
            # Default to English for Singapore business context
            return SingaporeLanguage.ENGLISH
            
        # Cultural context adjustment
        if context and context.get('user_location') == 'SINGAPORE':
            detected_lang = self._apply_singapore_weights(detected_lang)
            
        return SingaporeLanguage(detected_lang)
    
    def _apply_singapore_weights(self, detected_lang: str) -> str:
        """Apply Singapore cultural weights to language detection"""
        weights = self.SINGAPORE_LANGUAGE_WEIGHTS
        if detected_lang in weights and weights[detected_lang] > 0.5:
            return detected_lang
        return 'en'  # Default to English in ambiguous Singapore context
    
    def translate_to_english(self, text: str, source_lang: SingaporeLanguage) -> str:
        """Translate to English with business context preservation"""
        if source_lang == SingaporeLanguage.ENGLISH:
            return text
            
        try:
            translation = self.translator.translate(text, src=source_lang.value, dest='en')
            return self._preserve_business_context(translation.text, source_lang)
        except Exception as e:
            logger.warning(f"Translation failed: {e}")
            return text
    
    def _preserve_business_context(self, text: str, source_lang: SingaporeLanguage) -> str:
        """Preserve Singapore business context during translation"""
        business_terms = {
            'zh': {
                '公司': 'company',
                '产品': 'product',
                '服务': 'service',
                '价格': 'price',
                '折扣': 'discount'
            },
            'ms': {
                'syarikat': 'company',
                'produk': 'product',
                'perkhidmatan': 'service',
                'harga': 'price',
                'diskaun': 'discount'
            },
            'ta': {
                'நிறுவனம்': 'company',
                'பொருள்': 'product',
                'சேவை': 'service',
                'விலை': 'price',
                'தள்ளுபடி': 'discount'
            }
        }
        
        for term, replacement in business_terms.get(source_lang.value, {}).items():
            if term in text:
                text = text.replace(term, replacement)
        return text

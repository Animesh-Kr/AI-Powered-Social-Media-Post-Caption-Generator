"""
RAG (Retrieval-Augmented Generation) Pipeline

Enhances content generation with context-aware retrieval from brand examples
using vector similarity search for consistent, high-quality outputs.
"""

import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

from vector_store import BrandVectorStore, get_vector_store
from content_generator import ContentRequest, GeneratedPost

logger = logging.getLogger(__name__)


class RAGContentPipeline:
    """
    RAG pipeline that retrieves relevant brand examples before generation.
    Injects context into prompts for brand-consistent, high-quality content.
    """
    
    def __init__(self, content_generator, vector_store: Optional[BrandVectorStore] = None):
        """
        Initialize RAG pipeline.
        
        Args:
            content_generator: GeminiContentGenerator instance
            vector_store: BrandVectorStore instance (optional, will create if None)
        """
        self.generator = content_generator
        self.vector_store = vector_store or get_vector_store()
        
        if self.vector_store is None:
            logger.warning("⚠️ RAG pipeline initialized without vector store")
            self.enabled = False
        else:
            self.enabled = True
            logger.info("✅ RAG pipeline ready for context-aware generation")
    
    def generate_with_context(
        self,
        request: ContentRequest,
        num_examples: int = 3,
        use_platform_filter: bool = True
    ) -> List[GeneratedPost]:
        """
        Generate content with retrieved context from brand examples.
        
        Args:
            request: ContentRequest with generation parameters
            num_examples: Number of similar examples to retrieve
            use_platform_filter: Filter examples by target platform
            
        Returns:
            List of GeneratedPost objects
        """
        if not self.enabled or self.vector_store is None:
            # Fallback to regular generation
            logger.info("ℹ️ RAG disabled, using standard generation")
            return self.generator.generate(request)
        
        try:
            # Retrieve relevant brand examples
            platform_filter = request.platforms[0] if use_platform_filter and request.platforms else None
            
            logger.info(f"🔍 Retrieving {num_examples} similar examples...")
            similar_examples = self.vector_store.retrieve_similar(
                query=request.keywords,
                k=num_examples,
                filter_platform=platform_filter
            )
            
            if not similar_examples:
                logger.warning("⚠️ No similar examples found, using standard generation")
                return self.generator.generate(request)
            
            # Enhance request with context
            enhanced_request = self._enhance_request_with_context(
                request,
                similar_examples
            )
            
            # Generate with enhanced prompt
            logger.info(f"🎯 Generating with {len(similar_examples)} context examples")
            return self.generator.generate(enhanced_request)
            
        except Exception as e:
            logger.error(f"❌ RAG generation failed: {e}")
            logger.info("ℹ️ Falling back to standard generation")
            return self.generator.generate(request)
    
    def _enhance_request_with_context(
        self,
        request: ContentRequest,
        examples: List[Dict[str, Any]]
    ) -> ContentRequest:
        """
        Enhance content request with retrieved context.
        
        Args:
            request: Original ContentRequest
            examples: Retrieved similar examples
            
        Returns:
            Enhanced ContentRequest with context
        """
        # Build context section from examples
        context_text = self._format_context(examples)
        
        # Enhance keywords with context
        enhanced_keywords = f"""{request.keywords}

BRAND CONTEXT (Follow these examples):
{context_text}

Generate content that matches the style, tone, and quality of the examples above.
"""
        
        # Create enhanced request
        enhanced_request = ContentRequest(
            keywords=enhanced_keywords,
            post_type=request.post_type,
            platforms=request.platforms,
            num_generations=request.num_generations,
            image_data=request.image_data,
            image_mime_type=request.image_mime_type
        )
        
        return enhanced_request
    
    def _format_context(self, examples: List[Dict[str, Any]]) -> str:
        """
        Format retrieved examples into context string.
        
        Args:
            examples: List of similar examples
            
        Returns:
            Formatted context string
        """
        context_parts = []
        
        for i, ex in enumerate(examples, 1):
            similarity = ex.get('similarity_score', 0)
            caption = ex.get('caption', ex.get('content', ''))
            hashtags = ex.get('hashtags', [])
            platform = ex.get('platform', 'general')
            tone = ex.get('tone', 'neutral')
            
            context_part = f"""
Example {i} (Similarity: {similarity:.0%}, Platform: {platform}, Tone: {tone}):
Caption: {caption}
Hashtags: {' '.join(hashtags) if hashtags else 'N/A'}
"""
            context_parts.append(context_part.strip())
        
        return "\n\n".join(context_parts)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get RAG pipeline statistics"""
        stats = {
            'enabled': self.enabled,
            'vector_store_loaded': self.vector_store is not None
        }
        
        if self.vector_store:
            stats.update(self.vector_store.get_stats())
        
        return stats


def create_rag_pipeline(content_generator, enable_rag: bool = True) -> RAGContentPipeline:
    """
    Factory function to create RAG pipeline.
    
    Args:
        content_generator: GeminiContentGenerator instance
        enable_rag: Whether to enable RAG
        
    Returns:
        RAGContentPipeline instance
    """
    if not enable_rag:
        logger.info("ℹ️ RAG disabled by user preference")
        return RAGContentPipeline(content_generator, vector_store=None)
    
    try:
        vector_store = get_vector_store()
        pipeline = RAGContentPipeline(content_generator, vector_store)
        
        if pipeline.enabled:
            logger.info("✅ RAG pipeline created successfully")
        else:
            logger.warning("⚠️ RAG pipeline created but disabled (no vector store)")
        
        return pipeline
        
    except Exception as e:
        logger.error(f"❌ Failed to create RAG pipeline: {e}")
        logger.info("ℹ️ Creating pipeline without RAG")
        return RAGContentPipeline(content_generator, vector_store=None)

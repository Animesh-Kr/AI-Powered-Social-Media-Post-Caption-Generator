"""
Vector Store Module for RAG Pipeline

Manages brand content embeddings and similarity search using FAISS
and sentence transformers with GPU acceleration.
"""

import os
import json
import logging
import streamlit as st
from typing import List, Dict, Any, Optional
from pathlib import Path
from dataclasses import dataclass

logger = logging.getLogger(__name__)

# GPU-accelerated embedding model loading
@st.cache_resource
def load_embedding_model():
    """
    Load sentence transformer model onto GPU with caching.
    Model stays in VRAM for ultra-fast embedding generation.
    
    Returns:
        HuggingFaceEmbeddings: Cached embedding model
    """
    try:
        from langchain.embeddings import HuggingFaceEmbeddings
        import torch
        
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        logger.info(f"🚀 Loading embedding model onto {device.upper()}...")
        
        embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2",  # Fast, efficient model
            model_kwargs={'device': device},
            encode_kwargs={
                'normalize_embeddings': True,
                'batch_size': 32  # Optimize for GPU
            }
        )
        
        logger.info(f"✅ Embedding model loaded on {device.upper()}")
        return embeddings
        
    except ImportError as e:
        logger.error(f"❌ Failed to load embedding model: {e}")
        logger.error("💡 Install: pip install langchain sentence-transformers")
        return None
    except Exception as e:
        logger.error(f"❌ Unexpected error loading embeddings: {e}")
        return None


@dataclass
class BrandExample:
    """Represents a brand content example"""
    platform: str
    caption: str
    hashtags: List[str]
    tone: str
    engagement: str
    metadata: Dict[str, Any]


class BrandVectorStore:
    """
    Manages brand content in vector database for RAG retrieval.
    Uses FAISS for fast similarity search with GPU-accelerated embeddings.
    """
    
    def __init__(self, content_dir: str = "brand_content"):
        """
        Initialize vector store.
        
        Args:
            content_dir: Directory containing brand content files
        """
        self.content_dir = Path(content_dir)
        self.embeddings = load_embedding_model()
        self.vector_store = None
        self.examples = []
        
        if self.embeddings is None:
            logger.warning("⚠️ Vector store disabled (embeddings not available)")
    
    def load_brand_content(self) -> bool:
        """
        Load brand guidelines and example posts into vector store.
        
        Returns:
            bool: True if successful, False otherwise
        """
        if self.embeddings is None:
            return False
        
        try:
            from langchain.vectorstores import FAISS
            from langchain.docstore.document import Document
            
            documents = []
            
            # Load example posts
            examples_file = self.content_dir / "example_posts.json"
            if examples_file.exists():
                with open(examples_file, 'r', encoding='utf-8') as f:
                    examples_data = json.load(f)
                    
                for ex in examples_data:
                    # Create searchable text
                    text = f"{ex['caption']} {' '.join(ex.get('hashtags', []))}"
                    
                    # Create document with metadata
                    doc = Document(
                        page_content=text,
                        metadata={
                            'platform': ex.get('platform', 'general'),
                            'tone': ex.get('tone', 'neutral'),
                            'engagement': ex.get('engagement', 'unknown'),
                            'caption': ex['caption'],
                            'hashtags': ex.get('hashtags', [])
                        }
                    )
                    documents.append(doc)
                    self.examples.append(BrandExample(**ex, metadata={}))
            
            # Load brand voice guidelines
            voice_file = self.content_dir / "brand_voice.txt"
            if voice_file.exists():
                with open(voice_file, 'r', encoding='utf-8') as f:
                    voice_text = f.read()
                    
                doc = Document(
                    page_content=voice_text,
                    metadata={'type': 'brand_voice'}
                )
                documents.append(doc)
            
            if not documents:
                logger.warning("⚠️ No brand content found to load")
                return False
            
            # Create FAISS vector store
            logger.info(f"📚 Creating vector store from {len(documents)} documents...")
            self.vector_store = FAISS.from_documents(
                documents,
                self.embeddings
            )
            
            logger.info(f"✅ Vector store created with {len(documents)} documents")
            return True
            
        except ImportError as e:
            logger.error(f"❌ FAISS not available: {e}")
            logger.error("💡 Install: pip install faiss-cpu")
            return False
        except Exception as e:
            logger.error(f"❌ Failed to load brand content: {e}")
            return False
    
    def retrieve_similar(
        self,
        query: str,
        k: int = 3,
        filter_platform: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve k most similar brand examples for a query.
        
        Args:
            query: Search query (keywords, description)
            k: Number of results to return
            filter_platform: Optional platform filter
            
        Returns:
            List of similar examples with metadata
        """
        if self.vector_store is None:
            logger.warning("⚠️ Vector store not initialized")
            return []
        
        try:
            # Perform similarity search
            results = self.vector_store.similarity_search_with_score(
                query,
                k=k * 2  # Get more, then filter
            )
            
            # Filter and format results
            filtered_results = []
            for doc, score in results:
                # Apply platform filter if specified
                if filter_platform:
                    if doc.metadata.get('platform') != filter_platform:
                        continue
                
                filtered_results.append({
                    'content': doc.page_content,
                    'caption': doc.metadata.get('caption', ''),
                    'hashtags': doc.metadata.get('hashtags', []),
                    'platform': doc.metadata.get('platform', 'general'),
                    'tone': doc.metadata.get('tone', 'neutral'),
                    'similarity_score': float(1 - score)  # Convert distance to similarity
                })
                
                if len(filtered_results) >= k:
                    break
            
            logger.info(f"🔍 Retrieved {len(filtered_results)} similar examples")
            return filtered_results
            
        except Exception as e:
            logger.error(f"❌ Retrieval failed: {e}")
            return []
    
    def get_stats(self) -> Dict[str, Any]:
        """Get vector store statistics"""
        return {
            'total_examples': len(self.examples),
            'is_loaded': self.vector_store is not None,
            'embedding_model': 'all-MiniLM-L6-v2',
            'vector_db': 'FAISS'
        }


# Initialize global vector store (cached)
@st.cache_resource
def get_vector_store(content_dir: str = "brand_content") -> Optional[BrandVectorStore]:
    """
    Get or create cached vector store instance.
    
    Args:
        content_dir: Directory with brand content
        
    Returns:
        BrandVectorStore or None if initialization fails
    """
    try:
        store = BrandVectorStore(content_dir)
        
        # Try to load content
        if store.load_brand_content():
            logger.info("🎯 Vector store ready for RAG retrieval")
            return store
        else:
            logger.warning("⚠️ Vector store created but no content loaded")
            return store
            
    except Exception as e:
        logger.error(f"❌ Failed to initialize vector store: {e}")
        return None

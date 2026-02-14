"""
Content Generation Module
Handles AI-powered social media content generation with integrated 
sentiment analysis for tone validation using GPU acceleration.
"""

import requests
import json
import base64
import logging
import streamlit as st
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)

# --- GPU-Accelerated Sentiment Analysis Setup ---
# This function ensures the GPU stays 'warm' and the page loads fast
@st.cache_resource
def initialize_gpu_pipeline():
    """
    Load sentiment analysis model onto GPU with caching.
    This decorator ensures the model is loaded ONCE and kept in GPU VRAM
    for ultra-fast inference across all user sessions.
    
    Returns:
        tuple: (analyzer_pipeline, is_enabled, gpu_hardware_name)
    """
    try:
        from transformers import pipeline
        import torch
        
        # device=0 specifically targets your RTX card
        device = 0 if torch.cuda.is_available() else -1
        
        logger.info(f"🚀 Initializing GPU pipeline...")
        logger.info(f"CUDA Available: {torch.cuda.is_available()}")
        
        if device == 0:
            gpu_name = torch.cuda.get_device_name(0)
            logger.info(f"🎯 Targeting GPU: {gpu_name}")
        else:
            gpu_name = "CPU"
            logger.warning("⚠️ No GPU detected, using CPU")
        
        # Load model with explicit device assignment
        analyzer = pipeline(
            "sentiment-analysis",
            device=device,
            model="distilbert-base-uncased-finetuned-sst-2-english"  # Explicit model for consistency
        )
        
        logger.info(f"✅ Sentiment analyzer loaded successfully on {gpu_name}")
        logger.info(f"🎯 Model will remain in {'VRAM' if device == 0 else 'RAM'} for fast inference")
        
        return analyzer, True, gpu_name
        
    except ImportError as e:
        logger.warning(f"⚠️ Sentiment analysis disabled: {e}")
        logger.warning("💡 Install 'transformers' and 'torch' to enable GPU acceleration")
        logger.warning("💡 Run: pip install torch transformers")
        return None, False, "None"
    except Exception as e:
        logger.error(f"❌ Failed to load sentiment analyzer: {e}")
        return None, False, "None"

# Execute immediately on web page load - Initialize GPU model at module load time
SENTIMENT_ANALYZER, SENTIMENT_ENABLED, GPU_HARDWARE = initialize_gpu_pipeline()

if SENTIMENT_ENABLED:
    logger.info(f"🔥 GPU-accelerated sentiment analysis is READY on {GPU_HARDWARE}!")
else:
    logger.info("ℹ️ Sentiment analysis is disabled - check environment and dependencies")



@dataclass
class ContentRequest:
    keywords: str
    post_type: str
    platforms: List[str]
    num_generations: int = 1
    image_data: Optional[bytes] = None
    image_mime_type: Optional[str] = None

@dataclass
class GeneratedPost:
    caption: str
    hashtags: List[str]
    emojis: str
    sentiment: Optional[str] = None # Added for sentiment display

class ContentGenerationError(Exception):
    pass

class GeminiContentGenerator:
    def __init__(self, api_key: str, temperature: float = 0.7):
        self.api_key = api_key
        self.temperature = temperature
        self.api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

    def _analyze_sentiment(self, text: str) -> str:
        """Helper to run inference on generated captions."""
        if not SENTIMENT_ENABLED:
            return "Analysis Disabled"
        try:
            # Use first 512 tokens for BERT-based models
            result = SENTIMENT_ANALYZER(text[:512])[0]
            return f"{result['label']} ({result['score']:.2f})"
        except Exception as e:
            return f"Error: {str(e)}"

    def generate(self, request: ContentRequest) -> List[GeneratedPost]:
        """
        Generate social media content based on request.
        
        Args:
            request: ContentRequest with generation parameters
            
        Returns:
            List of GeneratedPost objects
            
        Raises:
            ContentGenerationError: If generation fails (with sanitized message)
        """
        try:
            # Build prompt and payload
            prompt = self._build_prompt(request)
            payload = self._build_payload(prompt, request)
            
            # Make API request
            logger.info("Sending request to Gemini API...")
            response = requests.post(
                self.api_url,
                json=payload,
                timeout=30
            )
            
            # Handle specific HTTP errors with user-friendly messages
            if response.status_code == 429:
                logger.warning("Rate limit exceeded (429)")
                raise ContentGenerationError(
                    "The AI service is currently busy (Rate Limit). "
                    "Please wait a minute and try again."
                )
            
            if response.status_code == 401:
                logger.error("Authentication failed (401)")
                raise ContentGenerationError(
                    "API authentication failed. Please check your API key configuration."
                )
            
            if response.status_code == 403:
                logger.error("Access forbidden (403)")
                raise ContentGenerationError(
                    "Access denied. Your API key may not have the required permissions."
                )
            
            if response.status_code >= 500:
                logger.error(f"Server error ({response.status_code})")
                raise ContentGenerationError(
                    f"The AI service is experiencing issues (Error {response.status_code}). "
                    "Please try again later."
                )
            
            # Raise for any other HTTP errors
            response.raise_for_status()
            
            # Parse and return results
            logger.info("Successfully received response from API")
            return self._parse_response(response.json())
            
        except requests.exceptions.HTTPError as e:
            # Log the full error internally (with URL) but don't expose it to users
            status_code = e.response.status_code if e.response else "Unknown"
            logger.error(f"HTTP Error {status_code}: {str(e)}")
            
            # Raise sanitized error for users
            raise ContentGenerationError(
                f"Server error ({status_code}). Please check your connection and try again."
            )
            
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Connection error: {str(e)}")
            raise ContentGenerationError(
                "Unable to connect to the AI service. Please check your internet connection."
            )
            
        except requests.exceptions.Timeout as e:
            logger.error(f"Request timed out: {str(e)}")
            raise ContentGenerationError(
                "Request timed out. The service may be slow. Please try again."
            )
            
        except ContentGenerationError:
            # Re-raise our custom errors as-is (already sanitized)
            raise
            
        except Exception as e:
            # Catch-all for unexpected errors - log internally but show generic message
            logger.error(f"Unexpected error during generation: {type(e).__name__}: {str(e)}")
            raise ContentGenerationError(
                "An unexpected error occurred while generating content. Please try again."
            )

    def _build_prompt(self, request: ContentRequest) -> str:
        prompt = f"Generate {request.num_generations} social media posts. Keywords: {request.keywords}. Tone: {request.post_type}."
        if request.image_data:
            prompt += " Analyze the provided image and include its context."
        prompt += "\nOutput as JSON array: [{'caption': '...', 'hashtags': ['...'], 'emojis': '...'}]"
        return prompt

    def _build_payload(self, prompt: str, request: ContentRequest) -> Dict[str, Any]:
        parts = [{"text": prompt}]
        if request.image_data:
            parts.append({"inlineData": {"mimeType": request.image_mime_type, "data": base64.b64encode(request.image_data).decode()}})
        return {"contents": [{"parts": parts}], "generationConfig": {"temperature": self.temperature, "responseMimeType": "application/json"}}

    def _parse_response(self, response_data: Dict[str, Any]) -> List[GeneratedPost]:
        json_string = response_data["candidates"][0]["content"]["parts"][0]["text"]
        parsed = json.loads(json_string)
        posts = []
        for item in parsed:
            cap = item.get("caption", "")
            posts.append(GeneratedPost(
                caption=cap,
                hashtags=[f"#{h}" for h in item.get("hashtags", [])],
                emojis=item.get("emojis", "✨"),
                sentiment=self._analyze_sentiment(cap) # Perform analysis
            ))
        return posts
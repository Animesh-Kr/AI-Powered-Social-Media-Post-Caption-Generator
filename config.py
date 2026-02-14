"""
Configuration Management for AI Social Media Caption Generator

This module provides secure configuration management with support for
environment variables and different deployment environments.
"""

import os
from typing import Optional
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    """
    Application configuration with support for multiple environments.
    
    Attributes:
        gemini_api_key: Google Gemini API key
        environment: Current environment (development/production)
        cache_enabled: Whether to enable response caching
        max_generations: Maximum number of captions to generate
        temperature: Model temperature for generation (0-1)
        debug: Enable debug mode
    """
    
    gemini_api_key: str
    environment: str = "development"
    cache_enabled: bool = True
    max_generations: int = 5
    temperature: float = 0.7
    debug: bool = False
    
    @classmethod
    def from_env(cls) -> "Config":
        """
        Load configuration from environment variables.
        
        Environment variables:
            GEMINI_API_KEY: Required. Google Gemini API key
            ENVIRONMENT: Optional. Deployment environment (default: development)
            CACHE_ENABLED: Optional. Enable caching (default: true)
            DEBUG: Optional. Enable debug mode (default: false)
        
        Returns:
            Config: Configuration object
            
        Raises:
            ValueError: If GEMINI_API_KEY is not set
        """
        api_key = os.getenv("GEMINI_API_KEY")
        
        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY environment variable is required. "
                "Please set it in a .env file or your environment."
            )
        
        return cls(
            gemini_api_key=api_key,
            environment=os.getenv("ENVIRONMENT", "development"),
            cache_enabled=os.getenv("CACHE_ENABLED", "true").lower() == "true",
            max_generations=int(os.getenv("MAX_GENERATIONS", "5")),
            temperature=float(os.getenv("TEMPERATURE", "0.7")),
            debug=os.getenv("DEBUG", "false").lower() == "true"
        )
    
    def validate(self) -> None:
        """
        Validate configuration parameters.
        
        Raises:
            ValueError: If configuration is invalid
        """
        if not self.gemini_api_key:
            raise ValueError("Gemini API key cannot be empty")
        
        if self.temperature < 0 or self.temperature > 1:
            raise ValueError("Temperature must be between 0 and 1")
        
        if self.max_generations < 1 or self.max_generations > 10:
            raise ValueError("Max generations must be between 1 and 10")

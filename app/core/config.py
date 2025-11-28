"""Centralized configuration management"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Centralized configuration for the classification system"""
    
    # File paths
    CACHE_FILE = os.getenv("CACHE_FILE", "classification_cache.json")
    PROMPT_TEMPLATE_FILE = "prompt_template.txt"
    
    # Processing settings
    MAX_WORKERS = int(os.getenv("MAX_WORKERS", "10"))
    MAX_RETRY = int(os.getenv("MAX_RETRY", "3"))
    RETRY_WAIT = float(os.getenv("RETRY_WAIT", "0.5"))
    
    # OpenAI API settings
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "DUMMY_KEY")
    OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "")
    MODEL = os.getenv("MODEL", "")
    
    # API parameters
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0"))
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "150"))
    
    @classmethod
    def load_prompt_template(cls) -> str:
        """Load prompt template from file"""
        try:
            return Path(cls.PROMPT_TEMPLATE_FILE).read_text(encoding="utf-8")
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Prompt template file '{cls.PROMPT_TEMPLATE_FILE}' not found."
            )
    
    @classmethod
    def validate(cls) -> bool:
        """Validate configuration"""
        errors = []
        
        if not cls.OPENAI_BASE_URL:
            errors.append("OPENAI_BASE_URL is not set")
        if not cls.MODEL:
            errors.append("MODEL is not set")
        # Allow DUMMY_KEY for self-hosted APIs that don't require authentication
        if not cls.OPENAI_API_KEY:
            errors.append("OPENAI_API_KEY is not set")
        
        if errors:
            raise ValueError(f"Configuration errors: {', '.join(errors)}")
        
        return True

"""Script to check system configuration"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core import Config


def check_config():
    """Check and display system configuration"""
    print("=" * 60)
    print("SPX Classification System - Configuration Check")
    print("=" * 60)
    
    print("\n📋 API Configuration:")
    print(f"  Base URL: {Config.OPENAI_BASE_URL}")
    print(f"  Model: {Config.MODEL}")
    print(f"  API Key: {'✅ Set' if Config.OPENAI_API_KEY != 'DUMMY_KEY' else '❌ Not set'}")
    
    print("\n⚙️  Processing Configuration:")
    print(f"  Max Workers: {Config.MAX_WORKERS}")
    print(f"  Max Retry: {Config.MAX_RETRY}")
    print(f"  Retry Wait: {Config.RETRY_WAIT}s")
    
    print("\n🤖 Model Parameters:")
    print(f"  Temperature: {Config.TEMPERATURE}")
    print(f"  Max Tokens: {Config.MAX_TOKENS}")
    
    print("\n📁 Files:")
    print(f"  Cache File: {Config.CACHE_FILE}")
    print(f"  Prompt Template: {Config.PROMPT_TEMPLATE_FILE}")
    
    # Check if files exist
    cache_exists = Path(Config.CACHE_FILE).exists()
    prompt_exists = Path(Config.PROMPT_TEMPLATE_FILE).exists()
    
    print(f"  Cache exists: {'✅' if cache_exists else '❌'}")
    print(f"  Prompt template exists: {'✅' if prompt_exists else '❌'}")
    
    # Validate configuration
    print("\n🔍 Validation:")
    try:
        Config.validate()
        print("  ✅ Configuration is valid")
    except Exception as e:
        print(f"  ❌ Configuration error: {e}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    check_config()

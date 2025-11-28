"""Script to clear the classification cache"""
from pathlib import Path

CACHE_FILE = "classification_cache.json"

if __name__ == "__main__":
    cache_path = Path(CACHE_FILE)
    
    if cache_path.exists():
        cache_path.unlink()
        print(f"✅ Cache cleared: {CACHE_FILE}")
    else:
        print(f"ℹ️  Cache file not found: {CACHE_FILE}")

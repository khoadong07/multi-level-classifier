"""Cache management for classification results"""
import json
from pathlib import Path
from typing import Dict, Optional


class CacheManager:
    """Manages classification cache with file persistence"""
    
    def __init__(self, cache_file: str):
        self.cache_file = Path(cache_file)
        self.cache: Dict[str, Dict] = self.load()
    
    def load(self) -> Dict[str, Dict]:
        """Load cache from file"""
        if self.cache_file.exists():
            try:
                return json.loads(self.cache_file.read_text(encoding="utf-8"))
            except Exception as e:
                print(f"Error loading cache: {e}")
                return {}
        return {}
    
    def save(self):
        """Save cache to file"""
        try:
            self.cache_file.write_text(
                json.dumps(self.cache, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
        except Exception as e:
            print(f"Error saving cache: {e}")
    
    def get(self, key: str) -> Optional[str]:
        """Get label from cache"""
        if key in self.cache:
            return self.cache[key].get("label_en")
        return None
    
    def set(self, key: str, label: str):
        """Set label in cache"""
        self.cache[key] = {"label_en": label}
    
    def clear(self):
        """Clear cache"""
        self.cache = {}
        if self.cache_file.exists():
            self.cache_file.unlink()
    
    def __contains__(self, key: str) -> bool:
        """Check if key exists in cache"""
        return key in self.cache

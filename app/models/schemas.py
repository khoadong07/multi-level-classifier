"""Data models for classification system"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class ClassificationTask:
    """Represents a single classification task"""
    index: int
    feedback: str
    feedback_key: str


@dataclass
class ClassificationResult:
    """Result of a classification task"""
    index: int
    label_en: Optional[str]
    label_1: Optional[str]
    label_2: Optional[str]
    label_3: Optional[str]
    label_4: Optional[str]
    status: str  # 'hit', 'miss', 'failed'
    feedback_key: str


@dataclass
class ProcessingStats:
    """Statistics for processing batch"""
    total_tasks: int = 0
    cache_hits: int = 0
    api_calls: int = 0
    failed: int = 0
    
    def update(self, status: str):
        """Update stats based on result status"""
        if status == 'hit':
            self.cache_hits += 1
        elif status == 'miss':
            self.api_calls += 1
        elif status == 'failed':
            self.failed += 1

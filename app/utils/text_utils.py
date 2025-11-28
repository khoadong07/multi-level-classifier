"""Text processing utilities"""
import re
import pandas as pd
from typing import Dict, Optional


def clean_text(text) -> str:
    """Cleans and strips text, handling None or NaN values"""
    if pd.isna(text) or text is None:
        return ""
    return str(text).strip()


def merge_feedback(row: pd.Series) -> str:
    """Merges relevant text fields into a single feedback string"""
    parts = [
        clean_text(row.get("Title", "")),
        clean_text(row.get("Content", "")),
        clean_text(row.get("Description", ""))
    ]
    unique_parts = []
    seen = set()
    for p in parts:
        if p and p not in seen:
            unique_parts.append(p)
            seen.add(p)
    return " | ".join(unique_parts).strip()


def normalize_feedback_key(feedback: str) -> str:
    """Normalizes the feedback string for use as a cache key"""
    if not feedback:
        return ""
    s = feedback.strip()
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"\s*\|\s*", " | ", s)
    return s.strip()


def split_label(label_en: str) -> Dict[str, Optional[str]]:
    """Splits a hierarchical label string into separate components"""
    result = {
        "label_1": None,
        "label_2": None,
        "label_3": None,
        "label_4": None
    }
    
    if not label_en:
        return result
    
    parts = [p.strip() for p in label_en.split('/')]
    
    result["label_1"] = parts[0].replace("~", "/") if len(parts) >= 1 and parts[0] else None
    result["label_2"] = parts[1].replace("~", "/") if len(parts) >= 2 and parts[1] else None
    result["label_3"] = parts[2].replace("~", "/") if len(parts) >= 3 and parts[2] else None
    result["label_4"] = parts[3].replace("~", "/") if len(parts) >= 4 and parts[3] else None
    
    return result

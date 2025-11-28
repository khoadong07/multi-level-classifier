"""LLM-based classification logic"""
import json
import re
import time
import openai
from typing import Optional


class Classifier:
    """Handles LLM-based text classification"""
    
    def __init__(self, base_url: str, api_key: str, model: str, 
                 prompt_template: str, temperature: float = 0, 
                 max_tokens: int = 150):
        self.base_url = base_url
        self.api_key = api_key
        self.model = model
        self.prompt_template = prompt_template
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.client = openai.OpenAI(base_url=base_url, api_key=api_key)
    
    def classify(self, feedback: str, max_retry: int = 3, 
                 wait_between_retry: float = 0.5) -> Optional[str]:
        """Classify a single feedback text"""
        if not feedback:
            return None
        
        prompt = self._build_prompt(feedback)
        
        for attempt in range(1, max_retry + 1):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an expert SPX feedback classification system."
                        },
                        {"role": "user", "content": prompt}
                    ],
                    temperature=self.temperature,
                    max_tokens=self.max_tokens
                )
                
                raw = response.choices[0].message.content.strip()
                data = self._extract_json(raw)
                
                if data and isinstance(data, dict):
                    label = data.get("label_en")
                    if label:
                        return label.strip()
            
            except Exception as e:
                print(f"API Error (Attempt {attempt}/{max_retry}): {e}")
            
            if attempt < max_retry:
                time.sleep(wait_between_retry)
        
        return None
    
    def _build_prompt(self, feedback: str) -> str:
        """Build classification prompt"""
        return self.prompt_template.replace("{FEEDBACK}", feedback) + "\n\n" + (
            "You must return exactly one single JSON object, NO other characters. "
            "The JSON structure must be strictly as follows (Example with hierarchical label):\n"
            '{ "label_en": "BUYER / Engagement / Seller/ Buyer" }'
        )
    
    @staticmethod
    def _extract_json(text: str):
        """Extract JSON object from text response"""
        if not text:
            return None
        
        # Remove markdown code blocks
        text_clean = re.sub(r"```(?:json)?", "", text, flags=re.IGNORECASE).strip()
        
        # Find JSON object
        try:
            start = text_clean.index('{')
            end = text_clean.rindex('}')
            if start < end:
                candidate = text_clean[start:end+1]
                return json.loads(candidate)
        except (ValueError, json.JSONDecodeError):
            pass
        
        # Fallback: try to parse entire text
        try:
            return json.loads(text_clean)
        except Exception:
            return None

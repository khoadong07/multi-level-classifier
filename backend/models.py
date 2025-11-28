"""
Pydantic Models
Request and response models for API endpoints
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# ==================== USER MODELS ====================

class UserCreate(BaseModel):
    """Model for creating a new user"""
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)
    role: str = Field(default="user", pattern="^(admin|user)$")


class UserLogin(BaseModel):
    """Model for user login"""
    username: str
    password: str


class UserResponse(BaseModel):
    """Model for user response"""
    username: str
    role: str
    must_change_password: bool
    created_at: datetime


class PasswordChange(BaseModel):
    """Model for password change"""
    old_password: str
    new_password: str = Field(..., min_length=6)


# ==================== TOPIC MODELS ====================

class TopicCreate(BaseModel):
    """Model for creating a new topic"""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    llm_provider: str = Field(..., description="LLM provider (openai, anthropic, etc)")
    model: str = Field(..., description="Model name")
    api_base_url: str = Field(..., description="API base URL")
    api_key: str = Field(..., description="API key")
    prompt_template: str = Field(..., description="Prompt template with {title}, {content}, {description}")
    temperature: float = Field(default=0.0, ge=0.0, le=2.0)
    max_tokens: int = Field(default=150, ge=1, le=4096)


class TopicUpdate(BaseModel):
    """Model for updating a topic"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    llm_provider: Optional[str] = None
    model: Optional[str] = None
    api_base_url: Optional[str] = None
    api_key: Optional[str] = None
    prompt_template: Optional[str] = None
    temperature: Optional[float] = Field(None, ge=0.0, le=2.0)
    max_tokens: Optional[int] = Field(None, ge=1, le=4096)


class TopicResponse(BaseModel):
    """Model for topic response"""
    topic_id: str
    name: str
    description: Optional[str]
    llm_provider: str
    model: str
    created_at: datetime
    created_by: str


# ==================== TASK MODELS ====================

class TaskCreate(BaseModel):
    """Model for creating a task"""
    topic_id: str
    filename: str
    rows: int


class TaskResponse(BaseModel):
    """Model for task response"""
    job_id: str
    topic_id: str
    user: str
    filename: str
    status: str
    progress: int
    created_at: datetime

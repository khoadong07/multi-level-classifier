"""Topic management routes"""
from fastapi import APIRouter, HTTPException, Depends, status
from backend.models import TopicCreate, TopicUpdate
from backend.auth import get_current_user, get_current_admin
from backend.database import (
    create_topic, get_topic, get_all_topics,
    update_topic, delete_topic
)
from typing import List

router = APIRouter(prefix="/api/topics", tags=["Topics"])


@router.post("", dependencies=[Depends(get_current_admin)])
async def create_new_topic(
    topic_data: TopicCreate,
    current_user: dict = Depends(get_current_admin)
):
    """Create new topic (Admin only)"""
    topic_dict = topic_data.dict()
    topic_dict["created_by"] = current_user["username"]
    
    topic_id = await create_topic(topic_dict)
    
    return {
        "message": "Topic created successfully",
        "topic_id": topic_id
    }


@router.get("")
async def list_topics(current_user: dict = Depends(get_current_user)):
    """List all topics"""
    topics = await get_all_topics()
    
    # Hide sensitive data for non-admin users
    if current_user["role"] != "admin":
        for topic in topics:
            topic.pop("api_key", None)
    
    return {"topics": topics}


@router.get("/{topic_id}")
async def get_topic_detail(
    topic_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get topic details"""
    topic = await get_topic(topic_id)
    
    if not topic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Topic not found"
        )
    
    # Hide API key for non-admin users
    if current_user["role"] != "admin":
        topic.pop("api_key", None)
    
    return topic


@router.put("/{topic_id}", dependencies=[Depends(get_current_admin)])
async def update_topic_config(
    topic_id: str,
    topic_data: TopicUpdate
):
    """Update topic configuration (Admin only)"""
    topic = await get_topic(topic_id)
    
    if not topic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Topic not found"
        )
    
    # Update only provided fields
    update_dict = {k: v for k, v in topic_data.dict().items() if v is not None}
    
    if update_dict:
        await update_topic(topic_id, update_dict)
    
    return {"message": "Topic updated successfully"}


@router.delete("/{topic_id}", dependencies=[Depends(get_current_admin)])
async def remove_topic(topic_id: str):
    """Delete topic (Admin only)"""
    topic = await get_topic(topic_id)
    
    if not topic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Topic not found"
        )
    
    await delete_topic(topic_id)
    return {"message": "Topic deleted successfully"}

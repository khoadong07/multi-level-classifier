"""
KMLC Backend API
Main FastAPI application for Kompa MultiLevel Classifier
"""
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pathlib import Path
from typing import Optional
import pandas as pd
import uuid
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core import Config, Classifier, CacheManager, CentralProcessor
from backend.database import (
    connect_to_mongo, close_mongo_connection,
    create_task, get_task, update_task,
    get_all_tasks, get_tasks_by_status, delete_task
)
from backend.auth import get_current_user, get_current_admin
from backend.auth_routes import router as auth_router
from backend.topic_routes import router as topic_router

# Initialize FastAPI app
app = FastAPI(
    title="KMLC API",
    description="Kompa MultiLevel Classifier API",
    version="2.1.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(topic_router)

# Global components
classifier = None
cache_manager = None
processor = None

# Directory configuration
UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", "uploads"))
OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", "outputs"))
CACHE_DIR = Path(os.getenv("CACHE_DIR", "."))

# Create directories
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)
CACHE_DIR.mkdir(exist_ok=True)


def initialize_classification_system() -> bool:
    """
    Initialize classification system components.
    
    Returns:
        bool: True if successful, False otherwise
    """
    global classifier, cache_manager, processor
    
    try:
        cache_file = CACHE_DIR / "classification_cache.json"
        cache_manager = CacheManager(str(cache_file))
        print(f"✅ Cache manager initialized (size: {len(cache_manager.cache)})")
        
        Config.validate()
        prompt_template = Config.load_prompt_template()
        
        classifier = Classifier(
            base_url=Config.OPENAI_BASE_URL,
            api_key=Config.OPENAI_API_KEY,
            model=Config.MODEL,
            prompt_template=prompt_template,
            temperature=Config.TEMPERATURE,
            max_tokens=Config.MAX_TOKENS
        )
        
        processor = CentralProcessor(classifier, cache_manager, Config.MAX_WORKERS)
        
        print("✅ Classification system initialized")
        print(f"   Model: {Config.MODEL}")
        print(f"   Base URL: {Config.OPENAI_BASE_URL}")
        return True
        
    except Exception as e:
        print(f"❌ Initialization error: {e}")
        return False


@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    initialize_classification_system()
    await connect_to_mongo()


@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown"""
    await close_mongo_connection()


@app.get("/")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "version": "2.1.0", "service": "KMLC"}


@app.get("/api/config")
async def get_system_config():
    """Get system configuration"""
    if not cache_manager:
        raise HTTPException(status_code=503, detail="System not initialized")
    
    return {
        "model": Config.MODEL or "Not configured",
        "base_url": Config.OPENAI_BASE_URL or "Not configured",
        "max_workers": Config.MAX_WORKERS,
        "cache_size": len(cache_manager.cache),
        "system_ready": processor is not None
    }


@app.post("/api/upload")
async def upload_file(
    file: UploadFile = File(...),
    topic_id: str = Form(...),
    current_user: dict = Depends(get_current_user)
):
    """
    Upload Excel file for classification.
    
    Args:
        file: Excel file (.xlsx)
        topic_id: Topic ID for classification
        current_user: Authenticated user
        
    Returns:
        dict: Upload information with job_id
    """
    # Validate file type
    if not file.filename.endswith('.xlsx'):
        raise HTTPException(status_code=400, detail="Only .xlsx files are supported")
    
    # Verify topic exists
    from backend.database import get_topic
    topic = await get_topic(topic_id)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    
    try:
        # Save uploaded file
        job_id = str(uuid.uuid4())
        file_path = UPLOAD_DIR / f"{job_id}.xlsx"
        
        content = await file.read()
        file_path.write_bytes(content)
        
        # Validate Excel structure
        df = pd.read_excel(file_path)
        required_cols = ["Title", "Content", "Description"]
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        if missing_cols:
            file_path.unlink()  # Clean up
            raise HTTPException(
                status_code=400,
                detail=f"Missing required columns: {', '.join(missing_cols)}"
            )
        
        # Create task in database
        task_data = {
            "job_id": job_id,
            "topic_id": topic_id,
            "topic_name": topic["name"],
            "user": current_user["username"],
            "status": "uploaded",
            "filename": file.filename,
            "rows": len(df),
            "progress": 0,
            "stats": None,
            "error": None
        }
        
        await create_task(task_data)
        
        return {
            "job_id": job_id,
            "filename": file.filename,
            "rows": len(df),
            "topic": topic["name"]
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/classify/{job_id}")
async def start_classification(
    job_id: str,
    clear_cache: bool = False,
    current_user: dict = Depends(get_current_user)
):
    """
    Start classification for a job.
    
    Args:
        job_id: Job identifier
        clear_cache: Whether to clear cache before processing
        current_user: Authenticated user
        
    Returns:
        dict: Status message
    """
    if not processor or not cache_manager:
        raise HTTPException(status_code=503, detail="System not initialized")
    
    # Get task from database
    task = await get_task(job_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Check permissions
    if current_user["role"] != "admin" and task["user"] != current_user["username"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Check task status
    if task["status"] in ["processing", "completed"]:
        raise HTTPException(
            status_code=400,
            detail=f"Task is already {task['status']}"
        )
    
    # Clear cache if requested
    if clear_cache:
        cache_manager.clear()
    
    # Update task to pending (worker will pick it up)
    await update_task(job_id, {
        "status": "pending",
        "progress": 0,
        "clear_cache": clear_cache
    })
    
    return {
        "message": "Task added to queue",
        "job_id": job_id,
        "status": "pending"
    }


@app.get("/api/status/{job_id}")
async def get_task_status(job_id: str):
    """Get task status and progress"""
    task = await get_task(job_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.get("/api/tasks")
async def list_tasks(
    status: Optional[str] = None,
    limit: int = 100,
    skip: int = 0,
    current_user: dict = Depends(get_current_user)
):
    """
    List tasks with optional filtering.
    
    Users see only their tasks, admins see all tasks.
    """
    if status:
        tasks = await get_tasks_by_status(status, limit=limit)
    else:
        tasks = await get_all_tasks(limit=limit, skip=skip)
    
    # Filter for non-admin users
    if current_user["role"] != "admin":
        tasks = [t for t in tasks if t.get("user") == current_user["username"]]
    
    return {"tasks": tasks, "count": len(tasks)}


@app.delete("/api/tasks/{job_id}")
async def delete_task_endpoint(
    job_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Delete or cancel a task"""
    task = await get_task(job_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Check permissions
    if current_user["role"] != "admin" and task["user"] != current_user["username"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Cancel if processing
    if task["status"] == "processing":
        await update_task(job_id, {"status": "cancelled"})
        return {"message": "Task cancelled"}
    
    # Delete files
    try:
        file_path = UPLOAD_DIR / f"{job_id}.xlsx"
        if file_path.exists():
            file_path.unlink()
        
        output_path = OUTPUT_DIR / f"{job_id}_classified.xlsx"
        if output_path.exists():
            output_path.unlink()
    except Exception as e:
        print(f"Error deleting files: {e}")
    
    # Delete from database
    await delete_task(job_id)
    
    return {"message": "Task deleted successfully"}


@app.get("/api/download/{job_id}")
async def download_result(
    job_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Download classified result file"""
    task = await get_task(job_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Check permissions
    if current_user["role"] != "admin" and task["user"] != current_user["username"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    if task["status"] != "completed":
        raise HTTPException(status_code=400, detail="Task not completed yet")
    
    output_path = OUTPUT_DIR / f"{job_id}_classified.xlsx"
    if not output_path.exists():
        raise HTTPException(status_code=404, detail="Output file not found")
    
    return FileResponse(
        output_path,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename=f"{task['filename'].replace('.xlsx', '')}_classified.xlsx"
    )


@app.delete("/api/cache")
async def clear_cache_endpoint(current_user: dict = Depends(get_current_admin)):
    """Clear classification cache (Admin only)"""
    if not cache_manager:
        raise HTTPException(status_code=503, detail="System not initialized")
    
    cache_manager.clear()
    return {"message": "Cache cleared successfully"}


@app.get("/api/cache/stats")
async def get_cache_stats():
    """Get cache statistics"""
    if not cache_manager:
        raise HTTPException(status_code=503, detail="System not initialized")
    
    return {
        "size": len(cache_manager.cache),
        "entries": list(cache_manager.cache.keys())[:10]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

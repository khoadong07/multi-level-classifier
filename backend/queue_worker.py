"""
Background Queue Worker
Processes classification tasks from MongoDB queue
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.database import (
    connect_to_mongo,
    get_tasks_by_status,
    update_task,
    get_topic
)
from app.core import Config, Classifier, CacheManager, CentralProcessor
import pandas as pd


async def process_single_task(task: dict):
    """
    Process a single classification task.
    
    Args:
        task: Task data from database
    """
    job_id = task["job_id"]
    topic_id = task.get("topic_id")
    
    try:
        # Update status to processing
        await update_task(job_id, {
            "status": "processing",
            "progress": 0
        })
        
        # Get topic configuration
        topic = await get_topic(topic_id) if topic_id else None
        
        # Initialize classifier with topic-specific or default config
        if topic:
            prompt_template = topic["prompt_template"]
            base_url = topic["api_base_url"]
            api_key = topic["api_key"]
            model = topic["model"]
            temperature = topic.get("temperature", 0.0)
            max_tokens = topic.get("max_tokens", 150)
        else:
            Config.validate()
            prompt_template = Config.load_prompt_template()
            base_url = Config.OPENAI_BASE_URL
            api_key = Config.OPENAI_API_KEY
            model = Config.MODEL
            temperature = Config.TEMPERATURE
            max_tokens = Config.MAX_TOKENS
        
        # Initialize components
        classifier = Classifier(
            base_url=base_url,
            api_key=api_key,
            model=model,
            prompt_template=prompt_template,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        cache_manager = CacheManager(Config.CACHE_FILE)
        processor = CentralProcessor(classifier, cache_manager, Config.MAX_WORKERS)
        
        # Load and process file
        file_path = Path("uploads") / f"{job_id}.xlsx"
        df = pd.read_excel(file_path)
        
        # Prepare classification tasks
        tasks = processor.prepare_tasks(df)
        
        # Process batch
        results, stats = processor.process_batch(tasks)
        
        # Apply results to dataframe
        df_output = processor.apply_results_to_dataframe(df, results)
        
        # Save output
        output_path = Path("outputs") / f"{job_id}_classified.xlsx"
        df_output.to_excel(output_path, index=False, engine='xlsxwriter')
        
        # Update task as completed
        await update_task(job_id, {
            "status": "completed",
            "progress": 100,
            "stats": {
                "total_tasks": stats.total_tasks,
                "cache_hits": stats.cache_hits,
                "api_calls": stats.api_calls,
                "failed": stats.failed,
                "success_rate": round(
                    ((stats.cache_hits + stats.api_calls) / stats.total_tasks * 100)
                    if stats.total_tasks > 0 else 0,
                    1
                )
            }
        })
        
        print(f"✅ Task {job_id} completed successfully")
        
    except Exception as e:
        print(f"❌ Task {job_id} failed: {e}")
        await update_task(job_id, {
            "status": "failed",
            "error": str(e)
        })


async def queue_worker():
    """
    Main queue worker loop.
    Continuously polls for pending tasks and processes them.
    """
    print("🔄 Queue worker started")
    
    # Connect to MongoDB
    await connect_to_mongo()
    
    while True:
        try:
            # Get pending tasks
            pending_tasks = await get_tasks_by_status("pending", limit=1)
            
            if pending_tasks:
                task = pending_tasks[0]
                print(f"📋 Processing task: {task['job_id']}")
                await process_single_task(task)
            else:
                # No pending tasks, wait before checking again
                await asyncio.sleep(2)
                
        except Exception as e:
            print(f"❌ Worker error: {e}")
            await asyncio.sleep(5)


if __name__ == "__main__":
    asyncio.run(queue_worker())

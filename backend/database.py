"""
MongoDB Database Operations
Handles all database interactions for KMLC
"""
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
from typing import Optional, List
from bson import ObjectId
import os

# MongoDB configuration
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://mongodb:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "kmlc")

# Global database client
client: Optional[AsyncIOMotorClient] = None
database = None


async def connect_to_mongo() -> bool:
    """
    Connect to MongoDB and initialize database.
    
    Returns:
        bool: True if successful, False otherwise
    """
    global client, database
    
    try:
        client = AsyncIOMotorClient(MONGODB_URL)
        database = client[DATABASE_NAME]
        
        # Test connection
        await client.admin.command('ping')
        print(f"✅ Connected to MongoDB: {MONGODB_URL}")
        print(f"   Database: {DATABASE_NAME}")
        
        # Create indexes
        await _create_indexes()
        
        # Create default admin user
        await _create_default_admin()
        
        return True
        
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        return False


async def close_mongo_connection():
    """Close MongoDB connection"""
    global client
    if client:
        client.close()
        print("MongoDB connection closed")


def get_database():
    """Get database instance"""
    return database


async def _create_indexes():
    """Create database indexes for performance"""
    # Users collection
    await database.users.create_index("username", unique=True)
    
    # Topics collection
    await database.topics.create_index("name", unique=True)
    
    # Tasks collection
    await database.tasks.create_index("job_id", unique=True)
    await database.tasks.create_index("user")
    await database.tasks.create_index("topic_id")
    await database.tasks.create_index("status")
    await database.tasks.create_index("created_at")


async def _create_default_admin():
    """Create default admin user if not exists"""
    from backend.auth import get_password_hash
    
    # Get admin credentials from environment
    admin_username = os.getenv("ADMIN_USERNAME", "admin")
    admin_password = os.getenv("ADMIN_PASSWORD", "admin123")
    
    try:
        admin = await database.users.find_one({"username": admin_username})
        if not admin:
            await database.users.insert_one({
                "username": admin_username,
                "password": get_password_hash(admin_password),
                "role": "admin",
                "must_change_password": False,
                "created_at": datetime.utcnow()
            })
            print(f"✅ Default admin created (username: {admin_username}, password: {admin_password})")
        else:
            print(f"ℹ️  Admin user '{admin_username}' already exists")
    except Exception as e:
        # Ignore duplicate key error (user already exists)
        if "duplicate key" in str(e).lower() or "E11000" in str(e):
            print(f"ℹ️  Admin user '{admin_username}' already exists")
        else:
            print(f"⚠️  Error creating admin user: {e}")


# ==================== USER OPERATIONS ====================

async def create_user(username: str, password_hash: str, role: str = "user") -> str:
    """
    Create a new user.
    
    Args:
        username: User's username
        password_hash: Hashed password
        role: User role (admin/user)
        
    Returns:
        str: Created user ID
    """
    user_data = {
        "username": username,
        "password": password_hash,
        "role": role,
        "must_change_password": True,
        "created_at": datetime.utcnow()
    }
    result = await database.users.insert_one(user_data)
    return str(result.inserted_id)


async def get_user_by_username(username: str) -> Optional[dict]:
    """Get user by username"""
    user = await database.users.find_one({"username": username})
    if user:
        user["_id"] = str(user["_id"])
    return user


async def get_all_users(skip: int = 0, limit: int = 100) -> List[dict]:
    """Get all users with pagination"""
    cursor = database.users.find().skip(skip).limit(limit)
    users = []
    async for user in cursor:
        user["_id"] = str(user["_id"])
        users.append(user)
    return users


async def update_user_password(
    username: str,
    password_hash: str,
    must_change: bool = False
):
    """Update user password"""
    await database.users.update_one(
        {"username": username},
        {"$set": {
            "password": password_hash,
            "must_change_password": must_change,
            "updated_at": datetime.utcnow()
        }}
    )


async def delete_user(username: str):
    """Delete user by username"""
    await database.users.delete_one({"username": username})


# ==================== TOPIC OPERATIONS ====================

async def create_topic(topic_data: dict) -> str:
    """
    Create a new topic.
    
    Args:
        topic_data: Topic configuration
        
    Returns:
        str: Created topic ID
    """
    topic_data["created_at"] = datetime.utcnow()
    result = await database.topics.insert_one(topic_data)
    return str(result.inserted_id)


async def get_topic(topic_id: str) -> Optional[dict]:
    """Get topic by ID"""
    try:
        topic = await database.topics.find_one({"_id": ObjectId(topic_id)})
        if topic:
            topic["_id"] = str(topic["_id"])
            topic["topic_id"] = str(topic["_id"])
        return topic
    except:
        return None


async def get_all_topics(skip: int = 0, limit: int = 100) -> List[dict]:
    """Get all topics with pagination"""
    cursor = database.topics.find().skip(skip).limit(limit)
    topics = []
    async for topic in cursor:
        topic["_id"] = str(topic["_id"])
        topic["topic_id"] = str(topic["_id"])
        topics.append(topic)
    return topics


async def update_topic(topic_id: str, update_data: dict):
    """Update topic configuration"""
    update_data["updated_at"] = datetime.utcnow()
    await database.topics.update_one(
        {"_id": ObjectId(topic_id)},
        {"$set": update_data}
    )


async def delete_topic(topic_id: str):
    """Delete topic by ID"""
    await database.topics.delete_one({"_id": ObjectId(topic_id)})


# ==================== TASK OPERATIONS ====================

async def create_task(task_data: dict) -> str:
    """
    Create a new classification task.
    
    Args:
        task_data: Task information
        
    Returns:
        str: Created task ID
    """
    task_data["created_at"] = datetime.utcnow()
    task_data["updated_at"] = datetime.utcnow()
    result = await database.tasks.insert_one(task_data)
    return str(result.inserted_id)


async def get_task(task_id: str) -> Optional[dict]:
    """
    Get task by ID or job_id.
    
    Args:
        task_id: Task _id or job_id
        
    Returns:
        dict: Task data or None
    """
    try:
        # Try ObjectId first
        task = await database.tasks.find_one({"_id": ObjectId(task_id)})
    except:
        # Try job_id
        task = await database.tasks.find_one({"job_id": task_id})
    
    if task:
        task["_id"] = str(task["_id"])
    return task


async def update_task(task_id: str, update_data: dict):
    """
    Update task data.
    
    Args:
        task_id: Task _id or job_id
        update_data: Fields to update
    """
    update_data["updated_at"] = datetime.utcnow()
    
    try:
        # Try ObjectId first
        await database.tasks.update_one(
            {"_id": ObjectId(task_id)},
            {"$set": update_data}
        )
    except:
        # Try job_id
        await database.tasks.update_one(
            {"job_id": task_id},
            {"$set": update_data}
        )


async def get_all_tasks(limit: int = 100, skip: int = 0) -> List[dict]:
    """Get all tasks with pagination"""
    cursor = database.tasks.find().sort("created_at", -1).skip(skip).limit(limit)
    tasks = []
    async for task in cursor:
        task["_id"] = str(task["_id"])
        tasks.append(task)
    return tasks


async def get_tasks_by_status(status: str, limit: int = 100) -> List[dict]:
    """Get tasks filtered by status"""
    cursor = database.tasks.find({"status": status}).sort("created_at", -1).limit(limit)
    tasks = []
    async for task in cursor:
        task["_id"] = str(task["_id"])
        tasks.append(task)
    return tasks


async def delete_task(task_id: str):
    """
    Delete task by ID or job_id.
    
    Args:
        task_id: Task _id or job_id
    """
    try:
        await database.tasks.delete_one({"_id": ObjectId(task_id)})
    except:
        await database.tasks.delete_one({"job_id": task_id})

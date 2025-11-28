"""Authentication routes"""
from fastapi import APIRouter, HTTPException, Depends, status
from backend.models import UserCreate, UserLogin, PasswordChange, UserResponse
from backend.auth import (
    verify_password, get_password_hash, create_access_token,
    get_current_user, get_current_admin
)
from backend.database import (
    create_user, get_user_by_username, get_all_users,
    update_user_password, delete_user
)
from typing import List

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/login")
async def login(credentials: UserLogin):
    """Login user"""
    user = await get_user_by_username(credentials.username)
    
    if not user or not verify_password(credentials.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    # Create access token
    access_token = create_access_token(data={"sub": user["username"]})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "username": user["username"],
            "role": user["role"],
            "must_change_password": user.get("must_change_password", False)
        }
    }


@router.post("/change-password")
async def change_password(
    password_data: PasswordChange,
    current_user: dict = Depends(get_current_user)
):
    """Change user password"""
    # Verify old password
    if not verify_password(password_data.old_password, current_user["password"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect old password"
        )
    
    # Update password
    new_password_hash = get_password_hash(password_data.new_password)
    await update_user_password(
        current_user["username"],
        new_password_hash,
        must_change=False
    )
    
    return {"message": "Password changed successfully"}


@router.get("/me")
async def get_me(current_user: dict = Depends(get_current_user)):
    """Get current user info"""
    return {
        "username": current_user["username"],
        "role": current_user["role"],
        "must_change_password": current_user.get("must_change_password", False)
    }


# Admin routes
@router.post("/users", dependencies=[Depends(get_current_admin)])
async def create_new_user(user_data: UserCreate):
    """Create new user (Admin only)"""
    # Check if user exists
    existing_user = await get_user_by_username(user_data.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )
    
    # Create user with default password
    password_hash = get_password_hash(user_data.password)
    user_id = await create_user(user_data.username, password_hash, user_data.role)
    
    return {
        "message": "User created successfully",
        "user_id": user_id,
        "username": user_data.username,
        "default_password": user_data.password
    }


@router.get("/users", dependencies=[Depends(get_current_admin)])
async def list_users():
    """List all users (Admin only)"""
    users = await get_all_users()
    return {
        "users": [
            {
                "username": u["username"],
                "role": u["role"],
                "must_change_password": u.get("must_change_password", False),
                "created_at": u["created_at"]
            }
            for u in users
        ]
    }


@router.delete("/users/{username}", dependencies=[Depends(get_current_admin)])
async def remove_user(username: str):
    """Delete user (Admin only)"""
    if username == "admin":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete admin user"
        )
    
    user = await get_user_by_username(username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    await delete_user(username)
    return {"message": "User deleted successfully"}

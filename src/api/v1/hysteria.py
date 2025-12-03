from fastapi import APIRouter, HTTPException, status

from src.schemas.hysteria import UserCreate, UserListResponse, UserConfigResponse
from src.services.hysteria import hysteria_service

router = APIRouter(tags=["Hysteria"])


@router.get("/users", response_model=UserListResponse)
async def get_users():
    users = hysteria_service.get_users()
    return UserListResponse(users=users)


@router.get("/users/{username}/config", response_model=UserConfigResponse)
async def get_user_config(username: str):
    try:
        uri = hysteria_service.get_connection_uri(username)
        return UserConfigResponse(uri=uri)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post("/users", status_code=status.HTTP_201_CREATED)
async def add_user(user_data: UserCreate):
    hysteria_service.add_user(user_data.username, user_data.password)
    return {"message": f"User {user_data.username} added"}


@router.delete("/users/{username}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_user(username: str):
    deleted = hysteria_service.remove_user(username)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {username} not found"
        )

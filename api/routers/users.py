from enum import Enum
from typing import Dict
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from ..dependencies import get_token_header


router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "dot found"}},
)


class Category(Enum):
    WEB3 = "web3"
    NONWEB3 = "non-web3"


class User(BaseModel):
    name: str
    verified: bool
    id: int
    category: Category


users: Dict[int, User] = {
    0: User(name="test1", verified=True, id=0, category=Category.NONWEB3),
    1: User(name="test2", verified=False, id=1, category=Category.WEB3),
    2: User(name="test1", verified=True, id=2, category=Category.NONWEB3),
    3: User(name="test2", verified=False, id=3, category=Category.WEB3),
}


@router.get("/")
def read_users() -> dict[str, Dict[int, User]]:
    return {"users": users}


@router.post("/")
def create_users(user: User) -> dict[str, User]:
    if user.id in users:
        raise HTTPException(status_code=400, detail=f"id {user.id} already exits")
    users[user.id] = user
    return {"users": user}


@router.get("/{user_id}")
def read_user(user_id: int) -> Dict[str, User | str]:
    if user_id not in users:
        raise HTTPException(status_code=404, detail=f"id {user_id} does not exist.")
    if user_id > len(users):
        return {"message": "invalid ID"}
    return {"users": users[user_id]}


@router.put(
    "/{user_id}",
    tags=["custom"],
    responses={403: {"description": "operation forbidden"}},
)
def update_users(user_id: int, user: User) -> dict[str, User]:
    if user_id is not user.id:
        raise HTTPException(status_code=400, detail=f"id {user_id} is invalid")
    if user.id not in users:
        raise HTTPException(status_code=400, detail=f"id {user_id} does not exits")
    users[user_id] = user
    return {"users": user}


@router.delete("/{user_id}")
def delete_users(user_id: int) -> dict[str, User]:
    if user_id not in users:
        raise HTTPException(status_code=404, detail=f"id {user_id} does not exist.")
    user = users.pop(user_id)
    return {"users": user}


@router.get("/status")
def read_users_by_status(completed: bool | None) -> dict[str, list[User]]:
    if completed is None:
        raise HTTPException(status_code=400, detail="completed status required")
    filtered_users = []
    for user in users.values():
        if user.verified is completed:
            filtered_users.append(user)

    # filtered_users = [user for user in users.values() if user.completed is completed]
    return {"users": filtered_users}

from enum import Enum
from typing import Dict, Union
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import shopify
import os

load_dotenv()

app = FastAPI()
access_token = os.getenv("SHOPIFY_ACCESS_TOKEN")
api_version = os.getenv("SHOPIFY_API_VERSION")
shop_url = os.getenv("SHOPIFY_SHOP_URL")
shop_name = os.getenv("SHOPIFY_SHOP_NAME")


class Category(Enum):
    PERSONAL = "personal"
    WORK = "work"


class Todo(BaseModel):
    title: str
    completed: bool
    id: int
    category: Category


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


items: list[Item] = [Item(name="fish", price=10.5, is_offer=True)]

todos: Dict[int, Todo] = {
    0: Todo(title="test1", completed=True, id=0, category=Category.WORK),
    1: Todo(title="test2", completed=False, id=1, category=Category.PERSONAL),
    2: Todo(title="test1", completed=True, id=2, category=Category.WORK),
    3: Todo(title="test2", completed=False, id=3, category=Category.PERSONAL),
}


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/shopify")
def shopify_session():
    session = shopify.Session(shop_url, api_version, access_token)
    shopify.ShopifyResource.activate_session(session)

    shop = shopify.Shop.current()
    product = shopify.Product.find()
    print(product)
    return {"Hello": "World"}


@app.get("/todos")
def read_todos() -> dict[str, Dict[int, Todo]]:
    return {"todos": todos}


@app.post("/todos")
def create_todos(todo: Todo) -> dict[str, Todo]:
    if todo.id in todos:
        raise HTTPException(status_code=400, detail=f"id {todo.id} already exits")
    todos[todo.id] = todo
    return {"todos": todo}


@app.put("/todos/{todo_id}")
def update_todos(todo_id: int, todo: Todo) -> dict[str, Todo]:
    if todo_id is not todo.id:
        raise HTTPException(status_code=400, detail=f"id {todo_id} is invalid")
    if todo.id not in todos:
        raise HTTPException(status_code=400, detail=f"id {todo_id} does not exits")
    todos[todo_id] = todo
    return {"todos": todo}


@app.delete("/todos/{todo_id}")
def delete_todos(todo_id: int) -> dict[str, Todo]:
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail=f"id {todo_id} does not exist.")
    todo = todos.pop(todo_id)
    return {"todos": todo}


@app.get("/todos/status")
def read_todos_by_status(completed: bool | None) -> dict[str, list[Todo]]:
    if completed is None:
        raise HTTPException(status_code=400, detail="completed status required")
    filtered_todos = []
    for todo in todos.values():
        if todo.completed is completed:
            filtered_todos.append(todo)

    # filtered_todos = [todo for todo in todos.values() if todo.completed is completed]
    return {"todos": filtered_todos}


@app.get("/todos/{todo_id}")
def read_todo(todo_id: int) -> Dict[str, Todo | str]:
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail=f"id {todo_id} does not exist.")
    if todo_id > len(todos):
        return {"message": "invalid ID"}
    return {"todos": todos[todo_id]}

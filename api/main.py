from enum import Enum
from typing import Dict, Union
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


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


@app.get("/items")
def read_items(name: Union[str, None] = None):
    for item in items:
        if item.name == name:
            return {"data": {"item_name": name}, "message": "success"}
    if name is None:
        return {"message": "not available"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_price": item.price, "item_id": item_id}

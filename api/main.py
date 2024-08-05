from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

from api import dependencies
from api.routers import shopify, users
from api.internal import admin

load_dotenv()

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(users.router)
app.include_router(shopify.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(dependencies.get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)


@app.exception_handler(Exception)
def global_exception_handler(request: Request, exc: Exception):
    print(exc)
    print(request)
    return JSONResponse(status_code=500, content={"message": "Internal server error"})

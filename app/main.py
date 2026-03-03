from fastapi import FastAPI
from app.api.v1 import routes

app = FastAPI(title = "Learning FastAPI")
print(10/0)

app.include_router(routes.router, prefix = "/api/v1")

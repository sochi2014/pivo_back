from fastapi import FastAPI

from .api.v1 import test_routes
from .database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(test_routes.router, tags=["pivo"])

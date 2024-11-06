from fastapi import FastAPI

from .api.v1 import test_routes, auth_api, users_api, beer_routes
from .database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(test_routes.router, tags=["pivo"])
app.include_router(auth_api.router, tags=["auth"])
app.include_router(users_api.router, tags=["user"])

app.include_router(beer_routes.router, tags=["beer"])

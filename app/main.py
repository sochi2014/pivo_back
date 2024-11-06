from fastapi import FastAPI

from .api.v1 import test_routes, address_routes, auth_routes, users_routes, beer_routes
from .database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(test_routes.router, tags=["pivo"])
app.include_router(auth_routes.router, tags=["auth"])
app.include_router(users_routes.router, tags=["user"])
app.include_router(address_routes.router, tags=["address"])
app.include_router(beer_routes.router, tags=["beer"])

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.v1 import test_routes, address_routes, auth_routes, users_routes, beer_routes, place_routes, \
    filter_routes, feedback_routes, geoposition_routes, level_routes
from .database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

# app.include_router(test_routes.router, tags=["pivo"])
app.include_router(auth_routes.router, tags=["auth"])
app.include_router(users_routes.router, tags=["user"])
app.include_router(address_routes.router, tags=["address"])
app.include_router(beer_routes.router, tags=["beer"])
app.include_router(place_routes.router, tags=["place"])
app.include_router(filter_routes.router, tags=["filters"])
app.include_router(feedback_routes.router, tags=["feedback"])
app.include_router(level_routes.router, tags=["level"])
app.include_router(geoposition_routes.router, tags=["geopos"])


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
from fastapi import FastAPI
from src.api.routers import users, properties, auth

app = FastAPI()

app.include_router(users.router)
app.include_router(properties.router)
app.include_router(auth.router)

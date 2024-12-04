from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routes import router as v1_router
from app.core.db import MongoDB

@asynccontextmanager
async def lifespan(app: FastAPI):
    MongoDB.connect_to_mongo()
    yield
    MongoDB.close_mongo_connection()

app = FastAPI(title="Content Service", lifespan=lifespan, root_path="/content")

app.include_router(v1_router, prefix="/api/v1")

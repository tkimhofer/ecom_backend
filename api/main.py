from fastapi import FastAPI
from api.v1.routes import router as v1_router
from contextlib import asynccontextmanager
from api.db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    init_db()
    yield
    # Optional: Add shutdown logic here


tags_metadata = [
    {
        "name": "Raw Layer",
        "description": "Endpoints for ingesting unprocessed external data (e.g., webhook dumps, raw payloads).",
    },
    {
        "name": "Staging Layer",
        "description": "Endpoints for validating and transforming data before it enters core business logic.",
    },
    {
        "name": "Business Layer",
        "description": "Main domain logic APIs for managing orders, customers, payments, and other core entities.",
    },
    {
        "name": "Monitoring",
        "description": "Endpoints for checking service health, uptime, and internal status.",
    },
    {
        "name": "Admin",
        "description": "Restricted endpoints for administrative or developer operations.",
    },
    {
        "name": "Internal",
        "description": "Private endpoints not meant for public/external clients.",
    },
]

app = FastAPI(
    title="ShopMate E-Commerce API",
    description="Backend API for handling ingestion, processing, and management of e-commerce operations.",
    version="1.0.0",
    openapi_tags=tags_metadata,
    lifespan=lifespan,
)

app.include_router(v1_router, prefix="/v1")
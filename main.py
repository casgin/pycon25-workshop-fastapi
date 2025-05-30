from fastapi import FastAPI
from routes.message_routes import router as message_router

app = FastAPI(
    title="My FastAPI Application",
    description="This is a sample FastAPI application.",
    version="1.0.0",
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
    contact={
        "name": "Support Team",
        "email": "",
        "url": "https://2025.pycon.it/en/event/fastapi-from-hello-world-to-production"
    },
)

# Include the message router
app.include_router(message_router)
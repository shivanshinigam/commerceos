"""
FastAPI Main Application Entry Point
Google UCP 2026 Specification Server
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import ucp_profile, ucp_checkout, ucp_complete

# Initialize DB Tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Google UCP 2026 Merchant Server",
    description="Production-ready REST API implementing Google's Universal Commerce Protocol (UCP) for Agentic Commerce.",
    version="2026-04-08"
)

# CORS Config
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Routers
app.include_router(ucp_profile.router)
app.include_router(ucp_checkout.router)
app.include_router(ucp_complete.router)

@app.get("/", summary="Root Health Check")
async def root_health():
    return {
        "status": "active",
        "service": "Google UCP 2026 Merchant Server",
        "specVersion": "2026-04-08",
        "profileEndpoint": "/.well-known/ucp",
        "checkoutSessionsEndpoint": "/ucp/v1/checkout-sessions"
    }

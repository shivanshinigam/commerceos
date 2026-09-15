from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
import os

from ucp_routes import router as ucp_router
from agent import router as agent_router

app = FastAPI(title="CommerceOS UCP Lab")

# Serve API routes
app.include_router(ucp_router)
app.include_router(agent_router)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    """Serve the main frontend UI."""
    return FileResponse("static/index.html")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=7860, reload=True)

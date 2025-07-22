from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, Response
import os

from mockapi.api.router import router
from mockapi.core.dependencies import get_settings

# Use settings provider for environment variables
settings = get_settings()

app = FastAPI(
    title="MockGen: AI-Powered Mock API Generator",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Include the main API router
app.include_router(router)

# Basic health check endpoint
@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}

# Add CORS middleware to allow all origins, which is useful for development.
# For production, you might want to restrict this to your frontend's domain.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

STATIC_DIR = os.getenv("STATIC_DIR")

if STATIC_DIR and os.path.exists(STATIC_DIR):
    # Mount the static files directory containing the built Vue.js app
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

    # This catch-all route serves the Vue app's index.html for any path
    # that is not an API endpoint. This is essential for single-page applications.
    @app.get("/{full_path:path}", include_in_schema=False)
    async def serve_vue_frontend(full_path: str):
        # Prevent API docs or mock routes from being overridden by the frontend
        if full_path.startswith(("docs", "redoc", "mocks/", "health")):
            return Response("Not Found", status_code=404)

        index_path = os.path.join(STATIC_DIR, "index.html")
        if os.path.exists(index_path):
            return FileResponse(index_path)
        
        return Response("Frontend not found.", status_code=404)
else:
    print("-" * 80)
    print("WARNING: STATIC_DIR environment variable is not set or directory not found.")
    print("The frontend will not be served by FastAPI.")
    print("This is expected during local development if you run the Vue dev server separately.")
    print("-" * 80)
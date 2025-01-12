from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import router
from app.ui.writer_ui import WriterUI
from app.core.config import settings
import uvicorn
import threading
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Essay Writer API",
    description="AI-powered essay writing assistant",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api")

# Initialize UI
ui = WriterUI()

def run_api():
    """Run the FastAPI application"""
    try:
        uvicorn.run(
            "app.main:app",
            host=settings.HOST,
            port=settings.PORT,
            reload=True
        )
    except Exception as e:
        logger.error(f"Failed to start API server: {e}")
        raise

def run_ui():
    """Run the Gradio UI"""
    try:
        ui.launch()
    except Exception as e:
        logger.error(f"Failed to start Gradio UI: {e}")
        raise

if __name__ == "__main__":
    try:
        # Start API in a separate thread
        api_thread = threading.Thread(target=run_api)
        api_thread.start()

        # Start UI in main thread
        run_ui()
    except Exception as e:
        logger.error(f"Application startup failed: {e}")
        raise
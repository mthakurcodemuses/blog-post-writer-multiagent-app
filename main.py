import uvicorn
from app import app
from app.core.config import settings
from app.ui.writer_ui import WriterUI
import threading

def run_api():
    """Run the FastAPI application"""
    uvicorn.run(
        app,
        host=settings.HOST,
        port=settings.PORT
    )

def run_ui():
    """Run the Gradio UI"""
    ui = WriterUI()
    ui.launch()

if __name__ == "__main__":
    # Start API in a separate thread
    api_thread = threading.Thread(target=run_api)
    api_thread.start()

    # Start UI in main thread
    run_ui()

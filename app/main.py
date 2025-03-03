from fastapi import FastAPI
import uvicorn

from app.api.transcription import router as transcription_router

app = FastAPI(
    title="Transcripter API",
    description="API for transcribing audio and video files",
    version="0.1.0"
)

# Include the transcription router
app.include_router(transcription_router)

def start():
    """Start the FastAPI application using uvicorn."""
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        timeout_keep_alive=3000000000,
        timeout_graceful_shutdown=5,
    )

if __name__ == "__main__":
    start() 
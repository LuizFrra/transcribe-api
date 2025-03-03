import os
import tempfile
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, UploadFile, HTTPException, Depends
import asyncio

from app.dependencies import get_transcription_handler
from app.transcription.handler import TranscriptionHandler

router = APIRouter()

@router.post("/transcribe/", response_model=str)
async def transcribe_file(
    file: UploadFile,
    handler: Annotated[TranscriptionHandler, Depends(get_transcription_handler)]
):
    """
    Endpoint to transcribe audio from a video or audio file.
    
    Args:
        file (UploadFile): The audio or video file to transcribe
        handler (TranscriptionHandler): The transcription handler dependency
        
    Returns:
        str: The transcribed text
        
    Raises:
        HTTPException: If the file format is not supported
    """
    return await asyncio.wait_for(handler.handle_file(file), timeout=300000)
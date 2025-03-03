from typing import Annotated
from fastapi import Depends

from app.transcription.interface import TranscriptionService
from app.transcription.handler import TranscriptionHandler
from app.transcription.whisperx_service import WhisperXService

def get_transcription_service() -> TranscriptionService:
    """
    Factory function for TranscriptionService dependency.
    This should be overridden in production with actual implementation.
    """
    return WhisperXService()

def get_transcription_handler(
    service: Annotated[TranscriptionService, Depends(get_transcription_service)]
) -> TranscriptionHandler:
    """
    Factory function for TranscriptionHandler dependency.
    """
    return TranscriptionHandler(service) 
import os
import tempfile
from pathlib import Path

from fastapi import UploadFile, HTTPException
import moviepy

from app.transcription.interface import TranscriptionService

class TranscriptionHandler:
    def __init__(self, transcription_service: TranscriptionService):
        self.transcription_service = transcription_service
        
    async def handle_file(self, file: UploadFile) -> str:
        # Create a temporary directory to store the uploaded file
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir_path = Path(temp_dir)
            
            # Save the uploaded file
            file_path = temp_dir_path / file.filename
            with open(file_path, "wb") as buffer:
                content = await file.read()
                buffer.write(content)
            
            # Check file extension
            file_extension = file_path.suffix.lower()
            audio_path = file_path
            
            # If it's a video file, extract the audio
            if file_extension in ['.mp4', '.avi', '.mov', '.mkv']:
                audio_path = temp_dir_path / f"{file_path.stem}.mp3"
                video = moviepy.VideoFileClip(str(file_path))
                video.audio.write_audiofile(str(audio_path))
                video.close()
            elif file_extension not in ['.mp3', '.wav', '.ogg', '.m4a']:
                raise HTTPException(
                    status_code=400,
                    detail="Unsupported file format. Please upload an audio or video file."
                )
            
            # Transcribe the audio
            transcription = await self.transcription_service.transcribe_audio(audio_path)
            return transcription 
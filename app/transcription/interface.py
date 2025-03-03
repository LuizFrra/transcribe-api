from abc import ABC, abstractmethod
from pathlib import Path

class TranscriptionService(ABC):
    @abstractmethod
    async def transcribe_audio(self, audio_path: Path) -> str:
        """
        Transcribe an audio file to text.
        
        Args:
            audio_path (Path): Path to the audio file
            
        Returns:
            str: The transcribed text
        """
        pass 
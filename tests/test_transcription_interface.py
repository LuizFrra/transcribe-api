import pytest
from pathlib import Path
from app.transcription.interface import TranscriptionService

class TestTranscriptionService:
    async def test_transcribe_audio_abstract_method(self):
        """Test that TranscriptionService cannot be instantiated directly"""
        with pytest.raises(TypeError) as exc_info:
            TranscriptionService()
        assert "Can't instantiate abstract class TranscriptionService" in str(exc_info.value)
    
    async def test_mock_transcription_service(self, test_files_dir):
        """Test that a concrete implementation of TranscriptionService works"""
        from tests.conftest import MockTranscriptionService
        
        service = MockTranscriptionService()
        audio_path = test_files_dir / "test_audio.mp3"
        
        result = await service.transcribe_audio(audio_path)
        assert isinstance(result, str)
        assert "Mocked transcription for test_audio.mp3" == result 
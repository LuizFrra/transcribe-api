import os
import pytest
from pathlib import Path
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from app.transcription.interface import TranscriptionService
from app.transcription.handler import TranscriptionHandler
from app.main import app
import app.dependencies as deps

# Mock VideoFileClip
class MockVideoFileClip:
    def __init__(self, filename):
        self.filename = filename
        self.audio = MagicMock()
        self.audio.write_audiofile = MagicMock()
    
    def close(self):
        pass

class MockTranscriptionService(TranscriptionService):
    async def transcribe_audio(self, audio_path: Path) -> str:
        # Mock implementation that returns a fixed response
        return f"Mocked transcription for {audio_path.name}"

@pytest.fixture
def mock_transcription_service():
    return MockTranscriptionService()

@pytest.fixture
def test_client(monkeypatch, mock_transcription_service):
    # Mock VideoFileClip
    import moviepy
    monkeypatch.setattr(moviepy, "VideoFileClip", MockVideoFileClip)
    
    # Override the transcription service dependency
    def get_mock_service():
        return mock_transcription_service
    
    app.dependency_overrides[deps.get_transcription_service] = get_mock_service
    
    # Create a test client
    client = TestClient(app)
    
    yield client
    
    # Clean up
    app.dependency_overrides.clear()

@pytest.fixture
def test_files_dir():
    # Get the path to the test files directory
    return Path(__file__).parent / "test_files"

@pytest.fixture(autouse=True)
def setup_test_files(test_files_dir):
    # Create test files directory if it doesn't exist
    test_files_dir.mkdir(exist_ok=True)
    
    # Create a test audio file
    audio_file = test_files_dir / "test_audio.mp3"
    if not audio_file.exists():
        audio_file.write_bytes(b"mock audio content")
    
    # Create a test video file
    video_file = test_files_dir / "test_video.mp4"
    if not video_file.exists():
        video_file.write_bytes(b"mock video content")
    
    yield
    
    # Cleanup (optional, since we might want to keep test files for inspection)
    # for file in test_files_dir.glob("*"):
    #     file.unlink()
    # test_files_dir.rmdir() 
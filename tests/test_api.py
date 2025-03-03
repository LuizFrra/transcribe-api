import pytest
from pathlib import Path
from fastapi import UploadFile
from app.transcription.handler import TranscriptionHandler

class TestTranscriptionAPI:
    def test_transcribe_endpoint_audio(self, test_client, test_files_dir):
        """Test transcribing an audio file"""
        audio_path = test_files_dir / "test_audio.mp3"
        
        with open(audio_path, "rb") as f:
            response = test_client.post(
                "/transcribe/",
                files={"file": ("test_audio.mp3", f, "audio/mpeg")}
            )
        
        assert response.status_code == 200
        assert response.text == f'"Mocked transcription for test_audio.mp3"'
    
    def test_transcribe_endpoint_video(self, test_client, test_files_dir):
        """Test transcribing a video file"""
        video_path = test_files_dir / "test_video.mp4"
        
        with open(video_path, "rb") as f:
            response = test_client.post(
                "/transcribe/",
                files={"file": ("test_video.mp4", f, "video/mp4")}
            )
        
        assert response.status_code == 200
        # The mock service will receive the extracted audio file
        assert "Mocked transcription for" in response.text
    
    def test_transcribe_endpoint_unsupported_format(self, test_client, test_files_dir):
        """Test uploading an unsupported file format"""
        # Create a temporary text file
        text_file = test_files_dir / "test.txt"
        text_file.write_text("This is a test file")
        
        with open(text_file, "rb") as f:
            response = test_client.post(
                "/transcribe/",
                files={"file": ("test.txt", f, "text/plain")}
            )
        
        assert response.status_code == 400
        assert "Unsupported file format" in response.json()["detail"]
        
        # Cleanup
        text_file.unlink()

class TestTranscriptionHandler:
    async def test_handle_file_audio(self, test_files_dir, mock_transcription_service):
        """Test handling an audio file with TranscriptionHandler"""
        handler = TranscriptionHandler(mock_transcription_service)
        audio_path = test_files_dir / "test_audio.mp3"
        
        # Create an UploadFile instance
        with open(audio_path, "rb") as f:
            upload_file = UploadFile(
                filename="test_audio.mp3",
                file=f
            )
            result = await handler.handle_file(upload_file)
        
        assert isinstance(result, str)
        assert "Mocked transcription for" in result
    
    async def test_handle_file_video(self, test_files_dir, mock_transcription_service, monkeypatch):
        """Test handling a video file with TranscriptionHandler"""
        from tests.conftest import MockVideoFileClip
        import moviepy
        
        # Mock VideoFileClip
        monkeypatch.setattr(moviepy, "VideoFileClip", MockVideoFileClip)
        
        handler = TranscriptionHandler(mock_transcription_service)
        video_path = test_files_dir / "test_video.mp4"
        
        # Create an UploadFile instance
        with open(video_path, "rb") as f:
            upload_file = UploadFile(
                filename="test_video.mp4",
                file=f
            )
            result = await handler.handle_file(upload_file)
        
        assert isinstance(result, str)
        assert "Mocked transcription for" in result 
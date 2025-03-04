from pathlib import Path
import torch
import whisperx
import logging
from .interface import TranscriptionService
import torch

class WhisperXService(TranscriptionService):
    def __init__(self, device: str = "cuda" if torch.cuda.is_available() else "cpu", 
                 compute_type: str = "float16" if torch.cuda.is_available() else "int8",
                 batch_size: int = 16,
                 language: str = "en"):
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"CUDA available: {torch.cuda.is_available()}")
        if torch.cuda.is_available():
            self.logger.info(f"Using CUDA device: {torch.cuda.get_device_name(0)}")
        self.device = device
        self.compute_type = compute_type
        self.batch_size = batch_size
        self.language = language
        # Load models
        self.model = whisperx.load_model("large-v2", self.device, compute_type=self.compute_type)
        self.diarize_model = whisperx.DiarizationPipeline(use_auth_token="", device=self.device)
        self.align_model, self.metadata = whisperx.load_align_model(language_code=self.language, device=self.device)

    async def transcribe_audio(self, audio_path: Path) -> str:
        """
        Transcribe an audio file to text using WhisperX with diarization.
        
        Args:
            audio_path (Path): Path to the audio file
            
        Returns:
            str: The transcribed text with speaker diarization
        """
        try:
            # Transcribe with original whisper model
            audio = whisperx.load_audio(str(audio_path))
            result = self.model.transcribe(audio, batch_size=self.batch_size)
            
            # Align whisper output
            result = whisperx.align(result["segments"], model=self.align_model, align_model_metadata=self.metadata, audio=audio, device=self.device, 
                                  return_char_alignments=False)

            # Get speaker diarization
            diarize_segments = self.diarize_model(audio)
            
            # Assign speaker labels
            result = whisperx.assign_word_speakers(diarize_segments, result)
            
            # Format output with speaker labels and timestamps
            formatted_output = []
            for segment in result["segments"]:
                speaker = segment.get("speaker", "UNKNOWN")
                start = round(segment["start"], 2)
                end = round(segment["end"], 2)
                text = segment["text"].strip()
                formatted_output.append(f"[{speaker}] ({start}s-{end}s): {text}")
            
            self.logger.info("Transcription segments: %s", formatted_output)
            return "\n".join(formatted_output)
            
        except Exception as e:
            self.logger.error("Error during transcription: %s", str(e))
            raise e
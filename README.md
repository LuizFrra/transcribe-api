# Transcripter API

A FastAPI-based service for transcribing audio from video and audio files.

## Features

- Support for various audio formats (mp3, wav, ogg, m4a)
- Support for video formats (mp4, avi, mov, mkv) with automatic audio extraction
- Async processing
- Easy to extend with custom transcription services

## Installation

```bash
poetry install --with test
```

## Running Tests

```bash
poetry run pytest
```

## Running the Server

```bash
poetry run uvicorn app.main:app --reload
```

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc #   t r a n s c r i b e - a p i  
 
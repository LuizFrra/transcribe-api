# Transcripter API

A FastAPI-based service for transcribing audio from video and audio files.

## Features

- Support for various audio formats (mp3, wav, ogg, m4a)
- Support for video formats (mp4, avi, mov, mkv) with automatic audio extraction
- Async processing for improved performance
- Easy to extend with custom transcription services
- RESTful API with comprehensive documentation
- Error handling and validation
- Progress tracking for long-running transcription tasks

## Prerequisites

- Python 3.8+
- Poetry for dependency management
- FFmpeg (for video processing)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/transcribe-api.git
cd transcribe-api
```

2. Install dependencies:
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

The server will start at `http://localhost:8000`

## API Documentation

Once the server is running, you can access the API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

- `POST /transcribe`: Upload and transcribe audio/video files
- `GET /status/{task_id}`: Check transcription status
- `GET /result/{task_id}`: Retrieve transcription results

## Configuration

The service can be configured through environment variables:
- `MAX_FILE_SIZE`: Maximum allowed file size (default: 100MB)
- `ALLOWED_FORMATS`: Comma-separated list of allowed file formats
- `TRANSCRIPTION_SERVICE`: Selected transcription service (default: "whisper")

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

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

## How to use cuda

1. Install cuda 11.8

2. Download dll from https://github.com/Purfview/whisper-standalone-win/releases/tag/libs

3. Put the downloaded dlls in the bin folder from cuda 

4. Rename the dll cublas64_11.dll to cublas64_12.dll
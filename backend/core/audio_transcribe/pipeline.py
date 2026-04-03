# core/audio_transcribe/pipeline.py

import logging
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

logger = logging.getLogger(__name__)

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

TRANSCRIPTION_MODEL = "gemini-2.5-flash-lite"

SUPPORTED_TYPES = [
    "audio/webm",
    "audio/webm;codecs=opus",
    "audio/mp4",
    "audio/wav",
    "audio/ogg"
]

def transcribe_audio(audio_bytes: bytes, mime_type: str) -> str:
    clean_mime = mime_type.split(";")[0].strip()

    response = client.models.generate_content(
        model=TRANSCRIPTION_MODEL,
        contents=[
            types.Content(parts=[
                types.Part(
                    inline_data=types.Blob(
                        mime_type=clean_mime,
                        data=audio_bytes
                    )
                ),
                types.Part(text="Transcreva o áudio.")
            ])
        ]
    )

    logger.debug("Transcription MIME: %s, audio size: %d bytes", clean_mime, len(audio_bytes))

    return response.text.strip() if response.text else ""
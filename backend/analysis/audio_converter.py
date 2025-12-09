from pydub import AudioSegment
import io

# Map MIME types to pydub formats
MIME_TO_FORMAT = {
    "audio/mpeg": "mp3",
    "audio/wav": "wav",
    "audio/x-wav": "wav",
    "audio/ogg": "ogg",
    "audio/flac": "flac",
}

def convert_to_wav_in_memory(audio_bytes: bytes, mime_type: str):
    """
    Convert any supported audio format to WAV in memory.

    Arguments: 
        audio_bytes: Raw audio file bytes.
        mime_type: MIME type of the audio file.

    Return: WAV bytes ready for librosa/OpenL3.

    """
    if mime_type in ("audio/wav", "audio/x-wav"):
        # Already WAV, return as-is
        return audio_bytes
    
    file_format = MIME_TO_FORMAT.get(mime_type)
    if not file_format:
        raise ValueError("Unsupported audio format. Please upload WAV, MP3, OGG, or FLAC.")
    
    # Read audio from bytes in memory
    try:
        audio = AudioSegment.from_file(io.BytesIO(audio_bytes), format=file_format)
    except Exception as e:
        raise ValueError(f"Error processing audio file: {str(e)}")

    # Export to WAV into a BytesIO buffer
    try:
        wav_io = io.BytesIO()
        audio.export(wav_io, format="wav")
        wav_io.seek(0)
        return wav_io.read()
    except Exception as e:
        raise ValueError(f"Error exporting audio to WAV: {str(e)}")
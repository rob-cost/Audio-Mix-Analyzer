from fastapi import UploadFile

from analysis.utils.helper import to_python
from analysis.utils.process_pool_executor import run_in_processpool

"""

Check max file size and file type uploaded.
Run process pool executor

Return:
    Report dictionary with analysis data

"""

# --- SET MAX FILE SIZE ---

MAX_FILE_SIZE_MB = 110
MAX_FILE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024


# --- SET ALLOWED AUDIO TYPES ---

ALLOWED_TYPES = {"audio/wav", "audio/mpeg", "audio/ogg", "audio/flac", "audio/x-wav" }


# --- PROCESS FILE UPLOADED ---

async def process_file(file:UploadFile):
    audio_bytes = await file.read()

    if len(audio_bytes) > MAX_FILE_BYTES:
        return {"error": f"File too large. Max is {MAX_FILE_SIZE_MB} MB."}
    
    if file.content_type not in ALLOWED_TYPES:
        return {"error": "Unsupported audio format"}
    
    try:
        report = await run_in_processpool(audio_bytes, file.content_type)
        return to_python(report)
    
    except ValueError as e:
        return {"success": False, "error": str(e)}
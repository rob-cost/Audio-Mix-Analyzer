import os
import asyncio

from fastapi import FastAPI, UploadFile, File, Request
from fastapi.middleware.cors import CORSMiddleware
from concurrent.futures import ProcessPoolExecutor
from slowapi import Limiter
from slowapi.util import get_remote_address


from analysis.pipeline import analyze_uploaded_track_complete
from analysis.helper import to_python


app = FastAPI()

executor = ProcessPoolExecutor(max_workers=os.cpu_count() - 1) # make sure 1 core is left for security reason

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

app.add_middleware(
    CORSMiddleware,
    allow_origins = ['http://localhost:5173'],
    allow_methods = ['POST'],
    allow_headers = ['*']
)


# --- SET MAX FILE SIZE ---

MAX_FILE_SIZE_MB = 110
MAX_FILE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024


# --- SET ALLOWED AUDIO TYPES

ALLOWED_TYPES = {"audio/wav", "audio/mpeg", "audio/ogg", "audio/flac", "audio/x-wav" }


# --- HELPER CPU PROCESSOR ---

async def run_in_processpool(audio_bytes: bytes, mime: str):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor (
        executor,
        analyze_uploaded_track_complete,
        audio_bytes,
        mime
    )

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
    

# --- ENDPOINTS ---

@app.post("/analyze")
@limiter.limit("5/minute") # Limit amount of request per IP
async def analyze(request: Request, file:UploadFile = File(...)):
    return await process_file(file)

@app.post("5/analyze_reference")
@limiter.limit("20/minute")
async def analyze_reference(request: Request, file:UploadFile = File(...)):
    return await process_file(file)

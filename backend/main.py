from fastapi import FastAPI, UploadFile, File, Request, HTTPException
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address
import asyncio


from analysis.llm.audio_analysis_generator import generate_report
from pipeline.analyze_track_complete import analyze_uploaded_track_complete

app = FastAPI()


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


# --- SET ALLOWED AUDIO TYPES ---

ALLOWED_TYPES = {"audio/wav", "audio/mpeg", "audio/ogg", "audio/flac", "audio/x-wav" }




# --- ENDPOINTS ---

@app.post("/analyze_and_report")
@limiter.limit("5/minute") # Limit amount of request per IP
async def analyze(request: Request, track_file: UploadFile, ref_file: Optional[UploadFile] = None):

    # Read files async
    audio_bytes = await track_file.read()
    ref_bytes = await ref_file.read() if ref_file else None

    # Validate uploaded files
    if len(audio_bytes) or len(ref_bytes) > MAX_FILE_BYTES:
        raise HTTPException(status_code=400, detail=f"File too large. Max is {MAX_FILE_SIZE_MB} MB.")
    
    if track_file.content_type or ref_file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Unsupported audio format")

    # Run CPU-bound analysis in separate threads
    features, ref_features = await asyncio.gather(
        asyncio.to_thread(analyze_uploaded_track_complete, audio_bytes, track_file.content_type),
        asyncio.to_thread(analyze_uploaded_track_complete, ref_bytes, ref_file.content_type) if ref_file else asyncio.sleep(0, result=None)
    )

    # Generate AI report (async if needed)
    report = await generate_report(features, ref_features)

    return {"features": features, "ref_features": ref_features, "report": report}

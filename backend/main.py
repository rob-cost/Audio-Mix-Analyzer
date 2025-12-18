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
async def analyze(
    request: Request, 
    main_audio_file: UploadFile = File(...), 
    ref_audio_file: Optional[UploadFile] = File (None)
    ):

    # Read files async
    try:
        main_audio_bytes = await main_audio_file.read()
        ref_audio_bytes = await ref_audio_file.read() if ref_audio_file else None

    except Exception as e:
        print(f"Error in converting files: {e}")

    # Validate uploaded files
    try:
        if len(main_audio_bytes) > MAX_FILE_BYTES:
            raise HTTPException(status_code=400, detail=f"Main file too large. Max is {MAX_FILE_SIZE_MB} MB.")
        
        if ref_audio_bytes and len(ref_audio_bytes) > MAX_FILE_BYTES:
            raise HTTPException(status_code=400, detail=f"Reference file too large. Max is {MAX_FILE_SIZE_MB} MB.")
        
        if main_audio_file.content_type not in ALLOWED_TYPES:
            raise HTTPException(status_code=400, detail="Main file unsupported audio format")
        
        if ref_audio_file and ref_audio_file.content_type not in ALLOWED_TYPES:
            raise HTTPException(status_code=400, detail="Reference file unsupported audio format")
    except Exception as e:
        print(f"Error in validating: {e}")


    # Run CPU-bound analysis in separate threads
    try:
        features, ref_features = await asyncio.gather(
            asyncio.to_thread(analyze_uploaded_track_complete, main_audio_bytes, main_audio_file.content_type),
            asyncio.to_thread(analyze_uploaded_track_complete, ref_audio_bytes, ref_audio_file.content_type) if ref_audio_file else asyncio.sleep(0, result=None)
        )
    except Exception as e:
        print(f"Error in generating features: {e}")

    # Generate AI report
    report = generate_report(features, ref_features)

    print(f"\n{'+'*50}")
    print(f"FINAL REPORT:")
    print(features)
    print(f"\n{'+'*50}")
    print(f"\n{'+'*50}")
    print(f"AI REPORT:")
    print(report['loudness_dynamics_analysis'])
    print(f"\n{'+'*50}")
    return {"features": features, "ref_features": ref_features, "report": report}

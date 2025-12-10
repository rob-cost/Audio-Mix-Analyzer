from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from concurrent.futures import ProcessPoolExecutor
import asyncio
import os
from analysis.pipeline import (
    # analyze_uploaded_track_loudness,
    # analyze_uploaded_track_harmonic,
    # analyze_uploaded_track_transient,
    analyze_uploaded_track_complete
)
from analysis.helper import to_python


app = FastAPI()

executor = ProcessPoolExecutor(max_workers=os.cpu_count() - 1) # make sure 1 core is left for security reason

app.add_middleware(
    CORSMiddleware,
    allow_origins = ['*'],
    allow_methods = ['*'],
    allow_headers = ['*']
)

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
    try:
        report = await run_in_processpool(audio_bytes, file.content_type)
        return to_python(report)
    except ValueError as e:
        return {"success": False, "error": str(e)}
    

# --- ENDPOINTS ---

@app.post("/analyze")
async def analyze(file:UploadFile = File(...)):
    return await process_file(file)

@app.post("/analyze_reference")
async def analyze_reference(file:UploadFile = File(...)):
    return await process_file(file)

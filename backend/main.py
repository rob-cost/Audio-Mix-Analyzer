from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import uuid, os
from analysis.pipeline import (
    analyze_uploaded_track_loudness,
    analyze_uploaded_track_harmonic,
    analyze_uploaded_track_transient
)
from analysis.helper import to_python


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ['*'],
    allow_methods = ['*'],
    allow_headers = ['*']
)

@app.post("/analyze-loudness")
async def analyze(file: UploadFile = File(...)):
    audio_bytes = await file.read()
    try:
        report = analyze_uploaded_track_loudness(audio_bytes, file.content_type)
        report_obj = to_python(report)
    except ValueError as e:
        return {"success": False, "error": str(e)}
    print(f"Report obj: {report_obj}")
    return report_obj


@app.post("/analyze-transient")
async def analyze(file: UploadFile = File(...)):
    audio_bytes = await file.read()
    try:
        report = analyze_uploaded_track_transient(audio_bytes, file.content_type)
        report_obj = to_python(report)
    except ValueError as e:
        return {"success": False, "error": str(e)}
    print(f"Report obj: {report_obj}")
    return report_obj


@app.post("/analyze-harmonic")
async def analyze(file: UploadFile = File(...)):
    audio_bytes = await file.read()
    try:
        report = analyze_uploaded_track_harmonic(audio_bytes, file.content_type)
        report_obj = to_python(report)
    except ValueError as e:
        return {"success": False, "error": str(e)}
    print(f"Report obj: {report_obj}")
    return report_obj



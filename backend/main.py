from fastapi import FastAPI, UploadFile, File, Request, HTTPException
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address
import asyncio


from analysis.llm.audio_analysis_generator import generate_report
from analysis.utils.file_upload import process_file


app = FastAPI()


limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

app.add_middleware(
    CORSMiddleware,
    allow_origins = ['http://localhost:5173'],
    allow_methods = ['POST'],
    allow_headers = ['*']
)


# --- ENDPOINTS ---

@app.post("/analyze_and_report")
@limiter.limit("5/minute") # Limit amount of request per IP
async def analyze_and_report(
    request: Request, 
    track_file:UploadFile = File(...),
    reference_file:Optional[UploadFile]=File(None)
    ):

    features = None
    ref_features = None
    report = None

    # Analyzing main track and reference if provided
    if reference_file is None:
        try:
            features = await process_file(track_file)
        except Exception as e:
            print(f"Error in generating features: {e}")
            raise HTTPException(status_code=500, detail="Error processing the main track file.")
    else:
        try:
            #  Process both files concurrently
            features, ref_features = await asyncio.gather(
                process_file(track_file),
                process_file(reference_file)
            )
        except Exception as e:
            print(f"Error in generating features: {e}")
            raise HTTPException(status_code=500, detail="Error processing one of the track files.")


    # Generate AI Report
    try:
        print("GENERATING AI REPORT")
        report = generate_report(features, ref_features)
    except Exception as e:
        print(f"Error in generating a report: {e}")
        raise HTTPException(status_code=500, detail="Error generating the analysis report.")

    return {
        "features": features,
        "ref_features": ref_features,
        "report": report
    }

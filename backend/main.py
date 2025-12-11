from fastapi import FastAPI, UploadFile, File, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address


from analysis.llm.report_generator import generate_report
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

# @app.post("/analyze")
# @limiter.limit("5/minute") # Limit amount of request per IP
# async def analyze(request: Request, file:UploadFile = File(...)):
#     return await process_file(file)

# @app.post("/analyze_reference")
# @limiter.limit("5/minute")
# async def analyze_reference(request: Request, file:UploadFile = File(...)):
#     return await process_file(file)

# @app.post("/generate_report")
# async def report_generator(payload: dict):
#     return await generate_report(payload)

@app.post("/analyze_and_report")
@limiter.limit("5/minute") # Limit amount of request per IP
async def analyze_and_report(request: Request, file:UploadFile = File(...)):
    try:
        features = await process_file(file)
    except Exception as e:
        print(f"Error in generating features: {e}")

    try:
        report = generate_report(features)
    except Exception as e:
        print(f"Error in generating a report: {e}")

    return {
        "features": features,
        "report": report
    }

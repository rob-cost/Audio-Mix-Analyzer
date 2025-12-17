import os
import asyncio

from concurrent.futures import ProcessPoolExecutor

from pipeline.analyze_track_complete import analyze_uploaded_track_complete


"""

Split "analyze track function" between computer cores

"""

executor = ProcessPoolExecutor(max_workers=os.cpu_count() - 1) # make sure 1 core is left for security reason


# --- HELPER CPU PROCESSOR ---

async def run_in_processpool(audio_bytes: bytes, mime: str):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor (
        executor,
        analyze_uploaded_track_complete,
        audio_bytes,
        mime
    )
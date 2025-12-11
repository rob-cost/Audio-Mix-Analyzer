from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv(".env.development")

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


async def generate_report(features:dict):

    prompt = f"""
    You are an expert mixing engineer.
    Analyze this audio data and produce a technical mix report.
    Output JSON ONLY.

    Features:
    {features}
    """

    completion = client.chat.completions.create(
        model=os.getenv("GROQ_MODEL"),
        messages=[
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"}
    )

    report_json = completion.choices[0].message["content"]

    return {"report": report_json}
    
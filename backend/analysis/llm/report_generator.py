from groq import Groq
import os
import time
import json
from dotenv import load_dotenv
from fastapi.encoders import jsonable_encoder

load_dotenv(".env.development")

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL = "openai/gpt-oss-120b"


def generate_report(features:dict):

    start_time = time.time()

    prompt = f"""
                Analyze the mix data provided from {features} and give detailed, actionable feedback.

                Your analysis should be technical yet accessible, focusing on specific issues and concrete solutions rather than general observations.

                Output JSON ONLY with the following keys:
                - summary: general overview of the mix
                - genre_context: genre and tempo style
                - subgenre_style_context: subgenre/style notes
                - strengths: list of mix strengths
                - areas_for_improvement: list of areas to improve
                - suggestions: actionable tips
                - processing_recommendations: technical processing instructions

                IMPORTANT: DO NOT use any markdown formatting (no asterisks, no bold, no italic, no backticks). Format your response as plain text only. Do not use any HTML tags or other formatting.

"""

    completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            { "role": "system", "content": "You are a professional audio engineer and mix analyst with extensive experience across multiple genres"},
            { "role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"}
    )

    raw_response = completion.choices[0].message.content

    safe_response = jsonable_encoder(raw_response)

    dict_response = json.loads(safe_response)
    print(f"Type: {type(dict_response)}")

    categories = [
        "summary",
        "genre_context",
        "subgenre_style_context",
        "strengths",
        "areas_for_improvement",
        "suggestions",
        "processing_recommendations"
    ]

    for cat in categories:
        if cat not in safe_response:
            safe_response[cat] = None

    end_time = time.time() - start_time
    print(f"\n{'='*50}")
    print(f"SAFE RESULT")
    print(dict_response['genre_context'])
    print(f"AI Analysis completed in: {end_time} seconds.")
    print(f"\n{'='*50}")

    return dict_response
    
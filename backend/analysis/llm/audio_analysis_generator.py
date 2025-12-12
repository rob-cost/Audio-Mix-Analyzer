from groq import Groq
import os
import time
import json
from dotenv import load_dotenv
from fastapi.encoders import jsonable_encoder
from analysis.llm.audio_analysis_prompt import create_audio_analysis_prompt
load_dotenv(".env.development")

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL = "openai/gpt-oss-120b"



def generate_report(features: dict, features_reference: dict = None):
    """
    Generates a comprehensive audio analysis report.
    
    Args:
        features: dict containing target track audio features
        features_reference: dict containing reference track features (optional)
    
    Returns:
        dict: Parsed JSON response with analysis
    """
    start_time = time.time()

    # Create the optimized prompt
    prompt = create_audio_analysis_prompt(features, features_reference)

    # Make API call
    completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a professional audio engineer and mastering specialist with extensive experience across multiple genres. You provide detailed, technical analysis with specific, actionable recommendations."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        response_format={"type": "json_object"},
        temperature=0.7,
        max_tokens=4096
    )

    raw_response = completion.choices[0].message.content

    # Parse response
    safe_response = jsonable_encoder(raw_response)
    dict_response = json.loads(safe_response)
    
    print(f"Type: {type(dict_response)}")

    # Define expected categories for validation
    required_categories = [
        "summary",
        "genre_context",
        "loudness_analysis",
        "spectral_analysis",
        "dynamics_analysis",
        "stereo_analysis",
        "strengths",
        "areas_for_improvement",
        "suggestions",
        "processing_recommendations"
    ]
    
    # Add reference_comparison if reference was provided
    if features_reference is not None:
        required_categories.append("reference_comparison")

    # Validate response structure
    for cat in required_categories:
        if cat not in dict_response:
            dict_response[cat] = None
            print(f"Warning: Missing category '{cat}' in response")

    end_time = time.time() - start_time
    
    print(f"\n{'='*50}")
    print(f"ANALYSIS COMPLETED")
    print(f"Genre Context: {dict_response.get('genre_context', 'N/A')}")
    if features_reference is not None:
        print(f"Reference Comparison: {'Included' if dict_response.get('reference_comparison') else 'Missing'}")
    print(f"AI Analysis completed in: {end_time:.2f} seconds")
    print(f"{'='*50}\n")

    return dict_response
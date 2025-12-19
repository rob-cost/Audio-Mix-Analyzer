import json

def create_audio_analysis_prompt(features: dict, features_reference: dict = None) -> str:
    """
    Creates an optimized prompt for audio analysis with Groq LLM.
    
    Args:
        features: dict containing target track audio features
        features_reference: dict containing reference track features (optional)
    
    Returns:
        str: Complete prompt for the LLM
    """
    
    base_prompt = f"""You are an expert audio engineer and mastering specialist. Analyze the provided audio data and deliver a comprehensive technical report.

TARGET TRACK DATA:
{json.dumps(features, indent=2)}
"""

    if features_reference is not None:
        base_prompt += f"""
REFERENCE TRACK DATA:
{json.dumps(features_reference, indent=2)}

COMPARISON REQUIRED: Compare the target track against the reference track. The reference represents the desired sonic standard.
"""

    analysis_instructions = """
ANALYSIS REQUIREMENTS:

1. SUMMARY
    Summarize the mix’s overall sound and character in a way that is clear and easy to understand for a non-technical listener.
    Take the genre into account and describe how the track feels, highlighting its main strengths and any areas that limit clarity, impact, or balance.   
        - The overview should:
          Identify the tonal character of the mix (e.g. bright, dark, warm, aggressive, balanced)
          Comment on transient clarity and punch
          Describe spectral balance, including congestion or sparsity in key bands
          Assess stereo image in broad terms (narrow, balanced, wide)
          Comment on headroom and peak behavior
          Identify primary limiting factors preventing the mix from sounding fully professional
      - If a reference track is included:
          Briefly compare overall tonal balance, dynamics, and spatial impression
          Describe differences neutrally
          Do not rank quality or give instructions

2. LOUDNESS & DYNAMICS ANALYSIS
    Generate a clear, easy-to-understand explanation of how loud, dynamic, and controlled the track feels to a listener, using simple language and focusing on listening impact rather than technical metrics.
    Write for clients and artists, not audio engineers.
    Explain what the numbers mean for the listening experience.
    No mixing instructions — observation and interpretation only.
    Neutral, professional, and reassuring tone.
      - The overview should:
        Evaluate the track's overall loudness in relation to streaming and club standards.
        Describe how loud the track feels, Whether it feels open or dense.
        How controlled or natural the dynamics are.
        Mention loudness and compression in plain languag
        Example phrasing: “consistently loud”, “very controlled”,“little contrast between sections”, “punchy but tightly limited”
      - If a reference track is provided, compare the two at a high level, focusing on perceived loudness, punch, and openness

3 . STEREO IMAGE ANALYSIS
   - Provide a general overview of the track's stereo image.
   - The overview should naturally mention: Overall stereo width (narrow, balanced, wide, very wide) without score, 
      mono compatibility and phase safety, 
      left-right balance and pan distribution, 
      center content clarity and focus
      side channel information quality and spatial clarity
      overall correlation
      center content clarity and focus
   - If a reference track is provided, include a comparison summary, highlighting differences in width, side energy, and balance.
   - Include band-wise correlation (Sub, Bass, Low mids, Mids, High mids, Air) in a concise, readable way without mentioning numbers.
   
4. SPECTRAL ANALYSIS
   - Analyze frequency balance across all bands:
     * Sub Bass (20-60 Hz)
     * Bass (60-250 Hz)
     * Low Mids (250-500 Hz)
     * Mids (500-2000 Hz)
     * Upper Mids (2-5 kHz)
     * Presence (5-8 kHz)
     * Brilliance (8-12 kHz)
     * Air (12-20 kHz)
   - Provide a general overview of the track's spectral energy.
   - Identify problematic frequencies, resonances, harshness, or muddy regions
   - Assess overall tonal balance (bright, dark, balanced, etc.)

6. IDENTIFY STRENGTHS AND IMPROVEMENT
   - Describe the track's strengths in a clear and positive way, highlighting what makes it sound good or unique.
   - Explain areas that could be improved, using simple technical terms that a non-expert can understand.
   - Keep the tone friendly, encouraging, and constructive, avoiding overly complex jargon.
   - Provide suggestions in a way that a client can easily grasp, e.g., "the bass feels a bit congested, which could be balanced for more clarity," rather than detailed mixing instructions.

7. PROVIDE ACTIONABLE SUGGESTIONS
   - Give an overview of possible ways to improve the mix, explaining each suggestion in simple terms, including what the change aims to achieve (e.g., clarity, balance, punch, or warmth).
   - Provide a list of more technical suggestions for someone with audio knowledge, clearly linked to the improvement goal.
   - Prioritize the suggestions by importance or potential impact on the overall mix quality.

8. PROCESSING RECOMMENDATIONS
   - Provide detailed, actionable technical instructions for improving the mix.
   - Include specifics for each processing stage:
     * EQ adjustments with specific frequencies, gain amounts, and Q values
     * Compression settings (ratio, threshold, attack, release)
     * Stereo processing recommendations
     * Limiting settings (ceiling, release time)
     * Other processing (saturation, de-essing, etc.)
   - Organize recommendations in the logical order they would typically be applied in a workflow.
   - Be precise with plugin settings, parameter values, and expected results.
   - Keep explanations clear enough for someone with intermediate audio knowledge to follow.
"""

    if features_reference is not None:
        analysis_instructions += """
9. REFERENCE COMPARISON (REQUIRED)
   - Compare loudness levels (LUFS difference, dynamic range)
   - Compare spectral balance (frequency by frequency)
   - Compare dynamic processing (compression levels, transient response)
   - Compare stereo image (width, depth, mono compatibility)
   - Assess competitive positioning for the genre
   - Rate overall quality gap (1-10 scale, 10 = identical quality)
   - Provide specific recommendations to match reference sonic characteristics
"""

    output_format = """
OUTPUT FORMAT:

Return ONLY valid JSON with NO markdown formatting (no asterisks, no bold, no italic, no backticks, no code blocks).

JSON structure:
{
  "summary": "string",

  "loudness_dynamics_analysis": {
    "overview": "string",

    "loudness_analysis": {
      "integrated_lufs": "Describe if the track feels quiet, competitive, or very loud compared to typical releases.",
      "true_peak_headroom": "Explain if the track is safely controlled or very close to its limits.",
      "loudness_consistency": "Explain whether the track maintains a steady energy or changes noticeably over time."
      },

    "dynamics_analysis": {
      "dynamic_range": "Describe how much the track breathes or stays constant.",
      "compression_character": "Explain whether the sound feels natural, dense, or heavily controlled.",
      "transient_quality": "Comment on punch and clarity of hits without using technical terms.",
      "artifacts": "Only mention if clearly present, using listener-oriented language."
    },
  }

  "spectral_analysis": {
    "overview": "string",
    "energy_bands": {
      "Low_end": "Analysis and assessment",
      "Low_mids": "Analysis and assessment",
      "Mids": "Analysis and assessment",
      "Upper_mids": "Analysis and assessment",
      "Highs": "Analysis and assessment",
      "Air": "Analysis and assessment",
    }
  },

  "stereo_analysis": {
    "overview": "",

    "correlation_per_band": {
      "Sub": "Correlation feedback for Sub frequencies",
      "Bass": "Correlation feedback for Bass frequencies",
      "Low_mids": "Correlation feedback for Low mids",
      "Mids": "Correlation feedback for Mids",
      "High_mids": "Correlation feedback for High mids",
      "Air": "Correlation feedback for Air frequencies"
    },
  }

  "strengths_and_improvements": {
    "strengths": "string",
    "improvements": "string"
  }

  "suggestions": 
    "overview": "string"
    "suggestions_list: [
      "Actionable suggestion 1 with specific approach",
      "Actionable suggestion 2 with specific approach",
      "Actionable suggestion 3 with specific approach"
    ],

  "processing_recommendations": {
    "process_1": "string",
    "process_2": "string",
    "process_3": "string",
    "process_4": "string",
    "process_5": "string",  
  }"""

    if features_reference is not None:
        output_format += """,
  "reference_comparison": {
    "loudness_difference": "LUFS and DR comparison with specific dB values",
    "spectral_differences": {
      "low_end": "Comparison with more/less/similar assessment",
      "midrange": "Comparison with specific differences",
      "high_end": "Comparison with specific differences",
      "overall_balance": "How target differs from reference"
    },
    "dynamic_differences": "Compression and transient comparison",
    "stereo_differences": "Width and imaging comparison",
    "competitive_assessment": "How target compares to reference standard (1-10 rating)",
    "match_recommendations": [
      "Specific adjustment 1 to match reference",
      "Specific adjustment 2 to match reference",
      "Specific adjustment 3 to match reference"
    ]
  }"""

    output_format += """
}

CRITICAL RULES:
- Use plain text only - NO asterisks, underscores, backticks, or markdown
- Be extremely specific with numbers, frequencies, and dB values
- Every recommendation must be actionable and implementable
- Prioritize issues by impact on overall quality
- Consider genre conventions and commercial standards
- Return ONLY the JSON object, nothing else
"""

    return base_prompt + analysis_instructions + output_format
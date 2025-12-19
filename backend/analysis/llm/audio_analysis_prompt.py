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

6. IDENTIFY STRENGTHS
   - List 3-5 specific positive aspects of the mix
   - Be concrete and technical

7. IDENTIFY AREAS FOR IMPROVEMENT
   - List 3-5 specific issues or limitations
   - Prioritize by impact on overall quality

8. PROVIDE ACTIONABLE SUGGESTIONS
   - Give specific, implementable advice
   - Use exact values when possible
   - Prioritize suggestions by importance

9. PROCESSING RECOMMENDATIONS
   - Provide detailed technical instructions:
     * EQ adjustments with specific frequencies, gain amounts, and Q values
     * Compression settings (ratio, threshold, attack, release)
     * Stereo processing recommendations
     * Limiting settings (ceiling, release time)
     * Other processing (saturation, de-essing, etc.)
   - Organize in recommended workflow order
   - Be specific with plugin settings and values
"""

    if features_reference is not None:
        analysis_instructions += """
10. REFERENCE COMPARISON (REQUIRED)
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
      "Low_end": "analysis and assessment",
      "Low_mids": "analysis and assessment",
      "Mids": "analysis and assessment",
      "Upper_mids": "analysis and assessment",
      "Highs": "analysis and assessment",
      "Air": "analysis and assessment",
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

  "strengths": [
    "Specific strength 1",
    "Specific strength 2",
    "Specific strength 3"
  ],
  "areas_for_improvement": [
    "Specific issue 1 with impact description",
    "Specific issue 2 with impact description",
    "Specific issue 3 with impact description"
  ],
  "suggestions": [
    "Actionable suggestion 1 with specific approach",
    "Actionable suggestion 2 with specific approach",
    "Actionable suggestion 3 with specific approach"
  ],
  "processing_recommendations": {
    "priority_order": [
      "First critical adjustment",
      "Second priority adjustment",
      "Third priority adjustment"
    ],
    "eq_adjustments": [
      "Specific EQ move 1 with frequency, gain, and Q value",
      "Specific EQ move 2 with frequency, gain, and Q value"
    ],
    "compression": [
      "Compression setting 1 with ratio, threshold, attack, release",
      "Compression setting 2 with specific values"
    ],
    "stereo_processing": [
      "Stereo processing recommendation with specific settings"
    ],
    "limiting": "Limiter settings with ceiling and release time",
    "other_processing": [
      "Additional processing recommendations"
    ]
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
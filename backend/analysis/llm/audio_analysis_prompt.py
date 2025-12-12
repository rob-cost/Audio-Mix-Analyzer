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

1. LOUDNESS & HEADROOM ANALYSIS
   - Evaluate integrated LUFS (target: -14 to -8 LUFS for streaming, -6 to -4 for club/radio)
   - Check true peak levels (should be below -1.0 dBTP for streaming)
   - Assess crest factor and dynamic range (DR meter scale)
   - Identify headroom availability
   - Determine if over-compressed or too quiet

2. SPECTRAL ANALYSIS
   - Analyze frequency balance across all bands:
     * Sub Bass (20-60 Hz)
     * Bass (60-250 Hz)
     * Low Mids (250-500 Hz)
     * Mids (500-2000 Hz)
     * Upper Mids (2-5 kHz)
     * Presence (5-8 kHz)
     * Brilliance (8-12 kHz)
     * Air (12-20 kHz)
   - Identify problematic frequencies, resonances, harshness, or muddy regions
   - Assess overall tonal balance (bright, dark, balanced, etc.)

3. DYNAMIC CHARACTERISTICS
   - Evaluate compression amount (light/medium/heavy/over-compressed)
   - Assess transient preservation quality
   - Check for micro-dynamics (natural/controlled/squashed)
   - Evaluate macro-dynamics range
   - Identify pumping, breathing, or artifacts

4. STEREO IMAGE ANALYSIS
   - Assess stereo width (narrow/balanced/wide/excessive)
   - Check mono compatibility and phase issues
   - Evaluate pan distribution and balance
   - Assess center content clarity and focus
   - Evaluate side information quality
   - Check correlation values for phase relationships

5. IDENTIFY STRENGTHS
   - List 3-5 specific positive aspects of the mix
   - Be concrete and technical

6. IDENTIFY AREAS FOR IMPROVEMENT
   - List 3-5 specific issues or limitations
   - Prioritize by impact on overall quality

7. PROVIDE ACTIONABLE SUGGESTIONS
   - Give specific, implementable advice
   - Use exact values when possible
   - Prioritize suggestions by importance

8. PROCESSING RECOMMENDATIONS
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
  "summary": "Brief overview of the overall mix quality and primary characteristics",
  "genre_context": "Identified genre and tempo style context",
  "loudness_analysis": {
    "lufs": "Integrated LUFS value and assessment",
    "true_peak": "True peak level and headroom status",
    "dynamic_range": "DR value and compression assessment",
    "headroom": "Available headroom and recommendations"
  },
  "spectral_analysis": {
    "low_end": "20-250 Hz analysis and assessment",
    "low_mids": "250-500 Hz analysis and assessment",
    "mids": "500-2000 Hz analysis and assessment",
    "upper_mids": "2-5 kHz analysis and assessment",
    "highs": "5-10 kHz analysis and assessment",
    "air": "10-20 kHz analysis and assessment",
    "balance": "Overall tonal balance description",
    "problem_frequencies": "List of problematic frequency ranges with specific Hz values"
  },
  "dynamics_analysis": {
    "compression_level": "Light/Medium/Heavy/Over-compressed assessment",
    "transient_quality": "Transient preservation evaluation",
    "micro_dynamics": "Micro-dynamic behavior",
    "macro_dynamics": "Overall dynamic range assessment",
    "artifacts": "Any pumping, breathing, or distortion issues"
  },
  "stereo_analysis": {
    "width": "Stereo width assessment",
    "mono_compatibility": "Phase relationship and mono fold-down quality",
    "balance": "Left-right balance and pan distribution",
    "center_focus": "Center content clarity",
    "correlation": "Stereo correlation assessment"
  },
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
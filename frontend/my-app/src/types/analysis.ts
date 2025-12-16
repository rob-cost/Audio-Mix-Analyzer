// --- TYPES ---

// types generated from ai report structure
type Report = {
  summary?: string;
  genre_context?: string;
  strengths?: string[];
  areas_for_improvement?: string[];
  suggestions?: string[];

  // Objects with string values
  loudness_analysis?: Record<string, string>;
  spectral_analysis?: Record<string, string>;
  dynamics_analysis?: Record<string, string>;
  stereo_analysis?: Record<string, string>;

  processing_recommendations?: {
    priority_order?: string[];
    eq_adjustments?: string[];
    compression?: string[];
    stereo_processing?: string[];
    limiting?: string;
    other_processing?: string[];
  };

  reference_comparison?: {
    loudness_difference?: string;
    spectral_difference?: Record<string, string>;
    dynamics_difference?: string;
    stereo_difference?: string;
    competitive_assessment?: string[];
  };

  features?: Features;
  ref_features?: Features;
};

// Types from features
type Features = {
  tempo_features?: TempoFeatures;
  loudness_features?: LoudnessFeatures;
};

type TempoFeatures = {
  tempo_bpm?: number;
};

type LoudnessFeatures = {
  loudness_lufs?: number;
  rms_db?: number;
  true_peak_db?: number;
  crest_factor_db?: number;
};

// AnalysisReport
export type AnalysisReport = {
  report?: Report;
  features?: Features;
};

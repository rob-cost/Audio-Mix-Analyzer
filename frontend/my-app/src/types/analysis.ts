// --- TYPES ---

// types generated from ai report structure
type Report = {
  summary?: string;
  genre_context?: string;
  strengths?: string[];
  areas_for_improvement?: string[];
  suggestions?: string[];
  processing_recommendations?: Record<string, unknown>;
  reference_comparison?: Record<string, unknown>;

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

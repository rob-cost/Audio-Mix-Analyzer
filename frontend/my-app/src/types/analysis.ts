// --- TYPES ---

// --- ANALYSIS REPORT ---
export type AnalysisReport = {
  report?: Report;
  features?: Features;
};

// --- TYPE REPORT ---

type Report = {
  summary?: string;
  loudness_dynamics_analysis?: LoudnessDynamicsAnalysis;
  spectral_analysis?: SpectralAnalysis;
  strengths?: string[];
  areas_for_improvement?: string[];
  suggestions?: string[];

  // Objects with string values
  // loudness_analysis?: Record<string, string>;
  // dynamics_analysis?: Record<string, string>;
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

type SpectralAnalysis = {
  overview?: string;
  correlation_per_band?: Record<string, string>;
};

type LoudnessDynamicsAnalysis = {
  overview?: string;
  loudness_analysis?: Record<string, string>;
  dynamics_analysis?: Record<string, string>;
};

// --- FEATURES TYPES ---
type Features = {
  tempo_features?: TempoFeatures;
  loudness_features?: LoudnessFeatures;
  harmonic_features?: HarmonicFeatures;
  stereo_image_features?: StereoImageFeatures;
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

type HarmonicFeatures = {
  tonal_stability?: number;
  estimated_key?: string;
};

type StereoImageFeatures = {
  stereo_width_label?: string;
};

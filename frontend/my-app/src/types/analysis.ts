// --- TYPES ---

// --- ANALYSIS REPORT ---
export type AnalysisReportTypes = {
  report?: Report;
  features?: Features;
  ref_features?: Features;
  graphic?: Graphic;
};

// --- TYPE REPORT ---

type Report = {
  summary?: string;
  loudness_dynamics_analysis?: LoudnessDynamicsAnalysis;
  spectral_analysis?: SpectralAnalysis;
  stereo_analysis?: Record<string, string>;
  strengths_and_improvements?: StrengthsAndImprovements;
  suggestions?: Suggestions;
  processing_recommendations?: Processing;

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

type LoudnessDynamicsAnalysis = {
  overview?: string;
  loudness_analysis?: Record<string, string>;
  dynamics_analysis?: Record<string, string>;
};

type SpectralAnalysis = {
  overview?: string;
  energy_bands?: Record<string, string>;
};

type StrengthsAndImprovements = {
  strengths?: string;
  improvements?: string;
};

type Suggestions = {
  overview?: string;
  suggestions_list?: string[];
};

type Processing = {
  processing_reccomendations?: Record<string, string>;
};

// --- TYPE FEATURES ---
type Features = {
  tempo_features?: TempoFeatures;
  loudness_features?: LoudnessFeatures;
  harmonic_features?: HarmonicFeatures;
  frequency_spectrum_features?: FrequencySpectrumFeatures;
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

type FrequencySpectrumFeatures = {
  energy_bands?: Record<string, number>;
};

type StereoImageFeatures = {
  stereo_width_label?: string;
};

// --- TYPE GRAPHIC ---
type Graphic = {
  graphic?: string;
};

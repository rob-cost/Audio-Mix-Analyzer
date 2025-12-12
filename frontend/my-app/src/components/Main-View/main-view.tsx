import { useState } from "react";

type AnalysisReport = {
  summary?: string;
  genre_context?: string;
  loudness_analysis?: Record<string, any>;
  spectral_analysis?: Record<string, any>;
  dynamics_analysis?: Record<string, any>;
  stereo_analysis?: Record<string, any>;
  strengths?: string[];
  areas_for_improvement?: string[];
  suggestions?: string[];
  processing_recommendations?: Record<string, any>;
  reference_comparison?: Record<string, any>;
  tempo_features?: Record<string, any>;
  loudness_features?: Record<string, any>;
  transient_features?: Record<string, any>;
  harmonic_features?: Record<string, any>;
  frequency_spectrum_energy?: Record<string, any>;
  stereo_image_features?: Record<string, any>;
};

export default function MainView() {
  const [mainFile, setMainFile] = useState<File | null>(null);
  const [refFile, setRefFile] = useState<File | null>(null);
  const [mainReport, setMainReport] = useState<AnalysisReport | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const uploadMain = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files![0];
    if (file) {
      setMainFile(file);
      console.log("Main Track ", file.name, " uploaded");
    }
  };

  const uploadRef = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files![0];
    if (file) {
      setRefFile(file);
      console.log("Reference Track ", file.name, " uploaded");
    }
  };

  const analyzeTrack = async () => {
    if (!mainFile) {
      setError("Please upload main track first");
      return;
    }

    setIsAnalyzing(true);
    setError(null);
    setMainReport(null);

    try {
      const form = new FormData();
      form.append("track_file", mainFile);

      if (refFile) {
        form.append("reference_file", refFile);
      }

      const res = await fetch("http://localhost:8000/analyze_and_report", {
        method: "POST",
        body: form,
      });

      if (!res.ok) {
        throw new Error(`Analysis failed: ${res.statusText}`);
      }
      const data = await res.json();
      setMainReport(data);
      console.log("Analysis complete:", data);
    } catch (err) {
      console.error("Analysis Failed", err);
      setError(err instanceof Error ? err.message : "Analysis failed");
    } finally {
      setIsAnalyzing(false);
    }
  };

  const clearFiles = () => {
    setMainFile(null);
    setRefFile(null);
    setMainReport(null);
    setError(null);
  };

  return (
    <div style={{ padding: 30, maxWidth: 1200, margin: "0 auto" }}>
      <h1>Audio Mix Analyzer</h1>

      {/* Upload Section */}
      <div
        style={{
          marginTop: 20,
          padding: 20,
          border: "2px dashed #ccc",
          borderRadius: 8,
          backgroundColor: "#f9f9f9",
        }}
      >
        <div style={{ marginBottom: 15 }}>
          <label
            style={{ display: "block", marginBottom: 5, fontWeight: "bold" }}
          >
            Main Track (Required)
          </label>
          <input
            type="file"
            accept="audio/*"
            onChange={uploadMain}
            style={{ marginBottom: 5 }}
          />
          {mainFile && (
            <div style={{ color: "green", fontSize: 14 }}>
              ✓ {mainFile.name}
            </div>
          )}
        </div>

        <div style={{ marginBottom: 15 }}>
          <label
            style={{ display: "block", marginBottom: 5, fontWeight: "bold" }}
          >
            Reference Track (Optional)
          </label>
          <input
            type="file"
            accept="audio/*"
            onChange={uploadRef}
            style={{ marginBottom: 5 }}
          />
          {refFile && (
            <div style={{ color: "green", fontSize: 14 }}>✓ {refFile.name}</div>
          )}
        </div>

        <div style={{ display: "flex", gap: 10 }}>
          <button
            onClick={analyzeTrack}
            disabled={!mainFile || isAnalyzing}
            style={{
              padding: "10px 20px",
              fontSize: 16,
              fontWeight: "bold",
              backgroundColor: mainFile && !isAnalyzing ? "#4CAF50" : "#ccc",
              color: "white",
              border: "none",
              borderRadius: 5,
              cursor: mainFile && !isAnalyzing ? "pointer" : "not-allowed",
            }}
          >
            {isAnalyzing ? "Analyzing..." : "Analyze Track"}
          </button>

          {(mainFile || refFile) && (
            <button
              onClick={clearFiles}
              disabled={isAnalyzing}
              style={{
                padding: "10px 20px",
                fontSize: 16,
                backgroundColor: "#f44336",
                color: "white",
                border: "none",
                borderRadius: 5,
                cursor: isAnalyzing ? "not-allowed" : "pointer",
              }}
            >
              Clear Files
            </button>
          )}
        </div>
      </div>

      {/* Error Display */}
      {error && (
        <div
          style={{
            marginTop: 20,
            padding: 15,
            backgroundColor: "#ffebee",
            color: "#c62828",
            borderRadius: 5,
            border: "1px solid #ef5350",
          }}
        >
          <strong>Error:</strong> {error}
        </div>
      )}

      {/* Loading Indicator */}
      {isAnalyzing && (
        <div
          style={{
            marginTop: 20,
            padding: 20,
            backgroundColor: "#e3f2fd",
            borderRadius: 5,
            textAlign: "center",
          }}
        >
          <div style={{ fontSize: 18, marginBottom: 10 }}>
            🎵 Analyzing your audio...
          </div>
          <div style={{ fontSize: 14, color: "#666" }}>
            This may take a few moments
          </div>
        </div>
      )}

      {/* Analysis Report */}
      {mainReport && !isAnalyzing && (
        <div style={{ marginTop: 30 }}>
          <h2>Analysis Report</h2>

          {/* Summary Section */}
          {mainReport.summary && (
            <div
              style={{
                marginBottom: 20,
                padding: 15,
                backgroundColor: "#e8f5e9",
                borderRadius: 5,
              }}
            >
              <h3>Summary</h3>
              <p>{mainReport.summary}</p>
            </div>
          )}

          {/* Genre Context */}
          {mainReport.genre_context && (
            <div
              style={{
                marginBottom: 20,
                padding: 15,
                backgroundColor: "#fff3e0",
                borderRadius: 5,
              }}
            >
              <h3>Genre Context</h3>
              {mainReport.genre_context && (
                <p>
                  <strong>Genre:</strong> {mainReport.genre_context}
                </p>
              )}
            </div>
          )}

          {/* Strengths */}
          {mainReport.strengths && mainReport.strengths.length > 0 && (
            <div
              style={{
                marginBottom: 20,
                padding: 15,
                backgroundColor: "#e8f5e9",
                borderRadius: 5,
              }}
            >
              <h3>✓ Strengths</h3>
              <ul>
                {mainReport.strengths.map((strength, idx) => (
                  <li key={idx}>{strength}</li>
                ))}
              </ul>
            </div>
          )}

          {/* Areas for Improvement */}
          {mainReport.areas_for_improvement &&
            mainReport.areas_for_improvement.length > 0 && (
              <div
                style={{
                  marginBottom: 20,
                  padding: 15,
                  backgroundColor: "#fff3e0",
                  borderRadius: 5,
                }}
              >
                <h3>⚠ Areas for Improvement</h3>
                <ul>
                  {mainReport.areas_for_improvement.map((area, idx) => (
                    <li key={idx}>{area}</li>
                  ))}
                </ul>
              </div>
            )}

          {/* Suggestions */}
          {mainReport.suggestions && mainReport.suggestions.length > 0 && (
            <div
              style={{
                marginBottom: 20,
                padding: 15,
                backgroundColor: "#e3f2fd",
                borderRadius: 5,
              }}
            >
              <h3>💡 Suggestions</h3>
              <ul>
                {mainReport.suggestions.map((suggestion, idx) => (
                  <li key={idx}>{suggestion}</li>
                ))}
              </ul>
            </div>
          )}

          {/* Processing Recommendations */}
          {mainReport.processing_recommendations && (
            <div
              style={{
                marginBottom: 20,
                padding: 15,
                backgroundColor: "#f3e5f5",
                borderRadius: 5,
              }}
            >
              <h3>🎛️ Processing Recommendations</h3>
              <pre
                style={{
                  backgroundColor: "white",
                  padding: 10,
                  borderRadius: 5,
                  overflow: "auto",
                }}
              >
                {JSON.stringify(mainReport.processing_recommendations, null, 2)}
              </pre>
            </div>
          )}

          {/* Reference Comparison */}
          {mainReport.reference_comparison && (
            <div
              style={{
                marginBottom: 20,
                padding: 15,
                backgroundColor: "#fce4ec",
                borderRadius: 5,
              }}
            >
              <h3>🔄 Reference Comparison</h3>
              <pre
                style={{
                  backgroundColor: "white",
                  padding: 10,
                  borderRadius: 5,
                  overflow: "auto",
                }}
              >
                {JSON.stringify(mainReport.reference_comparison, null, 2)}
              </pre>
            </div>
          )}

          {/* Technical Details (Collapsible) */}
          <details style={{ marginTop: 20 }}>
            <summary
              style={{
                cursor: "pointer",
                fontWeight: "bold",
                padding: 10,
                backgroundColor: "#f5f5f5",
                borderRadius: 5,
              }}
            >
              📊 Technical Details (Click to expand)
            </summary>
            <div style={{ marginTop: 10 }}>
              {Object.entries(mainReport).map(([section, metrics]) => (
                <div key={section} style={{ marginBottom: 15 }}>
                  <h4>{section}</h4>
                  <pre
                    style={{
                      backgroundColor: "#f5f5f5",
                      padding: 10,
                      borderRadius: 5,
                      overflow: "auto",
                      fontSize: 12,
                    }}
                  >
                    {JSON.stringify(metrics, null, 2)}
                  </pre>
                </div>
              ))}
            </div>
          </details>
        </div>
      )}
    </div>
  );
}

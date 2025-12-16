import type { AnalysisReport } from "../../types/analysis";

export function AnalysisReportDisplay(report: AnalysisReport) {
  return (
    <div style={{ marginTop: 30 }}>
      <h2>Analysis Report</h2>

      {/* Summary Section */}
      {report.report?.summary && (
        <div
          style={{
            marginBottom: 20,
            padding: 15,
            backgroundColor: "#e8f5e9",
            borderRadius: 5,
          }}
        >
          <h3>Summary</h3>
          <p>{report.report.summary}</p>
        </div>
      )}

      {/* Genre Context */}
      {report.report?.genre_context && (
        <div
          style={{
            marginBottom: 20,
            padding: 15,
            backgroundColor: "#fff3e0",
            borderRadius: 5,
          }}
        >
          <h3>Genre Context</h3>
          <p>
            <strong>Genre:</strong> {report.report.genre_context}
          </p>
        </div>
      )}

      {/* Loudness Analysis */}
      {report.report?.loudness_analysis && (
        <div
          style={{
            marginBottom: 20,
            padding: 15,
            backgroundColor: "#e8f5e9",
            borderRadius: 5,
          }}
        >
          <h3> Loudness Analysis</h3>
          <ul>
            {Object.entries(report.report.loudness_analysis).map(
              ([key, value]) => (
                <li key={key}>
                  <strong>{key}:</strong> {value}
                </li>
              )
            )}
          </ul>
        </div>
      )}

      {/* Spectral Analysis */}
      {report.report?.spectral_analysis && (
        <div
          style={{
            marginBottom: 20,
            padding: 15,
            backgroundColor: "#e8f5e9",
            borderRadius: 5,
          }}
        >
          <h3> Spectral Analysis</h3>
          <ul>
            {Object.entries(report.report.spectral_analysis).map(
              ([key, value]) => (
                <li key={key}>
                  <strong>{key}:</strong> {value}
                </li>
              )
            )}
          </ul>
        </div>
      )}

      {/* Dynamic Analysis */}
      {report.report?.dynamics_analysis && (
        <div
          style={{
            marginBottom: 20,
            padding: 15,
            backgroundColor: "#e8f5e9",
            borderRadius: 5,
          }}
        >
          <h3> Dynamic Analysis</h3>
          <ul>
            {Object.entries(report.report.dynamics_analysis).map(
              ([key, value]) => (
                <li key={key}>
                  <strong>{key}:</strong> {value}
                </li>
              )
            )}
          </ul>
        </div>
      )}

      {/* Stereo Analysis */}
      {report.report?.stereo_analysis && (
        <div
          style={{
            marginBottom: 20,
            padding: 15,
            backgroundColor: "#e8f5e9",
            borderRadius: 5,
          }}
        >
          <h3> Stereo Analysis</h3>
          <ul>
            {Object.entries(report.report.stereo_analysis).map(
              ([key, value]) => (
                <li key={key}>
                  <strong>{key}:</strong> {value}
                </li>
              )
            )}
          </ul>
        </div>
      )}

      {/* Strengths */}
      {report.report?.strengths && report.report?.strengths.length > 0 && (
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
            {report.report.strengths.map((strength, idx) => (
              <li key={idx}>{strength}</li>
            ))}
          </ul>
        </div>
      )}

      {/* Areas for Improvement */}
      {report.report?.areas_for_improvement &&
        report.report?.areas_for_improvement.length > 0 && (
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
              {report.report.areas_for_improvement.map((area, idx) => (
                <li key={idx}>{area}</li>
              ))}
            </ul>
          </div>
        )}

      {/* Suggestions */}
      {report.report?.suggestions && report.report?.suggestions.length > 0 && (
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
            {report.report.suggestions.map((suggestion, idx) => (
              <li key={idx}>{suggestion}</li>
            ))}
          </ul>
        </div>
      )}

      {/* Processing Recommendations */}
      {report.report?.processing_recommendations && (
        <div
          style={{
            marginBottom: 20,
            padding: 15,
            backgroundColor: "#f3e5f5",
            borderRadius: 5,
          }}
        >
          <h3>🎛️ Processing Recommendations</h3>

          <ul>
            {Object.entries(report.report.processing_recommendations).map(
              ([key, value]) => (
                <li key={key}>
                  <strong>{key}:</strong> {value}
                </li>
              )
            )}
          </ul>
        </div>
      )}

      {/* Reference Comparison */}
      {report.report?.reference_comparison && (
        <div
          style={{
            marginBottom: 20,
            padding: 15,
            backgroundColor: "#fce4ec",
            borderRadius: 5,
          }}
        >
          <h3>🔄 Reference Comparison</h3>
          <ul>
            {Object.entries(report.report.reference_comparison).map(
              ([key, value]) => (
                <li key={key}>
                  <strong>{key.replace(/_/g, " ")}:</strong>{" "}
                  {typeof value === "string" && value}
                  {Array.isArray(value) && (
                    <ul>
                      {value.map((item, i) => (
                        <li key={i}>{item}</li>
                      ))}
                    </ul>
                  )}
                  {typeof value === "object" && !Array.isArray(value) && (
                    <ul>
                      {Object.entries(value).map(([subKey, subValue]) => (
                        <li key={subKey}>
                          <strong>{subKey}:</strong> {subValue}
                        </li>
                      ))}
                    </ul>
                  )}
                </li>
              )
            )}
          </ul>
        </div>
      )}

      {/* Technical Details (Collapsible)
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
          {Object.entries(report).map(([section, metrics]) => (
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
      </details> */}
    </div>
  );
}

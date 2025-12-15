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
          <pre
            style={{
              backgroundColor: "white",
              padding: 10,
              borderRadius: 5,
              overflow: "auto",
            }}
          >
            {JSON.stringify(report.report?.processing_recommendations, null, 2)}
          </pre>
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
          <pre
            style={{
              backgroundColor: "white",
              padding: 10,
              borderRadius: 5,
              overflow: "auto",
            }}
          >
            {JSON.stringify(report.report.reference_comparison, null, 2)}
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
      </details>
    </div>
  );
}

import type { AnalysisReportTypes } from "../../types/analysis";

export function ReportOverview({ report }: { report: AnalysisReportTypes }) {
  return (
    <div style={{ marginTop: 30 }}>
      <h2>Overview</h2>

      {/* Overviews */}
      {report.report?.summary && (
        <div
          style={{
            marginBottom: 20,
            padding: 15,
            backgroundColor: "#e8f5e9",
            borderRadius: 5,
          }}
        >
          <p>{report.report?.summary}</p>
        </div>
      )}
    </div>
  );
}

export function ReportLoudnessAndDynamics({
  report,
}: {
  report: AnalysisReportTypes;
}) {
  const loudness_dynamics = report.report?.loudness_dynamics_analysis;

  if (!loudness_dynamics) return null;

  return (
    <div style={{ marginTop: 30 }}>
      <h2>Loudness & Dynamics</h2>

      {/* Loudness Analysis */}
      {loudness_dynamics.loudness_analysis &&
        loudness_dynamics.dynamics_analysis && (
          <div
            style={{
              marginBottom: 20,
              padding: 15,
              backgroundColor: "#e8f5e9",
              borderRadius: 5,
            }}
          >
            <h4> Overview</h4>
            <p>{loudness_dynamics.overview}</p>
            <div>
              <h4>Loudness Analysis</h4>
              <ul>
                {Object.entries(loudness_dynamics.loudness_analysis).map(
                  ([key, value]) => (
                    <li key={key}>
                      <strong>{key}:</strong> {value}
                    </li>
                  )
                )}
              </ul>
            </div>
            <div>
              <h4>Dynamic Analysis</h4>
              <ul>
                {Object.entries(loudness_dynamics.dynamics_analysis).map(
                  ([key, value]) => (
                    <li key={key}>
                      <strong>{key}:</strong> {value}
                    </li>
                  )
                )}
              </ul>
            </div>
          </div>
        )}
    </div>
  );
}

export function ReportStereoImage({ report }: { report: AnalysisReportTypes }) {
  const stereo = report.report?.stereo_analysis;
  const spectral_analysis = report.report?.spectral_analysis;

  if (!stereo) return null;
  if (!spectral_analysis) return null;

  return (
    <div style={{ marginTop: 30 }}>
      <h2>Stereo Image</h2>

      <div
        style={{
          marginBottom: 20,
          padding: 15,
          backgroundColor: "#e8f5e9",
          borderRadius: 5,
        }}
      >
        <h4>Overview</h4>
        {stereo.overview && <p>{stereo.overview}</p>}

        {stereo.correlation_per_band && (
          <>
            <h4>Correlation per band</h4>
            <ul>
              {Object.entries(stereo.correlation_per_band).map(
                ([band, value]) => (
                  <li key={band}>
                    <strong>{band}:</strong> {value}
                  </li>
                )
              )}
            </ul>
          </>
        )}
      </div>

      {/* Spectral Analysis */}
      <h2>Spectral Analysis</h2>
      {spectral_analysis.overview && spectral_analysis.energy_bands && (
        <div
          style={{
            marginBottom: 20,
            padding: 15,
            backgroundColor: "#e8f5e9",
            borderRadius: 5,
          }}
        >
          <h4>Overview</h4>
          <p>{spectral_analysis.overview}</p>
          <h4> Energy Bands</h4>
          <ul>
            {Object.entries(spectral_analysis.energy_bands).map(
              ([band, value]) => (
                <li key={band}>
                  <strong>{band}</strong>
                  {value}
                </li>
              )
            )}
          </ul>
        </div>
      )}
    </div>
  );
}

export function ReportStregthAndImprovement({
  report,
}: {
  report: AnalysisReportTypes;
}) {
  const strenghts_and_improvs = report.report?.strengths_and_improvements;

  if (!strenghts_and_improvs) return null;

  return (
    <div style={{ marginTop: 30 }}>
      {/* Strengths */}
      {strenghts_and_improvs.strengths &&
        strenghts_and_improvs.improvements && (
          <div
            style={{
              marginBottom: 20,
              padding: 15,
              backgroundColor: "#e8f5e9",
              borderRadius: 5,
            }}
          >
            <h3>Strengths</h3>
            <p>{strenghts_and_improvs.strengths}</p>
            <h3>Improvements</h3>
            <p>{strenghts_and_improvs.improvements}</p>
          </div>
        )}
    </div>
  );
}

export function ReportSuggestion({ report }: { report: AnalysisReportTypes }) {
  const suggestions = report.report?.suggestions;

  if (!suggestions) return null;

  return (
    <div style={{ marginTop: 30 }}>
      <h2>Suggestions</h2>

      {/* Suggestions */}
      {suggestions.overview && suggestions.suggestions_list && (
        <div
          style={{
            marginBottom: 20,
            padding: 15,
            backgroundColor: "#e3f2fd",
            borderRadius: 5,
          }}
        >
          <p>{suggestions.overview}</p>

          <ul>
            {suggestions.suggestions_list.map((value, index) => (
              <li key={index}>{value}</li>
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
                  <strong>{key}:</strong> {String(value)}
                </li>
              )
            )}
          </ul>
        </div>
      )}
    </div>
  );
}

export function ReportReferenceComparison({
  report,
}: {
  report: AnalysisReportTypes;
}) {
  return (
    <div style={{ marginTop: 30 }}>
      <h2>Reference Comparison</h2>

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
                  {typeof value === "object" &&
                    value !== null &&
                    !Array.isArray(value) && (
                      <ul>
                        {Object.entries(value).map(([subKey, subValue]) => (
                          <li key={subKey}>
                            <strong>{subKey}:</strong> {String(subValue)}
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
    </div>
  );
}

/* Technical Details (Collapsible)
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
      </details> */

import { useState } from "react";

type AnalysisReport = {
  tempo_features: Record<string, any>;
  loudness_features: Record<string, any>;
  transient_features: Record<string, any>;
  harmonic_features: Record<string, any>;
};

function App() {
  const [report, setReport] = useState<AnalysisReport | null>(null);

  const upload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files![0];
    const form = new FormData();
    form.append("file", file);

    const res = await fetch("http://localhost:8000/analyze", {
      method: "POST",
      body: form,
    });

    setReport(await res.json());
  };

  return (
    <div style={{ padding: 30 }}>
      <h1>Audio Mix Analyzer MVP</h1>

      <input type="file" onChange={upload} />

      {report && (
        <div style={{ marginTop: 30 }}>
          <h2>Analysis Report</h2>

          {Object.entries(report).map(([section, metrics]) => (
            <div key={section}>
              <h3>{section}</h3>
              <pre>{JSON.stringify(metrics, null, 2)}</pre>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default App;

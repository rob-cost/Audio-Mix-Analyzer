import type { AnalysisReport } from "../../types/analysis";

import { MetricCard } from "../../components/MetricCard/MetricCard";

export function MetricsDashboard(report: AnalysisReport) {
  // Extract metrics from report
  const lufs = report.features?.loudness_features?.loudness_lufs ?? "N/A";
  const rms = report.features?.loudness_features?.rms_db ?? "N/A";
  const peak = report.features?.loudness_features?.true_peak_db ?? "N/A";
  const crestFactor =
    report.features?.loudness_features?.crest_factor_db ?? "N/A";

  return (
    <div style={{ marginTop: 30 }}>
      <h2>Key Metrics</h2>
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))",
          gap: 20,
          marginTop: 15,
        }}
      >
        <MetricCard
          title="LUFS"
          value={typeof lufs === "number" ? lufs.toFixed(1) : lufs}
          unit="LUFS"
          description="Loudness Units relative to Full Scale - measures the perceived loudness of your audio. Target: -14 LUFS for streaming platforms."
          color="#2196F3"
        />
        <MetricCard
          title="RMS"
          value={typeof rms === "number" ? rms.toFixed(1) : rms}
          unit="dB"
          description="Root Mean Square - measures the average power level of your audio signal. Indicates overall energy and loudness."
          color="#4CAF50"
        />
        <MetricCard
          title="Peak"
          value={typeof peak === "number" ? peak.toFixed(1) : peak}
          unit="dB"
          description="True Peak Level - the highest point in your audio signal. Should stay below 0 dB to prevent clipping and distortion."
          color="#FF9800"
        />
        <MetricCard
          title="Crest Factor"
          value={
            typeof crestFactor === "number"
              ? crestFactor.toFixed(1)
              : crestFactor
          }
          unit="dB"
          description="Ratio between peak and RMS levels. Higher values indicate more dynamic range. Typical range: 8-20 dB depending on genre."
          color="#9C27B0"
        />
      </div>
    </div>
  );
}

// Upload and Analyze Component
import "./UploadAnalyze.css";

import type { UploadSectionProps } from "./types";

export function UploadSection({
  mainFile,
  refFile,
  isAnalyzing,
  onMainUpload,
  onRefUpload,
  onAnalyze,
}: UploadSectionProps) {
  return (
    <div className="upload-container">
      {/* Upload buttons side by side */}
      <div className="upload-buttons-row">
        <label className="upload-btn">
          Select Main Track
          <input type="file" accept="audio/*" onChange={onMainUpload} hidden />
        </label>

        <label className="upload-btn">
          Select Reference Track
          <input type="file" accept="audio/*" onChange={onRefUpload} hidden />
        </label>
      </div>

      {/* Show uploaded file names */}
      <div className="file-names">
        {mainFile && <div className="file-name">✓ {mainFile.name}</div>}
        {refFile && <div className="file-name">✓ {refFile.name}</div>}
      </div>

      {/* Analyze button */}
      <div className="actions">
        <button
          className="btn btn-analyze"
          onClick={onAnalyze}
          disabled={!mainFile || isAnalyzing}
        >
          {isAnalyzing ? "Analyzing..." : "Analyze"}
        </button>
      </div>

      <div className="upload-info">
        Supported formats: MP3, WAV, OGG, FLAC. | Max file size: 100 MB
      </div>
    </div>
  );
}

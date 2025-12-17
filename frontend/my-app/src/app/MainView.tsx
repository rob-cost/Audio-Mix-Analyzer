import { useState } from "react";

import type { AnalysisReport } from "../types/analysis";
import type { MainViewState } from "./types";

import { analyzeTrack as analyzeTrackApi } from "../services/api/analysisService";

import "./MainView.css";

import { UploadSection } from "../features/upload/UploadAnalyze";
// import { ReportOverview } from "../features/analysis/AnalysisReport";
// import { MetricsDashboard } from "../features/analysis/MetricsDashboard";
import AnalysisTabs from "../features/analysis/AnalysisTabs";

export default function MainView() {
  const [mainFile, setMainFile] = useState<MainViewState["mainFile"]>(null);
  const [refFile, setRefFile] = useState<MainViewState["refFile"]>(null);
  const [mainReport, setMainReport] = useState<AnalysisReport | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [loadingStep, setLoadingStep] =
    useState<MainViewState["loadingStep"]>("");
  const [error, setError] = useState<MainViewState["error"]>(null);

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
    if (!mainFile) return;

    setIsAnalyzing(true);
    setError(null);

    try {
      const data = await analyzeTrackApi(mainFile, refFile ?? undefined);
      setMainReport(data);
      console.log("Analysis completed and report generated");
      console.log("Main Report", { mainReport });
    } catch (err) {
      console.error("Analysis failed:", err);
      setError("Analysis failed. Please try again.");
    } finally {
      setIsAnalyzing(false);
      setLoadingStep("");
    }
  };

  const clearFiles = () => {
    setMainFile(null);
    setRefFile(null);
    setMainReport(null);
    setError(null);
  };

  return (
    <div className="main-view">
      <h1 className="main-view__title">Audio Mix Analyzer</h1>
      <h3 className="main-view_paragraph">
        Analyze your audio mixes with precision. Our tool leverages advanced AI
        and professional audio engineering techniques to provide detailed track
        data, real-time feedback, and actionable insights to help you perfect
        your mix.
      </h3>

      {/* Upload Section */}
      <section className="main-view__upload">
        <UploadSection
          mainFile={mainFile}
          refFile={refFile}
          isAnalyzing={isAnalyzing}
          onMainUpload={uploadMain}
          onRefUpload={uploadRef}
          onAnalyze={analyzeTrack}
          onClear={clearFiles}
        />
      </section>

      {/* Error Display */}
      {error && (
        <div className="main-view__error">
          <strong>Error:</strong> {error}
        </div>
      )}

      {/* Loading Indicator */}
      {isAnalyzing && (
        <div className="main-view__loading">
          <div className="main-view__loading-title">
            🎵 Analyzing your audio...
          </div>
          <div className="main-view__loading-subtitle">{loadingStep}</div>
          <div className="main-view__spinner">
            <span></span>
            <span></span>
            <span></span>
          </div>
        </div>
      )}

      {/* Metrics Dashboard & Main Report */}
      {mainReport && !isAnalyzing && (
        <section className="main-view__results">
          <AnalysisTabs report={mainReport} />
        </section>
      )}
    </div>
  );
}

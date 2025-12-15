import type { AnalysisReport } from "../types/analysis";

export type MainViewState = {
  mainFile: File | null;
  refFile: File | null;
  mainReport: AnalysisReport | null;
  isAnalyzing: boolean;
  error: string | null;
};

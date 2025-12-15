export type UploadSectionProps = {
  mainFile: File | null;
  refFile: File | null;
  isAnalyzing: boolean;
  onMainUpload: (e: React.ChangeEvent<HTMLInputElement>) => void;
  onRefUpload: (e: React.ChangeEvent<HTMLInputElement>) => void;
  onAnalyze: () => void;
  onClear: () => void;
};

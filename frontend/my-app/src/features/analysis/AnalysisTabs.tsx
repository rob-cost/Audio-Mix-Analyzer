import type { AnalysisReportTypes } from "../../types/analysis";
import { Tabs } from "../../components/Tabs/tabs";
import {
  ReportLoudnessAndDynamics,
  ReportOverview,
  ReportReferenceComparison,
  ReportStregthAndImprovement,
} from "./AnalysisReport";
import { ReportSuggestion } from "./AnalysisReport";
import { ReportStereoImage } from "./AnalysisReport";
import { MetricsDashboard } from "./MetricsDashboard";
import SpectralCurveChart from "../../components/Graphics/spectrum_energies_graphic";
export default function AnalysisTabs({
  report,
}: {
  report: AnalysisReportTypes;
}) {
  const tabData = [
    {
      label: "Overview",
      content: (
        <>
          <ReportOverview report={report} />
          <ReportStregthAndImprovement report={report} />
          <MetricsDashboard report={report} />
          <SpectralCurveChart report={report} />
        </>
      ),
    },
    {
      label: "Loudness & Dynamic",
      content: <ReportLoudnessAndDynamics report={report} />,
    },
    {
      label: "Stereo Image & Spectral Analysis",
      content: <ReportStereoImage report={report} />,
    },
    {
      label: "Suggestions",
      content: <ReportSuggestion report={report} />,
    },
    {
      label: "Reference Comparison",
      content: <ReportReferenceComparison report={report} />,
    },
  ];

  return <Tabs tabs={tabData} />;
}

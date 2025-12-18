import type { AnalysisReport } from "../../types/analysis";
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

export default function AnalysisTabs({ report }: { report: AnalysisReport }) {
  console.log("Main report in Analysis Tab:", report);
  const tabData = [
    {
      label: "Overview",
      content: (
        <>
          <ReportOverview report={report} />
          <MetricsDashboard report={report} />
        </>
      ),
    },
    {
      label: "Loudness & Dynamic",
      content: <ReportLoudnessAndDynamics report={report} />,
    },
    {
      label: "Stereo Image",
      content: <ReportStereoImage report={report} />,
    },
    {
      label: "Strengths & Improvements",
      content: <ReportStregthAndImprovement report={report} />,
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

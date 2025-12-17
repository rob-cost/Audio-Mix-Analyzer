import type { AnalysisReport } from "../../types/analysis";
import { Tabs } from "../../components/Tabs/tabs";
import { ReportOverview } from "./AnalysisReport";
import { ReportSuggestion } from "./AnalysisReport";
import { ReportStereoImage } from "./AnalysisReport";

export default function AnalysisTabs(report: AnalysisReport) {
  const tabData = [
    {
      label: "Overview",
      content: <ReportOverview report={report} />,
    },
    {
      label: "Stere Image",
      content: <ReportStereoImage report={report} />,
    },
    {
      label: "Suggestions",
      content: <ReportSuggestion report={report} />,
    },
  ];

  return <Tabs tabs={tabData} />;
}

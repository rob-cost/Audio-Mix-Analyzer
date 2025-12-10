import { useState } from "react";

// type AnalysisReport = {
//   tempo_features: Record<string, any>;
//   loudness_features: Record<string, any>;
//   transient_features: Record<string, any>;
//   harmonic_features: Record<string, any>;
//   frequency_spectrum_energy: Record<string, any>;
//   stereo_image_features: Record<string, any>;
// };

// export default function App() {
//   const [report, setReport] = useState<AnalysisReport | null>(null);

//   const upload = async (e: React.ChangeEvent<HTMLInputElement>) => {
//     const file = e.target.files![0];
//     const form = new FormData();
//     form.append("file", file);

//     try {
//       // call all three endpoints in parallel
//       const [transientRes, loudRes, harmonicRes] = await Promise.all([
//         fetch("http://localhost:8000/analyze-transient", {
//           method: "POST",
//           body: form,
//         }),
//         fetch("http://localhost:8000/analyze-loudness", {
//           method: "POST",
//           body: form,
//         }),
//         fetch("http://localhost:8000/analyze-harmonic", {
//           method: "POST",
//           body: form,
//         }),
//       ]);

//       // parse all endpoints
//       const [transient_features, loudness_features, harmonic_features] =
//         await Promise.all([
//           transientRes.json(),
//           loudRes.json(),
//           harmonicRes.json(),
//         ]);

//       const mergedReport: AnalysisReport = {
//         tempo_features: loudness_features.tempo_features,
//         loudness_features: loudness_features.loudness_features,
//         transient_features: transient_features.transient_features,
//         harmonic_features: harmonic_features.harmonic_features,
//         frequency_spectrum_energy: harmonic_features.frequency_spectrum_energy,
//         stereo_image_features: harmonic_features.stereo_image_features,
//       };

//       setReport(mergedReport);
//     } catch (err) {
//       console.error("Analysis Failed", { err });
//     }
//   };

//   return (
//     <div style={{ padding: 30 }}>
//       <h1>Audio Mix Analyzer</h1>

//       <input type="file" onChange={upload} />

//       {report && (
//         <div style={{ marginTop: 30 }}>
//           <h2>Analysis Report</h2>

//           {Object.entries(report).map(([section, metrics]) => (
//             <div key={section}>
//               <h3>{section}</h3>
//               <pre>{JSON.stringify(metrics, null, 2)}</pre>
//             </div>
//           ))}
//         </div>
//       )}
//     </div>
//   );
// }

type AnalysisReport = {
  tempo_features: Record<string, any>;
  loudness_features: Record<string, any>;
  transient_features: Record<string, any>;
  harmonic_features: Record<string, any>;
  frequency_spectrum_energy: Record<string, any>;
  stereo_image_features: Record<string, any>;
};

export default function App() {
  const [report, setReport] = useState<AnalysisReport | null>(null);

  const upload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files![0];
    const form = new FormData();
    form.append("file", file);

    try {
      const res = await fetch("http://localhost:8000/analyze", {
        method: "POST",
        body: form,
      });

      setReport(await res.json());
    } catch (err) {
      console.error("Analysis Failed", { err });
    }
  };

  return (
    <div style={{ padding: 30 }}>
      <h1>Audio Mix Analyzer</h1>

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

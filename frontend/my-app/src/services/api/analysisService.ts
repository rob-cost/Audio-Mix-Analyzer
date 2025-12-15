export async function analyzeTrack(mainFile: File, refFile?: File) {
  const form = new FormData();
  form.append("track_file", mainFile);
  if (refFile) form.append("reference_file", refFile);

  const res = await fetch("http://localhost:8000/analyze_and_report", {
    method: "POST",
    body: form,
  });

  if (!res.ok) {
    throw new Error(`Analysis failed: ${res.statusText}`);
  }

  return res.json();
}

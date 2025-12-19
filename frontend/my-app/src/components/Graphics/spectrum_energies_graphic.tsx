import {
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  Area,
  Scatter,
  ComposedChart,
} from "recharts";
import type { TooltipContentProps } from "recharts";
import type { AnalysisReportTypes } from "../../types/analysis";

/* ------------------------------------------------------------------ */
/* Types */
/* ------------------------------------------------------------------ */

interface MeasurementPoint {
  freq: number;
  db: number;
  band: string;
}

interface CurvePoint {
  freq: number;
  db: number;
}

interface TooltipData {
  freq: number;
  db: number;
  band?: string;
}

/* ------------------------------------------------------------------ */
/* Tooltip component (MUST be top-level) */
/* ------------------------------------------------------------------ */

const CustomTooltip = (props: TooltipContentProps<number, string>) => {
  const { active, payload } = props;

  if (!active || !payload || payload.length === 0) return null;

  const data = payload[0].payload as TooltipData;

  return (
    <div
      style={{
        backgroundColor: "#1a1a1a",
        border: "1px solid #333",
        padding: "10px",
        borderRadius: "4px",
        color: "white",
      }}
    >
      {data.band && (
        <p style={{ margin: 0, fontWeight: "bold" }}>{data.band}</p>
      )}
      <p style={{ margin: "4px 0", color: "#00ff88" }}>
        {data.freq >= 1000
          ? `${(data.freq / 1000).toFixed(1)}k Hz`
          : `${Math.round(data.freq)} Hz`}
      </p>
      <p style={{ margin: 0, color: "#ff4444" }}>{data.db.toFixed(1)} dB</p>
    </div>
  );
};

/* ------------------------------------------------------------------ */
/* Main chart component */
/* ------------------------------------------------------------------ */

const SpectralCurveChart = ({ report }: { report: AnalysisReportTypes }) => {
  const rawData = report.features?.frequency_spectrum_features?.energy_bands;

  if (!rawData) return null;

  const freqCenters: Record<string, number> = {
    Sub: 40,
    Bass: 130,
    Low_mids: 400,
    Mids: 1800,
    High_mids: 5500,
    Air: 14000,
  };

  const convertToDB = (value: number): number =>
    10 * Math.log10(Math.max(value, 1e-12));

  const measurementPoints: MeasurementPoint[] = Object.keys(rawData)
    .filter((band): band is keyof typeof freqCenters => band in freqCenters)
    .map(band => ({
      freq: freqCenters[band],
      db: convertToDB(rawData[band]),
      band,
    }))
    .sort((a, b) => a.freq - b.freq);

  const createSmoothCurve = (): CurvePoint[] => {
    const points: CurvePoint[] = [];
    const logMin = Math.log10(20);
    const logMax = Math.log10(20000);
    const steps = 150;

    for (let i = 0; i <= steps; i++) {
      const logFreq = logMin + ((logMax - logMin) * i) / steps;
      const freq = Math.pow(10, logFreq);

      let db = measurementPoints[0].db;

      for (let j = 0; j < measurementPoints.length - 1; j++) {
        const p1 = measurementPoints[j];
        const p2 = measurementPoints[j + 1];

        if (freq >= p1.freq && freq <= p2.freq) {
          const t =
            (Math.log10(freq) - Math.log10(p1.freq)) /
            (Math.log10(p2.freq) - Math.log10(p1.freq));
          db = p1.db + t * (p2.db - p1.db);
          break;
        }
      }

      if (freq > measurementPoints.at(-1)!.freq) {
        db = measurementPoints.at(-1)!.db;
      }

      points.push({ freq, db });
    }

    return points;
  };

  const smoothCurve = createSmoothCurve();

  return (
    <ResponsiveContainer width="100%" height={500}>
      <ComposedChart
        data={smoothCurve}
        margin={{ top: 20, right: 30, left: 20, bottom: 50 }}
      >
        <CartesianGrid stroke="#333" strokeDasharray="3 3" />

        <XAxis dataKey="freq" type="number" scale="log" domain={[20, 20000]} />

        <YAxis />

        {/* Tooltip receives a component reference, not JSX */}
        <Tooltip content={CustomTooltip} />

        <Legend />

        <Area
          dataKey="db"
          stroke="#00ff88"
          fill="#00ff8833"
          strokeWidth={3}
          dot={false}
          name="Frequency Response"
        />

        <Scatter
          data={measurementPoints}
          dataKey="db"
          fill="#ff4444"
          name="Measured Bands"
        />
      </ComposedChart>
    </ResponsiveContainer>
  );
};

export default SpectralCurveChart;

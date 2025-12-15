import { useState } from "react";

type MetricCardProps = {
  title: string;
  value: string | number;
  unit?: string;
  description: string;
  color: string;
};

export function MetricCard({
  title,
  value,
  unit,
  description,
  color,
}: MetricCardProps) {
  const [showTooltip, setShowTooltip] = useState(false);

  return (
    <div
      style={{
        position: "relative",
        padding: 20,
        backgroundColor: "white",
        borderRadius: 8,
        border: `2px solid ${color}`,
        boxShadow: "0 2px 4px rgba(0,0,0,0.1)",
        transition: "transform 0.2s",
        cursor: "pointer",
      }}
      onMouseEnter={() => setShowTooltip(true)}
      onMouseLeave={() => setShowTooltip(false)}
    >
      <div style={{ fontSize: 14, color: "#666", marginBottom: 5 }}>
        {title}
      </div>
      <div style={{ fontSize: 32, fontWeight: "bold", color }}>
        {value}
        {unit && <span style={{ fontSize: 18, marginLeft: 5 }}>{unit}</span>}
      </div>

      {/* Tooltip */}
      {showTooltip && (
        <div
          style={{
            position: "absolute",
            top: "100%",
            left: 0,
            right: 0,
            marginTop: 10,
            padding: 15,
            backgroundColor: "#333",
            color: "white",
            borderRadius: 8,
            fontSize: 14,
            zIndex: 1000,
            boxShadow: "0 4px 6px rgba(0,0,0,0.2)",
          }}
        >
          {description}
        </div>
      )}
    </div>
  );
}

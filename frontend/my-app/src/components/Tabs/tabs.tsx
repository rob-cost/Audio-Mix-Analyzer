import { useState } from "react";

interface Tab {
  label: string;
  content: React.ReactNode;
}

interface TabsProps {
  tabs: Tab[];
}

export function Tabs({ tabs }: TabsProps) {
  const [activeIndex, setActiveIndex] = useState(0);

  console.log("Tabs content", tabs[activeIndex].content);

  return (
    <div>
      {/* Tab headers */}
      <div style={{ display: "flex", marginBottom: 20 }}>
        {tabs.map((tab, idx) => (
          <button
            key={idx}
            onClick={() => setActiveIndex(idx)}
            style={{
              flex: 1,
              padding: "10px 20px",
              cursor: "pointer",
              backgroundColor: idx === activeIndex ? "#1976d2" : "#e0e0e0",
              color: idx === activeIndex ? "white" : "black",
              border: "none",
              borderBottom:
                idx === activeIndex
                  ? "2px solid #0d47a1"
                  : "2px solid transparent",
            }}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Tab content */}
      <div>{tabs[activeIndex].content}</div>
    </div>
  );
}

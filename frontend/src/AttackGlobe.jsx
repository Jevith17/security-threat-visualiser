import { useEffect, useState } from "react";
import {
  ComposableMap,
  Geographies,
  Geography,
  Marker,
} from "react-simple-maps";

const GEO_URL =
  "https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json";

export default function AttackGlobe() {
  const [points, setPoints] = useState([]);
  const [tick, setTick] = useState(0);

  // WebSocket: live attack stream
  useEffect(() => {
    const ws = new WebSocket("ws://127.0.0.1:8000/ws/events");

    ws.onmessage = (msg) => {
      const events = JSON.parse(msg.data);
      const now = Date.now();

      setPoints((prev) => [
        ...prev,
        ...events
          .filter((e) => e.geo && e.geo.lat && e.geo.lon)
          .map((e) => ({
            coordinates: [e.geo.lon, e.geo.lat],
            risk: e.risk,
            ts: now,
          })),
      ]);
    };

    ws.onerror = (err) => {
      console.error("WebSocket error:", err);
    };

    return () => ws.close();
  }, []);

  // Heartbeat for animation
  useEffect(() => {
    const id = setInterval(() => {
      setTick((t) => t + 1);
    }, 1000);

    return () => clearInterval(id);
  }, []);

  return (
    <div
      style={{
        width: "100vw",
        height: "100vh",
        background: "#0b1020",
      }}
    >
      <ComposableMap projectionConfig={{ scale: 160 }}>
        <Geographies geography={GEO_URL}>
          {({ geographies }) =>
            geographies.map((geo) => (
              <Geography
                key={geo.rsmKey}
                geography={geo}
                fill="#1a2238"
                stroke="#0b1020"
              />
            ))
          }
        </Geographies>

        {/* Live animated attack markers */}
        {points.map((p, i) => {
          const age = (Date.now() - p.ts) / 1000;
          const maxAge = 10;

          if (age > maxAge) return null;

          const pulse = Math.sin(age * 3) * 2 + 6;
          const opacity = 1 - age / maxAge;

          const color =
            p.risk === "HIGH"
              ? "red"
              : p.risk === "MEDIUM"
              ? "orange"
              : "yellow";

          return (
            <Marker key={i} coordinates={p.coordinates}>
              <circle
                r={pulse}
                fill={color}
                opacity={opacity}
                stroke="white"
                strokeWidth={0.5}
              />
            </Marker>
          );
        })}
      </ComposableMap>
    </div>
  );
}

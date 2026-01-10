import { ComposableMap, Geographies, Geography, Marker } from "react-simple-maps";
import { useEffect, useState } from "react";

const geoUrl =
  "https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json";

export default function AttackGlobe() {
  const [points, setPoints] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/events")
      .then(res => res.json())
      .then(data => {
        setPoints(
          data.map(e => ({
            coordinates: [e.geo.lon, e.geo.lat],
            risk: e.risk
          }))
        );
      });
  }, []);

  return (
    <div style={{ width: "100vw", height: "100vh", background: "#0b1020" }}>
      <ComposableMap projectionConfig={{ scale: 160 }}>
        <Geographies geography={geoUrl}>
          {({ geographies }) =>
            geographies.map(geo => (
              <Geography
                key={geo.rsmKey}
                geography={geo}
                fill="#1a2238"
                stroke="#0b1020"
              />
            ))
          }
        </Geographies>

        {points.map((p, i) => (
          <Marker key={i} coordinates={p.coordinates}>
            <circle
              r={3}
              fill={
                p.risk === "HIGH"
                  ? "red"
                  : p.risk === "MEDIUM"
                  ? "orange"
                  : "yellow"
              }
            />
          </Marker>
        ))}
      </ComposableMap>
    </div>
  );
}



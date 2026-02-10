import { useEffect, useState, useRef, useCallback } from "react";
import {
  ComposableMap,
  Geographies,
  Geography,
  Marker,
} from "react-simple-maps";
import * as d3 from "d3";

const GEO_URL =
  "https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json";

// Central point for attacks (can be configured to your location)
const CENTER_POINT = { lat: 40.7128, lon: -74.0060, name: "New York" }; // New York

// Risk colors
const RISK_COLORS = {
  HIGH: "#ff3b3b",
  MEDIUM: "#ff9f1c",
  LOW: "#ffd60a",
};

// Attack arc component
function AttackArc({ start, end, risk, onComplete }) {
  const [progress, setProgress] = useState(0);
  const [opacity, setOpacity] = useState(1);

  useEffect(() => {
    const duration = 1500; // Animation duration in ms
    const startTime = Date.now();

    const animate = () => {
      const elapsed = Date.now() - startTime;
      const newProgress = Math.min(elapsed / duration, 1);
      
      setProgress(newProgress);

      if (newProgress >= 1) {
        // Fade out after reaching destination
        setTimeout(() => {
          setOpacity(0);
          setTimeout(onComplete, 300);
        }, 200);
      } else {
        requestAnimationFrame(animate);
      }
    };

    requestAnimationFrame(animate);
  }, [onComplete]);

  // Calculate great circle path
  const interpolate = d3.geoInterpolate(start, end);
  const points = d3.range(0, progress + 0.01, 0.02).map(t => interpolate(t));
  
  // Create curved path with altitude
  const lineGenerator = d3.line()
    .curve(d3.curveBasis);

  // Add altitude curve (make the arc rise in the middle)
  const pathPoints = points.map((pt, i) => {
    const t = i / (points.length - 1);
    const altitude = Math.sin(t * Math.PI) * 30; // Arc height
    return [pt[0], pt[1] - altitude * 0.3];
  });

  const pathD = lineGenerator(pathPoints) || "";

  const color = RISK_COLORS[risk] || RISK_COLORS.LOW;

  return (
    <g style={{ opacity }}>
      {/* Outer glow */}
      <path
        d={pathD}
        fill="none"
        stroke={color}
        strokeWidth={4}
        opacity={0.3}
        strokeLinecap="round"
      />
      {/* Main arc line */}
      <path
        d={pathD}
        fill="none"
        stroke={color}
        strokeWidth={2}
        opacity={0.8}
        strokeLinecap="round"
        filter="url(#glow)"
      />
      {/* Animated head */}
      {progress >= 0.1 && (
        <circle
          cx={points[points.length - 1]?.[0]}
          cy={points[points.length - 1]?.[1]}
          r={3}
          fill={color}
          filter="url(#glow)"
        >
          <animate
            attributeName="r"
            values="3;6;3"
            dur="0.5s"
            repeatCount="indefinite"
          />
        </circle>
      )}
    </g>
  );
}

// Pulsing marker component
function PulsingMarker({ coordinates, risk, ts }) {
  const age = (Date.now() - ts) / 1000;
  const maxAge = 8;

  if (age > maxAge) return null;

  const pulse = Math.sin(age * 4) * 3 + 8;
  const opacity = 1 - age / maxAge;
  const color = RISK_COLORS[risk] || RISK_COLORS.LOW;

  return (
    <Marker coordinates={coordinates}>
      {/* Outer pulse ring */}
      <circle
        r={pulse * 1.5}
        fill={color}
        opacity={opacity * 0.2}
        style={{ transformOrigin: "center" }}
      >
        <animate
          attributeName="r"
          values={`${pulse};${pulse * 1.8};${pulse}`}
          dur="1s"
          repeatCount="indefinite"
        />
        <animate
          attributeName="opacity"
          values={`${opacity * 0.4};0;${opacity * 0.4}`}
          dur="1s"
          repeatCount="indefinite"
        />
      </circle>
      {/* Inner marker */}
      <circle
        r={6}
        fill={color}
        opacity={opacity}
        stroke="#ffffff"
        strokeWidth={1.5}
        filter="url(#glow)"
      />
      {/* Core dot */}
      <circle
        r={3}
        fill="#ffffff"
        opacity={opacity}
      />
    </Marker>
  );
}

// Stats Panel Component
function StatsPanel({ stats }) {
  return (
    <div className="stats-panel">
      <div className="stats-header">
        <h2>LIVE THREAT MAP</h2>
        <div className="live-indicator">
          <span className="pulse-dot"></span>
          <span>LIVE</span>
        </div>
      </div>
      
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-value" style={{ color: RISK_COLORS.HIGH }}>
            {stats.high}
          </div>
          <div className="stat-label">HIGH RISK</div>
        </div>
        <div className="stat-card">
          <div className="stat-value" style={{ color: RISK_COLORS.MEDIUM }}>
            {stats.medium}
          </div>
          <div className="stat-label">MEDIUM RISK</div>
        </div>
        <div className="stat-card">
          <div className="stat-value" style={{ color: RISK_COLORS.LOW }}>
            {stats.low}
          </div>
          <div className="stat-label">LOW RISK</div>
        </div>
        <div className="stat-card total">
          <div className="stat-value">{stats.total}</div>
          <div className="stat-label">TOTAL ATTACKS</div>
        </div>
      </div>

      <div className="legend">
        <div className="legend-item">
          <span className="legend-color" style={{ background: RISK_COLORS.HIGH }}></span>
          <span>Critical Threat</span>
        </div>
        <div className="legend-item">
          <span className="legend-color" style={{ background: RISK_COLORS.MEDIUM }}></span>
          <span>Moderate Threat</span>
        </div>
        <div className="legend-item">
          <span className="legend-color" style={{ background: RISK_COLORS.LOW }}></span>
          <span>Low Threat</span>
        </div>
      </div>

      <div className="center-point-info">
        <div className="center-label">MONITORING CENTER</div>
        <div className="center-name">{CENTER_POINT.name}</div>
        <div className="center-coords">
          {CENTER_POINT.lat.toFixed(4)}°N, {Math.abs(CENTER_POINT.lon).toFixed(4)}°W
        </div>
      </div>
    </div>
  );
}

export default function AttackGlobe() {
  const [points, setPoints] = useState([]);
  const [arcs, setArcs] = useState([]);
  const [stats, setStats] = useState({ high: 0, medium: 0, low: 0, total: 0 });
  const [tick, setTick] = useState(0);
  const arcIdRef = useRef(0);

  // WebSocket: live attack stream
  useEffect(() => {
    const ws = new WebSocket("ws://127.0.0.1:8000/ws/events");

    ws.onmessage = (msg) => {
      const events = JSON.parse(msg.data);
      const now = Date.now();

      const newPoints = events
        .filter((e) => e.geo && e.geo.lat && e.geo.lon)
        .map((e) => ({
          id: `${e.source_ip}-${now}`,
          coordinates: [e.geo.lon, e.geo.lat],
          risk: e.risk,
          ts: now,
          country: e.geo.country,
        }));

      // Create arcs for each new point
      const newArcs = newPoints.map((point) => ({
        id: arcIdRef.current++,
        start: point.coordinates,
        end: [CENTER_POINT.lon, CENTER_POINT.lat],
        risk: point.risk,
        ts: now,
      }));

      setPoints((prev) => [...prev, ...newPoints]);
      setArcs((prev) => [...prev, ...newArcs]);

      // Update stats
      setStats((prev) => {
        const newStats = { ...prev };
        newPoints.forEach((p) => {
          newStats.total++;
          if (p.risk === "HIGH") newStats.high++;
          else if (p.risk === "MEDIUM") newStats.medium++;
          else newStats.low++;
        });
        return newStats;
      });
    };

    ws.onerror = (err) => {
      console.error("WebSocket error:", err);
    };

    return () => ws.close();
  }, []);

  // Cleanup old arcs
  useEffect(() => {
    const interval = setInterval(() => {
      const now = Date.now();
      setArcs((prev) => prev.filter((arc) => now - arc.ts < 3000));
      setPoints((prev) => prev.filter((p) => now - p.ts < 8000));
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  // Animation heartbeat
  useEffect(() => {
    const id = setInterval(() => {
      setTick((t) => t + 1);
    }, 100);

    return () => clearInterval(id);
  }, []);

  const removeArc = useCallback((id) => {
    setArcs((prev) => prev.filter((a) => a.id !== id));
  }, []);

  return (
    <div className="attack-globe-container">
      <StatsPanel stats={stats} />
      
      <div className="map-container">
        <ComposableMap 
          projectionConfig={{ 
            scale: 180,
            center: [0, 20],
          }}
          style={{ width: "100%", height: "100%" }}
        >
          <defs>
            <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
              <feGaussianBlur stdDeviation="2" result="coloredBlur" />
              <feMerge>
                <feMergeNode in="coloredBlur" />
                <feMergeNode in="SourceGraphic" />
              </feMerge>
            </filter>
            <linearGradient id="oceanGradient" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#0a0e1a" />
              <stop offset="100%" stopColor="#050810" />
            </linearGradient>
            <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
              <path d="M 40 0 L 0 0 0 40" fill="none" stroke="rgba(0,255,255,0.03)" strokeWidth="0.5"/>
            </pattern>
          </defs>

          {/* Background */}
          <rect width="100%" height="100%" fill="url(#oceanGradient)" />
          <rect width="100%" height="100%" fill="url(#grid)" />

          {/* Graticule */}
          <g stroke="rgba(0,255,255,0.05)" strokeWidth="0.5" fill="none">
            {d3.range(-180, 181, 30).map(lon => (
              <path
                key={`lon-${lon}`}
                d={d3.geoPath(d3.geoGraticule()())}
              />
            ))}
          </g>

          <Geographies geography={GEO_URL}>
            {({ geographies }) =>
              geographies.map((geo) => (
                <Geography
                  key={geo.rsmKey}
                  geography={geo}
                  fill="#0d1421"
                  stroke="#1a2332"
                  strokeWidth={0.5}
                  style={{
                    default: { outline: "none" },
                    hover: { fill: "#1a2332", outline: "none" },
                    pressed: { outline: "none" },
                  }}
                />
              ))
            }
          </Geographies>

          {/* Center point marker */}
          <Marker coordinates={[CENTER_POINT.lon, CENTER_POINT.lat]}>
            {/* Radar rings */}
            <circle r={20} fill="none" stroke="#00d4ff" strokeWidth={0.5} opacity={0.3}>
              <animate attributeName="r" values="15;35;15" dur="3s" repeatCount="indefinite" />
              <animate attributeName="opacity" values="0.6;0.1;0.6" dur="3s" repeatCount="indefinite" />
            </circle>
            <circle r={15} fill="none" stroke="#00d4ff" strokeWidth={0.5} opacity={0.5}>
              <animate attributeName="r" values="10;25;10" dur="2s" repeatCount="indefinite" />
              <animate attributeName="opacity" values="0.8;0.2;0.8" dur="2s" repeatCount="indefinite" />
            </circle>
            {/* Center dot */}
            <circle r={6} fill="#00d4ff" filter="url(#glow)" />
            <circle r={3} fill="#ffffff" />
          </Marker>

          {/* Attack arcs */}
          {arcs.map((arc) => (
            <AttackArc
              key={arc.id}
              start={arc.start}
              end={arc.end}
              risk={arc.risk}
              onComplete={() => removeArc(arc.id)}
            />
          ))}

          {/* Attack markers */}
          {points.map((p) => (
            <PulsingMarker
              key={p.id}
              coordinates={p.coordinates}
              risk={p.risk}
              ts={p.ts}
            />
          ))}
        </ComposableMap>
      </div>

      {/* Overlay effects */}
      <div className="scan-line"></div>
      <div className="vignette"></div>
    </div>
  );
}

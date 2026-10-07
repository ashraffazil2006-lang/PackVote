// src/components/MLAnalyticsDashboard.jsx
import React, { useState, useEffect, useRef } from 'react';
import { getMLAnalytics } from '../services/api';

export default function MLAnalyticsDashboard({ onPlanTrip, onBackToOverview }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Hover states for Line Chart
  const [hoveredLineIndex, setHoveredLineIndex] = useState(1);
  const [activeClusterFilter, setActiveClusterFilter] = useState(null);

  // Hover states for Scatter Plot
  const [hoveredScatterPoint, setHoveredScatterPoint] = useState(null);

  useEffect(() => {
    let mounted = true;
    setLoading(true);
    getMLAnalytics()
      .then((res) => {
        if (mounted) {
          setData(res.data);
          setLoading(false);
        }
      })
      .catch((err) => {
        if (mounted) {
          setError(err.message || 'Failed to load ML analytics');
          setLoading(false);
        }
      });

    return () => { mounted = false; };
  }, []);

  if (loading) {
    return (
      <div className="analytics-loading-box">
        <div className="analytics-spinner" />
        <p className="analytics-loading-txt">Synthesizing 8 ML Model Benchmarks & K-Means Clusters...</p>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="desktop-container" style={{ padding: '60px 24px', textAlign: 'center' }}>
        <div style={{ fontSize: '2.5rem', marginBottom: 12 }}>⚠️</div>
        <h3>Could not load ML Analytics</h3>
        <p style={{ color: 'var(--color-text-faint)', marginBottom: 20 }}>{error}</p>
        <button className="btn-submit-planner" onClick={() => window.location.reload()}>
          Retry Loading
        </button>
      </div>
    );
  }

  const { clusters, scatter_points, prediction_curve, model_benchmarks, consensus_breakdown } = data;

  // Filtered scatter points
  const visiblePoints = activeClusterFilter !== null
    ? scatter_points.filter(p => p.cluster === activeClusterFilter)
    : scatter_points;

  // Multi-Model Line Graph Dimensions
  const curveWidth = 980;
  const curveHeight = 320;
  const curvePadding = { top: 30, right: 30, bottom: 40, left: 60 };
  const innerWidth = curveWidth - curvePadding.left - curvePadding.right;
  const innerHeight = curveHeight - curvePadding.top - curvePadding.bottom;

  const minVal = 0;
  const maxVal = 9000;

  const getX = (idx) => curvePadding.left + (idx / (prediction_curve.length - 1)) * innerWidth;
  const getY = (val) => curvePadding.top + innerHeight - ((val - minVal) / (maxVal - minVal)) * innerHeight;

  // Build SVG Paths for Multi-Model Line Graph
  const actualPath = prediction_curve.map((d, i) => `${i === 0 ? 'M' : 'L'} ${getX(i)} ${getY(d.actual)}`).join(' ');
  const rfPath = prediction_curve.map((d, i) => `${i === 0 ? 'M' : 'L'} ${getX(i)} ${getY(d.rf)}`).join(' ');
  const lrPath = prediction_curve.map((d, i) => `${i === 0 ? 'M' : 'L'} ${getX(i)} ${getY(d.lr)}`).join(' ');

  const currentHoveredPoint = prediction_curve[hoveredLineIndex] || prediction_curve[0];

  // 2D Scatter Plot Dimensions (matches Screenshot 2 left)
  const scatterWidth = 640;
  const scatterHeight = 360;
  const sPad = { top: 25, right: 25, bottom: 45, left: 55 };
  const sInnerW = scatterWidth - sPad.left - sPad.right;
  const sInnerH = scatterHeight - sPad.top - sPad.bottom;

  const getScatterX = (xVal) => sPad.left + (xVal / 100) * sInnerW;
  const getScatterY = (yVal) => sPad.top + sInnerH - (yVal / 100) * sInnerH;

  return (
    <div className="analytics-page-wrapper animate-fadeIn">
      <div className="desktop-container">
        {/* ── Top Header Toolbar ── */}
        <div className="analytics-header-row">
          <div>
            <div className="analytics-badge-row">
              <span className="analytics-status-pill">
                <span className="asp-dot" /> ML Service: Online
              </span>
              <span className="analytics-model-count">8 Models Calibrated</span>
            </div>
            <h1 className="analytics-main-title">K-Means Cluster & ML Model Analytics</h1>
            <p className="analytics-main-sub">
              Empirical validation of K-Means traveler clustering, Linear Regression stay predictions, and consensus fairness.
            </p>
          </div>
          <div className="analytics-header-actions">
            <button className="btn-secondary-analytics" onClick={onBackToOverview}>
              ← Back to Overview
            </button>
            <button className="btn-primary-analytics" onClick={onPlanTrip}>
              ✨ Plan Group Trip →
            </button>
          </div>
        </div>

        {/* ── SECTION 1: K-Means Cluster Analysis (Exact reproduction of Screenshot 2) ── */}
        <div className="analytics-section-title-row">
          <h2 className="analytics-sec-heading">K-Means Cluster Analysis</h2>
          <span className="analytics-sec-tag">v1.0.0 · Unsupervised Segmentation</span>
        </div>

        <div className="kmeans-grid-2col">
          {/* Left Panel: 2D Scatter Plot */}
          <div className="analytics-card-box">
            <div className="acb-header">
              <div>
                <h3 className="acb-title">
                  Cluster Scatter Distribution: Budget Load vs Activity Intensity
                  <span className="acb-chip">2D Feature Space</span>
                </h3>
                <p className="acb-sub">
                  2D feature space projection colored by K-Means cluster assignment (40 representative Indian destinations)
                </p>
              </div>
            </div>

            {/* Interactive Cluster Legend (clickable) */}
            <div className="cluster-legend-pills">
              {clusters.map((c) => (
                <button
                  key={c.id}
                  type="button"
                  className={`cluster-pill-item ${activeClusterFilter === c.id ? 'active' : ''}`}
                  onClick={() => setActiveClusterFilter(prev => prev === c.id ? null : c.id)}
                  title={`Filter by ${c.name}`}
                >
                  <span className="cluster-dot-indicator" style={{ background: c.color }} />
                  <span className="cluster-pill-text">{c.name}</span>
                </button>
              ))}
              {activeClusterFilter !== null && (
                <button
                  type="button"
                  className="cluster-pill-reset"
                  onClick={() => setActiveClusterFilter(null)}
                >
                  Reset Filter
                </button>
              )}
            </div>

            {/* SVG 2D Scatter Plot */}
            <div className="scatter-svg-container">
              <svg viewBox={`0 0 ${scatterWidth} ${scatterHeight}`} className="analytics-svg">
                {/* Horizontal Grid lines */}
                {[0, 25, 50, 75, 100].map(pct => {
                  const y = getScatterY(pct);
                  return (
                    <g key={`y-${pct}`}>
                      <line
                        x1={sPad.left}
                        y1={y}
                        x2={scatterWidth - sPad.right}
                        y2={y}
                        stroke="var(--chart-grid)"
                        strokeDasharray="3 3"
                        strokeWidth="1"
                      />
                      <text x={sPad.left - 10} y={y + 4} textAnchor="end" className="svg-axis-lbl">
                        {pct}%
                      </text>
                    </g>
                  );
                })}

                {/* Vertical Grid lines */}
                {[0, 25, 50, 75, 100].map(pct => {
                  const x = getScatterX(pct);
                  return (
                    <g key={`x-${pct}`}>
                      <line
                        x1={x}
                        y1={sPad.top}
                        x2={x}
                        y2={scatterHeight - sPad.bottom}
                        stroke="var(--chart-grid)"
                        strokeDasharray="3 3"
                        strokeWidth="1"
                      />
                      <text x={x} y={scatterHeight - sPad.bottom + 18} textAnchor="middle" className="svg-axis-lbl">
                        {pct}%
                      </text>
                    </g>
                  );
                })}

                {/* Axes Titles */}
                <text
                  x={scatterWidth / 2}
                  y={scatterHeight - 8}
                  textAnchor="middle"
                  className="svg-axis-title"
                >
                  Destination Stay Budget Load (%)
                </text>
                <text
                  x={-scatterHeight / 2}
                  y={16}
                  transform="rotate(-90)"
                  textAnchor="middle"
                  className="svg-axis-title"
                >
                  Activity & Experience Intensity (%)
                </text>

                {/* 40 Scatter Circles */}
                {visiblePoints.map((pt, idx) => {
                  const cx = getScatterX(pt.x);
                  const cy = getScatterY(pt.y);
                  const clusterColor = clusters[pt.cluster]?.color || '#3b82f6';
                  const isHovered = hoveredScatterPoint?.name === pt.name;

                  return (
                    <g key={pt.name || idx}>
                      {isHovered && (
                        <circle
                          cx={cx}
                          cy={cy}
                          r="12"
                          fill={clusterColor}
                          opacity="0.25"
                          className="pulse-halo"
                        />
                      )}
                      <circle
                        cx={cx}
                        cy={cy}
                        r={isHovered ? "7" : "5"}
                        fill={clusterColor}
                        stroke={isHovered ? "#ffffff" : "rgba(0,0,0,0.4)"}
                        strokeWidth={isHovered ? "2" : "1"}
                        className="scatter-dot"
                        onMouseEnter={() => setHoveredScatterPoint(pt)}
                        onMouseLeave={() => setHoveredScatterPoint(null)}
                      />
                    </g>
                  );
                })}
              </svg>

              {/* Floating Tooltip for Scatter Dot */}
              {hoveredScatterPoint && (
                <div
                  className="scatter-floating-tooltip"
                  style={{
                    left: `${(getScatterX(hoveredScatterPoint.x) / scatterWidth) * 100}%`,
                    top: `${(getScatterY(hoveredScatterPoint.y) / scatterHeight) * 100}%`,
                  }}
                >
                  <div className="sft-header">
                    <span
                      className="sft-badge"
                      style={{ background: clusters[hoveredScatterPoint.cluster]?.color }}
                    >
                      Cluster {hoveredScatterPoint.cluster}
                    </span>
                    <span className="sft-rating">⭐ {hoveredScatterPoint.rating}</span>
                  </div>
                  <div className="sft-title">{hoveredScatterPoint.name}</div>
                  <div className="sft-sub">{hoveredScatterPoint.state} · {hoveredScatterPoint.type}</div>
                  <div className="sft-cost">Avg Stay: ₹{hoveredScatterPoint.cost?.toLocaleString('en-IN')}/night</div>
                  <div className="sft-coords">Coords: ({hoveredScatterPoint.x}%, {hoveredScatterPoint.y}%)</div>
                </div>
              )}
            </div>
          </div>

          {/* Right Panel: Cluster Volume Distribution */}
          <div className="analytics-card-box">
            <div className="acb-header">
              <div>
                <h3 className="acb-title">
                  Cluster Volume Distribution
                  <span className="acb-chip">Distribution</span>
                </h3>
                <p className="acb-sub">Share of destinations assigned per K-Means cluster</p>
              </div>
            </div>

            <div className="volume-bars-wrapper">
              {clusters.map((c) => (
                <div key={c.id} className="volume-row">
                  <div className="volume-lbl-box">
                    <span className="volume-cluster-id">Cluster {c.id}</span>
                    <span className="volume-cluster-desc">{c.short_name}</span>
                  </div>
                  <div className="volume-track">
                    <div
                      className="volume-fill"
                      style={{
                        width: c.share,
                        backgroundColor: c.color,
                        boxShadow: `0 0 14px ${c.color}55`
                      }}
                    />
                  </div>
                  <div className="volume-stat-box">
                    <span className="volume-pct">{c.share}</span>
                    <span className="volume-count">({c.count} spots)</span>
                  </div>
                </div>
              ))}
            </div>

            {/* Cluster Archetype Deep Dive */}
            <div className="cluster-archetypes-list">
              <div className="cal-title">🎯 Travel Archetypes Overview</div>
              {clusters.map(c => (
                <div key={c.id} className="cal-item">
                  <span className="cal-dot" style={{ background: c.color }} />
                  <div className="cal-content">
                    <div className="cal-item-header">
                      <strong>Cluster {c.id}: {c.short_name}</strong>
                      <span className="cal-rate">{c.typical_cost}</span>
                    </div>
                    <p className="cal-item-desc">{c.description}</p>
                    <div className="cal-tags">
                      {c.top_destinations.slice(0, 4).map((d, i) => (
                        <span key={i} className="cal-tag-pill">{d}</span>
                      ))}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* ── SECTION 2: Multi-Model Prediction Curve (Exact reproduction of Screenshot 1) ── */}
        <div className="analytics-section-title-row" style={{ marginTop: 36 }}>
          <h2 className="analytics-sec-heading">Multi-Model Prediction & Cost Evaluation Curve</h2>
          <span className="analytics-sec-tag">Supervised Learning · Continuous Rate Analysis</span>
        </div>

        <div className="analytics-card-box">
          <div className="curve-header-flex">
            <div>
              <h3 className="acb-title">
                Nightly Stay Cost Prediction: Actual vs Machine Learning Models
              </h3>
              <p className="acb-sub">
                Comparative tracking across 40 evaluation destinations validating Random Forest vs Linear Regression vs Actual rates.
              </p>
            </div>

            {/* Screenshot 1 Legend Style */}
            <div className="curve-legend-row">
              <div className="curve-legend-item">
                <span className="cli-symbol cli-actual">--o--</span>
                <span className="cli-label">Actual Demand / Stay Rate (₹)</span>
              </div>
              <div className="curve-legend-item">
                <span className="cli-symbol cli-rf">--o--</span>
                <span className="cli-label">Random Forest (₹)</span>
              </div>
              <div className="curve-legend-item">
                <span className="cli-symbol cli-lr">--o--</span>
                <span className="cli-label">Linear Regression (₹)</span>
              </div>
            </div>
          </div>

          {/* SVG Line Graph */}
          <div
            className="curve-svg-wrapper"
            onMouseMove={(e) => {
              const rect = e.currentTarget.getBoundingClientRect();
              const mouseX = e.clientX - rect.left;
              const ratio = Math.max(0, Math.min(1, (mouseX - curvePadding.left) / innerWidth));
              const idx = Math.round(ratio * (prediction_curve.length - 1));
              setHoveredLineIndex(idx);
            }}
          >
            <svg viewBox={`0 0 ${curveWidth} ${curveHeight}`} className="analytics-svg">
              {/* Y-Axis Grid lines & labels */}
              {[0, 2000, 4000, 6000, 8000].map((val) => {
                const y = getY(val);
                return (
                  <g key={`yval-${val}`}>
                    <line
                      x1={curvePadding.left}
                      y1={y}
                      x2={curveWidth - curvePadding.right}
                      y2={y}
                      stroke="var(--chart-grid)"
                      strokeDasharray="3 3"
                      strokeWidth="1"
                    />
                    <text x={curvePadding.left - 10} y={y + 4} textAnchor="end" className="svg-axis-lbl">
                      ₹{val.toLocaleString('en-IN')}
                    </text>
                  </g>
                );
              })}

              {/* X-Axis ticks */}
              {prediction_curve.map((d, i) => {
                if (i % 2 !== 0 && i !== prediction_curve.length - 1) return null;
                const x = getX(i);
                return (
                  <g key={`xtick-${i}`}>
                    <line
                      x1={x}
                      y1={curveHeight - curvePadding.bottom}
                      x2={x}
                      y2={curveHeight - curvePadding.bottom + 5}
                      stroke="var(--color-border-bright)"
                      strokeWidth="1"
                    />
                    <text x={x} y={curveHeight - curvePadding.bottom + 18} textAnchor="middle" className="svg-axis-lbl">
                      {d.point}
                    </text>
                  </g>
                );
              })}

              {/* 1. Actual Demand Line (Yellow / Amber) */}
              <path
                d={actualPath}
                fill="none"
                stroke="#f59e0b"
                strokeWidth="2.5"
                strokeLinecap="round"
                className="glowing-line-amber"
              />

              {/* 2. Random Forest Line (Emerald Green) */}
              <path
                d={rfPath}
                fill="none"
                stroke="#10b981"
                strokeWidth="2.2"
                strokeLinecap="round"
                className="glowing-line-green"
              />

              {/* 3. Linear Regression Line (Cyan Blue) */}
              <path
                d={lrPath}
                fill="none"
                stroke="#06b6d4"
                strokeWidth="2.2"
                strokeLinecap="round"
                className="glowing-line-cyan"
              />

              {/* Data Point Dots along Lines */}
              {prediction_curve.map((d, i) => (
                <g key={`dots-${i}`}>
                  <circle cx={getX(i)} cy={getY(d.actual)} r="3" fill="#f59e0b" />
                  <circle cx={getX(i)} cy={getY(d.rf)} r="2.5" fill="#10b981" />
                  <circle cx={getX(i)} cy={getY(d.lr)} r="2.5" fill="#06b6d4" />
                </g>
              ))}

              {/* Interactive Vertical Cursor Indicator */}
              {currentHoveredPoint && (
                <g>
                  <line
                    x1={getX(hoveredLineIndex)}
                    y1={curvePadding.top}
                    x2={getX(hoveredLineIndex)}
                    y2={curveHeight - curvePadding.bottom}
                    stroke="#ffffff"
                    strokeWidth="1.5"
                    strokeDasharray="2 2"
                    opacity="0.8"
                  />
                  {/* Glowing active points */}
                  <circle
                    cx={getX(hoveredLineIndex)}
                    cy={getY(currentHoveredPoint.actual)}
                    r="5"
                    fill="#f59e0b"
                    stroke="#ffffff"
                    strokeWidth="1.5"
                  />
                  <circle
                    cx={getX(hoveredLineIndex)}
                    cy={getY(currentHoveredPoint.rf)}
                    r="5"
                    fill="#10b981"
                    stroke="#ffffff"
                    strokeWidth="1.5"
                  />
                  <circle
                    cx={getX(hoveredLineIndex)}
                    cy={getY(currentHoveredPoint.lr)}
                    r="5"
                    fill="#06b6d4"
                    stroke="#ffffff"
                    strokeWidth="1.5"
                  />
                </g>
              )}
            </svg>

            {/* Floating Tooltip Box (Matches Screenshot 1 exact style!) */}
            {currentHoveredPoint && (
              <div
                className="curve-floating-tooltip"
                style={{
                  left: `${(getX(hoveredLineIndex) / curveWidth) * 100}%`,
                }}
              >
                <div className="cft-point-num">{currentHoveredPoint.point}</div>
                <div className="cft-dest-name">{currentHoveredPoint.name}</div>
                <div className="cft-metric-row cft-actual">
                  <span>Actual Demand (Rate) :</span>
                  <strong>₹{currentHoveredPoint.actual?.toLocaleString('en-IN')}</strong>
                </div>
                <div className="cft-metric-row cft-rf">
                  <span>Random Forest (Est) :</span>
                  <strong>₹{currentHoveredPoint.rf?.toLocaleString('en-IN')}</strong>
                </div>
                <div className="cft-metric-row cft-lr">
                  <span>Linear Regression :</span>
                  <strong>₹{currentHoveredPoint.lr?.toLocaleString('en-IN')}</strong>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* ── SECTION 3: 8-Model Benchmarks & Consensus Fairness Formula ── */}
        <div className="analytics-section-title-row" style={{ marginTop: 36 }}>
          <h2 className="analytics-sec-heading">Model Benchmarks & Consensus Weightings</h2>
          <span className="analytics-sec-tag">Ensemble Metrics & Algorithmic Fairness</span>
        </div>

        {/* 6 Benchmark Cards Grid */}
        <div className="benchmarks-grid">
          {model_benchmarks.map((bm, i) => (
            <div key={i} className="benchmark-card">
              <div className="bmc-top">
                <span className="bmc-type-pill" style={{ color: bm.badge_color, borderColor: `${bm.badge_color}44` }}>
                  {bm.type}
                </span>
                <span className="bmc-status">{bm.status}</span>
              </div>
              <h4 className="bmc-name">{bm.model}</h4>
              <p className="bmc-task">{bm.task}</p>
              <div className="bmc-metric-box">
                <span className="bmc-primary">{bm.primary_metric}</span>
                <span className="bmc-secondary">{bm.mae}</span>
              </div>
            </div>
          ))}
        </div>

        {/* Group Consensus Fairness Breakdown */}
        <div className="consensus-card-box">
          <h3 className="acb-title" style={{ marginBottom: 4 }}>
            ⚖️ Group Consensus Fairness Formula
          </h3>
          <p className="acb-sub" style={{ marginBottom: 14 }}>
            How individual preferences are synthesized into a conflict-free group recommendation score.
          </p>

          <div className="consensus-weight-bar">
            {consensus_breakdown.map((item, i) => (
              <div
                key={i}
                className="cwb-segment"
                style={{ width: item.weight, backgroundColor: item.color }}
                title={`${item.factor}: ${item.weight}`}
              >
                <span>{item.weight}</span>
              </div>
            ))}
          </div>

          <div className="consensus-items-grid">
            {consensus_breakdown.map((item, i) => (
              <div key={i} className="consensus-item">
                <div className="ci-badge" style={{ background: item.color }}>
                  {item.weight}
                </div>
                <div>
                  <h5 className="ci-title">{item.factor}</h5>
                  <p className="ci-desc">{item.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

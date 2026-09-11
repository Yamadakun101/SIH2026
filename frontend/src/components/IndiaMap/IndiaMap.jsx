import React, { useState } from 'react';
import { 
  ChevronRight, 
  X, 
  ArrowRight
} from 'lucide-react';
import { CASES_LIST } from '../../data/casesData';

// Color definitions according to importance specification:
// 🔴 Red: High Importance / Big Case
// 🟡 Yellow: Medium Importance
// 🟢 Green: Low Importance / Minor Case
// 🔵 Blue: Closed Case / Resolved
const COLOR_TIERS = {
  HIGH: {
    key: 'HIGH',
    label: 'High Importance / Big Case',
    shortLabel: 'High Priority',
    color: '#dc2626',
    border: '#f87171',
    bgLight: '#fef2f2',
    badgeText: '#991b1b',
    glow: 'rgba(220, 38, 38, 0.4)'
  },
  MEDIUM: {
    key: 'MEDIUM',
    label: 'Medium Importance',
    shortLabel: 'Medium',
    color: '#d97706',
    border: '#fbbf24',
    bgLight: '#fefce8',
    badgeText: '#92400e',
    glow: 'rgba(217, 119, 6, 0.35)'
  },
  LOW: {
    key: 'LOW',
    label: 'Low Importance / Minor',
    shortLabel: 'Low / Routine',
    color: '#16a34a',
    border: '#86efac',
    bgLight: '#f0fdf4',
    badgeText: '#166534',
    glow: 'rgba(22, 163, 74, 0.3)'
  },
  CLOSED: {
    key: 'CLOSED',
    label: 'Closed Case / Resolved',
    shortLabel: 'Closed Case',
    color: '#2563eb',
    border: '#93c5fd',
    bgLight: '#eff6ff',
    badgeText: '#1e40af',
    glow: 'rgba(37, 99, 235, 0.35)'
  }
};

// Clean, simple and accurate India state polygons and coordinates
const INDIA_REGIONS = [
  // 🔴 RED - HIGH IMPORTANCE / BIG CASES
  { 
    code: 'DL', 
    name: 'Delhi NCR', 
    capital: 'New Delhi', 
    cx: 288, 
    cy: 222, 
    cases: 4, 
    importance: 'HIGH', 
    dominantCase: 'Kidnapping & Criminal Nexus (DL-2026-0412)',
    path: 'M 280,215 L 296,215 L 296,230 L 280,230 Z'
  },
  { 
    code: 'UP', 
    name: 'Uttar Pradesh', 
    capital: 'Lucknow', 
    cx: 350, 
    cy: 265, 
    cases: 6, 
    importance: 'HIGH', 
    dominantCase: 'Inter-State Arms Supply Syndicate',
    path: 'M 290,210 L 410,240 L 415,300 L 340,320 L 285,270 Z'
  },
  { 
    code: 'MH', 
    name: 'Maharashtra', 
    capital: 'Mumbai', 
    cx: 255, 
    cy: 455, 
    cases: 7, 
    importance: 'HIGH', 
    dominantCase: 'Organized Hawala & Money Laundering',
    path: 'M 195,410 L 310,410 L 330,490 L 220,500 L 190,450 Z'
  },
  { 
    code: 'PB', 
    name: 'Punjab', 
    capital: 'Chandigarh', 
    cx: 242, 
    cy: 175, 
    cases: 3, 
    importance: 'HIGH', 
    dominantCase: 'Cross-Border Drone Contraband Network',
    path: 'M 220,150 L 265,165 L 255,200 L 220,190 Z'
  },

  // 🟡 YELLOW - MEDIUM IMPORTANCE
  { 
    code: 'RJ', 
    name: 'Rajasthan', 
    capital: 'Jaipur', 
    cx: 195, 
    cy: 270, 
    cases: 4, 
    importance: 'MEDIUM', 
    dominantCase: 'Recruitment & Examination Fraud',
    path: 'M 160,205 L 245,230 L 250,300 L 195,335 L 140,270 Z'
  },
  { 
    code: 'HR', 
    name: 'Haryana', 
    capital: 'Chandigarh', 
    cx: 270, 
    cy: 220, 
    cases: 3, 
    importance: 'MEDIUM', 
    dominantCase: 'Vehicle Re-Registration Racket',
    path: 'M 255,195 L 295,205 L 285,250 L 245,230 Z'
  },
  { 
    code: 'WB', 
    name: 'West Bengal', 
    capital: 'Kolkata', 
    cx: 485, 
    cy: 315, 
    cases: 5, 
    importance: 'MEDIUM', 
    dominantCase: 'Counterfeit Currency Circulation',
    path: 'M 480,260 L 515,260 L 500,375 L 460,370 Z'
  },
  { 
    code: 'BR', 
    name: 'Bihar', 
    capital: 'Patna', 
    cx: 445, 
    cy: 280, 
    cases: 3, 
    importance: 'MEDIUM', 
    dominantCase: 'Synthetic SIM Cloning Ring',
    path: 'M 410,240 L 485,260 L 480,315 L 415,300 Z'
  },
  { 
    code: 'MP', 
    name: 'Madhya Pradesh', 
    capital: 'Bhopal', 
    cx: 290, 
    cy: 360, 
    cases: 4, 
    importance: 'MEDIUM', 
    dominantCase: 'Mining Heavy Equipment Scam',
    path: 'M 220,320 L 350,320 L 360,395 L 240,410 Z'
  },
  { 
    code: 'TG', 
    name: 'Telangana', 
    capital: 'Hyderabad', 
    cx: 325, 
    cy: 480, 
    cases: 3, 
    importance: 'MEDIUM', 
    dominantCase: 'Crypto Investment Layering',
    path: 'M 290,445 L 365,450 L 345,515 L 290,490 Z'
  },
  { 
    code: 'AS', 
    name: 'Assam & North East', 
    capital: 'Dispur', 
    cx: 575, 
    cy: 265, 
    cases: 3, 
    importance: 'MEDIUM', 
    dominantCase: 'Wildlife Transit Network',
    path: 'M 525,250 L 610,230 L 620,290 L 535,300 Z'
  },

  // 🟢 GREEN - LOW IMPORTANCE / MINOR CASES / ROUTINE
  { 
    code: 'GJ', 
    name: 'Gujarat', 
    capital: 'Gandhinagar', 
    cx: 160, 
    cy: 370, 
    cases: 2, 
    importance: 'LOW', 
    dominantCase: 'Port Cargo Weight Discrepancy',
    path: 'M 120,320 L 195,335 L 210,400 L 155,420 L 120,370 Z'
  },
  { 
    code: 'OR', 
    name: 'Odisha', 
    capital: 'Bhubaneswar', 
    cx: 415, 
    cy: 420, 
    cases: 3, 
    importance: 'LOW', 
    dominantCase: 'Commercial Trademark Dispute',
    path: 'M 390,370 L 465,370 L 430,470 L 370,440 Z'
  },
  { 
    code: 'CT', 
    name: 'Chhattisgarh', 
    capital: 'Raipur', 
    cx: 360, 
    cy: 385, 
    cases: 2, 
    importance: 'LOW', 
    dominantCase: 'Highway Checkpost Log Audit',
    path: 'M 350,330 L 395,360 L 370,440 L 330,410 Z'
  },
  { 
    code: 'JH', 
    name: 'Jharkhand', 
    capital: 'Ranchi', 
    cx: 440, 
    cy: 335, 
    cases: 2, 
    importance: 'LOW', 
    dominantCase: 'Industrial Equipment Verification',
    path: 'M 415,300 L 480,315 L 460,370 L 400,350 Z'
  },
  { 
    code: 'AP', 
    name: 'Andhra Pradesh', 
    capital: 'Amaravati', 
    cx: 355, 
    cy: 535, 
    cases: 3, 
    importance: 'LOW', 
    dominantCase: 'Retail Counterfeit Brand Alert',
    path: 'M 345,500 L 400,470 L 360,600 L 315,570 Z'
  },
  { 
    code: 'KL', 
    name: 'Kerala', 
    capital: 'Thiruvananthapuram', 
    cx: 258, 
    cy: 640, 
    cases: 2, 
    importance: 'LOW', 
    dominantCase: 'Local Stamp Paper Forgery',
    path: 'M 240,600 L 270,600 L 275,680 L 250,680 Z'
  },
  { 
    code: 'HP', 
    name: 'Himachal Pradesh', 
    capital: 'Shimla', 
    cx: 285, 
    cy: 150, 
    cases: 1, 
    importance: 'LOW', 
    dominantCase: 'Tourist ID Verification Log',
    path: 'M 260,135 L 305,140 L 300,175 L 265,165 Z'
  },
  { 
    code: 'UT', 
    name: 'Uttarakhand', 
    capital: 'Dehradun', 
    cx: 320, 
    cy: 200, 
    cases: 2, 
    importance: 'LOW', 
    dominantCase: 'Toll Barrier Evasion Record',
    path: 'M 300,175 L 340,185 L 325,225 L 295,205 Z'
  },
  { 
    code: 'JK', 
    name: 'Jammu & Kashmir / Ladakh', 
    capital: 'Srinagar', 
    cx: 275, 
    cy: 95, 
    cases: 2, 
    importance: 'LOW', 
    dominantCase: 'Routine Entry Checkpoint Register',
    path: 'M 230,70 L 270,50 L 320,60 L 335,110 L 305,140 L 260,135 L 235,110 Z'
  },
  { 
    code: 'GA', 
    name: 'Goa', 
    capital: 'Panaji', 
    cx: 220, 
    cy: 522, 
    cases: 1, 
    importance: 'LOW', 
    dominantCase: 'Commercial Establishment Infraction',
    path: 'M 215,515 L 230,515 L 228,530 L 213,530 Z'
  },

  // 🔵 BLUE - CLOSED CASES / RESOLVED / CHARGESHEETED
  { 
    code: 'KA', 
    name: 'Karnataka', 
    capital: 'Bengaluru', 
    cx: 260, 
    cy: 550, 
    cases: 3, 
    importance: 'CLOSED', 
    dominantCase: 'SIM Box Gateway (Chargesheet Filed)',
    path: 'M 220,495 L 290,500 L 295,600 L 230,590 Z'
  },
  { 
    code: 'TN', 
    name: 'Tamil Nadu', 
    capital: 'Chennai', 
    cx: 295, 
    cy: 645, 
    cases: 4, 
    importance: 'CLOSED', 
    dominantCase: 'Spurious Pharma Network (Convicted)',
    path: 'M 270,600 L 330,590 L 305,690 L 265,685 Z'
  }
];

export default function IndiaMap({ onSelectCase }) {
  const [selectedState, setSelectedState] = useState(null);
  const [hoveredState, setHoveredState] = useState(null);
  const [activeFilter, setActiveFilter] = useState('ALL'); // 'ALL', 'HIGH', 'MEDIUM', 'LOW', 'CLOSED'

  const activeCasesForState = selectedState ? CASES_LIST[selectedState.code] || [] : [];

  // Filtered regions based on user's color coordination filter
  const displayedRegions = INDIA_REGIONS.filter(region => {
    if (activeFilter === 'ALL') return true;
    return region.importance === activeFilter;
  });

  // Calculate stats for each importance category
  const stats = {
    high: INDIA_REGIONS.filter(r => r.importance === 'HIGH').length,
    medium: INDIA_REGIONS.filter(r => r.importance === 'MEDIUM').length,
    low: INDIA_REGIONS.filter(r => r.importance === 'LOW').length,
    closed: INDIA_REGIONS.filter(r => r.importance === 'CLOSED').length
  };

  return (
    <div className="map-screen">
      {/* Left Sidebar */}
      <div className="map-sidebar">
        <div className="map-sidebar-header">
          <div style={{ fontSize: '0.72rem', fontWeight: 800, color: 'var(--gov-navy)', letterSpacing: '0.06em', marginBottom: '0.2rem' }}>
            CRIME INTELLIGENCE & JURISDICTIONAL GRID
          </div>
          <h2 className="map-sidebar-title">National Investigation Map</h2>
          <p className="map-sidebar-desc">
            Jurisdictional cases categorized by severity, priority tier, and closure status.
          </p>
        </div>

        {/* 4-Color Priority Summary Cards */}
        <div className="map-color-stats-grid">
          <div 
            className={`map-stat-pill ${activeFilter === 'HIGH' ? 'active' : ''}`}
            onClick={() => setActiveFilter(activeFilter === 'HIGH' ? 'ALL' : 'HIGH')}
            style={{ borderLeftColor: COLOR_TIERS.HIGH.color }}
          >
            <div className="stat-pill-label" style={{ color: COLOR_TIERS.HIGH.color }}>
              <span className="color-dot red" /> High / Critical
            </div>
            <div className="stat-pill-val" style={{ color: COLOR_TIERS.HIGH.color }}>{stats.high} States</div>
          </div>

          <div 
            className={`map-stat-pill ${activeFilter === 'MEDIUM' ? 'active' : ''}`}
            onClick={() => setActiveFilter(activeFilter === 'MEDIUM' ? 'ALL' : 'MEDIUM')}
            style={{ borderLeftColor: COLOR_TIERS.MEDIUM.color }}
          >
            <div className="stat-pill-label" style={{ color: COLOR_TIERS.MEDIUM.color }}>
              <span className="color-dot yellow" /> Medium Priority
            </div>
            <div className="stat-pill-val" style={{ color: COLOR_TIERS.MEDIUM.color }}>{stats.medium} States</div>
          </div>

          <div 
            className={`map-stat-pill ${activeFilter === 'LOW' ? 'active' : ''}`}
            onClick={() => setActiveFilter(activeFilter === 'LOW' ? 'ALL' : 'LOW')}
            style={{ borderLeftColor: COLOR_TIERS.LOW.color }}
          >
            <div className="stat-pill-label" style={{ color: COLOR_TIERS.LOW.color }}>
              <span className="color-dot green" /> Low / Routine
            </div>
            <div className="stat-pill-val" style={{ color: COLOR_TIERS.LOW.color }}>{stats.low} States</div>
          </div>

          <div 
            className={`map-stat-pill ${activeFilter === 'CLOSED' ? 'active' : ''}`}
            onClick={() => setActiveFilter(activeFilter === 'CLOSED' ? 'ALL' : 'CLOSED')}
            style={{ borderLeftColor: COLOR_TIERS.CLOSED.color }}
          >
            <div className="stat-pill-label" style={{ color: COLOR_TIERS.CLOSED.color }}>
              <span className="color-dot blue" /> Closed Cases
            </div>
            <div className="stat-pill-val" style={{ color: COLOR_TIERS.CLOSED.color }}>{stats.closed} States</div>
          </div>
        </div>

        {/* State List with Color Tags */}
        <div className="state-list-section">
          <div className="section-heading">
            <span>State / UT ({displayedRegions.length})</span>
            <span>Priority</span>
          </div>

          <div style={{ overflowY: 'auto', maxHeight: 'calc(100vh - 350px)' }}>
            {displayedRegions.map((state) => {
              const isSelected = selectedState?.code === state.code;
              const tier = COLOR_TIERS[state.importance];

              return (
                <div 
                  key={state.code}
                  className={`state-item ${isSelected ? 'selected' : ''}`}
                  onClick={() => setSelectedState(state)}
                  onMouseEnter={() => setHoveredState(state)}
                  onMouseLeave={() => setHoveredState(null)}
                  style={{
                    borderLeft: `3.5px solid ${tier.color}`,
                    background: isSelected ? tier.bgLight : '#ffffff'
                  }}
                >
                  <div>
                    <div className="state-item-name" style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                      <span 
                        style={{
                          width: '8px',
                          height: '8px',
                          borderRadius: '50%',
                          background: tier.color,
                          display: 'inline-block'
                        }} 
                      />
                      <span>{state.name}</span>
                    </div>
                    <div className="state-item-cases" style={{ fontSize: '0.68rem', color: 'var(--text-secondary)' }}>
                      {state.capital} • {state.cases} Cases
                    </div>
                  </div>

                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
                    <span 
                      style={{
                        fontSize: '0.65rem',
                        fontWeight: 700,
                        padding: '0.15rem 0.45rem',
                        borderRadius: '4px',
                        background: tier.bgLight,
                        color: tier.badgeText,
                        border: `1px solid ${tier.border}`
                      }}
                    >
                      {tier.shortLabel}
                    </span>
                    <ChevronRight size={14} color="var(--text-muted)" />
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* Map Viewport Area */}
      <div 
        className="map-canvas-area"
        style={{ 
          background: '#f8fafc',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          position: 'relative'
        }}
      >
        {/* Top Filter Chips Bar */}
        <div className="map-top-bar" style={{ zIndex: 20 }}>
          <div className="map-filter-group">
            <button 
              className={`map-filter-btn ${activeFilter === 'ALL' ? 'active' : ''}`}
              onClick={() => setActiveFilter('ALL')}
            >
              All Jurisdictions ({INDIA_REGIONS.length})
            </button>
            <button 
              className={`map-filter-btn high ${activeFilter === 'HIGH' ? 'active' : ''}`}
              onClick={() => setActiveFilter('HIGH')}
            >
              <span className="color-dot red" /> High Importance (Red)
            </button>
            <button 
              className={`map-filter-btn med ${activeFilter === 'MEDIUM' ? 'active' : ''}`}
              onClick={() => setActiveFilter('MEDIUM')}
            >
              <span className="color-dot yellow" /> Medium (Yellow)
            </button>
            <button 
              className={`map-filter-btn low ${activeFilter === 'LOW' ? 'active' : ''}`}
              onClick={() => setActiveFilter('LOW')}
            >
              <span className="color-dot green" /> Low / Routine (Green)
            </button>
            <button 
              className={`map-filter-btn closed ${activeFilter === 'CLOSED' ? 'active' : ''}`}
              onClick={() => setActiveFilter('CLOSED')}
            >
              <span className="color-dot blue" /> Closed (Blue)
            </button>
          </div>
        </div>

        {/* Clean, Flat Simple Map Container */}
        <div 
          style={{
            width: '640px',
            height: '700px',
            position: 'relative',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center'
          }}
        >
          <svg
            viewBox="0 0 700 720"
            style={{
              width: '100%',
              height: '100%',
              filter: 'drop-shadow(0 10px 25px rgba(15, 23, 42, 0.08))'
            }}
          >
            <defs>
              <filter id="simpleMapShadow" x="-5%" y="-5%" width="115%" height="115%">
                <feDropShadow dx="0" dy="4" stdDeviation="6" floodColor="#0f172a" floodOpacity="0.08" />
              </filter>
            </defs>

            {/* Base Map State Polygons */}
            <g id="mapBaseGeometry" filter="url(#simpleMapShadow)">
              {INDIA_REGIONS.map((state) => {
                const isSelected = selectedState?.code === state.code;
                const isHovered = hoveredState?.code === state.code;
                const tier = COLOR_TIERS[state.importance];
                const isDimmed = activeFilter !== 'ALL' && state.importance !== activeFilter;

                let fill = '#ffffff';
                if (isSelected) fill = tier.bgLight;
                else if (isHovered) fill = '#f8fafc';

                return (
                  <path
                    key={state.code}
                    d={state.path}
                    fill={fill}
                    stroke={isSelected ? tier.color : isHovered ? '#0f172a' : '#94a3b8'}
                    strokeWidth={isSelected ? 2.5 : 1.5}
                    strokeLinejoin="round"
                    onClick={() => setSelectedState(state)}
                    onMouseEnter={() => setHoveredState(state)}
                    onMouseLeave={() => setHoveredState(null)}
                    style={{
                      cursor: 'pointer',
                      opacity: isDimmed ? 0.25 : 1,
                      transition: 'all 0.15s ease'
                    }}
                  >
                    <title>{state.name} ({tier.label})</title>
                  </path>
                );
              })}
            </g>

            {/* Color Coordinated Hotspot Pins & State Badges */}
            <g id="mapHotspots">
              {INDIA_REGIONS.map((state) => {
                const isSelected = selectedState?.code === state.code;
                const isHovered = hoveredState?.code === state.code;
                const tier = COLOR_TIERS[state.importance];
                const isDimmed = activeFilter !== 'ALL' && state.importance !== activeFilter;

                return (
                  <g 
                    key={`pin-${state.code}`}
                    onClick={() => setSelectedState(state)}
                    onMouseEnter={() => setHoveredState(state)}
                    onMouseLeave={() => setHoveredState(null)}
                    style={{ 
                      cursor: 'pointer',
                      opacity: isDimmed ? 0.25 : 1,
                      transition: 'opacity 0.2s ease'
                    }}
                  >
                    {/* Pulsing Beacon for High Importance */}
                    {state.importance === 'HIGH' && (
                      <circle
                        cx={state.cx}
                        cy={state.cy}
                        r="12"
                        fill="none"
                        stroke={tier.color}
                        strokeWidth="1.5"
                        opacity="0.6"
                      >
                        <animate 
                          attributeName="r" 
                          values="6;16;6" 
                          dur="2.2s" 
                          repeatCount="indefinite" 
                        />
                        <animate 
                          attributeName="opacity" 
                          values="0.8;0.1;0.8" 
                          dur="2.2s" 
                          repeatCount="indefinite" 
                        />
                      </circle>
                    )}

                    {/* Outer Glow Halo on Hover / Select */}
                    {(isSelected || isHovered) && (
                      <circle
                        cx={state.cx}
                        cy={state.cy}
                        r={14}
                        fill={tier.color}
                        opacity={0.25}
                      />
                    )}

                    {/* Core State Pin Dot with Color Coordination */}
                    <circle
                      cx={state.cx}
                      cy={state.cy}
                      r={isSelected ? 6 : state.code === 'DL' ? 5.5 : 4.5}
                      fill={tier.color}
                      stroke="#ffffff"
                      strokeWidth="1.8"
                    />

                    {/* State Name Callout Badge */}
                    <g transform={`translate(${state.cx + 8}, ${state.cy - 9})`}>
                      <rect
                        x="0"
                        y="0"
                        width={state.name.length * 6.2 + 20}
                        height="18"
                        rx="3"
                        fill={isSelected ? '#0f172a' : '#ffffff'}
                        stroke={isSelected ? '#0f172a' : tier.border}
                        strokeWidth="1.2"
                        filter="drop-shadow(0 1px 3px rgba(0,0,0,0.08))"
                      />

                      {/* Color Stripe on Left Edge */}
                      <rect
                        x="0"
                        y="0"
                        width="3.5"
                        height="18"
                        rx="1.5"
                        fill={tier.color}
                      />

                      <text
                        x="8"
                        y="12.5"
                        fontSize="8.5"
                        fontWeight="700"
                        fill={isSelected ? '#ffffff' : '#0f172a'}
                        fontFamily="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
                      >
                        {state.name} ({state.cases})
                      </text>
                    </g>
                  </g>
                );
              })}
            </g>
          </svg>
        </div>

        {/* Floating Map Legend (Color Coordination Guide) */}
        <div className="map-legend-dock" style={{ zIndex: 30 }}>
          <div className="map-legend-header">
            <span style={{ fontWeight: 800 }}>CASE SEVERITY & STATUS CODE</span>
          </div>
          <div className="map-legend-items-grid">
            <div className="map-legend-item-card red">
              <span className="color-dot red" />
              <div>
                <div className="legend-label">Red</div>
                <div className="legend-desc">High Importance / Big Case</div>
              </div>
            </div>

            <div className="map-legend-item-card yellow">
              <span className="color-dot yellow" />
              <div>
                <div className="legend-label">Yellow</div>
                <div className="legend-desc">Medium Importance</div>
              </div>
            </div>

            <div className="map-legend-item-card green">
              <span className="color-dot green" />
              <div>
                <div className="legend-label">Green</div>
                <div className="legend-desc">Low Importance / Minor</div>
              </div>
            </div>

            <div className="map-legend-item-card blue">
              <span className="color-dot blue" />
              <div>
                <div className="legend-label">Blue</div>
                <div className="legend-desc">Closed Case / Resolved</div>
              </div>
            </div>
          </div>
        </div>

        {/* State Cases Drawer */}
        {selectedState && (
          <div className="state-cases-panel" style={{ zIndex: 40 }}>
            <div 
              className="panel-header"
              style={{
                borderTop: `4px solid ${COLOR_TIERS[selectedState.importance].color}`
              }}
            >
              <div>
                <div className="panel-title" style={{ display: 'flex', alignItems: 'center', gap: '0.45rem' }}>
                  <span 
                    style={{
                      width: '10px',
                      height: '10px',
                      borderRadius: '50%',
                      background: COLOR_TIERS[selectedState.importance].color,
                      display: 'inline-block'
                    }} 
                  />
                  <span>{selectedState.name} ({selectedState.code})</span>
                </div>
                <div style={{ fontSize: '0.72rem', color: 'var(--text-secondary)', marginTop: '0.2rem' }}>
                  Capital: {selectedState.capital} • Status: <strong>{COLOR_TIERS[selectedState.importance].label}</strong>
                </div>
              </div>
              <button className="panel-close-btn" onClick={() => setSelectedState(null)}>
                <X size={18} />
              </button>
            </div>

            <div className="case-card-list">
              {activeCasesForState.map((caseItem) => {
                const itemTier = COLOR_TIERS[caseItem.importance || selectedState.importance];

                return (
                  <div 
                    key={caseItem.id}
                    className="case-card"
                    onClick={() => onSelectCase(caseItem.id)}
                    style={{
                      borderLeft: `4px solid ${itemTier.color}`
                    }}
                  >
                    <div className="case-card-header">
                      <span className="case-card-id">{caseItem.id}</span>
                      <span 
                        style={{
                          fontSize: '0.68rem',
                          fontWeight: 700,
                          padding: '0.15rem 0.5rem',
                          borderRadius: '4px',
                          background: itemTier.bgLight,
                          color: itemTier.badgeText,
                          border: `1px solid ${itemTier.border}`
                        }}
                      >
                        {itemTier.label}
                      </span>
                    </div>

                    <h3 className="case-card-title">{caseItem.title}</h3>
                    <p className="case-card-summary">{caseItem.summary}</p>

                    <div className="case-card-footer">
                      <span style={{ fontWeight: 600 }}>{caseItem.fir}</span>
                      <span style={{ color: itemTier.color, fontWeight: 700, display: 'flex', alignItems: 'center', gap: '0.2rem' }}>
                        Open Case <ArrowRight size={13} />
                      </span>
                    </div>
                  </div>
                );
              })}

              {activeCasesForState.length === 0 && (
                <div style={{ padding: '2rem 1.5rem', textAlign: 'center', color: 'var(--text-secondary)' }}>
                  <div style={{ fontWeight: 600, color: 'var(--text-primary)', marginBottom: '0.35rem' }}>
                    Dominant Log: {selectedState.dominantCase}
                  </div>
                  <div style={{ fontSize: '0.78rem' }}>
                    {selectedState.cases} active records under {COLOR_TIERS[selectedState.importance].label}.
                  </div>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

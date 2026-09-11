import React, { useState } from 'react';
import { 
  ChevronRight, 
  X, 
  ArrowRight,
  Rotate3d
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

// Standard normal India state coordinates & color-coordinated data
const INDIA_REGIONS = [
  // 🔴 RED - HIGH IMPORTANCE / BIG CASES
  { code: 'DL', name: 'Delhi NCR', capital: 'New Delhi', x: 345, y: 245, cases: 4, importance: 'HIGH', dominantCase: 'Kidnapping & Criminal Nexus (DL-2026-0412)' },
  { code: 'UP', name: 'Uttar Pradesh', capital: 'Lucknow', x: 445, y: 285, cases: 6, importance: 'HIGH', dominantCase: 'Inter-State Arms Supply Syndicate' },
  { code: 'MH', name: 'Maharashtra', capital: 'Mumbai', x: 275, y: 520, cases: 7, importance: 'HIGH', dominantCase: 'Organized Hawala & Money Laundering' },
  { code: 'PB', name: 'Punjab', capital: 'Chandigarh', x: 285, y: 185, cases: 3, importance: 'HIGH', dominantCase: 'Cross-Border Drone Contraband Network' },

  // 🟡 YELLOW - MEDIUM IMPORTANCE
  { code: 'RJ', name: 'Rajasthan', capital: 'Jaipur', x: 235, y: 295, cases: 4, importance: 'MEDIUM', dominantCase: 'Recruitment & Examination Fraud' },
  { code: 'HR', name: 'Haryana', capital: 'Chandigarh', x: 315, y: 225, cases: 3, importance: 'MEDIUM', dominantCase: 'Vehicle Re-Registration Racket' },
  { code: 'WB', name: 'West Bengal', capital: 'Kolkata', x: 635, y: 410, cases: 5, importance: 'MEDIUM', dominantCase: 'Counterfeit Currency Circulation' },
  { code: 'BR', name: 'Bihar', capital: 'Patna', x: 575, y: 320, cases: 3, importance: 'MEDIUM', dominantCase: 'Synthetic SIM Cloning Ring' },
  { code: 'MP', name: 'Madhya Pradesh', capital: 'Bhopal', x: 365, y: 395, cases: 4, importance: 'MEDIUM', dominantCase: 'Mining Heavy Equipment Scam' },
  { code: 'TG', name: 'Telangana', capital: 'Hyderabad', x: 385, y: 575, cases: 3, importance: 'MEDIUM', dominantCase: 'Crypto Investment Layering' },
  { code: 'AS', name: 'Assam', capital: 'Dispur', x: 745, y: 325, cases: 3, importance: 'MEDIUM', dominantCase: 'Wildlife Transit Network' },

  // 🟢 GREEN - LOW IMPORTANCE / MINOR CASES / ROUTINE
  { code: 'GJ', name: 'Gujarat', capital: 'Gandhinagar', x: 165, y: 395, cases: 2, importance: 'LOW', dominantCase: 'Port Cargo Weight Discrepancy' },
  { code: 'OR', name: 'Odisha', capital: 'Bhubaneswar', x: 555, y: 485, cases: 3, importance: 'LOW', dominantCase: 'Commercial Trademark Dispute' },
  { code: 'CT', name: 'Chhattisgarh', capital: 'Raipur', x: 475, y: 455, cases: 2, importance: 'LOW', dominantCase: 'Highway Checkpost Log Audit' },
  { code: 'JH', name: 'Jharkhand', capital: 'Ranchi', x: 565, y: 390, cases: 2, importance: 'LOW', dominantCase: 'Industrial Equipment Verification' },
  { code: 'AP', name: 'Andhra Pradesh', capital: 'Amaravati', x: 405, y: 655, cases: 3, importance: 'LOW', dominantCase: 'Retail Counterfeit Brand Alert' },
  { code: 'KL', name: 'Kerala', capital: 'Thiruvananthapuram', x: 285, y: 795, cases: 2, importance: 'LOW', dominantCase: 'Local Stamp Paper Forgery' },
  { code: 'HP', name: 'Himachal Pradesh', capital: 'Shimla', x: 345, y: 150, cases: 1, importance: 'LOW', dominantCase: 'Tourist ID Verification Log' },
  { code: 'UT', name: 'Uttarakhand', capital: 'Dehradun', x: 395, y: 195, cases: 2, importance: 'LOW', dominantCase: 'Toll Barrier Evasion Record' },
  { code: 'JK', name: 'Jammu & Kashmir', capital: 'Srinagar', x: 275, y: 105, cases: 2, importance: 'LOW', dominantCase: 'Routine Entry Checkpoint Register' },
  { code: 'LA', name: 'Ladakh', capital: 'Leh', x: 360, y: 80, cases: 1, importance: 'LOW', dominantCase: 'High Altitude Station Report' },
  { code: 'GA', name: 'Goa', capital: 'Panaji', x: 225, y: 645, cases: 1, importance: 'LOW', dominantCase: 'Commercial Establishment Infraction' },
  { code: 'SK', name: 'Sikkim', capital: 'Gangtok', x: 625, y: 275, cases: 1, importance: 'LOW', dominantCase: 'Border Transit Goods Inspection' },
  { code: 'AR', name: 'Arunachal Pradesh', capital: 'Itanagar', x: 805, y: 260, cases: 1, importance: 'LOW', dominantCase: 'Regional Patrol Register' },
  { code: 'ML', name: 'Meghalaya', capital: 'Shillong', x: 725, y: 355, cases: 1, importance: 'LOW', dominantCase: 'Timber Movement Permit Check' },
  { code: 'NL', name: 'Nagaland', capital: 'Kohima', x: 835, y: 330, cases: 1, importance: 'LOW', dominantCase: 'Jurisdictional Boundary Log' },
  { code: 'MN', name: 'Manipur', capital: 'Imphal', x: 825, y: 375, cases: 1, importance: 'LOW', dominantCase: 'Local Movement Permit Audit' },
  { code: 'TR', name: 'Tripura', capital: 'Agartala', x: 735, y: 405, cases: 1, importance: 'LOW', dominantCase: 'Border Fencing Maintenance Log' },
  { code: 'MZ', name: 'Mizoram', capital: 'Aizawl', x: 805, y: 425, cases: 1, importance: 'LOW', dominantCase: 'Routine Verification Dossier' },

  // 🔵 BLUE - CLOSED CASES / RESOLVED / CHARGESHEETED
  { code: 'KA', name: 'Karnataka', capital: 'Bengaluru', x: 295, y: 675, cases: 3, importance: 'CLOSED', dominantCase: 'SIM Box Gateway (Chargesheet Filed)' },
  { code: 'TN', name: 'Tamil Nadu', capital: 'Chennai', x: 365, y: 775, cases: 4, importance: 'CLOSED', dominantCase: 'Spurious Pharma Network (Convicted)' }
];

export default function IndiaMap({ onSelectCase }) {
  const [selectedState, setSelectedState] = useState(null);
  const [hoveredState, setHoveredState] = useState(null);
  const [tilt, setTilt] = useState({ rx: 18, rz: -3 });
  const [is3DMode, setIs3DMode] = useState(true);
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

  const handleMouseMove = (e) => {
    if (!is3DMode) return;
    const rect = e.currentTarget.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const rx = 16 + ((y / rect.height) - 0.5) * 14;
    const rz = -4 + ((x / rect.width) - 0.5) * 12;
    setTilt({ rx, rz });
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
        onMouseMove={handleMouseMove}
        style={{ 
          perspective: is3DMode ? '1100px' : 'none',
          background: '#ffffff'
        }}
      >
        {/* Top Filter Chips & View Mode Controls */}
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

          <button 
            className={`header-btn ${is3DMode ? 'primary' : ''}`}
            onClick={() => setIs3DMode(!is3DMode)}
            style={{ marginLeft: 'auto' }}
          >
            <Rotate3d size={14} />
            {is3DMode ? '3D Perspective' : '2D Overhead'}
          </button>
        </div>

        {/* 3D Container Stage */}
        <div 
          className="map-3d-stage"
          style={{
            transform: is3DMode 
              ? `rotateX(${tilt.rx}deg) rotateZ(${tilt.rz}deg) scale(0.92)` 
              : 'none',
            transformStyle: 'preserve-3d',
            transition: 'transform 0.15s ease-out',
            width: '640px',
            height: '740px',
            position: 'relative'
          }}
        >
          {/* Authentic Normal Vector Outline of India */}
          <svg
            viewBox="0 0 900 960"
            style={{
              width: '100%',
              height: '100%',
              filter: 'drop-shadow(0 16px 32px rgba(15, 23, 42, 0.12))'
            }}
          >
            {/* SVG Filter for Glowing Beacons */}
            <defs>
              <filter id="beacon-glow-red" x="-50%" y="-50%" width="200%" height="200%">
                <feGaussianBlur stdDeviation="4" result="blur" />
                <feMerge>
                  <feMergeNode in="blur" />
                  <feMergeNode in="SourceGraphic" />
                </feMerge>
              </filter>
            </defs>

            {/* Natural Geographic Map Outline of India */}
            <path
              d="M 270,30 
                 C 290,15 340,25 365,45 
                 C 390,65 375,100 360,115 
                 C 380,125 415,150 420,185 
                 C 455,190 530,225 580,255 
                 C 620,250 635,275 625,290 
                 C 645,290 670,270 730,245 
                 C 790,220 840,250 835,295 
                 C 830,335 790,375 805,435 
                 C 790,470 760,470 740,430 
                 C 730,390 690,420 670,440 
                 C 640,450 635,410 610,380 
                 C 590,360 570,370 560,420 
                 C 580,450 600,500 580,545 
                 C 540,570 480,570 455,610 
                 C 440,660 415,745 370,830 
                 C 345,880 300,900 290,870 
                 C 275,820 280,760 260,700 
                 C 230,660 200,600 215,530 
                 C 195,490 145,465 110,470 
                 C 70,445 75,370 120,345 
                 C 140,330 185,350 205,320 
                 C 175,280 150,230 185,190 
                 C 220,165 240,180 255,140 
                 C 240,110 240,65 270,30 Z"
              fill="#ffffff"
              stroke="#0f172a"
              strokeWidth="2.5"
              strokeLinejoin="round"
            />

            {/* Internal State Boundaries Contours */}
            <path
              d="M 255,140 Q 300,160 360,115
                 M 285,185 Q 360,200 420,185
                 M 205,320 Q 330,340 450,290
                 M 120,345 Q 260,375 365,395
                 M 205,320 Q 300,430 475,455
                 M 450,290 Q 560,320 610,380
                 M 215,530 Q 360,540 455,610
                 M 260,700 Q 350,680 440,660
                 M 275,820 Q 345,800 370,830
                 M 610,380 Q 700,320 805,435"
              fill="none"
              stroke="#94a3b8"
              strokeWidth="1.2"
              strokeDasharray="3 3"
            />

            {/* State Markers & Callout Pills with Color Coordination */}
            {INDIA_REGIONS.map((state) => {
              const isSelected = selectedState?.code === state.code;
              const isHovered = hoveredState?.code === state.code;
              const tier = COLOR_TIERS[state.importance];
              const isDimmed = activeFilter !== 'ALL' && state.importance !== activeFilter;

              return (
                <g 
                  key={state.code}
                  onClick={() => setSelectedState(state)}
                  onMouseEnter={() => setHoveredState(state)}
                  onMouseLeave={() => setHoveredState(null)}
                  style={{ 
                    cursor: 'pointer',
                    opacity: isDimmed ? 0.25 : 1,
                    transition: 'opacity 0.2s ease, transform 0.2s ease'
                  }}
                >
                  {/* Pulsing Beacon Ring for High / Critical States */}
                  {state.importance === 'HIGH' && (
                    <circle
                      cx={state.x}
                      cy={state.y}
                      r="12"
                      fill="none"
                      stroke={tier.color}
                      strokeWidth="1.5"
                      opacity="0.6"
                    >
                      <animate 
                        attributeName="r" 
                        values="8;18;8" 
                        dur="2.4s" 
                        repeatCount="indefinite" 
                      />
                      <animate 
                        attributeName="opacity" 
                        values="0.8;0.1;0.8" 
                        dur="2.4s" 
                        repeatCount="indefinite" 
                      />
                    </circle>
                  )}

                  {/* Outer Glow Halo on Hover / Select */}
                  {(isSelected || isHovered) && (
                    <circle
                      cx={state.x}
                      cy={state.y}
                      r={isSelected ? 16 : 12}
                      fill={tier.color}
                      opacity={isSelected ? 0.35 : 0.22}
                    />
                  )}

                  {/* Core State Pin Dot with Color Coordination */}
                  <circle
                    cx={state.x}
                    cy={state.y}
                    r={isSelected ? 6 : state.importance === 'HIGH' ? 5.5 : 4.5}
                    fill={tier.color}
                    stroke="#ffffff"
                    strokeWidth="1.8"
                  />

                  {/* State Name Callout Pill with Left Color Accent */}
                  <g transform={`translate(${state.x + 8}, ${state.y - 10})`}>
                    <rect
                      x="0"
                      y="0"
                      width={state.name.length * 6.5 + 24}
                      height="20"
                      rx="4"
                      fill={isSelected ? '#0f172a' : '#ffffff'}
                      stroke={isSelected ? '#0f172a' : tier.border}
                      strokeWidth="1.2"
                      filter="drop-shadow(0 2px 4px rgba(0,0,0,0.08))"
                    />

                    {/* Color Stripe on Left Edge of Pill */}
                    <rect
                      x="0"
                      y="0"
                      width="4"
                      height="20"
                      rx="2"
                      fill={tier.color}
                    />

                    <text
                      x="10"
                      y="13"
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

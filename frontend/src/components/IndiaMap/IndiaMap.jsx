import React, { useState } from 'react';
import { 
  MapPin, 
  ChevronRight, 
  X, 
  ArrowRight,
  Compass,
  Rotate3d,
  Layers,
  ZoomIn,
  ZoomOut
} from 'lucide-react';
import { STATES_DATA, CASES_LIST } from '../../data/casesData';

// Standard normal India state coordinates & data
const INDIA_REGIONS = [
  { code: 'DL', name: 'Delhi NCR', capital: 'New Delhi', x: 345, y: 245, cases: 4, risk: 'HIGH', highlight: true },
  { code: 'JK', name: 'Jammu & Kashmir', capital: 'Srinagar', x: 275, y: 105, cases: 2, risk: 'LOW' },
  { code: 'LA', name: 'Ladakh', capital: 'Leh', x: 360, y: 80, cases: 1, risk: 'LOW' },
  { code: 'PB', name: 'Punjab', capital: 'Chandigarh', x: 285, y: 185, cases: 3, risk: 'LOW' },
  { code: 'HR', name: 'Haryana', capital: 'Chandigarh', x: 315, y: 225, cases: 3, risk: 'MED' },
  { code: 'HP', name: 'Himachal Pradesh', capital: 'Shimla', x: 345, y: 150, cases: 1, risk: 'LOW' },
  { code: 'UT', name: 'Uttarakhand', capital: 'Dehradun', x: 395, y: 195, cases: 2, risk: 'LOW' },
  { code: 'RJ', name: 'Rajasthan', capital: 'Jaipur', x: 235, y: 295, cases: 4, risk: 'MED' },
  { code: 'UP', name: 'Uttar Pradesh', capital: 'Lucknow', x: 445, y: 285, cases: 6, risk: 'HIGH' },
  { code: 'BR', name: 'Bihar', capital: 'Patna', x: 575, y: 320, cases: 3, risk: 'MED' },
  { code: 'WB', name: 'West Bengal', capital: 'Kolkata', x: 635, y: 410, cases: 5, risk: 'MED' },
  { code: 'JH', name: 'Jharkhand', capital: 'Ranchi', x: 565, y: 390, cases: 2, risk: 'LOW' },
  { code: 'OR', name: 'Odisha', capital: 'Bhubaneswar', x: 555, y: 485, cases: 3, risk: 'LOW' },
  { code: 'MP', name: 'Madhya Pradesh', capital: 'Bhopal', x: 365, y: 395, cases: 4, risk: 'MED' },
  { code: 'GJ', name: 'Gujarat', capital: 'Gandhinagar', x: 165, y: 395, cases: 2, risk: 'LOW' },
  { code: 'MH', name: 'Maharashtra', capital: 'Mumbai', x: 275, y: 520, cases: 7, risk: 'MED' },
  { code: 'CT', name: 'Chhattisgarh', capital: 'Raipur', x: 475, y: 455, cases: 2, risk: 'LOW' },
  { code: 'TG', name: 'Telangana', capital: 'Hyderabad', x: 385, y: 575, cases: 3, risk: 'MED' },
  { code: 'AP', name: 'Andhra Pradesh', capital: 'Amaravati', x: 405, y: 655, cases: 3, risk: 'LOW' },
  { code: 'KA', name: 'Karnataka', capital: 'Bengaluru', x: 295, y: 675, cases: 3, risk: 'MED' },
  { code: 'GA', name: 'Goa', capital: 'Panaji', x: 225, y: 645, cases: 1, risk: 'LOW' },
  { code: 'TN', name: 'Tamil Nadu', capital: 'Chennai', x: 365, y: 775, cases: 4, risk: 'LOW' },
  { code: 'KL', name: 'Kerala', capital: 'Thiruvananthapuram', x: 285, y: 795, cases: 2, risk: 'LOW' },
  { code: 'AS', name: 'Assam', capital: 'Dispur', x: 745, y: 325, cases: 3, risk: 'MED' },
  { code: 'SK', name: 'Sikkim', capital: 'Gangtok', x: 625, y: 275, cases: 1, risk: 'LOW' },
  { code: 'AR', name: 'Arunachal Pradesh', capital: 'Itanagar', x: 805, y: 260, cases: 1, risk: 'LOW' },
  { code: 'ML', name: 'Meghalaya', capital: 'Shillong', x: 725, y: 355, cases: 1, risk: 'LOW' },
  { code: 'NL', name: 'Nagaland', capital: 'Kohima', x: 835, y: 330, cases: 1, risk: 'LOW' },
  { code: 'MN', name: 'Manipur', capital: 'Imphal', x: 825, y: 375, cases: 1, risk: 'LOW' },
  { code: 'TR', name: 'Tripura', capital: 'Agartala', x: 735, y: 405, cases: 1, risk: 'LOW' },
  { code: 'MZ', name: 'Mizoram', capital: 'Aizawl', x: 805, y: 425, cases: 1, risk: 'LOW' }
];

export default function IndiaMap({ onSelectCase }) {
  const [selectedState, setSelectedState] = useState(null);
  const [hoveredState, setHoveredState] = useState(null);
  const [tilt, setTilt] = useState({ rx: 20, rz: -4 });
  const [is3DMode, setIs3DMode] = useState(true);

  const activeCasesForState = selectedState ? CASES_LIST[selectedState.code] || [] : [];

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
          <div style={{ fontSize: '0.72rem', fontWeight: 800, color: '#0f172a', letterSpacing: '0.06em', marginBottom: '0.2rem' }}>
            NATIONAL INVESTIGATION PORTAL
          </div>
          <h2 className="map-sidebar-title">India Jurisdictional Map</h2>
          <p className="map-sidebar-desc">
            Select any state on the map to view active investigative cases
          </p>
        </div>

        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-label">Active Cases</div>
            <div className="stat-val" style={{ color: '#0f172a' }}>18 Total</div>
          </div>
          <div className="stat-card">
            <div className="stat-label">High Priority</div>
            <div className="stat-val" style={{ color: '#dc2626' }}>5 Alerts</div>
          </div>
        </div>

        <div className="state-list-section">
          <div className="section-heading">
            <span>State / UT</span>
            <span>Cases</span>
          </div>

          {INDIA_REGIONS.map((state) => {
            const isSelected = selectedState?.code === state.code;
            return (
              <div 
                key={state.code}
                className={`state-item ${isSelected ? 'selected' : ''}`}
                onClick={() => setSelectedState(state)}
                onMouseEnter={() => setHoveredState(state)}
                onMouseLeave={() => setHoveredState(null)}
              >
                <div>
                  <div className="state-item-name">{state.name}</div>
                  <div className="state-item-cases" style={{ fontSize: '0.68rem' }}>
                    {state.capital}
                  </div>
                </div>

                <div style={{ display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
                  <span className={`gov-badge-subtle ${state.code === 'DL' ? 'gov-badge-lead' : ''}`}>
                    {state.cases} Cases
                  </span>
                  <ChevronRight size={14} color="var(--text-muted)" />
                </div>
              </div>
            );
          })}
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
        {/* Top Control Bar */}
        <div className="map-instructions" style={{ zIndex: 20 }}>
          <Compass size={15} color="#0f172a" />
          <span>Click any <strong>State Node</strong> on the map of India to inspect active cases.</span>
        </div>

        <div style={{ position: 'absolute', top: '1.25rem', right: '1.5rem', display: 'flex', gap: '0.45rem', zIndex: 20 }}>
          <button 
            className={`header-btn ${is3DMode ? 'primary' : ''}`}
            onClick={() => setIs3DMode(!is3DMode)}
          >
            <Rotate3d size={14} />
            {is3DMode ? '3D View' : '2D View'}
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
              filter: 'drop-shadow(0 12px 24px rgba(15, 23, 42, 0.1))'
            }}
          >
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
              stroke="#64748b"
              strokeWidth="1.2"
              strokeDasharray="3 3"
            />

            {/* State Markers & Callout Pills */}
            {INDIA_REGIONS.map((state) => {
              const isSelected = selectedState?.code === state.code;
              const isHovered = hoveredState?.code === state.code;

              return (
                <g 
                  key={state.code}
                  onClick={() => setSelectedState(state)}
                  onMouseEnter={() => setHoveredState(state)}
                  onMouseLeave={() => setHoveredState(null)}
                  style={{ cursor: 'pointer' }}
                >
                  {/* Outer Ring on Hover / Select */}
                  {(isSelected || isHovered) && (
                    <circle
                      cx={state.x}
                      cy={state.y}
                      r={isSelected ? 14 : 10}
                      fill={isSelected ? '#0f172a' : '#94a3b8'}
                      opacity={isSelected ? 0.2 : 0.15}
                    />
                  )}

                  {/* Core State Pin Dot */}
                  <circle
                    cx={state.x}
                    cy={state.y}
                    r={state.code === 'DL' ? 5.5 : isSelected ? 5 : 4}
                    fill={state.code === 'DL' ? '#dc2626' : isSelected ? '#0f172a' : '#1e293b'}
                    stroke="#ffffff"
                    strokeWidth="1.5"
                  />

                  {/* State Name Pill */}
                  <rect
                    x={state.x + 8}
                    y={state.y - 9}
                    width={state.code === 'DL' ? 76 : state.name.length * 6.5 + 16}
                    height="18"
                    rx="3"
                    fill={isSelected ? '#0f172a' : '#ffffff'}
                    stroke={isSelected ? '#0f172a' : '#cbd5e1'}
                    strokeWidth="1"
                    filter="drop-shadow(0 1px 2px rgba(0,0,0,0.08))"
                  />

                  <text
                    x={state.x + 14}
                    y={state.y + 3.5}
                    fontSize="8"
                    fontWeight="700"
                    fill={isSelected ? '#ffffff' : '#0f172a'}
                    fontFamily="sans-serif"
                  >
                    {state.name} ({state.cases})
                  </text>
                </g>
              );
            })}
          </svg>
        </div>

        {/* State Cases Drawer */}
        {selectedState && (
          <div className="state-cases-panel" style={{ zIndex: 40 }}>
            <div className="panel-header">
              <div>
                <div className="panel-title">{selectedState.name} ({selectedState.code})</div>
                <div style={{ fontSize: '0.72rem', color: 'var(--text-secondary)' }}>
                  Capital: {selectedState.capital} • {activeCasesForState.length} Active Investigations
                </div>
              </div>
              <button className="panel-close-btn" onClick={() => setSelectedState(null)}>
                <X size={18} />
              </button>
            </div>

            <div className="case-card-list">
              {activeCasesForState.map((caseItem) => (
                <div 
                  key={caseItem.id}
                  className="case-card"
                  onClick={() => onSelectCase(caseItem.id)}
                >
                  <div className="case-card-header">
                    <span className="case-card-id">{caseItem.id}</span>
                    <span className="gov-badge-match">
                      {caseItem.matchRate} Case Match
                    </span>
                  </div>

                  <h3 className="case-card-title">{caseItem.title}</h3>
                  <p className="case-card-summary">{caseItem.summary}</p>

                  <div className="case-card-footer">
                    <span>{caseItem.fir}</span>
                    <span style={{ color: '#0f172a', fontWeight: 700, display: 'flex', alignItems: 'center', gap: '0.2rem' }}>
                      Open Workspace <ArrowRight size={13} />
                    </span>
                  </div>
                </div>
              ))}

              {activeCasesForState.length === 0 && (
                <div style={{ padding: '2rem', textAlign: 'center', color: 'var(--text-secondary)' }}>
                  No active investigations logged for {selectedState.name}.
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

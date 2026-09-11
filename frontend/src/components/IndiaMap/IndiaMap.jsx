import React, { useState } from 'react';
import { 
  Compass, 
  Rotate3d, 
  ZoomIn, 
  ZoomOut, 
  ChevronRight, 
  X, 
  ArrowRight,
  ShieldAlert
} from 'lucide-react';
import { CASES_LIST } from '../../data/casesData';

// Black & White Administrative Polygons matching the provided reference image
export const BW_INDIA_STATES = [
  // North
  {
    code: 'LA',
    name: 'Ladakh',
    capital: 'Leh',
    cx: 295,
    cy: 70,
    path: 'M 260,35 C 275,25 310,20 335,45 C 350,60 365,100 340,120 C 315,130 290,115 270,105 C 255,95 250,60 260,35 Z',
    casesCount: 1
  },
  {
    code: 'JK',
    name: 'Jammu & Kashmir',
    capital: 'Srinagar / Jammu',
    cx: 235,
    cy: 90,
    path: 'M 215,60 C 230,45 255,40 265,55 C 255,80 260,110 245,125 C 230,135 210,120 205,100 C 200,80 205,70 215,60 Z',
    casesCount: 2
  },
  {
    code: 'HP',
    name: 'Himachal Pradesh',
    capital: 'Shimla',
    cx: 295,
    cy: 145,
    path: 'M 265,120 C 285,115 315,120 330,140 C 320,165 295,175 275,170 C 265,160 255,140 265,120 Z',
    casesCount: 1
  },
  {
    code: 'PB',
    name: 'Punjab',
    capital: 'Chandigarh',
    cx: 245,
    cy: 175,
    path: 'M 230,140 C 250,135 270,145 275,165 C 265,195 240,205 225,190 C 215,175 220,150 230,140 Z',
    casesCount: 3
  },
  {
    code: 'UT',
    name: 'Uttarakhand',
    capital: 'Dehradun',
    cx: 345,
    cy: 185,
    path: 'M 310,160 C 335,145 365,160 380,185 C 370,210 340,220 320,205 C 305,190 305,170 310,160 Z',
    casesCount: 2
  },
  {
    code: 'HR',
    name: 'Haryana',
    capital: 'Chandigarh',
    cx: 270,
    cy: 215,
    path: 'M 255,185 C 280,180 295,195 300,225 C 290,250 265,255 245,235 C 240,215 245,195 255,185 Z',
    casesCount: 3
  },
  {
    code: 'DL',
    name: 'Delhi',
    capital: 'New Delhi',
    cx: 295,
    cy: 232,
    isCapital: true,
    path: 'M 288,226 C 296,222 304,226 304,236 C 302,244 292,244 288,238 Z',
    casesCount: 4,
    highlight: true
  },

  // West & Central
  {
    code: 'RJ',
    name: 'Rajasthan',
    capital: 'Jaipur',
    cx: 200,
    cy: 285,
    path: 'M 160,205 C 215,195 260,230 265,280 C 270,335 220,380 170,365 C 130,345 125,260 160,205 Z',
    casesCount: 4
  },
  {
    code: 'UP',
    name: 'Uttar Pradesh',
    capital: 'Lucknow',
    cx: 395,
    cy: 285,
    path: 'M 305,215 C 380,210 470,255 485,310 C 470,355 385,360 330,340 C 295,320 280,250 305,215 Z',
    casesCount: 6
  },
  {
    code: 'GJ',
    name: 'Gujarat',
    capital: 'Gandhinagar',
    cx: 130,
    cy: 395,
    path: 'M 100,340 C 150,330 180,370 185,410 C 175,465 110,470 75,430 C 60,390 75,355 100,340 Z',
    casesCount: 2
  },
  {
    code: 'MP',
    name: 'Madhya Pradesh',
    capital: 'Bhopal',
    cx: 335,
    cy: 400,
    path: 'M 255,340 C 350,330 435,360 450,420 C 430,475 320,490 250,460 C 215,420 215,365 255,340 Z',
    casesCount: 4
  },
  {
    code: 'BR',
    name: 'Bihar',
    capital: 'Patna',
    cx: 525,
    cy: 320,
    path: 'M 480,285 C 530,280 575,300 585,335 C 570,370 515,375 475,355 C 465,330 465,300 480,285 Z',
    casesCount: 3
  },
  {
    code: 'JH',
    name: 'Jharkhand',
    capital: 'Ranchi',
    cx: 515,
    cy: 395,
    path: 'M 475,360 C 520,355 560,370 565,410 C 550,445 495,450 465,425 C 455,400 460,375 475,360 Z',
    casesCount: 2
  },
  {
    code: 'WB',
    name: 'West Bengal',
    capital: 'Kolkata',
    cx: 585,
    cy: 405,
    path: 'M 565,335 C 585,320 610,340 615,385 C 625,445 585,480 565,465 C 555,430 555,365 565,335 Z',
    casesCount: 5
  },
  {
    code: 'CT',
    name: 'Chhattisgarh',
    capital: 'Raipur',
    cx: 435,
    cy: 475,
    path: 'M 415,415 C 455,410 475,450 470,510 C 450,560 415,570 395,530 C 385,480 395,430 415,415 Z',
    casesCount: 2
  },
  {
    code: 'OR',
    name: 'Odisha',
    capital: 'Bhubaneswar',
    cx: 520,
    cy: 485,
    path: 'M 475,445 C 535,430 580,465 590,515 C 570,560 500,565 465,535 C 455,490 460,460 475,445 Z',
    casesCount: 3
  },
  {
    code: 'MH',
    name: 'Maharashtra',
    capital: 'Mumbai',
    cx: 235,
    cy: 535,
    path: 'M 175,450 C 265,440 335,480 350,550 C 330,620 220,630 160,580 C 140,530 145,475 175,450 Z',
    casesCount: 7
  },

  // South
  {
    code: 'TG',
    name: 'Telangana',
    capital: 'Hyderabad',
    cx: 345,
    cy: 585,
    path: 'M 310,540 C 365,535 400,565 405,615 C 385,655 325,660 295,630 C 285,590 295,555 310,540 Z',
    casesCount: 3
  },
  {
    code: 'AP',
    name: 'Andhra Pradesh',
    capital: 'Amaravati',
    cx: 360,
    cy: 675,
    path: 'M 350,615 C 415,595 460,650 435,725 C 390,775 345,765 315,715 C 310,670 325,630 350,615 Z',
    casesCount: 3
  },
  {
    code: 'KA',
    name: 'Karnataka',
    capital: 'Bengaluru',
    cx: 250,
    cy: 695,
    path: 'M 215,610 C 275,600 310,645 305,730 C 285,795 225,800 195,745 C 180,690 190,635 215,610 Z',
    casesCount: 3
  },
  {
    code: 'GA',
    name: 'Goa',
    capital: 'Panaji',
    cx: 175,
    cy: 660,
    path: 'M 170,650 C 182,650 185,665 180,675 C 172,678 168,668 170,650 Z',
    casesCount: 1
  },
  {
    code: 'KL',
    name: 'Kerala',
    capital: 'Thiruvananthapuram',
    cx: 245,
    cy: 825,
    path: 'M 235,760 C 255,750 265,785 270,845 C 265,885 235,890 220,860 C 215,815 220,775 235,760 Z',
    casesCount: 2
  },
  {
    code: 'TN',
    name: 'Tamil Nadu',
    capital: 'Chennai',
    cx: 320,
    cy: 815,
    path: 'M 275,745 C 345,730 380,780 375,855 C 350,910 290,910 265,860 C 255,810 260,765 275,745 Z',
    casesCount: 4
  },

  // North-East
  {
    code: 'SK',
    name: 'Sikkim',
    capital: 'Gangtok',
    cx: 605,
    cy: 285,
    path: 'M 595,275 C 615,270 625,285 620,300 C 605,305 590,295 595,275 Z',
    casesCount: 1
  },
  {
    code: 'AS',
    name: 'Assam',
    capital: 'Dispur',
    cx: 715,
    cy: 325,
    path: 'M 655,300 C 745,290 775,330 765,365 C 725,385 660,370 655,300 Z',
    casesCount: 3
  },
  {
    code: 'AR',
    name: 'Arunachal Pradesh',
    capital: 'Itanagar',
    cx: 770,
    cy: 265,
    path: 'M 720,240 C 785,220 835,250 825,295 C 785,315 735,300 720,240 Z',
    casesCount: 1
  },
  {
    code: 'ML',
    name: 'Meghalaya',
    capital: 'Shillong',
    cx: 685,
    cy: 355,
    path: 'M 660,345 C 710,340 725,360 715,375 C 675,385 655,370 660,345 Z',
    casesCount: 1
  },
  {
    code: 'NL',
    name: 'Nagaland',
    capital: 'Kohima',
    cx: 805,
    cy: 335,
    path: 'M 790,315 C 815,315 825,340 815,360 C 795,365 785,340 790,315 Z',
    casesCount: 1
  },
  {
    code: 'MN',
    name: 'Manipur',
    capital: 'Imphal',
    cx: 800,
    cy: 385,
    path: 'M 785,365 C 810,365 820,390 810,415 C 790,420 780,395 785,365 Z',
    casesCount: 1
  },
  {
    code: 'TR',
    name: 'Tripura',
    capital: 'Agartala',
    cx: 695,
    cy: 415,
    path: 'M 685,395 C 710,395 715,420 705,435 C 685,440 680,415 685,395 Z',
    casesCount: 1
  },
  {
    code: 'MZ',
    name: 'Mizoram',
    capital: 'Aizawl',
    cx: 775,
    cy: 435,
    path: 'M 760,410 C 785,410 790,445 780,475 C 760,475 755,440 760,410 Z',
    casesCount: 1
  }
];

export default function IndiaMap({ onSelectCase }) {
  const [selectedState, setSelectedState] = useState(null);
  const [hoveredState, setHoveredState] = useState(null);
  const [tilt, setTilt] = useState({ rx: 26, rz: -6 });
  const [zoom, setZoom] = useState(1);
  const [is3DMode, setIs3DMode] = useState(true);

  const activeCasesForState = selectedState ? CASES_LIST[selectedState.code] || [] : [];

  const handleMouseMove = (e) => {
    if (!is3DMode) return;
    const rect = e.currentTarget.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const rx = 24 + ((y / rect.height) - 0.5) * 16;
    const rz = -6 + ((x / rect.width) - 0.5) * 14;
    setTilt({ rx, rz });
  };

  const handleReset = () => {
    setTilt({ rx: 26, rz: -6 });
    setZoom(1);
  };

  return (
    <div className="map-screen">
      {/* Sidebar Navigation */}
      <div className="map-sidebar">
        <div className="map-sidebar-header">
          <div style={{ fontSize: '0.72rem', fontWeight: 800, color: '#0f172a', letterSpacing: '0.08em', marginBottom: '0.2rem' }}>
            NATIONAL INVESTIGATION MAP
          </div>
          <h2 className="map-sidebar-title">Black & White 3D Territory Model</h2>
          <p className="map-sidebar-desc">
            Architectural Vector Blueprint & Jurisdictional Case Tracking
          </p>
        </div>

        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-label">Indexed States</div>
            <div className="stat-val" style={{ color: '#0f172a' }}>28 States</div>
          </div>
          <div className="stat-card">
            <div className="stat-label">Active Alerts</div>
            <div className="stat-val" style={{ color: '#0f172a' }}>5 High</div>
          </div>
          <div className="stat-card">
            <div className="stat-label">Total Cases</div>
            <div className="stat-val" style={{ color: '#0f172a' }}>18 Tracked</div>
          </div>
          <div className="stat-card">
            <div className="stat-label">Avg Match</div>
            <div className="stat-val" style={{ color: '#0f172a' }}>92.4%</div>
          </div>
        </div>

        <div className="state-list-section">
          <div className="section-heading">
            <span>State Jurisdiction</span>
            <span>Case Count</span>
          </div>

          {BW_INDIA_STATES.map((state) => {
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
                    Capital: {state.capital}
                  </div>
                </div>

                <div style={{ display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
                  <span className="gov-badge-subtle" style={{ fontWeight: 700 }}>
                    {state.casesCount} Cases
                  </span>
                  <ChevronRight size={14} color="var(--text-muted)" />
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* 3D Black & White Viewport Canvas */}
      <div 
        className="map-canvas-area"
        onMouseMove={handleMouseMove}
        style={{ 
          perspective: is3DMode ? '1200px' : 'none',
          background: '#f8fafc'
        }}
      >
        {/* Top Control Bar */}
        <div className="map-instructions" style={{ zIndex: 20 }}>
          <Compass size={15} color="#0f172a" />
          <span>Interactive <strong>Black & White 3D Map</strong>. Move cursor to tilt perspective. Click a state to view cases.</span>
        </div>

        <div style={{ position: 'absolute', top: '1.25rem', right: '1.5rem', display: 'flex', gap: '0.45rem', zIndex: 20 }}>
          <button 
            className={`header-btn ${is3DMode ? 'primary' : ''}`}
            onClick={() => setIs3DMode(!is3DMode)}
          >
            <Rotate3d size={14} />
            {is3DMode ? '3D Perspective' : '2D Flat'}
          </button>
          <button 
            className="header-btn"
            onClick={() => setZoom((z) => Math.min(z + 0.15, 1.4))}
            title="Zoom In"
          >
            <ZoomIn size={14} />
          </button>
          <button 
            className="header-btn"
            onClick={() => setZoom((z) => Math.max(z - 0.15, 0.7))}
            title="Zoom Out"
          >
            <ZoomOut size={14} />
          </button>
          <button 
            className="header-btn"
            onClick={handleReset}
            title="Reset Perspective"
          >
            Reset
          </button>
        </div>

        {/* 3D Map Stage */}
        <div 
          className="map-3d-stage"
          style={{
            transform: is3DMode 
              ? `rotateX(${tilt.rx}deg) rotateZ(${tilt.rz}deg) scale(${zoom * 0.88})` 
              : `scale(${zoom * 0.95})`,
            transformStyle: 'preserve-3d',
            transition: 'transform 0.15s ease-out',
            width: '680px',
            height: '750px',
            position: 'relative'
          }}
        >
          {/* Base 3D Shadow / Ground Grid */}
          <div 
            style={{
              position: 'absolute',
              inset: '-40px',
              borderRadius: '20px',
              background: '#ffffff',
              border: '1px solid #e2e8f0',
              boxShadow: '0 20px 40px rgba(15, 23, 42, 0.08)',
              transform: 'translateZ(-30px)',
              pointerEvents: 'none',
              display: 'flex',
              flexDirection: 'column',
              justifyContent: 'space-between',
              padding: '1.5rem'
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', color: '#94a3b8', fontSize: '0.72rem', fontWeight: 700, letterSpacing: '0.12em' }}>
              <span>ARABIAN SEA</span>
              <span>BAY OF BENGAL</span>
            </div>
            <div style={{ textAlign: 'center', color: '#94a3b8', fontSize: '0.75rem', fontWeight: 700, letterSpacing: '0.2em' }}>
              INDIAN OCEAN
            </div>
          </div>

          {/* 3D Extrusion Bottom Layer (Depth Plate) */}
          <div 
            style={{
              position: 'absolute',
              inset: 0,
              transform: 'translateZ(-12px)',
              opacity: 0.4,
              pointerEvents: 'none'
            }}
          >
            <svg viewBox="0 0 900 980" style={{ width: '100%', height: '100%', overflow: 'visible' }}>
              {BW_INDIA_STATES.map((state) => (
                <path
                  key={`depth-${state.code}`}
                  d={state.path}
                  fill="#94a3b8"
                  stroke="#64748b"
                  strokeWidth="2"
                />
              ))}
            </svg>
          </div>

          {/* Main Top Vector SVG Plate matching User's Black & White Image */}
          <svg 
            viewBox="0 0 900 980" 
            style={{ 
              width: '100%', 
              height: '100%', 
              overflow: 'visible',
              filter: 'drop-shadow(0 10px 20px rgba(15, 23, 42, 0.12))'
            }}
          >
            {/* All Black & White State Outlines */}
            {BW_INDIA_STATES.map((state) => {
              const isSelected = selectedState?.code === state.code;
              const isHovered = hoveredState?.code === state.code;

              return (
                <g 
                  key={state.code}
                  onClick={() => setSelectedState(state)}
                  onMouseEnter={() => setHoveredState(state)}
                  onMouseLeave={() => setHoveredState(null)}
                  style={{ cursor: 'pointer', transition: 'all 0.15s ease' }}
                >
                  {/* State Polygon (White surface with sharp black outline) */}
                  <path
                    d={state.path}
                    fill={isSelected ? '#0f172a' : isHovered ? '#f1f5f9' : '#ffffff'}
                    stroke={isSelected ? '#0f172a' : '#0f172a'}
                    strokeWidth={isSelected ? '2.5' : '1.8'}
                    strokeLinejoin="round"
                    style={{
                      transition: 'all 0.15s ease'
                    }}
                  />

                  {/* State Label */}
                  <text
                    x={state.cx}
                    y={state.cy}
                    fontSize="9.5"
                    fontWeight="700"
                    fill={isSelected ? '#ffffff' : '#0f172a'}
                    textAnchor="middle"
                    fontFamily="-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
                    style={{ pointerEvents: 'none', userSelect: 'none' }}
                  >
                    {state.code}
                  </text>

                  {/* Capital Dot */}
                  <circle
                    cx={state.cx}
                    cy={state.cy + 8}
                    r="2"
                    fill={isSelected ? '#ffffff' : '#0f172a'}
                  />

                  {/* Special Beacon on Delhi */}
                  {state.code === 'DL' && (
                    <g transform={`translate(${state.cx + 20}, ${state.cy - 12})`}>
                      <circle cx="0" cy="0" r="6" fill="#0f172a" opacity="0.25" />
                      <circle cx="0" cy="0" r="3" fill="#0f172a" stroke="#ffffff" strokeWidth="1" />
                      <rect x="6" y="-8" width="76" height="18" rx="3" fill="#0f172a" />
                      <text x="12" y="4" fontSize="7.5" fontWeight="700" fill="#ffffff">
                        DL-2026-0412
                      </text>
                    </g>
                  )}
                </g>
              );
            })}
          </svg>
        </div>

        {/* Selected State Cases Drawer */}
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
                  No active high-priority syndicates logged for {selectedState.name}.
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

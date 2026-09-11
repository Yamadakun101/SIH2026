import React, { useState, useRef, useEffect } from 'react';
import { 
  Compass, 
  Rotate3d, 
  ZoomIn, 
  ZoomOut, 
  Maximize2, 
  Layers, 
  MapPin, 
  ChevronRight, 
  X, 
  ArrowRight,
  ShieldAlert,
  Crosshair
} from 'lucide-react';
import { CASES_LIST } from '../../data/casesData';

// Accurate Administrative States & Union Territories of India (Matching Reference Map)
export const DETAILED_INDIA_STATES = [
  // North
  {
    code: 'LA',
    name: 'Ladakh',
    capital: 'Leh',
    type: 'UT',
    color: '#86efac', // Soft green matching map
    borderColor: '#4ade80',
    cx: 295,
    cy: 70,
    path: 'M 260,35 C 275,25 310,20 335,45 C 350,60 365,100 340,120 C 315,130 290,115 270,105 C 255,95 250,60 260,35 Z',
    casesCount: 1,
    highRisk: 0,
    status: 'low'
  },
  {
    code: 'JK',
    name: 'Jammu & Kashmir',
    capital: 'Srinagar / Jammu',
    type: 'UT',
    color: '#c4b5fd', // Soft purple matching map
    borderColor: '#a78bfa',
    cx: 235,
    cy: 90,
    path: 'M 215,60 C 230,45 255,40 265,55 C 255,80 260,110 245,125 C 230,135 210,120 205,100 C 200,80 205,70 215,60 Z',
    casesCount: 2,
    highRisk: 0,
    status: 'low'
  },
  {
    code: 'HP',
    name: 'Himachal Pradesh',
    capital: 'Shimla',
    type: 'State',
    color: '#f472b6', // Pink
    borderColor: '#ec4899',
    cx: 295,
    cy: 145,
    path: 'M 265,120 C 285,115 315,120 330,140 C 320,165 295,175 275,170 C 265,160 255,140 265,120 Z',
    casesCount: 1,
    highRisk: 0,
    status: 'low'
  },
  {
    code: 'PB',
    name: 'Punjab',
    capital: 'Chandigarh',
    type: 'State',
    color: '#fef08a', // Yellow
    borderColor: '#facc15',
    cx: 245,
    cy: 175,
    path: 'M 230,140 C 250,135 270,145 275,165 C 265,195 240,205 225,190 C 215,175 220,150 230,140 Z',
    casesCount: 3,
    highRisk: 1,
    status: 'low'
  },
  {
    code: 'UT',
    name: 'Uttarakhand',
    capital: 'Dehradun',
    type: 'State',
    color: '#cbd5e1', // Slate/Lavender
    borderColor: '#94a3b8',
    cx: 345,
    cy: 185,
    path: 'M 310,160 C 335,145 365,160 380,185 C 370,210 340,220 320,205 C 305,190 305,170 310,160 Z',
    casesCount: 2,
    highRisk: 0,
    status: 'low'
  },
  {
    code: 'HR',
    name: 'Haryana',
    capital: 'Chandigarh',
    type: 'State',
    color: '#fed7aa', // Orange
    borderColor: '#fb923c',
    cx: 270,
    cy: 215,
    path: 'M 255,185 C 280,180 295,195 300,225 C 290,250 265,255 245,235 C 240,215 245,195 255,185 Z',
    casesCount: 3,
    highRisk: 1,
    status: 'medium'
  },
  {
    code: 'DL',
    name: 'Delhi',
    capital: 'New Delhi',
    type: 'National Capital Territory',
    color: '#fca5a5', // Red tint
    borderColor: '#dc2626',
    cx: 295,
    cy: 232,
    isCapital: true,
    path: 'M 288,226 C 296,222 304,226 304,236 C 302,244 292,244 288,238 Z',
    casesCount: 4,
    highRisk: 2,
    status: 'high',
    highlight: true
  },

  // West & Central
  {
    code: 'RJ',
    name: 'Rajasthan',
    capital: 'Jaipur',
    type: 'State',
    color: '#f472b6', // Vibrant pink matching map
    borderColor: '#ec4899',
    cx: 200,
    cy: 285,
    path: 'M 160,205 C 215,195 260,230 265,280 C 270,335 220,380 170,365 C 130,345 125,260 160,205 Z',
    casesCount: 4,
    highRisk: 1,
    status: 'medium'
  },
  {
    code: 'UP',
    name: 'Uttar Pradesh',
    capital: 'Lucknow',
    type: 'State',
    color: '#bef264', // Lime green matching map
    borderColor: '#84cc16',
    cx: 395,
    cy: 285,
    path: 'M 305,215 C 380,210 470,255 485,310 C 470,355 385,360 330,340 C 295,320 280,250 305,215 Z',
    casesCount: 6,
    highRisk: 2,
    status: 'high'
  },
  {
    code: 'GJ',
    name: 'Gujarat',
    capital: 'Gandhinagar',
    type: 'State',
    color: '#fb923c', // Orange matching map
    borderColor: '#ea580c',
    cx: 130,
    cy: 395,
    path: 'M 100,340 C 150,330 180,370 185,410 C 175,465 110,470 75,430 C 60,390 75,355 100,340 Z',
    casesCount: 2,
    highRisk: 0,
    status: 'low'
  },
  {
    code: 'MP',
    name: 'Madhya Pradesh',
    capital: 'Bhopal',
    type: 'State',
    color: '#fde047', // Yellow matching map
    borderColor: '#eab308',
    cx: 335,
    cy: 400,
    path: 'M 255,340 C 350,330 435,360 450,420 C 430,475 320,490 250,460 C 215,420 215,365 255,340 Z',
    casesCount: 4,
    highRisk: 1,
    status: 'medium'
  },
  {
    code: 'BR',
    name: 'Bihar',
    capital: 'Patna',
    type: 'State',
    color: '#f59e0b', // Amber/Orange
    borderColor: '#d97706',
    cx: 525,
    cy: 320,
    path: 'M 480,285 C 530,280 575,300 585,335 C 570,370 515,375 475,355 C 465,330 465,300 480,285 Z',
    casesCount: 3,
    highRisk: 1,
    status: 'medium'
  },
  {
    code: 'JH',
    name: 'Jharkhand',
    capital: 'Ranchi',
    type: 'State',
    color: '#e879f9', // Light purple/pink
    borderColor: '#c026d3',
    cx: 515,
    cy: 395,
    path: 'M 475,360 C 520,355 560,370 565,410 C 550,445 495,450 465,425 C 455,400 460,375 475,360 Z',
    casesCount: 2,
    highRisk: 0,
    status: 'low'
  },
  {
    code: 'WB',
    name: 'West Bengal',
    capital: 'Kolkata',
    type: 'State',
    color: '#86efac', // Light green
    borderColor: '#22c55e',
    cx: 585,
    cy: 405,
    path: 'M 565,335 C 585,320 610,340 615,385 C 625,445 585,480 565,465 C 555,430 555,365 565,335 Z',
    casesCount: 5,
    highRisk: 1,
    status: 'medium'
  },
  {
    code: 'CT',
    name: 'Chhattisgarh',
    capital: 'Raipur',
    type: 'State',
    color: '#cbd5e1', // Light blue/gray
    borderColor: '#64748b',
    cx: 435,
    cy: 475,
    path: 'M 415,415 C 455,410 475,450 470,510 C 450,560 415,570 395,530 C 385,480 395,430 415,415 Z',
    casesCount: 2,
    highRisk: 0,
    status: 'low'
  },
  {
    code: 'OR',
    name: 'Odisha',
    capital: 'Bhubaneswar',
    type: 'State',
    color: '#fde047', // Yellow
    borderColor: '#ca8a04',
    cx: 520,
    cy: 485,
    path: 'M 475,445 C 535,430 580,465 590,515 C 570,560 500,565 465,535 C 455,490 460,460 475,445 Z',
    casesCount: 3,
    highRisk: 0,
    status: 'low'
  },
  {
    code: 'MH',
    name: 'Maharashtra',
    capital: 'Mumbai',
    type: 'State',
    color: '#bef264', // Lime green
    borderColor: '#65a30d',
    cx: 235,
    cy: 535,
    path: 'M 175,450 C 265,440 335,480 350,550 C 330,620 220,630 160,580 C 140,530 145,475 175,450 Z',
    casesCount: 7,
    highRisk: 1,
    status: 'medium'
  },

  // South
  {
    code: 'TG',
    name: 'Telangana',
    capital: 'Hyderabad',
    type: 'State',
    color: '#f472b6', // Pink
    borderColor: '#db2777',
    cx: 345,
    cy: 585,
    path: 'M 310,540 C 365,535 400,565 405,615 C 385,655 325,660 295,630 C 285,590 295,555 310,540 Z',
    casesCount: 3,
    highRisk: 1,
    status: 'medium'
  },
  {
    code: 'AP',
    name: 'Andhra Pradesh',
    capital: 'Amaravati',
    type: 'State',
    color: '#fb923c', // Orange
    borderColor: '#ea580c',
    cx: 360,
    cy: 675,
    path: 'M 350,615 C 415,595 460,650 435,725 C 390,775 345,765 315,715 C 310,670 325,630 350,615 Z',
    casesCount: 3,
    highRisk: 0,
    status: 'low'
  },
  {
    code: 'KA',
    name: 'Karnataka',
    capital: 'Bengaluru',
    type: 'State',
    color: '#fde047', // Yellow
    borderColor: '#eab308',
    cx: 250,
    cy: 695,
    path: 'M 215,610 C 275,600 310,645 305,730 C 285,795 225,800 195,745 C 180,690 190,635 215,610 Z',
    casesCount: 3,
    highRisk: 1,
    status: 'medium'
  },
  {
    code: 'GA',
    name: 'Goa',
    capital: 'Panaji',
    type: 'State',
    color: '#67e8f9', // Cyan
    borderColor: '#06b6d4',
    cx: 175,
    cy: 660,
    path: 'M 170,650 C 182,650 185,665 180,675 C 172,678 168,668 170,650 Z',
    casesCount: 1,
    highRisk: 0,
    status: 'low'
  },
  {
    code: 'KL',
    name: 'Kerala',
    capital: 'Thiruvananthapuram',
    type: 'State',
    color: '#cbd5e1', // Slate
    borderColor: '#94a3b8',
    cx: 245,
    cy: 825,
    path: 'M 235,760 C 255,750 265,785 270,845 C 265,885 235,890 220,860 C 215,815 220,775 235,760 Z',
    casesCount: 2,
    highRisk: 0,
    status: 'low'
  },
  {
    code: 'TN',
    name: 'Tamil Nadu',
    capital: 'Chennai',
    type: 'State',
    color: '#86efac', // Green
    borderColor: '#16a34a',
    cx: 320,
    cy: 815,
    path: 'M 275,745 C 345,730 380,780 375,855 C 350,910 290,910 265,860 C 255,810 260,765 275,745 Z',
    casesCount: 4,
    highRisk: 0,
    status: 'resolved'
  },

  // North-East States
  {
    code: 'SK',
    name: 'Sikkim',
    capital: 'Gangtok',
    type: 'State',
    color: '#f472b6',
    borderColor: '#ec4899',
    cx: 605,
    cy: 285,
    path: 'M 595,275 C 615,270 625,285 620,300 C 605,305 590,295 595,275 Z',
    casesCount: 1,
    highRisk: 0,
    status: 'low'
  },
  {
    code: 'AS',
    name: 'Assam',
    capital: 'Dispur',
    type: 'State',
    color: '#fde047',
    borderColor: '#eab308',
    cx: 715,
    cy: 325,
    path: 'M 655,300 C 745,290 775,330 765,365 C 725,385 660,370 655,300 Z',
    casesCount: 3,
    highRisk: 1,
    status: 'medium'
  },
  {
    code: 'AR',
    name: 'Arunachal Pradesh',
    capital: 'Itanagar',
    type: 'State',
    color: '#a78bfa',
    borderColor: '#8b5cf6',
    cx: 770,
    cy: 265,
    path: 'M 720,240 C 785,220 835,250 825,295 C 785,315 735,300 720,240 Z',
    casesCount: 1,
    highRisk: 0,
    status: 'low'
  },
  {
    code: 'ML',
    name: 'Meghalaya',
    capital: 'Shillong',
    type: 'State',
    color: '#bef264',
    borderColor: '#84cc16',
    cx: 685,
    cy: 355,
    path: 'M 660,345 C 710,340 725,360 715,375 C 675,385 655,370 660,345 Z',
    casesCount: 1,
    highRisk: 0,
    status: 'low'
  },
  {
    code: 'NL',
    name: 'Nagaland',
    capital: 'Kohima',
    type: 'State',
    color: '#f472b6',
    borderColor: '#ec4899',
    cx: 805,
    cy: 335,
    path: 'M 790,315 C 815,315 825,340 815,360 C 795,365 785,340 790,315 Z',
    casesCount: 1,
    highRisk: 0,
    status: 'low'
  },
  {
    code: 'MN',
    name: 'Manipur',
    capital: 'Imphal',
    type: 'State',
    color: '#86efac',
    borderColor: '#22c55e',
    cx: 800,
    cy: 385,
    path: 'M 785,365 C 810,365 820,390 810,415 C 790,420 780,395 785,365 Z',
    casesCount: 1,
    highRisk: 0,
    status: 'low'
  },
  {
    code: 'TR',
    name: 'Tripura',
    capital: 'Agartala',
    type: 'State',
    color: '#fed7aa',
    borderColor: '#fb923c',
    cx: 695,
    cy: 415,
    path: 'M 685,395 C 710,395 715,420 705,435 C 685,440 680,415 685,395 Z',
    casesCount: 1,
    highRisk: 0,
    status: 'low'
  },
  {
    code: 'MZ',
    name: 'Mizoram',
    capital: 'Aizawl',
    type: 'State',
    color: '#e879f9',
    borderColor: '#c026d3',
    cx: 775,
    cy: 435,
    path: 'M 760,410 C 785,410 790,445 780,475 C 760,475 755,440 760,410 Z',
    casesCount: 1,
    highRisk: 0,
    status: 'low'
  },

  // Island Groups
  {
    code: 'AN',
    name: 'Andaman & Nicobar Islands',
    capital: 'Port Blair',
    type: 'Union Territory',
    color: '#bef264',
    borderColor: '#84cc16',
    cx: 755,
    cy: 795,
    path: 'M 748,720 C 758,715 765,745 755,800 C 748,845 760,895 750,915 C 740,890 740,760 748,720 Z',
    casesCount: 1,
    highRisk: 0,
    status: 'low'
  },
  {
    code: 'LD',
    name: 'Lakshadweep',
    capital: 'Kavaratti',
    type: 'Union Territory',
    color: '#fde047',
    borderColor: '#eab308',
    cx: 155,
    cy: 820,
    path: 'M 148,785 C 160,780 162,805 156,845 C 150,865 142,835 148,785 Z',
    casesCount: 1,
    highRisk: 0,
    status: 'low'
  }
];

export default function IndiaMap({ onSelectCase }) {
  const [selectedState, setSelectedState] = useState(null);
  const [hoveredState, setHoveredState] = useState(null);
  const [tilt, setTilt] = useState({ rx: 28, rz: -8 });
  const [zoom, setZoom] = useState(1);
  const [is3DMode, setIs3DMode] = useState(true);

  const activeCasesForState = selectedState ? CASES_LIST[selectedState.code] || [] : [];

  const handleMouseMove = (e) => {
    if (!is3DMode) return;
    const rect = e.currentTarget.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const rx = 24 + ((y / rect.height) - 0.5) * 18;
    const rz = -6 + ((x / rect.width) - 0.5) * 16;
    setTilt({ rx, rz });
  };

  const handleReset = () => {
    setTilt({ rx: 28, rz: -8 });
    setZoom(1);
  };

  return (
    <div className="map-screen">
      {/* Sidebar Navigation */}
      <div className="map-sidebar">
        <div className="map-sidebar-header">
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', marginBottom: '0.35rem' }}>
            <span style={{ fontSize: '1rem' }}>🇮🇳</span>
            <span style={{ fontSize: '0.75rem', fontWeight: 800, color: 'var(--gov-navy)', letterSpacing: '0.08em' }}>
              INDIA STATES & UNION TERRITORIES
            </span>
          </div>
          <h2 className="map-sidebar-title">National Case Intelligence</h2>
          <p className="map-sidebar-desc">
            3D Administrative Geospatial Network & Multi-Jurisdiction Tracking
          </p>
        </div>

        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-label">States Indexed</div>
            <div className="stat-val blue">28 + 8 UTs</div>
          </div>
          <div className="stat-card">
            <div className="stat-label">Active Alerts</div>
            <div className="stat-val high">5 High</div>
          </div>
          <div className="stat-card">
            <div className="stat-label">Total Cases</div>
            <div className="stat-val med">18 Tracked</div>
          </div>
          <div className="stat-card">
            <div className="stat-label">Avg Match</div>
            <div className="stat-val" style={{ color: 'var(--gov-navy)' }}>92.4%</div>
          </div>
        </div>

        <div className="state-list-section">
          <div className="section-heading">
            <span>Jurisdiction</span>
            <span>Capital / Cases</span>
          </div>

          {DETAILED_INDIA_STATES.map((state) => {
            const isSelected = selectedState?.code === state.code;
            return (
              <div 
                key={state.code}
                className={`state-item ${isSelected ? 'selected' : ''}`}
                onClick={() => setSelectedState(state)}
                onMouseEnter={() => setHoveredState(state)}
                onMouseLeave={() => setHoveredState(null)}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.45rem' }}>
                  <span 
                    style={{
                      width: '10px',
                      height: '10px',
                      borderRadius: '2px',
                      background: state.color,
                      border: `1px solid ${state.borderColor}`
                    }} 
                  />
                  <div>
                    <div className="state-item-name">{state.name}</div>
                    <div className="state-item-cases" style={{ fontSize: '0.68rem' }}>
                      {state.capital}
                    </div>
                  </div>
                </div>

                <div style={{ display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
                  <span className={`gov-badge-subtle ${state.code === 'DL' ? 'gov-badge-lead' : ''}`}>
                    {state.casesCount} Cases
                  </span>
                  <ChevronRight size={14} color="var(--text-muted)" />
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* 3D Map Viewport Canvas */}
      <div 
        className="map-canvas-area"
        onMouseMove={handleMouseMove}
        style={{ 
          perspective: is3DMode ? '1300px' : 'none',
          background: 'radial-gradient(circle at 50% 50%, #f0fdfa 0%, #f8fafc 100%)'
        }}
      >
        {/* Top Control Bar */}
        <div className="map-instructions" style={{ zIndex: 20 }}>
          <Compass size={15} color="var(--gov-navy)" />
          <span>Interactive <strong>3D Model of India</strong>. Click any State/UT to open its active investigative cases.</span>
        </div>

        <div style={{ position: 'absolute', top: '1.25rem', right: '1.5rem', display: 'flex', gap: '0.45rem', zIndex: 20 }}>
          <button 
            className={`header-btn ${is3DMode ? 'primary' : ''}`}
            onClick={() => setIs3DMode(!is3DMode)}
          >
            <Rotate3d size={14} />
            {is3DMode ? '3D Isometric' : '2D Flat'}
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
          {/* Base Ocean / Continental Shelf Plane */}
          <div 
            style={{
              position: 'absolute',
              inset: '-40px',
              borderRadius: '24px',
              background: 'linear-gradient(135deg, rgba(224, 242, 254, 0.6) 0%, rgba(240, 249, 255, 0.4) 100%)',
              border: '1.5px dashed #93c5fd',
              transform: 'translateZ(-30px)',
              pointerEvents: 'none',
              display: 'flex',
              flexDirection: 'column',
              justifyContent: 'space-between',
              padding: '1.5rem'
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', color: '#0369a1', fontSize: '0.75rem', fontWeight: 800, letterSpacing: '0.15em' }}>
              <span>ARABIAN SEA</span>
              <span>BAY OF BENGAL</span>
            </div>
            <div style={{ textAlign: 'center', color: '#0369a1', fontSize: '0.85rem', fontWeight: 800, letterSpacing: '0.25em' }}>
              INDIAN OCEAN
            </div>
          </div>

          {/* SVG 3D Extruded Model */}
          <svg 
            viewBox="0 0 900 980" 
            style={{ 
              width: '100%', 
              height: '100%', 
              overflow: 'visible',
              filter: 'drop-shadow(0 14px 28px rgba(15, 23, 42, 0.15))'
            }}
          >
            {/* Neighboring Country Outlines & Labels */}
            <g opacity="0.6" fontFamily="sans-serif" fontSize="11" fontWeight="700" fill="#64748b">
              {/* Pakistan */}
              <text x="70" y="210">PAKISTAN</text>
              <text x="35" y="110">AFGHANISTAN</text>
              <text x="580" y="190">CHINA (TIBET)</text>
              <text x="500" y="260">NEPAL</text>
              <text x="635" y="295">BHUTAN</text>
              <text x="650" y="380">BANGLADESH</text>
              <text x="810" y="470">MYANMAR (BURMA)</text>
              <text x="390" y="910">SRI LANKA</text>
            </g>

            {/* Sri Lanka Polygon */}
            <path
              d="M 395,870 C 410,865 425,885 420,915 C 410,935 390,930 385,905 Z"
              fill="#e2e8f0"
              stroke="#cbd5e1"
              strokeWidth="1.5"
            />

            {/* State Polygons with 3D Hover & Interaction */}
            {DETAILED_INDIA_STATES.map((state) => {
              const isSelected = selectedState?.code === state.code;
              const isHovered = hoveredState?.code === state.code;

              return (
                <g 
                  key={state.code}
                  onClick={() => setSelectedState(state)}
                  onMouseEnter={() => setHoveredState(state)}
                  onMouseLeave={() => setHoveredState(null)}
                  style={{ cursor: 'pointer', transition: 'all 0.2s ease' }}
                >
                  {/* Extruded Side Shadow on Hover */}
                  {(isSelected || isHovered) && (
                    <path
                      d={state.path}
                      fill="none"
                      stroke="rgba(15, 23, 42, 0.3)"
                      strokeWidth="8"
                      transform="translate(0, 4)"
                    />
                  )}

                  {/* Main State Polygon */}
                  <path
                    d={state.path}
                    fill={isSelected ? '#1e3a8a' : isHovered ? '#3b82f6' : state.color}
                    stroke={isSelected ? '#0f172a' : state.borderColor}
                    strokeWidth={isSelected ? '2.5' : '1.5'}
                    strokeLinejoin="round"
                    style={{
                      transition: 'fill 0.15s ease, stroke 0.15s ease',
                      filter: isSelected ? 'drop-shadow(0 6px 12px rgba(30, 58, 138, 0.3))' : 'none'
                    }}
                  />

                  {/* State Name Text */}
                  <text
                    x={state.cx}
                    y={state.cy}
                    fontSize={state.code === 'DL' ? '10' : '9.5'}
                    fontWeight="800"
                    fill={isSelected ? '#ffffff' : '#0f172a'}
                    textAnchor="middle"
                    fontFamily="sans-serif"
                    style={{ pointerEvents: 'none', userSelect: 'none' }}
                  >
                    {state.name.toUpperCase()}
                  </text>

                  {/* Capital Dot */}
                  <circle
                    cx={state.cx}
                    cy={state.cy + 10}
                    r={state.isCapital ? '4' : '2.5'}
                    fill={state.isCapital ? '#dc2626' : '#1e293b'}
                    stroke="#ffffff"
                    strokeWidth="1"
                  />

                  {/* Capital Label */}
                  <text
                    x={state.cx}
                    y={state.cy + 20}
                    fontSize="7.5"
                    fontWeight="600"
                    fill={isSelected ? '#e2e8f0' : '#475569'}
                    textAnchor="middle"
                    fontFamily="sans-serif"
                    style={{ pointerEvents: 'none', userSelect: 'none' }}
                  >
                    {state.capital}
                  </text>

                  {/* Delhi Special Highlighted Beacon */}
                  {state.code === 'DL' && (
                    <g transform={`translate(${state.cx + 22}, ${state.cy - 12})`}>
                      <circle cx="0" cy="0" r="8" fill="#dc2626" opacity="0.3" className="pulse-circle" />
                      <circle cx="0" cy="0" r="4" fill="#dc2626" stroke="#ffffff" strokeWidth="1.5" />
                      <rect x="8" y="-10" width="84" height="20" rx="4" fill="#1e293b" />
                      <text x="14" y="4" fontSize="8" fontWeight="800" fill="#ffffff">
                        DL-2026-0412 ★
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
                    <span style={{ color: 'var(--gov-navy)', fontWeight: 700, display: 'flex', alignItems: 'center', gap: '0.2rem' }}>
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

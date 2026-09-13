/**
 * CRIMENET-AI — INDIA MAP VISUALIZER
 * Interactive SVG Map of India with State Boundaries, Risk Hotspots & Case Selectors
 */

const indiaMap = {
  container: null,
  selectedState: null,

  // Simplified and visually balanced SVG paths representing major regions & states of India
  stateData: [
    { code: "DL", name: "Delhi NCR", cx: 285, cy: 220, risk: "high", casesCount: 1, primaryId: "DL-2026-0412" },
    { code: "MH", name: "Maharashtra", cx: 260, cy: 440, risk: "medium", casesCount: 1, primaryId: "MH-2026-0189" },
    { code: "WB", name: "West Bengal", cx: 485, cy: 330, risk: "high", casesCount: 1, primaryId: "WB-2026-0304" },
    { code: "KA", name: "Karnataka", cx: 265, cy: 540, risk: "low", casesCount: 1, primaryId: "KA-2026-0091" },
    { code: "PB", name: "Punjab", cx: 245, cy: 165, risk: "medium", casesCount: 1, primaryId: "PB-2026-0215" },
    { code: "RJ", name: "Rajasthan", cx: 205, cy: 255, risk: "low", casesCount: 1, primaryId: "RJ-2026-0112" },
    { code: "TS", name: "Telangana", cx: 320, cy: 460, risk: "medium", casesCount: 1, primaryId: "TS-2026-0402" },
    { code: "AS", name: "Assam", cx: 580, cy: 260, risk: "high", casesCount: 1, primaryId: "AS-2026-0177" }
  ],

  init() {
    this.container = document.getElementById("indiaMapContainer");
    if (!this.container) return;
    this.render();
  },

  render() {
    const svgHTML = `
      <svg class="india-svg-map" viewBox="0 0 700 720" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <filter id="mapShadow" x="-5%" y="-5%" width="115%" height="115%">
            <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#0f172a" flood-opacity="0.08" />
          </filter>
          <filter id="pinGlow" x="-20%" y="-20%" width="140%" height="140%">
            <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#000" flood-opacity="0.2" />
          </filter>
        </defs>

        <!-- Base Map Outline of India -->
        <g id="mapBaseGeometry" filter="url(#mapShadow)">
          <!-- Jammu & Kashmir / Ladakh -->
          <path id="state-JK" class="state-path" d="M 230,70 L 270,50 L 320,60 L 335,110 L 305,140 L 260,135 L 235,110 Z" title="Jammu & Kashmir / Ladakh"></path>
          <!-- Himachal Pradesh -->
          <path id="state-HP" class="state-path" d="M 260,135 L 305,140 L 300,175 L 265,165 Z" title="Himachal Pradesh"></path>
          <!-- Punjab -->
          <path id="state-PB" class="state-path has-cases" d="M 220,150 L 265,165 L 255,200 L 220,190 Z" title="Punjab" onclick="indiaMap.handleStateClick('PB')"></path>
          <!-- Uttarakhand -->
          <path id="state-UK" class="state-path" d="M 300,175 L 340,185 L 325,225 L 295,205 Z" title="Uttarakhand"></path>
          <!-- Haryana -->
          <path id="state-HR" class="state-path" d="M 255,195 L 295,205 L 285,250 L 245,230 Z" title="Haryana"></path>
          <!-- Delhi NCR -->
          <path id="state-DL" class="state-path has-cases selected" d="M 280,215 L 292,215 L 292,228 L 280,228 Z" title="Delhi NCR" onclick="indiaMap.handleStateClick('DL')"></path>
          <!-- Rajasthan -->
          <path id="state-RJ" class="state-path has-cases" d="M 160,205 L 245,230 L 250,300 L 195,335 L 140,270 Z" title="Rajasthan" onclick="indiaMap.handleStateClick('RJ')"></path>
          <!-- Uttar Pradesh -->
          <path id="state-UP" class="state-path" d="M 290,210 L 410,240 L 415,300 L 340,320 L 285,270 Z" title="Uttar Pradesh"></path>
          <!-- Gujarat -->
          <path id="state-GJ" class="state-path" d="M 120,320 L 195,335 L 210,400 L 155,420 L 120,370 Z" title="Gujarat"></path>
          <!-- Madhya Pradesh -->
          <path id="state-MP" class="state-path" d="M 220,320 L 350,320 L 360,395 L 240,410 Z" title="Madhya Pradesh"></path>
          <!-- Bihar -->
          <path id="state-BR" class="state-path" d="M 410,240 L 485,260 L 480,315 L 415,300 Z" title="Bihar"></path>
          <!-- Jharkhand -->
          <path id="state-JH" class="state-path" d="M 415,300 L 480,315 L 460,370 L 400,350 Z" title="Jharkhand"></path>
          <!-- West Bengal -->
          <path id="state-WB" class="state-path has-cases" d="M 480,260 L 515,260 L 500,375 L 460,370 Z" title="West Bengal" onclick="indiaMap.handleStateClick('WB')"></path>
          <!-- Odisha -->
          <path id="state-OD" class="state-path" d="M 390,370 L 465,370 L 430,470 L 370,440 Z" title="Odisha"></path>
          <!-- Chhattisgarh -->
          <path id="state-CG" class="state-path" d="M 350,330 L 395,360 L 370,440 L 330,410 Z" title="Chhattisgarh"></path>
          <!-- Maharashtra -->
          <path id="state-MH" class="state-path has-cases" d="M 195,410 L 310,410 L 330,490 L 220,500 L 190,450 Z" title="Maharashtra" onclick="indiaMap.handleStateClick('MH')"></path>
          <!-- Telangana -->
          <path id="state-TS" class="state-path has-cases" d="M 290,445 L 365,450 L 345,515 L 290,490 Z" title="Telangana" onclick="indiaMap.handleStateClick('TS')"></path>
          <!-- Andhra Pradesh -->
          <path id="state-AP" class="state-path" d="M 345,500 L 400,470 L 360,600 L 315,570 Z" title="Andhra Pradesh"></path>
          <!-- Karnataka -->
          <path id="state-KA" class="state-path has-cases" d="M 220,495 L 290,500 L 295,600 L 230,590 Z" title="Karnataka" onclick="indiaMap.handleStateClick('KA')"></path>
          <!-- Goa -->
          <path id="state-GA" class="state-path" d="M 215,515 L 230,515 L 228,530 L 213,530 Z" title="Goa"></path>
          <!-- Kerala -->
          <path id="state-KL" class="state-path" d="M 240,600 L 270,600 L 275,680 L 250,680 Z" title="Kerala"></path>
          <!-- Tamil Nadu -->
          <path id="state-TN" class="state-path" d="M 270,600 L 330,590 L 305,690 L 265,685 Z" title="Tamil Nadu"></path>
          <!-- North East Region / Assam -->
          <path id="state-AS" class="state-path has-cases" d="M 525,250 L 610,230 L 620,290 L 535,300 Z" title="Assam & North East" onclick="indiaMap.handleStateClick('AS')"></path>
        </g>

        <!-- Dynamic Case Markers & Hotspots -->
        <g id="mapHotspots">
          ${this.stateData.map(st => {
            const riskColor = st.risk === 'high' ? '#dc2626' : (st.risk === 'medium' ? '#d97706' : (st.risk === 'closed' ? '#2563eb' : '#16a34a'));
            const isDelhi = st.code === 'DL';
            const radius = isDelhi ? 13 : 10;
            return `
              <g class="map-pin" onclick="indiaMap.handleStateClick('${st.code}')" filter="url(#pinGlow)">
                <!-- Pulse Circle for High Risk -->
                ${st.risk === 'high' ? `
                  <circle cx="${st.cx}" cy="${st.cy}" r="${radius + 7}" fill="${riskColor}" opacity="0.25">
                    <animate attributeName="r" values="${radius + 4};${radius + 12};${radius + 4}" dur="2.2s" repeatCount="indefinite" />
                    <animate attributeName="opacity" values="0.4;0.05;0.4" dur="2.2s" repeatCount="indefinite" />
                  </circle>
                ` : ''}
                
                <!-- Main Pin Dot -->
                <circle cx="${st.cx}" cy="${st.cy}" r="${radius}" fill="${riskColor}" stroke="#ffffff" stroke-width="2.5" />
                
                <!-- Case Count / Code inside pin -->
                <text x="${st.cx}" y="${st.cy + 3.5}" fill="#ffffff" font-size="${isDelhi ? '10' : '9'}" font-weight="700" text-anchor="middle">
                  ${st.code}
                </text>

                <!-- City / State Label -->
                <text x="${st.cx}" y="${st.cy + radius + 11}" class="pin-label">
                  ${st.name}
                </text>
              </g>
            `;
          }).join('')}
        </g>
      </svg>
    `;

    this.container.innerHTML = svgHTML;
  },

  handleStateClick(stateCode) {
    this.selectedState = stateCode;
    
    // Update SVG selection highlight
    document.querySelectorAll('.state-path').forEach(p => p.classList.remove('selected'));
    const pathEl = document.getElementById(`state-${stateCode}`);
    if (pathEl) pathEl.classList.add('selected');

    // Notify App to filter or open case
    app.filterCasesByState(stateCode);
  }
};

/**
 * CRIMENET-AI — MAIN APPLICATION CONTROLLER
 * Coordinates State Machine, Views, Tab Switching, Node Inspection & Evidence Audit Trails
 */

const app = {
  currentView: "map", // "map" or "workspace"
  activeCaseId: null,
  activeTab: "tab-network",
  selectedStateFilter: null,

  init() {
    this.renderNationalCases();
    this.updateStats();
    
    // Initialize Submodules
    indiaMap.init();

    // Default primary case preloaded
    this.activeCaseId = "DL-2026-0412";
  },

  // 1. Navigation & View Routing
  showMapView() {
    this.currentView = "map";
    document.getElementById("mapView").classList.add("active");
    document.getElementById("caseWorkspaceView").classList.remove("active");

    // Reset breadcrumbs
    document.getElementById("navHomeBtn").classList.add("active");
    document.getElementById("breadcrumbSep1").style.display = "none";
    document.getElementById("navStateBtn").style.display = "none";
    document.getElementById("breadcrumbSep2").style.display = "none";
    document.getElementById("navCaseBtn").style.display = "none";

    // Refresh national cases list
    this.selectedStateFilter = null;
    this.renderNationalCases();
  },

  showStateCases() {
    if (this.selectedStateFilter) {
      this.filterCasesByState(this.selectedStateFilter);
    } else {
      this.showMapView();
    }
  },

  openCase(caseId) {
    this.activeCaseId = caseId;
    const caseObj = SYNTHETIC_DATA.cases.find(c => c.id === caseId) || SYNTHETIC_DATA.cases[0];

    // Update Header Breadcrumbs
    this.currentView = "workspace";
    document.getElementById("mapView").classList.remove("active");
    document.getElementById("caseWorkspaceView").classList.add("active");

    document.getElementById("navHomeBtn").classList.remove("active");
    
    document.getElementById("breadcrumbSep1").style.display = "inline";
    const navStateBtn = document.getElementById("navStateBtn");
    navStateBtn.style.display = "inline";
    navStateBtn.innerText = caseObj.stateName;
    navStateBtn.classList.remove("active");

    document.getElementById("breadcrumbSep2").style.display = "inline";
    const navCaseBtn = document.getElementById("navCaseBtn");
    navCaseBtn.style.display = "inline";
    navCaseBtn.innerText = caseObj.id;
    navCaseBtn.classList.add("active");

    // Populate Case Header Metadata
    const riskBadge = document.getElementById("caseRiskBadge");
    riskBadge.className = `badge ${caseObj.risk}`;
    riskBadge.innerText = `${caseObj.risk.toUpperCase()} RISK`;

    document.getElementById("caseIdDisplay").innerText = caseObj.id;
    document.getElementById("caseStatusDisplay").innerText = caseObj.status;
    document.getElementById("caseTitleDisplay").innerText = caseObj.title;
    document.getElementById("caseSummaryDisplay").innerText = caseObj.summary;

    // Initialize Workspace Tabs
    this.populateOverviewTab();
    this.populateEvidenceTable();
    timelineViewer.init(SYNTHETIC_DATA.timeline);
    aiAssistant.init();

    // Initialize Network Graph
    networkGraph.init(SYNTHETIC_DATA.primaryCase);

    // Switch to graph tab by default
    this.switchTab("tab-network");
  },

  // 2. Tab Controller
  switchTab(tabId) {
    this.activeTab = tabId;

    // Update Tab Buttons
    document.querySelectorAll(".tab-btn").forEach(btn => {
      btn.classList.toggle("active", btn.dataset.tab === tabId);
    });

    // Update Tab Contents
    document.querySelectorAll(".tab-content").forEach(content => {
      content.classList.toggle("active", content.id === tabId);
    });

    // Re-render graph if opening graph tab to fix container dimensions
    if (tabId === "tab-network") {
      setTimeout(() => {
        networkGraph.render();
      }, 50);
    }
  },

  showAiAssistantTab() {
    this.switchTab("tab-ai");
  },

  // 3. National Case List & State Filter
  filterCasesByState(stateCode) {
    this.selectedStateFilter = stateCode;
    const cases = SYNTHETIC_DATA.cases.filter(c => c.stateCode === stateCode);
    const stateObj = indiaMap.stateData.find(s => s.code === stateCode);
    const stateName = stateObj ? stateObj.name : stateCode;

    document.getElementById("caseListHeading").innerText = `Cases in ${stateName}`;
    document.getElementById("caseListCount").innerText = `${cases.length} case${cases.length !== 1 ? 's' : ''}`;

    this.renderCaseList(cases);
  },

  renderNationalCases() {
    document.getElementById("caseListHeading").innerText = "All National Cases (Click to open)";
    document.getElementById("caseListCount").innerText = `${SYNTHETIC_DATA.cases.length} cases`;
    this.renderCaseList(SYNTHETIC_DATA.cases);
  },

  renderCaseList(cases) {
    const listEl = document.getElementById("nationalCaseList");
    if (!listEl) return;

    if (cases.length === 0) {
      listEl.innerHTML = `<div style="padding: 16px; text-align: center; color: #94a3b8;">No cases recorded in this region.</div>`;
      return;
    }

    listEl.innerHTML = cases.map(c => {
      const isDL = c.id === 'DL-2026-0412';
      return `
        <div class="case-card-item ${isDL ? 'active-spotlight' : ''}" onclick="app.openCase('${c.id}')">
          <div class="case-card-top">
            <span class="case-chip ${c.risk}">${c.id} • ${c.risk.toUpperCase()}</span>
            <span style="font-size: 10px; color: #64748b; font-weight: 500;">${c.status}</span>
          </div>
          <div class="case-card-title">${c.title}</div>
          <div class="case-card-meta">
            <span>📍 ${c.location}</span>
            <span>📅 ${c.date}</span>
          </div>
        </div>
      `;
    }).join('');
  },

  updateStats() {
    const total = SYNTHETIC_DATA.cases.length;
    const high = SYNTHETIC_DATA.cases.filter(c => c.risk === 'high').length;
    const med = SYNTHETIC_DATA.cases.filter(c => c.risk === 'medium').length;
    const closed = SYNTHETIC_DATA.cases.filter(c => c.risk === 'low' || c.risk === 'closed').length;

    document.getElementById("statTotalCases").innerText = total;
    document.getElementById("statHighCases").innerText = high;
    document.getElementById("statMedCases").innerText = med;
    document.getElementById("statClosedCases").innerText = closed;
  },

  // 4. Node Inspection Drawer Logic
  displayNodeInspection(node) {
    const emptyState = document.getElementById("inspectorEmptyState");
    const detailContent = document.getElementById("inspectorDetailContent");

    if (!node) {
      emptyState.style.display = "flex";
      detailContent.style.display = "none";
      return;
    }

    emptyState.style.display = "none";
    detailContent.style.display = "flex";

    const conf = networkGraph.typeColors[node.type] || { fill: "#2563eb", bg: "#eff6ff", icon: "●" };
    const d = node.details || {};

    let detailsTableHTML = "";
    if (node.type === "Person") {
      detailsTableHTML = `
        <table class="data-table-simple">
          <tr><td>Role / Status:</td><td>${d.role || 'Investigative Subject'}</td></tr>
          <tr><td>Age:</td><td>${d.age || 'Unknown'}</td></tr>
          <tr><td>Jurisdiction:</td><td>${d.residence || 'Delhi NCR'}</td></tr>
          <tr><td>Status:</td><td>${d.status || 'Active'}</td></tr>
        </table>
      `;
    } else if (node.type === "Phone") {
      detailsTableHTML = `
        <table class="data-table-simple">
          <tr><td>Record Type:</td><td>${d.recordType || 'CDR Log'}</td></tr>
          <tr><td>Subscriber Link:</td><td>${d.associatedPerson || 'Unassigned'}</td></tr>
          <tr><td>Key Tower:</td><td>${d.locations || 'NCR Grid'}</td></tr>
        </table>
      `;
    } else if (node.type === "Vehicle") {
      detailsTableHTML = `
        <table class="data-table-simple">
          <tr><td>Make / Model:</td><td>${d.model || 'Commercial Sedan'}</td></tr>
          <tr><td>VAHAN Owner:</td><td>${d.registeredOwner || 'Sunil Mehta'}</td></tr>
          <tr><td>Sensors:</td><td>FASTag & Optical CCTV</td></tr>
        </table>
      `;
    } else if (node.type === "Bank Account") {
      detailsTableHTML = `
        <table class="data-table-simple">
          <tr><td>Bank Name:</td><td>${d.bankName || 'HDFC Bank'}</td></tr>
          <tr><td>Account Holder:</td><td>${d.accountHolder || 'Rakesh Kumar'}</td></tr>
          <tr><td>Switch Protocol:</td><td>NPCI IMPS 24x7</td></tr>
        </table>
      `;
    } else if (node.type === "CCTV Event") {
      detailsTableHTML = `
        <table class="data-table-simple">
          <tr><td>Camera Node:</td><td>${d.cameraLocation || 'DMRC Optical Sensor'}</td></tr>
          <tr><td>Timestamp:</td><td>${d.timestamp || '12 Aug 2026'}</td></tr>
          <tr><td>Detection:</td><td>License Plate & Passenger Recognition</td></tr>
        </table>
      `;
    } else if (node.type === "FIR / Case") {
      detailsTableHTML = `
        <table class="data-table-simple">
          <tr><td>Legal Sections:</td><td>${d.sections || 'Sec 365, 370 BNS'}</td></tr>
          <tr><td>Complainant:</td><td>${d.complainant || 'State Police'}</td></tr>
          <tr><td>Repository:</td><td>CCTNS National Index</td></tr>
        </table>
      `;
    } else {
      detailsTableHTML = `
        <table class="data-table-simple">
          <tr><td>Type:</td><td>${node.type}</td></tr>
          <tr><td>Entity Label:</td><td>${node.label}</td></tr>
        </table>
      `;
    }

    const whyConnectedHTML = d.whyConnected ? `
      <div class="inspector-section">
        <span class="inspector-section-label">Why is it connected?</span>
        <ul class="bullet-list">
          ${d.whyConnected.map(w => `<li>${w}</li>`).join('')}
        </ul>
      </div>
    ` : '';

    detailContent.innerHTML = `
      <!-- Header -->
      <div class="inspector-card-header">
        <div>
          <span class="inspector-type-badge" style="background: ${conf.bg}; color: ${conf.fill}; border: 1px solid ${conf.fill}40;">
            ${conf.icon} ${node.type}
          </span>
          <h2 class="inspector-entity-title">${node.label}</h2>
        </div>
      </div>

      <!-- Match Confidence Bar -->
      <div class="confidence-bar-block">
        <div class="confidence-label-row">
          <span>Association / Match Confidence</span>
          <span style="color: ${conf.fill};">${node.confidence}%</span>
        </div>
        <div class="confidence-track">
          <div class="confidence-fill" style="width: ${node.confidence}%; background-color: ${conf.fill};"></div>
        </div>
      </div>

      <!-- Stored Details Table -->
      <div class="inspector-section">
        <span class="inspector-section-label">Stored Synthetic Details</span>
        <div class="inspector-box">
          ${detailsTableHTML}
        </div>
      </div>

      <!-- Why Connected -->
      ${whyConnectedHTML}

      <!-- Spatio-temporal Info -->
      <div class="inspector-section">
        <span class="inspector-section-label">Temporal & Spatial Anchors</span>
        <div class="inspector-box">
          <table class="data-table-simple">
            <tr><td>Activity Dates:</td><td>${d.dates || '12 Aug 2026'}</td></tr>
            <tr><td>Locations:</td><td>${d.locations || 'Delhi NCR'}</td></tr>
          </table>
        </div>
      </div>

      <!-- Provenance Source -->
      <div class="inspector-section">
        <span class="inspector-section-label">Data Ingestion Provenance</span>
        <div>
          <span class="source-tag">
            <svg viewBox="0 0 20 20" fill="currentColor" width="12" height="12">
              <path fill-rule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4z" clip-rule="evenodd"/>
            </svg>
            ${d.source || 'Synthetic Knowledge Base'}
          </span>
        </div>
      </div>

      <!-- Short AI Rationale -->
      <div class="inspector-section">
        <span class="inspector-section-label">AI Investigation Rationale</span>
        <div class="ai-reasoning-box">
          💡 <em>${d.aiExplanation || 'Correlation derived from multi-modal graph fusion.'}</em>
        </div>
      </div>
    `;
  },

  inspectNodeById(nodeId) {
    this.switchTab("tab-network");
    setTimeout(() => {
      networkGraph.selectNode(nodeId);
    }, 100);
  },

  inspectCentralPerson() {
    this.inspectNodeById("person-1");
  },

  askAssistantAboutPerson(name) {
    this.switchTab("tab-ai");
    setTimeout(() => {
      aiAssistant.askPreset(`What connects ${name} to this case?`);
    }, 100);
  },

  // 5. Overview Tab Associates List
  populateOverviewTab() {
    const container = document.getElementById("associatesListContainer");
    if (!container) return;

    const associates = [
      { id: "person-2", name: "Vikram 'Vicky' Sharma", type: "Logistics Coordinator", conf: "84%", icon: "👤", risk: "high", desc: "14 CDR calls, co-accused in historical FIR 78/2024" },
      { id: "person-3", name: "Sunil Mehta", type: "Driver / Transport Custodian", conf: "78%", icon: "👤", risk: "medium", desc: "Owner of Swift Dzire DL 01 AX 4492, received ₹50k IMPS" },
      { id: "phone-1", name: "+91 98765 43210", type: "Primary Mobile Handset", conf: "94%", icon: "📱", risk: "high", desc: "Active during Kashmere Gate transit window" },
      { id: "veh-1", name: "DL 01 AX 4492 (White Sedan)", type: "Transit Vehicle", conf: "92%", icon: "🚗", risk: "high", desc: "Optical CCTV match & Murthal FASTag toll pass" }
    ];

    container.innerHTML = associates.map(a => {
      return `
        <div class="associate-row">
          <div class="assoc-left">
            <div class="assoc-icon" style="background: #eff6ff; color: #2563eb;">${a.icon}</div>
            <div>
              <div class="assoc-name">${a.name}</div>
              <div class="assoc-sub">${a.type} • ${a.desc}</div>
            </div>
          </div>
          <div>
            <button class="btn btn-secondary btn-sm" onclick="app.inspectNodeById('${a.id}')">
              Inspect Node (${a.conf}) →
            </button>
          </div>
        </div>
      `;
    }).join('');
  },

  // 6. Evidence Provenance Table
  populateEvidenceTable() {
    const tbody = document.getElementById("evidenceTableBody");
    if (!tbody) return;

    tbody.innerHTML = SYNTHETIC_DATA.evidenceLogs.map(ev => {
      return `
        <tr>
          <td><code style="font-family: var(--font-mono); font-weight: 600; color: #2563eb;">${ev.id}</code></td>
          <td><span style="font-weight: 500; color: #1e293b;">${ev.agency}</span></td>
          <td><span style="font-family: var(--font-mono); font-size: 11px;">${ev.timestamp}</span></td>
          <td><strong>${ev.entity}</strong></td>
          <td><span style="color: #475569;">${ev.metadata}</span></td>
          <td><span class="badge low">${ev.confidence} Match</span></td>
          <td>
            <button class="btn btn-secondary btn-sm" onclick="app.inspectNodeById('${ev.entityId}')">
              View Node →
            </button>
          </td>
        </tr>
      `;
    }).join('');
  }
};

// Launch Application on DOM Ready
document.addEventListener("DOMContentLoaded", () => {
  app.init();
});

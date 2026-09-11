/**
 * CRIMENET-AI — INTERACTIVE NETWORK GRAPH VISUALIZER
 * D3.js Force Simulation Engine with Entity Inspection & Relationship Mapping
 */

const networkGraph = {
  container: null,
  svg: null,
  g: null,
  simulation: null,
  zoomBehavior: null,
  
  // Data State
  rawNodes: [],
  rawLinks: [],
  activeFilter: 'all',
  selectedNodeId: null,

  // Color Mapping
  typeColors: {
    "Person": { fill: "#2563eb", bg: "#eff6ff", border: "#93c5fd", icon: "👤" },
    "Phone": { fill: "#059669", bg: "#ecfdf5", border: "#a7f3d0", icon: "📱" },
    "Vehicle": { fill: "#d97706", bg: "#fffbeb", border: "#fde68a", icon: "🚗" },
    "Bank Account": { fill: "#7c3aed", bg: "#f5f3ff", border: "#ddd6fe", icon: "🏦" },
    "Location": { fill: "#ea580c", bg: "#fff7ed", border: "#fed7aa", icon: "📍" },
    "CCTV Event": { fill: "#0284c7", bg: "#f0f9ff", border: "#bae6fd", icon: "📹" },
    "FIR / Case": { fill: "#e11d48", bg: "#fff1f2", border: "#fecdd3", icon: "📜" },
    "Transaction": { fill: "#4f46e5", bg: "#eef2ff", border: "#c7d2fe", icon: "💳" }
  },

  init(caseData) {
    this.container = document.getElementById("graphContainer");
    if (!this.container) return;

    this.rawNodes = JSON.parse(JSON.stringify(caseData.nodes));
    this.rawLinks = JSON.parse(JSON.stringify(caseData.links));

    this.setupFilterListeners();
    this.render();

    // Auto-select central node (Rakesh Kumar) for initial inspection
    setTimeout(() => {
      this.selectNode("person-1");
    }, 400);
  },

  setupFilterListeners() {
    const filterContainer = document.getElementById("graphFilterChips");
    if (!filterContainer) return;

    filterContainer.querySelectorAll(".chip").forEach(chip => {
      chip.addEventListener("click", (e) => {
        filterContainer.querySelectorAll(".chip").forEach(c => c.classList.remove("active"));
        chip.classList.add("active");
        this.activeFilter = chip.dataset.filter;
        this.render();
      });
    });
  },

  render() {
    this.container.innerHTML = "";
    const width = this.container.clientWidth || 800;
    const height = this.container.clientHeight || 550;

    // Filter nodes and links
    let displayNodes = [...this.rawNodes];
    if (this.activeFilter !== 'all') {
      displayNodes = displayNodes.filter(n => n.type === this.activeFilter || n.isCentral);
    }
    const nodeIds = new Set(displayNodes.map(n => n.id));
    const displayLinks = this.rawLinks.filter(l => {
      const srcId = typeof l.source === 'object' ? l.source.id : l.source;
      const tgtId = typeof l.target === 'object' ? l.target.id : l.target;
      return nodeIds.has(srcId) && nodeIds.has(tgtId);
    });

    // Create Root SVG
    this.svg = d3.select(this.container)
      .append("svg")
      .attr("width", "100%")
      .attr("height", "100%")
      .attr("viewBox", `0 0 ${width} ${height}`)
      .attr("class", "graph-svg-root");

    // Arrow markers for directed relationships
    const defs = this.svg.append("defs");
    defs.append("marker")
      .attr("id", "arrowhead")
      .attr("viewBox", "0 -5 10 10")
      .attr("refX", 26)
      .attr("refY", 0)
      .attr("orient", "auto")
      .attr("markerWidth", 6)
      .attr("markerHeight", 6)
      .append("path")
      .attr("d", "M 0,-5 L 10 ,0 L 0,5")
      .attr("fill", "#94a3b8");

    // Zoom Group
    this.g = this.svg.append("g").attr("class", "graph-zoom-group");

    this.zoomBehavior = d3.zoom()
      .scaleExtent([0.3, 3])
      .on("zoom", (event) => {
        this.g.attr("transform", event.transform);
      });

    this.svg.call(this.zoomBehavior);

    // D3 Force Simulation
    this.simulation = d3.forceSimulation(displayNodes)
      .force("link", d3.forceLink(displayLinks).id(d => d.id).distance(d => d.isCentral ? 140 : 110))
      .force("charge", d3.forceManyBody().strength(d => d.isCentral ? -700 : -350))
      .force("center", d3.forceCenter(width / 2, height / 2))
      .force("collision", d3.forceCollide().radius(d => d.isCentral ? 50 : 38));

    // Render Links (Edges)
    const linkGroup = this.g.append("g").attr("class", "links");
    const link = linkGroup.selectAll("line")
      .data(displayLinks)
      .enter()
      .append("line")
      .attr("class", "graph-link")
      .attr("stroke-width", d => d.confidence === "99%" ? 2.5 : 1.6)
      .attr("marker-end", "url(#arrowhead)");

    // Render Link Labels
    const linkLabelGroup = this.g.append("g").attr("class", "link-labels");
    const linkText = linkLabelGroup.selectAll("text")
      .data(displayLinks)
      .enter()
      .append("text")
      .attr("class", "link-label")
      .text(d => `${d.label}`);

    // Render Nodes Group
    const nodeGroup = this.g.append("g").attr("class", "nodes");
    const node = nodeGroup.selectAll("g")
      .data(displayNodes)
      .enter()
      .append("g")
      .attr("class", d => `node-group ${d.isCentral ? 'central-node' : ''}`)
      .call(d3.drag()
        .on("start", (event, d) => this.dragstarted(event, d))
        .on("drag", (event, d) => this.dragged(event, d))
        .on("end", (event, d) => this.dragended(event, d)))
      .on("click", (event, d) => {
        event.stopPropagation();
        this.selectNode(d.id);
      });

    // Central Node Outer Glow Pulse
    node.filter(d => d.isCentral)
      .append("circle")
      .attr("r", 32)
      .attr("fill", "rgba(37, 99, 235, 0.15)")
      .attr("class", "central-pulse");

    // Node Outer Circle
    node.append("circle")
      .attr("r", d => d.isCentral ? 26 : (d.type === 'Person' ? 22 : 18))
      .attr("fill", d => {
        const conf = this.typeColors[d.type] || { bg: "#f1f5f9" };
        return conf.bg;
      })
      .attr("stroke", d => {
        const conf = this.typeColors[d.type] || { fill: "#64748b" };
        return conf.fill;
      })
      .attr("class", "node-circle")
      .attr("id", d => `node-circle-${d.id}`);

    // Node Type Icon / Emoji
    node.append("text")
      .attr("text-anchor", "middle")
      .attr("dominant-baseline", "central")
      .attr("font-size", d => d.isCentral ? "16px" : "13px")
      .text(d => (this.typeColors[d.type] ? this.typeColors[d.type].icon : "●"));

    // Node Text Label (Title)
    node.append("text")
      .attr("class", "node-label")
      .attr("text-anchor", "middle")
      .attr("dy", d => (d.isCentral ? 38 : (d.type === 'Person' ? 34 : 28)))
      .text(d => d.label);

    // Node Type Sub-label
    node.append("text")
      .attr("class", "node-type-sub")
      .attr("text-anchor", "middle")
      .attr("dy", d => (d.isCentral ? 48 : (d.type === 'Person' ? 44 : 38)))
      .text(d => `${d.type} (${d.confidence}%)`);

    // Simulation Tick Update
    this.simulation.on("tick", () => {
      link
        .attr("x1", d => d.source.x)
        .attr("y1", d => d.source.y)
        .attr("x2", d => d.target.x)
        .attr("y2", d => d.target.y);

      linkText
        .attr("x", d => (d.source.x + d.target.x) / 2)
        .attr("y", d => (d.source.y + d.target.y) / 2 - 3);

      node
        .attr("transform", d => `translate(${d.x},${d.y})`);
    });

    // Reset selection styling if a node was already selected
    if (this.selectedNodeId) {
      this.updateSelectionStyling(this.selectedNodeId);
    }
  },

  selectNode(nodeId) {
    this.selectedNodeId = nodeId;
    this.updateSelectionStyling(nodeId);
    
    // Find node record
    const node = this.rawNodes.find(n => n.id === nodeId);
    if (node) {
      app.displayNodeInspection(node);
    }
  },

  updateSelectionStyling(nodeId) {
    d3.selectAll(".node-circle").classed("selected", false);
    d3.select(`#node-circle-${nodeId}`).classed("selected", true);

    // Highlight immediate links
    d3.selectAll(".graph-link").classed("highlighted", d => {
      const srcId = typeof d.source === 'object' ? d.source.id : d.source;
      const tgtId = typeof d.target === 'object' ? d.target.id : d.target;
      return srcId === nodeId || tgtId === nodeId;
    });
  },

  dragstarted(event, d) {
    if (!event.active) this.simulation.alphaTarget(0.3).restart();
    d.fx = d.x;
    d.fy = d.y;
  },

  dragged(event, d) {
    d.fx = event.x;
    d.fy = event.y;
  },

  dragended(event, d) {
    if (!event.active) this.simulation.alphaTarget(0);
    d.fx = null;
    d.fy = null;
  },

  zoomIn() {
    if (this.svg && this.zoomBehavior) {
      this.svg.transition().duration(250).call(this.zoomBehavior.scaleBy, 1.3);
    }
  },

  zoomOut() {
    if (this.svg && this.zoomBehavior) {
      this.svg.transition().duration(250).call(this.zoomBehavior.scaleBy, 0.75);
    }
  },

  resetZoom() {
    if (this.svg && this.zoomBehavior) {
      this.svg.transition().duration(350).call(this.zoomBehavior.transform, d3.zoomIdentity);
    }
  }
};

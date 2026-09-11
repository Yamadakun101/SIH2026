import React, { useEffect, useRef, useState } from 'react';
import cytoscape from 'cytoscape';
import fcose from 'cytoscape-fcose';
import { 
  ZoomIn, 
  ZoomOut, 
  Maximize2, 
  RotateCcw, 
  Search, 
  Filter,
  Layers,
  Crosshair,
  ShieldAlert
} from 'lucide-react';

cytoscape.use(fcose);

// Crisp SVG Vector Icons converted to Data URIs for Cytoscape node backgrounds
const createSvgIcon = (svgContent, bgColor = '#ffffff', strokeColor = '#0f172a') => {
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40" width="40" height="40">
    <circle cx="20" cy="20" r="18" fill="${bgColor}" stroke="${strokeColor}" stroke-width="2"/>
    <g transform="translate(10, 10)" stroke="${strokeColor}" stroke-width="1.8" fill="none" stroke-linecap="round" stroke-linejoin="round">
      ${svgContent}
    </g>
  </svg>`;
  return `data:image/svg+xml;utf8,${encodeURIComponent(svg)}`;
};

// Category SVG paths
const ICONS = {
  PERSON: createSvgIcon(
    '<path d="M10 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8zM3 18a7 7 0 0 1 14 0H3z"/>',
    '#ede9fe',
    '#6b21a8'
  ),
  PERSON_CENTRAL: createSvgIcon(
    '<path d="M10 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8zM3 18a7 7 0 0 1 14 0H3z"/><circle cx="10" cy="10" r="9" stroke="#dc2626" stroke-width="1.5" stroke-dasharray="2 2"/>',
    '#fef2f2',
    '#b91c1c'
  ),
  PHONE: createSvgIcon(
    '<rect x="4" y="2" width="12" height="16" rx="2"/><line x1="9" y1="15" x2="11" y2="15"/><line x1="8" y1="5" x2="12" y2="5"/>',
    '#dcfce7',
    '#15803d'
  ),
  VEHICLE: createSvgIcon(
    '<path d="M4 11h12l-2-6H6L4 11zM3 11v5h2v-2h10v2h2v-5H3z"/><circle cx="6.5" cy="13.5" r="1.5"/><circle cx="13.5" cy="13.5" r="1.5"/>',
    '#fef3c7',
    '#b45309'
  ),
  BANK_ACCOUNT: createSvgIcon(
    '<path d="M2 7l8-4 8 4v2H2V7zM4 9v6M8 9v6M12 9v6M16 9v6M2 17h16v2H2v-2z"/>',
    '#f3e8ff',
    '#7e22ce'
  ),
  TRANSACTION: createSvgIcon(
    '<rect x="2" y="4" width="16" height="12" rx="2"/><line x1="2" y1="8" x2="18" y2="8"/><line x1="5" y1="13" x2="9" y2="13"/>',
    '#e0f2fe',
    '#0369a1'
  ),
  LOCATION: createSvgIcon(
    '<path d="M10 2a6 6 0 0 0-6 6c0 4.5 6 10 6 10s6-5.5 6-10a6 6 0 0 0-6-6z"/><circle cx="10" cy="8" r="2"/>',
    '#ffe4e6',
    '#be123c'
  ),
  CCTV_EVENT: createSvgIcon(
    '<path d="M14 6l4-2v12l-4-2M2 6h12v8H2z"/><circle cx="7" cy="10" r="2"/>',
    '#f1f5f9',
    '#334155'
  ),
  FIR_CASE: createSvgIcon(
    '<path d="M4 2h8l4 4v12a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2z"/><polyline points="12 2 12 6 16 6"/><line x1="6" y1="10" x2="14" y2="10"/><line x1="6" y1="14" x2="11" y2="14"/>',
    '#ffedd5',
    '#c2410c'
  )
};

export default function NetworkGraph({ 
  graphData, 
  onSelectNode, 
  onSelectEdge,
  highlightedEntityIds = []
}) {
  const containerRef = useRef(null);
  const cyRef = useRef(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedFilter, setSelectedFilter] = useState('ALL');
  const [focusedEntityName, setFocusedEntityName] = useState(null);

  useEffect(() => {
    if (!containerRef.current || !graphData) return;

    // Spacious non-overlapping topology layout with generous hitbox clearances
    const initialPositions = {
      'fir-104-maurice': { x: 120, y: 120 },
      'person-pooja': { x: 360, y: 220 },
      'loc-north-campus': { x: 600, y: 300 },
      'cctv-du-exit': { x: 480, y: 480 },
      'vehicle-dl01-ax': { x: 740, y: 520 },
      'vehicle-hr26-dq': { x: 700, y: 340 },
      'loc-murthal-toll': { x: 800, y: 180 },
      'cctv-isbt-gate3': { x: 960, y: 360 },
      'loc-safehouse-kundli': { x: 580, y: 740 },
      'loc-kashmere-isbt': { x: 880, y: 720 },
      'person-sunil': { x: 1120, y: 520 },
      'bank-icici': { x: 1360, y: 360 },
      'txn-upi-50k': { x: 1600, y: 520 },
      'bank-hdfc': { x: 1440, y: 720 },
      'person-vikram': { x: 1220, y: 800 },
      'person-rakesh': { x: 1040, y: 1020 },
      'fir-78-civil-lines': { x: 1300, y: 1020 },
      'phone-fir-linked': { x: 1560, y: 1020 },
      'phone-rakesh-primary': { x: 1180, y: 1240 },
      'phone-associate-contact': { x: 1180, y: 1440 }
    };

    const cyNodes = graphData.nodes.map((node) => {
      let iconUrl = ICONS[node.type] || ICONS.PERSON;
      let size = 42;

      if (node.id === 'person-rakesh') {
        iconUrl = ICONS.PERSON_CENTRAL;
        size = 52;
      } else if (node.id === 'fir-78-civil-lines') {
        iconUrl = ICONS.FIR_CASE;
        size = 46;
      }

      const formattedLabel = `${node.label}\n${node.sub_type}`;

      return {
        data: {
          id: node.id,
          label: formattedLabel,
          type: node.type,
          match_pct: node.match_pct,
          iconUrl: iconUrl,
          size: size,
          original: node
        },
        position: initialPositions[node.id] || { x: 500, y: 500 }
      };
    });

    const cyEdges = graphData.edges.map((edge) => {
      return {
        data: {
          id: edge.id,
          source: edge.source,
          target: edge.target,
          label: edge.label,
          match_pct: edge.match_pct,
          original: edge
        }
      };
    });

    const cy = cytoscape({
      container: containerRef.current,
      elements: [...cyNodes, ...cyEdges],
      style: [
        {
          selector: 'node',
          style: {
            'label': 'data(label)',
            'width': 'data(size)',
            'height': 'data(size)',
            'background-image': 'data(iconUrl)',
            'background-fit': 'cover',
            'background-clip': 'node',
            'border-width': 2,
            'border-color': '#0f172a',
            'color': '#0f172a',
            'font-size': '9.5px',
            'font-weight': '600',
            'font-family': '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
            'text-valign': 'bottom',
            'text-margin-y': 7,
            'text-wrap': 'wrap',
            'text-max-width': '125px',
            'text-background-color': '#ffffff',
            'text-background-opacity': 0.95,
            'text-background-padding': '3px',
            'text-background-shape': 'roundrectangle',
            'text-border-width': 1,
            'text-border-color': '#e2e8f0',
            'shadow-blur': 10,
            'shadow-color': 'rgba(15, 23, 42, 0.1)',
            'shadow-opacity': 0.8
          }
        },
        {
          selector: 'edge',
          style: {
            'width': 1.8,
            'line-color': '#94a3b8',
            'target-arrow-color': '#94a3b8',
            'target-arrow-shape': 'triangle',
            'arrow-scale': 1.0,
            'curve-style': 'bezier',
            'label': 'data(label)',
            'font-size': '8px',
            'font-weight': '600',
            'color': '#475569',
            'text-background-color': '#ffffff',
            'text-background-opacity': 0.95,
            'text-background-padding': '2px',
            'text-background-shape': 'roundrectangle',
            'text-border-width': 0.8,
            'text-border-color': '#e2e8f0',
            'text-rotation': 'autorotate'
          }
        },
        // Active clicked node & its direct connection paths
        {
          selector: '.highlighted-node',
          style: {
            'border-width': 4.5,
            'border-color': '#1e3a8a',
            'shadow-blur': 24,
            'shadow-color': 'rgba(30, 58, 138, 0.45)',
            'shadow-opacity': 1
          }
        },
        {
          selector: '.highlighted-edge',
          style: {
            'width': 3.5,
            'line-color': '#1e3a8a',
            'target-arrow-color': '#1e3a8a',
            'color': '#1e3a8a',
            'font-weight': '700',
            'z-index': 100
          }
        },
        // Central Person (Rakesh Kumar) special incoming evidence highlight
        {
          selector: '.culprit-focus-node',
          style: {
            'border-width': 5,
            'border-color': '#b91c1c',
            'shadow-blur': 28,
            'shadow-color': 'rgba(185, 28, 28, 0.55)',
            'shadow-opacity': 1
          }
        },
        {
          selector: '.culprit-incoming-edge',
          style: {
            'width': 4,
            'line-color': '#b91c1c',
            'target-arrow-color': '#b91c1c',
            'color': '#b91c1c',
            'font-weight': '700',
            'line-style': 'solid',
            'z-index': 110
          }
        },
        {
          selector: '.dimmed',
          style: {
            'opacity': 0.18
          }
        }
      ],
      layout: {
        name: 'preset',
        fit: true,
        padding: 60
      },
      minZoom: 0.25,
      maxZoom: 3.5,
      wheelSensitivity: 0.25,
      boxSelectionEnabled: false
    });

    // Handle Node Click & Directional Arrow Highlighting
    cy.on('tap', 'node', (evt) => {
      const node = evt.target;
      const nodeData = node.data('original');
      setFocusedEntityName(node.data('original').label);

      // Reset all previous highlights
      cy.elements().removeClass('highlighted-node highlighted-edge culprit-focus-node culprit-incoming-edge dimmed');

      // Check if clicked node is Rakesh Kumar (Main Person of Interest)
      if (node.id() === 'person-rakesh') {
        // Dim everything first
        cy.elements().addClass('dimmed');

        // Highlight Rakesh
        node.removeClass('dimmed').addClass('culprit-focus-node');

        // Highlight all directly connected edges and nodes
        const connectedEdges = node.connectedEdges();
        const connectedNeighbors = node.neighborhood();

        // Also trace incoming paths and nexus evidence
        const incomingEdges = node.incomers('edge');
        const outgoingEdges = node.outgoers('edge');

        connectedEdges.removeClass('dimmed').addClass('culprit-incoming-edge');
        connectedNeighbors.removeClass('dimmed').addClass('highlighted-node');

        // Also highlight 2nd degree financial and call links (Phones & FIR 78/2024)
        cy.$('#fir-78-civil-lines, #phone-rakesh-primary, #person-vikram, #bank-hdfc').removeClass('dimmed').addClass('highlighted-node');
        cy.$('#e16, #e17, #e18, #e19, #e21, #e22, #e24').removeClass('dimmed').addClass('culprit-incoming-edge');

      } else {
        // Any other evidence node clicked:
        // Dim all non-related elements
        cy.elements().addClass('dimmed');

        // Highlight the clicked node
        node.removeClass('dimmed').addClass('highlighted-node');

        // Highlight all incoming & outgoing connecting arrows and their target/source nodes
        const connectedEdges = node.connectedEdges();
        const neighborNodes = node.neighborhood('node');

        connectedEdges.removeClass('dimmed').addClass('highlighted-edge');
        neighborNodes.removeClass('dimmed').addClass('highlighted-node');
      }

      if (onSelectNode) onSelectNode(nodeData);
    });

    // Handle Edge Click
    cy.on('tap', 'edge', (evt) => {
      const edge = evt.target;
      const edgeData = edge.data('original');
      setFocusedEntityName(edge.data('label'));

      cy.elements().addClass('dimmed');
      edge.removeClass('dimmed').addClass('highlighted-edge');
      edge.source().removeClass('dimmed').addClass('highlighted-node');
      edge.target().removeClass('dimmed').addClass('highlighted-node');

      if (onSelectEdge) onSelectEdge(edgeData);
    });

    // Background Click -> Reset Highlight
    cy.on('tap', (evt) => {
      if (evt.target === cy) {
        cy.elements().removeClass('highlighted-node highlighted-edge culprit-focus-node culprit-incoming-edge dimmed');
        setFocusedEntityName(null);
      }
    });

    cyRef.current = cy;

    return () => {
      cy.destroy();
    };
  }, [graphData]);

  // Handle external highlights from Assistant / Dossier
  useEffect(() => {
    if (!cyRef.current) return;
    const cy = cyRef.current;

    if (highlightedEntityIds.length > 0) {
      cy.elements().addClass('dimmed');
      highlightedEntityIds.forEach((id) => {
        const ele = cy.$(`#${id}`);
        if (ele && ele.length > 0) {
          ele.removeClass('dimmed').addClass('highlighted-node');
          ele.connectedEdges().removeClass('dimmed').addClass('highlighted-edge');
        }
      });
    } else {
      cy.elements().removeClass('dimmed highlighted-node highlighted-edge culprit-focus-node culprit-incoming-edge');
    }
  }, [highlightedEntityIds]);

  // Filter nodes by category
  const handleFilterChange = (category) => {
    setSelectedFilter(category);
    if (!cyRef.current) return;
    const cy = cyRef.current;

    if (category === 'ALL') {
      cy.elements().show();
    } else {
      cy.nodes().forEach((node) => {
        if (node.data('type') === category) {
          node.show();
          node.connectedEdges().show();
        } else {
          node.hide();
        }
      });
    }
    cy.fit();
  };

  // Search node
  const handleSearch = (e) => {
    const val = e.target.value.toLowerCase();
    setSearchTerm(val);
    if (!cyRef.current) return;
    const cy = cyRef.current;

    if (!val.trim()) {
      cy.elements().removeClass('highlighted-node highlighted-edge dimmed');
      return;
    }

    cy.elements().addClass('dimmed');
    const matched = cy.nodes().filter((n) => {
      const label = n.data('label').toLowerCase();
      return label.includes(val);
    });

    matched.removeClass('dimmed').addClass('highlighted-node');
    matched.connectedEdges().removeClass('dimmed').addClass('highlighted-edge');
  };

  const handleReset = () => {
    if (!cyRef.current) return;
    cyRef.current.elements().removeClass('highlighted-node highlighted-edge culprit-focus-node culprit-incoming-edge dimmed');
    setFocusedEntityName(null);
    cyRef.current.fit();
  };

  const handleAutoSpace = () => {
    if (!cyRef.current) return;
    cyRef.current.layout({
      name: 'fcose',
      quality: 'proof',
      randomize: false,
      animate: true,
      animationDuration: 600,
      nodeDimensionsIncludeLabels: true,
      nodeRepulsion: 15000,
      idealEdgeLength: 220,
      edgeElasticity: 0.35,
      nestingFactor: 0.1,
      gravity: 0.15,
      fit: true,
      padding: 60
    }).run();
  };

  return (
    <div className="graph-view-container">
      {/* Graph Toolbar */}
      <div className="graph-toolbar">
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
          <Search size={15} color="var(--text-secondary)" />
          <input
            type="text"
            className="graph-search-input"
            placeholder="Search evidence, vehicle, phone..."
            value={searchTerm}
            onChange={handleSearch}
          />
        </div>

        <div style={{ width: '1px', height: '20px', background: 'var(--border-light)', margin: '0 0.2rem' }} />

        <button 
          className="graph-tool-btn" 
          title="Zoom In"
          onClick={() => cyRef.current?.zoom(cyRef.current.zoom() * 1.25)}
        >
          <ZoomIn size={16} />
        </button>

        <button 
          className="graph-tool-btn" 
          title="Zoom Out"
          onClick={() => cyRef.current?.zoom(cyRef.current.zoom() * 0.8)}
        >
          <ZoomOut size={16} />
        </button>

        <button 
          className="graph-tool-btn" 
          title="Fit Network"
          onClick={() => cyRef.current?.fit()}
        >
          <Maximize2 size={16} />
        </button>

        <button 
          className="graph-tool-btn" 
          title="Auto Space & Avoid Collisions"
          onClick={handleAutoSpace}
        >
          <Layers size={16} />
        </button>

        <button 
          className="graph-tool-btn" 
          title="Reset View & Clear Highlights"
          onClick={handleReset}
        >
          <RotateCcw size={16} />
        </button>

        <div style={{ width: '1px', height: '20px', background: 'var(--border-light)', margin: '0 0.2rem' }} />

        {/* Filter Dropdown */}
        <select
          value={selectedFilter}
          onChange={(e) => handleFilterChange(e.target.value)}
          style={{
            border: '1px solid var(--border-medium)',
            borderRadius: 'var(--radius-sm)',
            padding: '0.35rem 0.5rem',
            fontSize: '0.78rem',
            outline: 'none',
            color: 'var(--text-primary)',
            background: 'white'
          }}
        >
          <option value="ALL">All Categories ({graphData?.nodes?.length || 0})</option>
          <option value="PERSON">Persons</option>
          <option value="PHONE">Phones & Call Logs</option>
          <option value="VEHICLE">Vehicles</option>
          <option value="LOCATION">Locations</option>
          <option value="BANK_ACCOUNT">Bank Accounts</option>
          <option value="TRANSACTION">Transactions</option>
          <option value="CCTV_EVENT">CCTV Sightings</option>
          <option value="FIR_CASE">FIR / Cases</option>
        </select>
      </div>

      {/* Focus Indicator Pill */}
      {focusedEntityName && (
        <div style={{
          position: 'absolute',
          top: '1rem',
          right: '1.5rem',
          background: 'var(--gov-navy)',
          color: 'white',
          padding: '0.4rem 0.85rem',
          borderRadius: '9999px',
          fontSize: '0.78rem',
          fontWeight: 700,
          boxShadow: '0 4px 10px rgba(0,0,0,0.15)',
          zIndex: 10,
          display: 'flex',
          alignItems: 'center',
          gap: '0.4rem'
        }}>
          <Crosshair size={14} />
          <span>Active Focus: {focusedEntityName}</span>
        </div>
      )}

      {/* Main Canvas */}
      <div className="graph-canvas-wrapper">
        <div id="cy-container" ref={containerRef} />
      </div>

      {/* Graph Legend Overlay with Real Category Icons */}
      <div className="graph-legend-overlay">
        <div className="graph-legend-item">
          <span style={{ display: 'inline-block', width: '12px', height: '12px', borderRadius: '50%', background: '#b91c1c', border: '1.5px solid #ffffff' }}></span>
          <span>Central Subject (Rakesh)</span>
        </div>
        <div className="graph-legend-item">
          <span style={{ display: 'inline-block', width: '12px', height: '12px', borderRadius: '50%', background: '#6b21a8' }}></span>
          <span>Person</span>
        </div>
        <div className="graph-legend-item">
          <span style={{ display: 'inline-block', width: '12px', height: '12px', borderRadius: '50%', background: '#15803d' }}></span>
          <span>Phone / Call Record</span>
        </div>
        <div className="graph-legend-item">
          <span style={{ display: 'inline-block', width: '12px', height: '12px', borderRadius: '50%', background: '#b45309' }}></span>
          <span>Vehicle</span>
        </div>
        <div className="graph-legend-item">
          <span style={{ display: 'inline-block', width: '12px', height: '12px', borderRadius: '50%', background: '#7e22ce' }}></span>
          <span>Bank Account</span>
        </div>
        <div className="graph-legend-item">
          <span style={{ display: 'inline-block', width: '12px', height: '12px', borderRadius: '50%', background: '#be123c' }}></span>
          <span>Location Hub</span>
        </div>
      </div>
    </div>
  );
}

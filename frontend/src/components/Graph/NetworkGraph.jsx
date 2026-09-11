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
  Sparkles
} from 'lucide-react';

cytoscape.use(fcose);

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

  useEffect(() => {
    if (!containerRef.current || !graphData) return;

    // Layout positions matching the spatial layout of Image 1
    const initialPositions = {
      'fir-104-maurice': { x: 100, y: 80 },
      'person-pooja': { x: 200, y: 150 },
      'loc-north-campus': { x: 300, y: 200 },
      'cctv-du-exit': { x: 280, y: 280 },
      'vehicle-dl01-ax': { x: 400, y: 340 },
      'cctv-isbt-gate3': { x: 480, y: 240 },
      'vehicle-hr26-dq': { x: 380, y: 240 },
      'loc-murthal-toll': { x: 420, y: 190 },
      'loc-safehouse-kundli': { x: 340, y: 440 },
      'loc-kashmere-isbt': { x: 490, y: 500 },
      'person-sunil': { x: 560, y: 370 },
      'bank-icici': { x: 670, y: 310 },
      'txn-upi-50k': { x: 770, y: 410 },
      'bank-hdfc': { x: 700, y: 540 },
      'person-vikram': { x: 650, y: 550 },
      'fir-78-civil-lines': { x: 670, y: 690 },
      'person-rakesh': { x: 590, y: 650 },
      'phone-rakesh-primary': { x: 670, y: 820 },
      'phone-fir-linked': { x: 730, y: 690 },
      'phone-associate-contact': { x: 690, y: 940 }
    };

    // Color definitions matching Image 1
    const cyNodes = graphData.nodes.map((node) => {
      let nodeColor = '#e2e8f0';
      let borderColor = '#94a3b8';
      let borderWidth = 2;
      let size = 38;

      if (node.id === 'person-rakesh') {
        nodeColor = '#e0e7ff';
        borderColor = '#4338ca';
        borderWidth = 3.5;
        size = 46;
      } else if (node.id === 'fir-78-civil-lines') {
        nodeColor = '#ffedd5';
        borderColor = '#0f172a';
        borderWidth = 3.5;
        size = 44;
      } else if (node.type === 'PERSON') {
        nodeColor = '#ede9fe';
        borderColor = '#7c3aed';
      } else if (node.type === 'LOCATION') {
        nodeColor = '#ffe4e6';
        borderColor = '#e11d48';
      } else if (node.type === 'VEHICLE') {
        nodeColor = '#fef3c7';
        borderColor = '#d97706';
      } else if (node.type === 'BANK_ACCOUNT') {
        nodeColor = '#f3e8ff';
        borderColor = '#9333ea';
      } else if (node.type === 'TRANSACTION') {
        nodeColor = '#e0f2fe';
        borderColor = '#0284c7';
      } else if (node.type === 'PHONE') {
        nodeColor = '#dcfce7';
        borderColor = '#16a34a';
      } else if (node.type === 'CCTV_EVENT') {
        nodeColor = '#f1f5f9';
        borderColor = '#475569';
      } else if (node.type === 'FIR_CASE') {
        nodeColor = '#ffedd5';
        borderColor = '#ea580c';
      }

      const formattedLabel = `${node.label}\n${node.sub_type}`;

      return {
        data: {
          id: node.id,
          label: formattedLabel,
          type: node.type,
          match_pct: node.match_pct,
          color: nodeColor,
          borderColor: borderColor,
          borderWidth: borderWidth,
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
            'background-color': 'data(color)',
            'border-width': 'data(borderWidth)',
            'border-color': 'data(borderColor)',
            'color': '#1e293b',
            'font-size': '9.5px',
            'font-weight': '600',
            'font-family': '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
            'text-valign': 'bottom',
            'text-margin-y': 7,
            'text-wrap': 'wrap',
            'text-max-width': '120px',
            'text-background-color': '#ffffff',
            'text-background-opacity': 0.95,
            'text-background-padding': '3px',
            'text-background-shape': 'roundrectangle',
            'text-border-width': 1,
            'text-border-color': '#e2e8f0',
            'shadow-blur': 8,
            'shadow-color': 'rgba(15, 23, 42, 0.08)',
            'shadow-opacity': 0.8
          }
        },
        {
          selector: 'node:selected',
          style: {
            'border-width': 4,
            'border-color': '#1e3a8a',
            'shadow-blur': 16,
            'shadow-color': 'rgba(30, 58, 138, 0.35)',
            'shadow-opacity': 1
          }
        },
        {
          selector: 'edge',
          style: {
            'width': 1.6,
            'line-color': '#94a3b8',
            'target-arrow-color': '#94a3b8',
            'target-arrow-shape': 'triangle',
            'arrow-scale': 0.9,
            'curve-style': 'bezier',
            'label': 'data(label)',
            'font-size': '7.5px',
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
        {
          selector: 'edge:selected',
          style: {
            'width': 2.8,
            'line-color': '#1e3a8a',
            'target-arrow-color': '#1e3a8a',
            'color': '#1e3a8a',
            'font-weight': '700'
          }
        },
        {
          selector: '.highlighted',
          style: {
            'border-width': 4.5,
            'border-color': '#dc2626',
            'shadow-blur': 22,
            'shadow-color': 'rgba(220, 38, 38, 0.5)',
            'shadow-opacity': 1
          }
        },
        {
          selector: '.dimmed',
          style: {
            'opacity': 0.22
          }
        }
      ],
      layout: {
        name: 'preset',
        fit: true,
        padding: 50
      }
    });

    cy.on('tap', 'node', (evt) => {
      const nodeData = evt.target.data('original');
      if (onSelectNode) onSelectNode(nodeData);
    });

    cy.on('tap', 'edge', (evt) => {
      const edgeData = evt.target.data('original');
      if (onSelectEdge) onSelectEdge(edgeData);
    });

    cy.on('tap', (evt) => {
      if (evt.target === cy) {
        cy.elements().removeClass('highlighted dimmed');
      }
    });

    cyRef.current = cy;

    return () => {
      cy.destroy();
    };
  }, [graphData]);

  // Handle highlights from AI assistant
  useEffect(() => {
    if (!cyRef.current) return;
    const cy = cyRef.current;

    if (highlightedEntityIds.length > 0) {
      cy.elements().addClass('dimmed');
      highlightedEntityIds.forEach((id) => {
        const ele = cy.$(`#${id}`);
        if (ele && ele.length > 0) {
          ele.removeClass('dimmed').addClass('highlighted');
          ele.connectedEdges().removeClass('dimmed');
        }
      });
    } else {
      cy.elements().removeClass('dimmed highlighted');
    }
  }, [highlightedEntityIds]);

  // Filter nodes
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
      cy.elements().removeClass('highlighted dimmed');
      return;
    }

    cy.elements().addClass('dimmed');
    const matched = cy.nodes().filter((n) => {
      const label = n.data('label').toLowerCase();
      return label.includes(val);
    });

    matched.removeClass('dimmed').addClass('highlighted');
    matched.connectedEdges().removeClass('dimmed');
  };

  const handleRunForceLayout = () => {
    if (!cyRef.current) return;
    cyRef.current.layout({
      name: 'fcose',
      quality: 'proof',
      randomize: false,
      animate: true,
      animationDuration: 600,
      nodeDimensionsIncludeLabels: true,
      nodeRepulsion: 9500,
      idealEdgeLength: 150,
      edgeElasticity: 0.45,
      fit: true,
      padding: 40
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
            placeholder="Search node, FIR, phone..."
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
          onClick={handleRunForceLayout}
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
          <option value="ALL">All Network Entities ({graphData?.nodes?.length || 0})</option>
          <option value="PERSON">Persons</option>
          <option value="PHONE">Phones</option>
          <option value="VEHICLE">Vehicles</option>
          <option value="LOCATION">Locations</option>
          <option value="BANK_ACCOUNT">Bank Accounts</option>
          <option value="CCTV_EVENT">CCTV Events</option>
          <option value="FIR_CASE">FIR / Cases</option>
        </select>
      </div>

      {/* Main Canvas */}
      <div className="graph-canvas-wrapper">
        <div id="cy-container" ref={containerRef} />
      </div>

      {/* Graph Legend Overlay */}
      <div className="graph-legend-overlay">
        <div className="graph-legend-item">
          <span className="node-chip" style={{ background: '#ede9fe', border: '1.5px solid #7c3aed' }}></span>
          <span>Person (e.g. Rakesh 91%, Pooja 100%)</span>
        </div>
        <div className="graph-legend-item">
          <span className="node-chip" style={{ background: '#ffe4e6', border: '1.5px solid #e11d48' }}></span>
          <span>Location (e.g. North Campus 98%)</span>
        </div>
        <div className="graph-legend-item">
          <span className="node-chip" style={{ background: '#fef3c7', border: '1.5px solid #d97706' }}></span>
          <span>Vehicle (e.g. DL 01 AX 4492 92%)</span>
        </div>
        <div className="graph-legend-item">
          <span className="node-chip" style={{ background: '#f3e8ff', border: '1.5px solid #9333ea' }}></span>
          <span>Bank Account (e.g. HDFC 96%)</span>
        </div>
        <div className="graph-legend-item">
          <span className="node-chip" style={{ background: '#dcfce7', border: '1.5px solid #16a34a' }}></span>
          <span>Phone (e.g. +91 98765 94%)</span>
        </div>
      </div>
    </div>
  );
}

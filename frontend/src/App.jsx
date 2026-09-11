import React, { useState } from 'react';
import { 
  Network, 
  Clock, 
  FileCheck, 
  Bot, 
  ChevronRight, 
  Award,
  Sparkles,
  ArrowLeft,
  Users
} from 'lucide-react';
import IndiaMap from './components/IndiaMap/IndiaMap';
import NetworkGraph from './components/Graph/NetworkGraph';
import EntityInspector from './components/Inspector/EntityInspector';
import OverviewTab from './components/Overview/OverviewTab';
import TimelineView from './components/Timeline/TimelineView';
import EvidenceTab from './components/Evidence/EvidenceTab';
import AiAssistant from './components/Assistant/AiAssistant';
import BsaCertificateModal from './components/Certificate/BsaCertificateModal';
import { CASE_PROTOTYPE_DATA } from './data/casesData';
import './styles/main.css';

export default function App() {
  // Navigation State
  const [currentView, setCurrentView] = useState('MAP'); // 'MAP' or 'WORKSPACE'
  const [activeTab, setActiveTab] = useState('GRAPH'); // 'GRAPH', 'OVERVIEW', 'TIMELINE', 'EVIDENCE'
  const [selectedCaseId, setSelectedCaseId] = useState('DL-2026-0412');
  
  // Inspection & Interaction State
  const [selectedEntity, setSelectedEntity] = useState(null);
  const [selectedEdge, setSelectedEdge] = useState(null);
  const [highlightedEntityIds, setHighlightedEntityIds] = useState([]);
  
  // Modals & Drawers
  const [isAssistantOpen, setIsAssistantOpen] = useState(false);
  const [isCertificateOpen, setIsCertificateOpen] = useState(false);

  const caseData = CASE_PROTOTYPE_DATA;

  // Handle case selection from India Map
  const handleSelectCase = (caseId) => {
    setSelectedCaseId(caseId);
    setCurrentView('WORKSPACE');
    setActiveTab('GRAPH');
  };

  // Node & Edge selection
  const handleSelectNode = (node) => {
    setSelectedEntity(node);
    setSelectedEdge(null);
  };

  const handleSelectEdge = (edge) => {
    setSelectedEdge(edge);
    setSelectedEntity(null);
  };

  const handleCloseInspector = () => {
    setSelectedEntity(null);
    setSelectedEdge(null);
  };

  // Inspect primary person (Rakesh Kumar)
  const handleInspectPrimarySubject = () => {
    const subjectNode = caseData.graph.nodes.find((n) => n.id === 'person-rakesh');
    if (subjectNode) {
      setSelectedEntity(subjectNode);
      setActiveTab('GRAPH');
      setHighlightedEntityIds(['person-rakesh']);
    }
  };

  // Inspect specific associate node from Overview
  const handleInspectAssociate = (nodeId) => {
    const targetNode = caseData.graph.nodes.find((n) => n.id === nodeId);
    if (targetNode) {
      setSelectedEntity(targetNode);
      setActiveTab('GRAPH');
      setHighlightedEntityIds([nodeId]);
    }
  };

  return (
    <div className="app-container">
      {/* Top Application Header */}
      <header className="app-header">
        <div className="brand-section">
          <div className="brand-logo">KN</div>
          <div>
            <div className="brand-title">
              <span>KavachNet</span>
              <span className="brand-badge">NCRB / MHA • PS #26189</span>
            </div>
            <div className="brand-subtitle">
              AI-Powered Criminal Network Analysis & Evidentiary Integrity System
            </div>
          </div>
        </div>

        <div className="header-actions">
          {currentView === 'WORKSPACE' && (
            <button 
              className="header-btn"
              onClick={() => setCurrentView('MAP')}
            >
              <ArrowLeft size={14} />
              National Case Map
            </button>
          )}

          <div className="gov-badge-match">
            <span>Overall Case Match: {caseData.metadata.overall_match_rate}%</span>
          </div>

          <button 
            className="header-btn primary"
            onClick={() => setIsCertificateOpen(true)}
          >
            <Award size={14} />
            Court Evidence Certificate
          </button>
        </div>
      </header>

      {/* Breadcrumb Bar (Matching Image 2) */}
      <div className="breadcrumb-bar">
        <div className="breadcrumb-path">
          <span 
            className="breadcrumb-link"
            onClick={() => setCurrentView('MAP')}
          >
            National Case Map
          </span>
          {currentView === 'WORKSPACE' && (
            <>
              <ChevronRight size={13} color="var(--text-muted)" />
              <span>{caseData.metadata.state_name}</span>
              <ChevronRight size={13} color="var(--text-muted)" />
              <span style={{ fontWeight: 700, color: 'var(--text-primary)' }}>
                {caseData.metadata.case_id}
              </span>
            </>
          )}
        </div>

        <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>
          LOCAL DEMO MODE (SYNTHETIC CASE DATA)
        </div>
      </div>

      {/* Main Viewport */}
      <main className="main-viewport">
        {currentView === 'MAP' ? (
          <IndiaMap onSelectCase={handleSelectCase} />
        ) : (
          <div className="case-workspace">
            {/* Case Header Sub-Bar */}
            <div className="case-header-bar">
              <div className="case-title-area">
                <span className="gov-badge-lead">
                  {caseData.metadata.status.replace(/_/g, ' ')}
                </span>
                <div>
                  <h1 className="case-title-text">{caseData.metadata.title}</h1>
                  <div className="case-meta-pills" style={{ marginTop: '0.15rem' }}>
                    <span className="meta-pill">Case ID: {caseData.metadata.case_id}</span>
                    <span className="meta-pill">FIR: {caseData.metadata.fir_number}</span>
                    <span className="meta-pill">Incident: {caseData.metadata.incident_date}</span>
                    <span className="meta-pill">Agency: {caseData.metadata.lead_agency}</span>
                  </div>
                </div>
              </div>

              <div style={{ display: 'flex', gap: '0.5rem' }}>
                <button 
                  className="header-btn"
                  onClick={() => setIsAssistantOpen(true)}
                  style={{ background: '#eff6ff', borderColor: '#bfdbfe', color: 'var(--gov-navy)' }}
                >
                  <Sparkles size={14} />
                  Ask AI Assistant
                </button>
              </div>
            </div>

            {/* Navigation Tabs (Matching Image 2) */}
            <div className="workspace-tabs">
              <button
                className={`tab-btn ${activeTab === 'GRAPH' ? 'active' : ''}`}
                onClick={() => setActiveTab('GRAPH')}
              >
                <Network size={15} />
                Network Graph
              </button>

              <button
                className={`tab-btn ${activeTab === 'OVERVIEW' ? 'active' : ''}`}
                onClick={() => setActiveTab('OVERVIEW')}
              >
                <Users size={15} />
                Case Overview & Suspects
              </button>

              <button
                className={`tab-btn ${activeTab === 'TIMELINE' ? 'active' : ''}`}
                onClick={() => setActiveTab('TIMELINE')}
              >
                <Clock size={15} />
                Chronological Timeline
              </button>

              <button
                className={`tab-btn ${activeTab === 'EVIDENCE' ? 'active' : ''}`}
                onClick={() => setActiveTab('EVIDENCE')}
              >
                <FileCheck size={15} />
                Evidence Provenance Log
              </button>

              <button
                className="tab-btn"
                onClick={() => setIsAssistantOpen(true)}
                style={{ marginLeft: 'auto', color: 'var(--gov-navy)' }}
              >
                <Bot size={15} />
                Case-Aware AI Assistant
              </button>
            </div>

            {/* Workspace Body Area */}
            <div className="workspace-body">
              {activeTab === 'GRAPH' && (
                <>
                  <NetworkGraph
                    graphData={caseData.graph}
                    onSelectNode={handleSelectNode}
                    onSelectEdge={handleSelectEdge}
                    highlightedEntityIds={highlightedEntityIds}
                  />

                  {/* Inspector Drawer */}
                  {(selectedEntity || selectedEdge) && (
                    <EntityInspector
                      selectedEntity={selectedEntity}
                      selectedEdge={selectedEdge}
                      onClose={handleCloseInspector}
                    />
                  )}
                </>
              )}

              {activeTab === 'OVERVIEW' && (
                <OverviewTab
                  caseData={caseData}
                  onInspectSubject={handleInspectPrimarySubject}
                  onInspectAssociate={handleInspectAssociate}
                  onAskAi={(prompt) => {
                    setIsAssistantOpen(true);
                  }}
                />
              )}

              {activeTab === 'TIMELINE' && (
                <TimelineView
                  timelineData={caseData.timeline}
                  onSelectEntity={(entityId) => {
                    setActiveTab('GRAPH');
                    setHighlightedEntityIds([entityId]);
                  }}
                />
              )}

              {activeTab === 'EVIDENCE' && (
                <EvidenceTab
                  caseData={caseData}
                  onOpenCertificate={() => setIsCertificateOpen(true)}
                />
              )}
            </div>
          </div>
        )}
      </main>

      {/* Case-Aware AI Assistant Drawer */}
      <AiAssistant
        isOpen={isAssistantOpen}
        onToggle={() => setIsAssistantOpen(!isAssistantOpen)}
        onHighlightEntities={(entityIds) => {
          setActiveTab('GRAPH');
          setHighlightedEntityIds(entityIds);
        }}
      />

      {/* BSA 2023 Section 63 Evidence Certificate Modal */}
      {isCertificateOpen && (
        <BsaCertificateModal
          caseData={caseData}
          onClose={() => setIsCertificateOpen(false)}
        />
      )}
    </div>
  );
}

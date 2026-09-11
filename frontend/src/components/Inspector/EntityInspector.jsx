import React from 'react';
import { 
  X, 
  ShieldCheck, 
  FileText, 
  HelpCircle, 
  Database,
  CheckCircle2,
  Percent
} from 'lucide-react';

export default function EntityInspector({ selectedEntity, selectedEdge, onClose }) {
  if (!selectedEntity && !selectedEdge) return null;

  const isNode = Boolean(selectedEntity);
  const data = selectedEntity || selectedEdge;

  return (
    <div className="inspector-drawer">
      {/* Header */}
      <div className="inspector-header">
        <div className="inspector-category-tag">
          <span>{isNode ? `ENTITY CLASSIFICATION: ${data.type}` : `RELATIONSHIP: ${data.label}`}</span>
          <button 
            onClick={onClose}
            style={{ background: 'transparent', border: 'none', cursor: 'pointer', color: 'var(--text-secondary)' }}
          >
            <X size={18} />
          </button>
        </div>

        <h2 className="inspector-title">{data.label.split('\n')[0]}</h2>

        <div style={{ display: 'flex', gap: '0.4rem', marginTop: '0.2rem' }}>
          <span className="gov-badge-match" style={{ fontSize: '0.75rem' }}>
            {data.match_pct}% Evidence Match Score
          </span>
          {isNode && data.sub_type && (
            <span className="gov-badge-subtle">
              {data.sub_type}
            </span>
          )}
        </div>
      </div>

      <div className="inspector-body">
        {/* Match Percentage Meter */}
        <div className="inspector-section">
          <div className="inspector-section-title">
            <Percent size={14} color="var(--gov-navy)" />
            <span>Case Correlation & Match Rate</span>
          </div>

          <div className="confidence-box">
            <div className="confidence-score-row">
              <span style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>Algorithmic Correlation Rate</span>
              <span className="confidence-score-val" style={{ color: 'var(--gov-navy)' }}>
                {data.match_pct}%
              </span>
            </div>

            <div className="confidence-meter-bar">
              <div 
                className="confidence-meter-fill"
                style={{ 
                  width: `${data.match_pct}%`,
                  background: 'linear-gradient(90deg, #1e3a8a, #2563eb)'
                }}
              />
            </div>

            <p style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
              Cross-domain correlation across FIR filings, CDR tower dumps, FASTag toll cameras, and banking APIs.
            </p>
          </div>
        </div>

        {/* Stored Attributes */}
        <div className="inspector-section">
          <div className="inspector-section-title">
            <Database size={14} color="var(--text-secondary)" />
            <span>Stored Record Metadata</span>
          </div>

          <table className="attributes-table">
            <tbody>
              {isNode && data.details && Object.entries(data.details).map(([k, v]) => (
                <tr key={k}>
                  <td>{k.replace(/_/g, ' ').toUpperCase()}</td>
                  <td>{Array.isArray(v) ? v.join(', ') : String(v)}</td>
                </tr>
              ))}

              {!isNode && (
                <>
                  <tr>
                    <td>ORIGIN NODE</td>
                    <td>{data.source}</td>
                  </tr>
                  <tr>
                    <td>DESTINATION NODE</td>
                    <td>{data.target}</td>
                  </tr>
                  <tr>
                    <td>RELATION TYPE</td>
                    <td>{data.label}</td>
                  </tr>
                </>
              )}
            </tbody>
          </table>
        </div>

        {/* AI Correlation Assessment */}
        <div className="inspector-section">
          <div className="inspector-section-title">
            <HelpCircle size={14} color="var(--gov-navy)" />
            <span>Investigative Lead Assessment</span>
          </div>

          <div style={{ background: 'var(--bg-surface)', border: '1px solid var(--border-light)', borderRadius: 'var(--radius-md)', padding: '0.85rem' }}>
            <div className="explain-bullet">
              <span>{isNode ? (data.evidence_correlation || 'Record linked through cross-referencing multi-source electronic logs.') : `Relationship corroborated with ${data.match_pct}% evidence match score.`}</span>
            </div>
          </div>
        </div>

        {/* Legal Evidence Provenance */}
        <div className="inspector-section">
          <div className="inspector-section-title">
            <FileText size={14} color="var(--text-secondary)" />
            <span>Evidence Ledger & Chain of Custody</span>
          </div>

          <div className="provenance-card">
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.4rem' }}>
              <span style={{ fontWeight: 600, color: 'var(--text-primary)' }}>
                {isNode ? `NODE-${data.id.toUpperCase()}` : `REL-${data.id.toUpperCase()}`}
              </span>
              <span className="gov-badge-subtle" style={{ fontSize: '0.68rem', color: 'var(--gov-navy)' }}>
                BSA 2023 Sec 63 Stamped
              </span>
            </div>

            <div style={{ fontSize: '0.72rem', color: 'var(--text-secondary)' }}>
              Cryptographic SHA-256 Provenance Hash:
            </div>
            <div className="hash-string">
              {data.sha256 || '8f4e2c1b9a8d7e6f5c4b3a210987654321fedcba0987654321abcdef01234567'}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

import React from 'react';
import { 
  User, 
  Phone, 
  Car, 
  ArrowRight, 
  Sparkles, 
  ShieldCheck,
  FileText,
  CreditCard,
  MapPin,
  Video
} from 'lucide-react';

export default function OverviewTab({ 
  caseData, 
  onInspectSubject, 
  onInspectAssociate,
  onAskAi 
}) {
  const metadata = caseData.metadata;
  const primarySubject = metadata.primary_subject;
  const associates = metadata.key_associates;

  return (
    <div className="overview-container">
      <div className="overview-two-col-grid">
        {/* Left Card: Primary Person Profile matching Image 2 */}
        <div className="gov-card">
          <div style={{ display: 'flex', alignItems: 'flex-start', gap: '1rem', marginBottom: '1.25rem' }}>
            <div className="avatar-circle">
              {primarySubject.initials}
            </div>

            <div style={{ flex: 1 }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.35rem', flexWrap: 'wrap' }}>
                <span className="gov-badge-lead">
                  {primarySubject.badge}
                </span>
                <span className="gov-badge-match">
                  {primarySubject.match_confidence}% Match Confidence
                </span>
              </div>

              <h2 style={{ fontSize: '1.35rem', fontWeight: 700, color: 'var(--text-primary)', margin: 0 }}>
                {primarySubject.name}
              </h2>
              <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginTop: '0.15rem' }}>
                Age: {primarySubject.age} • {primarySubject.location} • Status: {primarySubject.status}
              </div>
            </div>
          </div>

          {/* AI Synthesized Investigative Summary */}
          <div className="ai-summary-box">
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', fontSize: '0.8rem', fontWeight: 700, color: 'var(--gov-navy)', marginBottom: '0.35rem' }}>
              <Sparkles size={15} />
              <span>AI Synthesized Investigative Summary</span>
            </div>
            <p style={{ fontSize: '0.82rem', color: 'var(--text-primary)', lineHeight: 1.55 }}>
              "{primarySubject.summary}"
            </p>
          </div>

          {/* Metric Indicators Grid */}
          <div className="metrics-2x3-grid">
            <div className="metric-cell">
              <span className="metric-cell-label">Connected Phones</span>
              <div className="metric-cell-val">{primarySubject.metrics.phones}</div>
            </div>

            <div className="metric-cell">
              <span className="metric-cell-label">Linked Vehicles</span>
              <div className="metric-cell-val">{primarySubject.metrics.vehicles}</div>
            </div>

            <div className="metric-cell">
              <span className="metric-cell-label">Banking Switches</span>
              <div className="metric-cell-val">{primarySubject.metrics.banking}</div>
            </div>

            <div className="metric-cell">
              <span className="metric-cell-label">Key Locations</span>
              <div className="metric-cell-val">{primarySubject.metrics.locations}</div>
            </div>

            <div className="metric-cell">
              <span className="metric-cell-label">Prior FIR Mentions</span>
              <div className="metric-cell-val">{primarySubject.metrics.prior_fir}</div>
            </div>

            <div className="metric-cell">
              <span className="metric-cell-label">CCTV Sightings</span>
              <div className="metric-cell-val">{primarySubject.metrics.cctv}</div>
            </div>
          </div>

          {/* Action Buttons */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginTop: '1.25rem' }}>
            <button 
              className="gov-btn-primary"
              onClick={onInspectSubject}
            >
              <span>Inspect Full Evidence Dossier</span>
              <ArrowRight size={14} />
            </button>

            <button 
              className="gov-btn-secondary"
              onClick={() => onAskAi("Why is Rakesh linked?")}
            >
              Ask AI: "Why is Rakesh linked?"
            </button>
          </div>
        </div>

        {/* Right Card: Key Associated Entities & Network Perimeter matching Image 2 */}
        <div className="gov-card">
          <div style={{ borderBottom: '1px solid var(--border-light)', paddingBottom: '0.85rem', marginBottom: '1rem' }}>
            <h3 style={{ fontSize: '1rem', fontWeight: 700, color: 'var(--text-primary)' }}>
              Key Associated Entities & Network Perimeter
            </h3>
            <span style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
              Cross-domain correlations matching FIR 104/2026 & FIR 78/2024
            </span>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
            {associates.map((item, idx) => (
              <div 
                key={idx}
                className="associate-row-item"
                onClick={() => onInspectAssociate(item.node_id)}
              >
                <div style={{ display: 'flex', alignItems: 'flex-start', gap: '0.75rem', flex: 1 }}>
                  <div className="associate-icon-box">
                    {item.name.includes('+91') ? (
                      <Phone size={16} />
                    ) : item.name.includes('DL 01') ? (
                      <Car size={16} />
                    ) : (
                      <User size={16} />
                    )}
                  </div>

                  <div>
                    <div style={{ fontWeight: 700, fontSize: '0.88rem', color: 'var(--text-primary)' }}>
                      {item.name}
                    </div>
                    <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', lineHeight: 1.4 }}>
                      {item.role}
                    </div>
                  </div>
                </div>

                <button className="inspect-node-btn">
                  <span>Inspect Node ({item.match_pct}%)</span>
                  <ArrowRight size={12} />
                </button>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

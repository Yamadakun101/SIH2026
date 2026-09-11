import React from 'react';
import { 
  ShieldCheck, 
  Lock, 
  Award, 
  CheckCircle2,
  Percent
} from 'lucide-react';

export default function EvidenceTab({ caseData, onOpenCertificate }) {
  const ledger = caseData.evidence_ledger;
  const metadata = caseData.metadata;

  return (
    <div className="evidence-container">
      {/* Banner / Compliance Summary */}
      <div className="overview-banner" style={{ background: '#f8faff', borderColor: '#bfdbfe' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
            <div style={{ background: 'var(--gov-navy)', color: 'white', padding: '0.45rem', borderRadius: 'var(--radius-md)', display: 'flex' }}>
              <ShieldCheck size={22} />
            </div>
            <div>
              <h2 style={{ fontSize: '1.15rem', fontWeight: 700, color: 'var(--text-primary)' }}>
                Evidence Provenance Log & Bharatiya Sakshya Adhiniyam (BSA) 2023 Sec 63
              </h2>
              <div style={{ fontSize: '0.78rem', color: 'var(--text-secondary)' }}>
                Cryptographic Admissibility Audit & Multi-Source Evidence Correlation Percentages
              </div>
            </div>
          </div>

          <button 
            className="gov-btn-primary"
            onClick={onOpenCertificate}
            style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}
          >
            <Award size={16} />
            View Sec 63 Court Certificate
          </button>
        </div>

        <p style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', lineHeight: 1.5, marginTop: '0.5rem' }}>
          Every ingested digital record (FIR, Telecom Tower Triangulation Dumps, ANPR Plate Captures, NPCI IMPS Switch Logs) is assigned a cryptographic SHA-256 Merkle root hash at entry, alongside an algorithmic cross-domain correlation match percentage.
        </p>
      </div>

      {/* Immutable Custody Ledger Table */}
      <div className="ledger-table-card">
        <div style={{ padding: '1rem 1.25rem', borderBottom: '1px solid var(--border-light)', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <h3 style={{ fontSize: '0.95rem', fontWeight: 700, color: 'var(--text-primary)' }}>
            Digital Evidence Audit Trail ({ledger.length} Verified Ledger Blocks)
          </h3>
          <span style={{ fontSize: '0.75rem', color: 'var(--gov-navy)', fontWeight: 600 }}>
            Overall Case Correlation: {metadata.overall_match_rate}%
          </span>
        </div>

        <table className="ledger-table">
          <thead>
            <tr>
              <th>BLOCK #</th>
              <th>RECORD ID</th>
              <th>EVIDENCE CLASSIFICATION</th>
              <th>TIMESTAMP (IST)</th>
              <th>SHA-256 HASH STAMP</th>
              <th>MATCH PERCENTAGE</th>
            </tr>
          </thead>
          <tbody>
            {ledger.map((item) => (
              <tr key={item.block}>
                <td style={{ fontWeight: 700, color: 'var(--gov-navy)' }}>#{item.block}</td>
                <td style={{ fontWeight: 600 }}>{item.record_id}</td>
                <td>
                  <span className="gov-badge-subtle">
                    {item.type}
                  </span>
                </td>
                <td style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>{item.timestamp}</td>
                <td style={{ fontFamily: 'monospace', fontSize: '0.7rem', color: 'var(--text-secondary)' }}>
                  {item.sha256.substring(0, 16)}...{item.sha256.substring(item.sha256.length - 8)}
                </td>
                <td>
                  <span className="gov-badge-match">
                    {item.match_pct}% Match
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

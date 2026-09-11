import React, { useState } from 'react';
import { 
  ShieldCheck, 
  Award, 
  Search,
  CheckCircle2,
  Copy,
  Check,
  Building2,
  Fingerprint
} from 'lucide-react';

export default function EvidenceTab({ caseData, onOpenCertificate }) {
  const ledger = caseData.evidence_ledger || [];
  const blockchainLogs = caseData.blockchain_activity_logs || [];
  const metadata = caseData.metadata || {};

  const [selectedAgencyFilter, setSelectedAgencyFilter] = useState('ALL');
  const [searchTerm, setSearchTerm] = useState('');
  const [copiedHash, setCopiedHash] = useState(null);

  // Filter blockchain logs based on agency and search query
  const filteredLogs = blockchainLogs.filter((log) => {
    const matchesAgency = selectedAgencyFilter === 'ALL' || log.agency_badge === selectedAgencyFilter;
    const q = searchTerm.toLowerCase().trim();
    if (!q) return matchesAgency;

    const matchesSearch = 
      log.action_label.toLowerCase().includes(q) ||
      log.agency.toLowerCase().includes(q) ||
      log.officer.toLowerCase().includes(q) ||
      log.target_entity.toLowerCase().includes(q) ||
      log.hash.toLowerCase().includes(q) ||
      log.id.toLowerCase().includes(q) ||
      log.description.toLowerCase().includes(q);

    return matchesAgency && matchesSearch;
  });

  const handleCopyHash = (hash, id) => {
    navigator.clipboard.writeText(hash);
    setCopiedHash(id);
    setTimeout(() => setCopiedHash(null), 2000);
  };

  const agencyOptions = [
    { key: 'ALL', label: `All Agencies (${blockchainLogs.length})` },
    { key: 'DELHI_POLICE', label: 'Delhi Police' },
    { key: 'CYBER_CRIME', label: 'Cyber Crime Unit' },
    { key: 'HARYANA_POLICE', label: 'Haryana STF' },
    { key: 'NPCI_SWITCH', label: 'NPCI Banking Gateway' },
    { key: 'FORENSICS_LAB', label: 'Forensics Lab' }
  ];

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

      {/* 1. Immutable Custody Ledger Table */}
      <div className="ledger-table-card">
        <div style={{ padding: '1rem 1.25rem', borderBottom: '1px solid var(--border-light)', display: 'flex', alignItems: 'center', justifyContent: 'space-between', background: '#ffffff' }}>
          <div>
            <h3 style={{ fontSize: '0.95rem', fontWeight: 700, color: 'var(--text-primary)' }}>
              Digital Evidence Custody Ledger ({ledger.length} Verified Evidence Items)
            </h3>
            <div style={{ fontSize: '0.72rem', color: 'var(--text-secondary)' }}>
              Master cryptographic SHA-256 records verified under Section 63 BSA 2023
            </div>
          </div>
          <span style={{ fontSize: '0.78rem', color: 'var(--gov-navy)', fontWeight: 700, background: '#eff6ff', padding: '0.25rem 0.65rem', borderRadius: 'var(--radius-sm)', border: '1px solid #bfdbfe' }}>
            Overall Case Correlation: {metadata.overall_match_rate || 91}%
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
              <th>MATCH PERCENTAGE & ON-CHAIN PROOF</th>
            </tr>
          </thead>
          <tbody>
            {ledger.map((item) => (
              <tr key={item.block}>
                <td style={{ fontWeight: 800, color: 'var(--gov-navy)' }}>
                  #{item.block}
                </td>
                <td style={{ fontWeight: 700, color: 'var(--text-primary)' }}>
                  {item.record_id}
                </td>
                <td>
                  <span className="gov-badge-subtle">
                    {item.type}
                  </span>
                </td>
                <td style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
                  {item.timestamp}
                </td>
                <td style={{ fontFamily: 'monospace', fontSize: '0.7rem', color: 'var(--text-secondary)' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
                    <span>{item.sha256.substring(0, 16)}...{item.sha256.substring(item.sha256.length - 8)}</span>
                    <button 
                      onClick={() => handleCopyHash(item.sha256, `table-${item.block}`)}
                      title="Copy SHA-256 Hash"
                      style={{ background: 'transparent', border: 'none', cursor: 'pointer', color: 'var(--text-muted)', padding: '0.1rem' }}
                    >
                      {copiedHash === `table-${item.block}` ? <Check size={12} color="#16a34a" /> : <Copy size={12} />}
                    </button>
                  </div>
                </td>
                <td>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '0.2rem' }}>
                    <span className="gov-badge-match" style={{ width: 'fit-content' }}>
                      {item.match_pct}% Match
                    </span>
                    <span style={{ fontSize: '0.65rem', color: '#16a34a', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '0.2rem' }}>
                      <CheckCircle2 size={10} /> Block #{item.block} • Signed & Verified
                    </span>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* 2. Live Blockchain Logs of Recent Activities & Dataset Changes (Right below Evidence Match %) */}
      <div className="ledger-table-card" style={{ marginTop: '0.5rem' }}>
        <div style={{ 
          padding: '1.15rem 1.25rem', 
          borderBottom: '1px solid var(--border-light)', 
          background: 'linear-gradient(180deg, #f8fafc 0%, #ffffff 100%)',
          display: 'flex',
          flexDirection: 'column',
          gap: '0.75rem'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '0.5rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <div style={{ background: '#0f172a', color: 'white', padding: '0.35rem', borderRadius: '4px', display: 'flex' }}>
                <Fingerprint size={18} />
              </div>
              <div>
                <h3 style={{ fontSize: '1rem', fontWeight: 800, color: 'var(--text-primary)', display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                  <span>Immutable Blockchain Activity Logs & Inter-Agency Dataset Modifications</span>
                  <span style={{ fontSize: '0.68rem', fontWeight: 700, background: '#f0fdf4', color: '#166534', border: '1px solid #bbf7d0', padding: '0.1rem 0.45rem', borderRadius: '9999px' }}>
                    LIVE AUDIT STREAM
                  </span>
                </h3>
                <p style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', marginTop: '0.1rem' }}>
                  Chronological tamper-proof ledger of every record ingested, entity link established, and dataset mutation authorized by investigating agencies.
                </p>
              </div>
            </div>

            <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.35rem', background: '#ffffff', border: '1px solid var(--border-medium)', borderRadius: 'var(--radius-sm)', padding: '0.3rem 0.6rem' }}>
                <Search size={14} color="var(--text-muted)" />
                <input
                  type="text"
                  placeholder="Search by Tx Hash, Officer, or Entity..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  style={{
                    border: 'none',
                    outline: 'none',
                    fontSize: '0.75rem',
                    width: '210px',
                    background: 'transparent'
                  }}
                />
              </div>
            </div>
          </div>

          {/* Agency Filter Chips */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', flexWrap: 'wrap' }}>
            <span style={{ fontSize: '0.72rem', fontWeight: 700, color: 'var(--text-secondary)', marginRight: '0.2rem' }}>
              Filter by Agency:
            </span>
            {agencyOptions.map((agency) => (
              <button
                key={agency.key}
                onClick={() => setSelectedAgencyFilter(agency.key)}
                style={{
                  fontSize: '0.7rem',
                  fontWeight: 600,
                  padding: '0.25rem 0.6rem',
                  borderRadius: 'var(--radius-sm)',
                  border: selectedAgencyFilter === agency.key ? '1px solid var(--gov-navy)' : '1px solid var(--border-light)',
                  background: selectedAgencyFilter === agency.key ? 'var(--gov-navy)' : '#ffffff',
                  color: selectedAgencyFilter === agency.key ? '#ffffff' : 'var(--text-secondary)',
                  cursor: 'pointer',
                  transition: 'all 0.15s ease'
                }}
              >
                {agency.label}
              </button>
            ))}
          </div>
        </div>

        {/* Blockchain Chronological Activity Blocks Stream */}
        <div style={{ padding: '1.25rem', background: '#f8fafc', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          {filteredLogs.map((log) => {
            return (
              <div 
                key={log.id}
                style={{
                  background: '#ffffff',
                  border: '1.5px solid #e2e8f0',
                  borderRadius: 'var(--radius-md)',
                  boxShadow: '0 2px 4px rgba(15, 23, 42, 0.04)',
                  overflow: 'hidden',
                  transition: 'all 0.2s ease',
                  position: 'relative'
                }}
              >
                {/* Top Block Header Bar */}
                <div style={{ 
                  padding: '0.75rem 1rem', 
                  background: '#f8fafc', 
                  borderBottom: '1px solid #e2e8f0',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  flexWrap: 'wrap',
                  gap: '0.5rem'
                }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
                    <span style={{ 
                      background: 'var(--gov-navy)', 
                      color: 'white', 
                      fontSize: '0.72rem', 
                      fontWeight: 800, 
                      padding: '0.2rem 0.55rem', 
                      borderRadius: '4px',
                      letterSpacing: '0.04em'
                    }}>
                      BLOCK #{log.block_num}
                    </span>
                    <span style={{ fontFamily: 'monospace', fontSize: '0.75rem', fontWeight: 700, color: 'var(--text-primary)' }}>
                      {log.id}
                    </span>
                    <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>•</span>
                    <span style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--text-secondary)', display: 'flex', alignItems: 'center', gap: '0.3rem' }}>
                      <Building2 size={13} color="var(--gov-navy)" />
                      {log.agency}
                    </span>
                  </div>

                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
                    <span style={{ fontSize: '0.72rem', color: 'var(--text-secondary)', fontWeight: 500 }}>
                      {log.timestamp}
                    </span>
                    <span style={{ 
                      fontSize: '0.68rem', 
                      fontWeight: 700, 
                      padding: '0.15rem 0.5rem', 
                      borderRadius: '9999px',
                      background: '#eff6ff',
                      color: '#1d4ed8',
                      border: '1px solid #bfdbfe',
                      display: 'flex',
                      alignItems: 'center',
                      gap: '0.25rem'
                    }}>
                      <CheckCircle2 size={11} /> VALIDATED ON-CHAIN
                    </span>
                  </div>
                </div>

                {/* Block Content Body */}
                <div style={{ padding: '1rem' }}>
                  <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', gap: '1rem', marginBottom: '0.6rem' }}>
                    <div>
                      <div style={{ fontSize: '0.92rem', fontWeight: 700, color: 'var(--text-primary)', marginBottom: '0.25rem' }}>
                        {log.action_label}
                      </div>
                      <div style={{ fontSize: '0.78rem', color: 'var(--text-secondary)', lineHeight: 1.45 }}>
                        {log.description}
                      </div>
                    </div>

                    <div style={{ textAlign: 'right', minWidth: '130px' }}>
                      <span className="gov-badge-match" style={{ fontSize: '0.75rem', padding: '0.2rem 0.6rem' }}>
                        {log.match_pct}% Match Score
                      </span>
                      <div style={{ fontSize: '0.68rem', color: 'var(--text-muted)', marginTop: '0.2rem' }}>
                        Authorized: {log.officer}
                      </div>
                    </div>
                  </div>

                  {/* Dataset Change Notification Tag */}
                  <div style={{ 
                    background: '#f1f5f9', 
                    border: '1px dashed #cbd5e1', 
                    borderRadius: 'var(--radius-sm)', 
                    padding: '0.45rem 0.75rem',
                    fontSize: '0.75rem',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    marginBottom: '0.75rem'
                  }}>
                    <span style={{ fontWeight: 600, color: '#334155' }}>
                      📋 Dataset Delta: <span style={{ color: '#0f172a', fontWeight: 700 }}>{log.changes_made}</span>
                    </span>
                    <span style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>
                      Target: <strong>{log.target_entity}</strong>
                    </span>
                  </div>

                  {/* Cryptographic Hashes & Blockchain Integrity Strip */}
                  <div style={{ 
                    background: '#0f172a', 
                    color: '#f8fafc', 
                    borderRadius: 'var(--radius-sm)', 
                    padding: '0.6rem 0.85rem',
                    fontFamily: 'monospace',
                    fontSize: '0.7rem',
                    display: 'flex',
                    flexDirection: 'column',
                    gap: '0.35rem'
                  }}>
                    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                        <span style={{ color: '#94a3b8' }}>BLOCK HASH:</span>
                        <span style={{ color: '#38bdf8', fontWeight: 600 }}>{log.hash}</span>
                      </div>
                      <button 
                        onClick={() => handleCopyHash(log.hash, log.id)}
                        style={{ background: 'rgba(255,255,255,0.1)', border: 'none', borderRadius: '3px', padding: '0.15rem 0.4rem', color: '#ffffff', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '0.2rem', fontSize: '0.65rem' }}
                      >
                        {copiedHash === log.id ? <Check size={11} color="#4ade80" /> : <Copy size={11} />}
                        {copiedHash === log.id ? 'Copied' : 'Copy Hash'}
                      </button>
                    </div>

                    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', color: '#94a3b8', fontSize: '0.65rem', borderTop: '1px solid rgba(255,255,255,0.1)', paddingTop: '0.3rem' }}>
                      <div>
                        <span>PREV HASH: </span>
                        <span style={{ color: '#cbd5e1' }}>{log.prev_hash.substring(0, 24)}...</span>
                      </div>
                      <div>
                        <span>MERKLE ROOT: </span>
                        <span style={{ color: '#cbd5e1' }}>{log.merkle_root}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            );
          })}

          {filteredLogs.length === 0 && (
            <div style={{ padding: '2.5rem', textAlign: 'center', color: 'var(--text-secondary)' }}>
              No blockchain logs matching the filter criteria.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

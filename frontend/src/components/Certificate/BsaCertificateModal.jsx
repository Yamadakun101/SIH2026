import React from 'react';
import { 
  X, 
  Printer, 
  ShieldCheck 
} from 'lucide-react';

export default function BsaCertificateModal({ caseData, onClose }) {
  if (!caseData) return null;

  const metadata = caseData.metadata;
  const ledger = caseData.evidence_ledger;

  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal-container" onClick={(e) => e.stopPropagation()}>
        {/* Top Control Bar */}
        <div style={{ padding: '0.85rem 1.25rem', borderBottom: '1px solid var(--border-light)', display: 'flex', alignItems: 'center', justifyContent: 'space-between', background: '#f8fafc' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', fontWeight: 700, fontSize: '0.9rem', color: 'var(--text-primary)' }}>
            <ShieldCheck size={18} color="var(--info-blue)" />
            <span>Digital Evidence Certificate Viewer</span>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <button className="header-btn" onClick={handlePrint}>
              <Printer size={15} />
              Print Certificate
            </button>
            <button className="header-btn" onClick={onClose}>
              <X size={15} />
            </button>
          </div>
        </div>

        {/* Certificate Paper */}
        <div className="certificate-paper">
          <div className="cert-header">
            <div className="cert-emblem">GOVERNMENT OF NATIONAL CAPITAL TERRITORY OF DELHI</div>
            <div style={{ fontSize: '0.9rem', fontWeight: 700, color: '#1e293b' }}>DELHI POLICE • CRIME BRANCH / SPECIAL CELL</div>
            <h1 className="cert-main-title">
              CERTIFICATE UNDER SECTION 63 OF THE BHARATIYA SAKSHYA ADHINIYAM (BSA), 2023
            </h1>
            <div className="cert-sub">
              (Admissibility of Electronic Records in Judicial Proceedings)
            </div>
          </div>

          <div className="cert-legal-text">
            <p style={{ marginBottom: '0.75rem' }}>
              I, the undersigned Investigating Officer / Cyber Forensic Analyst, hereby certify that the electronic records, knowledge graph extractions, and timeline events cataloged under Case ID <strong>{metadata.case_id}</strong> (FIR: <em>{metadata.fir_number}</em>) were produced by the automated computer system <strong>KavachNet</strong> during the ordinary course of investigative operations.
            </p>

            <p style={{ marginBottom: '0.75rem' }}>
              1. <strong>System Integrity:</strong> During the entire ingestion period, the computer output and network database operated securely without malfunction or tampering.
            </p>

            <p style={{ marginBottom: '0.75rem' }}>
              2. <strong>Cryptographic Chain of Custody:</strong> Every raw record (CDR, ANPR Toll feeds, and Banking API streams) was hashed at entry using the cryptographic algorithm <strong>SHA-256</strong>.
            </p>
          </div>

          {/* Merkle Stamp Box */}
          <div style={{ background: '#f8fafc', border: '1px solid #cbd5e1', borderRadius: '4px', padding: '0.85rem', marginBottom: '1.25rem' }}>
            <div style={{ fontSize: '0.75rem', fontWeight: 700, color: '#334155', marginBottom: '0.35rem' }}>
              IMMUTABLE MERKLE ROOT PROOF
            </div>
            <div style={{ fontFamily: 'monospace', fontSize: '0.72rem', wordBreak: 'break-all', color: '#0f172a', fontWeight: 600 }}>
              {metadata.merkle_root}
            </div>
            <div style={{ fontSize: '0.7rem', color: '#64748b', marginTop: '0.35rem' }}>
              Total Verified Evidence Blocks: {ledger.length} Records • Genesis Timestamp: {metadata.incident_date}
            </div>
          </div>

          {/* Signature Block */}
          <div className="cert-seal-row">
            <div className="cert-signature-box">
              <div style={{ height: '35px', display: 'flex', alignItems: 'center', justifyContent: 'center', fontStyle: 'italic', fontFamily: 'serif', fontSize: '1rem', color: '#1e3a8a' }}>
                DP-CYBER-SIGN-2026-9901
              </div>
              <div style={{ borderTop: '1px solid #94a3b8', paddingTop: '0.25rem', fontWeight: 600 }}>
                Certifying Cyber Forensics Officer
              </div>
              <div>Special Cell / Anti-Trafficking Unit</div>
            </div>

            <div style={{ textAlign: 'center' }}>
              <div style={{ width: '60px', height: '60px', borderRadius: '50%', border: '2px solid #2563eb', display: 'inline-flex', alignItems: 'center', justifyContent: 'center', color: '#2563eb', fontWeight: 800, fontSize: '0.65rem', textTransform: 'uppercase' }}>
                SEALED<br />BSA 2023
              </div>
            </div>

            <div className="cert-signature-box">
              <div style={{ height: '35px', display: 'flex', alignItems: 'center', justifyContent: 'center', fontStyle: 'italic', fontFamily: 'serif', fontSize: '1rem', color: '#1e3a8a' }}>
                DP-SI-4921 (Authorized)
              </div>
              <div style={{ borderTop: '1px solid #94a3b8', paddingTop: '0.25rem', fontWeight: 600 }}>
                Station House Officer / Investigating Officer
              </div>
              <div>PS Kashmere Gate, North District</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

# KavachNet — Development & Collaboration Rules

> **Team Norms, Quality Standards, and Legal Compliance**  
> Smart India Hackathon (SIH 2026) · Problem Statement #26189

---

## 1. Non-Negotiable Rules

1. **Synthetic Data Exclusively**:
   - Never use or ingest real personally identifiable information (PII). All names, phone numbers, vehicle registrations, and bank accounts must be synthetic.
2. **Strict Terminology Standard (Investigative Leads, Never Verdicts)**:
   - This platform surfaces leads for law enforcement, not courtroom verdicts.
   - Allowed: *"Investigative Lead"*, *"High Centrality Node"*, *"Suspected Conduit"*, *"Corroborated Association"*.
   - Prohibited: *"Guilty"*, *"Criminal Confirmed"*, *"Convicted"*.
3. **Evidence Integrity & Provenance**:
   - Every ingested piece of data must carry a SHA-256 hash and timestamp to comply with **Section 63 of Bharatiya Sakshya Adhiniyam (BSA) 2023**.
4. **API Contract Immutability**:
   - Never modify or break an endpoint in `docs/API_CONTRACT.md` without agreement across Sanjay, Shaswat, and Anish.
5. **Phase 1 Focus**:
   - Deliver a pristine, high-impact local prototype first. Do not introduce unnecessary infrastructure overhead (e.g. heavy cloud deployments) until the core demo story is solid.

---

## 2. Git Branching & Workflow

- `main`: Protected stable branch.
- `sanjay-core`: Sanjay's branch for AI algorithms, graph logic, and integration.
- `shaswat-frontend`: Shaswat's branch for React UI, maps, graph canvas, and user flows.
- `anish-backend`: Anish's branch for data generation, databases, and FastAPI services.

### Routine Sync Protocol:
Before starting work on your branch:
```bash
git checkout main
git pull
git checkout your-branch
git merge main
```

When ready to share work:
1. Push branch to GitHub.
2. Open a Pull Request into `main`.
3. Verify test runs and merge cleanly.

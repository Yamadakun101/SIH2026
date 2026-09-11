// API Client Service for KavachNet
// Connects to Anish's FastAPI backend at http://localhost:8000/api/v1
// Gracefully falls back to local synthetic datasets if backend is offline

import { CASE_PROTOTYPE_DATA, STATES_DATA, CASES_LIST } from '../data/casesData';

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

async function fetchWithFallback(endpoint, fallbackData) {
  try {
    const response = await fetch(`${BASE_URL}${endpoint}`, {
      headers: {
        'Accept': 'application/json',
      },
    });

    if (!response.ok) {
      console.warn(`[API] ${endpoint} returned status ${response.status}. Using local data.`);
      return fallbackData;
    }

    const data = await response.json();
    return data;
  } catch (err) {
    console.info(`[API] Live backend unavailable (${err.message}). Running in Standalone Demo Mode.`);
    return fallbackData;
  }
}

export const ApiService = {
  // 1. GET /states
  getStates: async () => {
    return fetchWithFallback('/states', STATES_DATA);
  },

  // 2. GET /cases?state=DL
  getCasesByState: async (stateCode = 'DL') => {
    return fetchWithFallback(`/cases?state=${stateCode}`, CASES_LIST[stateCode] || []);
  },

  // 3. GET /cases/{case_id}
  getCaseOverview: async (caseId = 'DL-2026-0412') => {
    return fetchWithFallback(`/cases/${caseId}`, CASE_PROTOTYPE_DATA);
  },

  // 4. GET /cases/{case_id}/graph
  getCaseGraph: async (caseId = 'DL-2026-0412') => {
    return fetchWithFallback(`/cases/${caseId}/graph`, CASE_PROTOTYPE_DATA.graph);
  },

  // 5. GET /cases/{case_id}/timeline
  getCaseTimeline: async (caseId = 'DL-2026-0412') => {
    return fetchWithFallback(`/cases/${caseId}/timeline`, CASE_PROTOTYPE_DATA.timeline);
  },

  // 6. GET /cases/{case_id}/entities/{entity_id}
  getEntityDetails: async (caseId = 'DL-2026-0412', entityId) => {
    const fallback = CASE_PROTOTYPE_DATA.graph.nodes.find(n => n.id === entityId);
    return fetchWithFallback(`/cases/${caseId}/entities/${entityId}`, fallback);
  },

  // 7. POST /cases/{case_id}/query
  queryAiAssistant: async (caseId = 'DL-2026-0412', queryText) => {
    try {
      const response = await fetch(`${BASE_URL}/cases/${caseId}/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: JSON.stringify({ query: queryText })
      });

      if (response.ok) {
        return await response.json();
      }
    } catch (err) {
      // Fallback handled in AiAssistant component
    }
    return null;
  },

  // 8. GET /cases/{case_id}/provenance/verify
  verifyProvenance: async (caseId = 'DL-2026-0412') => {
    return fetchWithFallback(`/cases/${caseId}/provenance/verify`, {
      case_id: caseId,
      status: 'VERIFIED_INTACT',
      bsa_section_63_compliant: true,
      total_evidence_blocks: CASE_PROTOTYPE_DATA.evidence_ledger.length,
      merkle_root: CASE_PROTOTYPE_DATA.metadata.merkle_root
    });
  }
};

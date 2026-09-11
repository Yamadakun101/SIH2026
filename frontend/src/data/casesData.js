// Exact Synthetic Dataset matching User Prototype Image 1 & Image 2
// Government standard investigation schema with match percentages

export const STATES_DATA = [
  {
    code: 'DL',
    name: 'Delhi NCR',
    casesCount: 4,
    highRiskCount: 2,
    activeMonitoring: 2,
    status: 'high-risk',
    lat: 28.6139,
    lng: 77.2090,
    elevation: 35,
    x: 42,
    y: 30
  },
  {
    code: 'KA',
    name: 'Karnataka',
    casesCount: 3,
    highRiskCount: 1,
    activeMonitoring: 2,
    status: 'medium-risk',
    lat: 15.3173,
    lng: 75.7139,
    elevation: 25,
    x: 38,
    y: 74
  },
  {
    code: 'MH',
    name: 'Maharashtra',
    casesCount: 7,
    highRiskCount: 1,
    activeMonitoring: 4,
    status: 'medium-risk',
    lat: 19.7515,
    lng: 75.7139,
    elevation: 28,
    x: 36,
    y: 58
  },
  {
    code: 'UP',
    name: 'Uttar Pradesh',
    casesCount: 6,
    highRiskCount: 2,
    activeMonitoring: 3,
    status: 'high-risk',
    lat: 26.8467,
    lng: 80.9462,
    elevation: 32,
    x: 52,
    y: 36
  },
  {
    code: 'WB',
    name: 'West Bengal',
    casesCount: 5,
    highRiskCount: 1,
    activeMonitoring: 3,
    status: 'medium-risk',
    lat: 22.9868,
    lng: 87.8550,
    elevation: 22,
    x: 72,
    y: 46
  },
  {
    code: 'PB',
    name: 'Punjab',
    casesCount: 3,
    highRiskCount: 1,
    activeMonitoring: 1,
    status: 'low-risk',
    lat: 31.1471,
    lng: 75.3412,
    elevation: 20,
    x: 36,
    y: 22
  },
  {
    code: 'GJ',
    name: 'Gujarat',
    casesCount: 2,
    highRiskCount: 0,
    activeMonitoring: 2,
    status: 'low-risk',
    lat: 22.2587,
    lng: 71.1924,
    elevation: 18,
    x: 24,
    y: 48
  },
  {
    code: 'TN',
    name: 'Tamil Nadu',
    casesCount: 4,
    highRiskCount: 0,
    activeMonitoring: 3,
    status: 'resolved',
    lat: 11.1271,
    lng: 78.6569,
    elevation: 22,
    x: 44,
    y: 84
  }
];

export const CASES_LIST = {
  DL: [
    {
      id: 'DL-2026-0412',
      title: 'Missing Woman — Suspected Trafficking Network',
      fir: 'FIR 104/2026 PS Maurice Nagar',
      date: '02 Sep 2026',
      agency: 'Crime Branch / Special Cell, Delhi Police',
      status: 'ACTIVE_INVESTIGATION',
      importance: 'HIGH',
      importanceLabel: 'High Importance / Critical',
      importanceColor: '#dc2626',
      risk: 'HIGH',
      summary: 'Victim Pooja Sharma disappeared near North Campus DU. CCTV and ANPR correlation tracks transit vehicle DL 01 AX 4492 towards Singhu/Murthal and Kundli safehouse.',
      entitiesCount: 17,
      evidenceCount: 84,
      matchRate: '94.2%'
    },
    {
      id: 'DL-2026-0309',
      title: 'Cyber Financial Syndicate — Mule Account Ring',
      fir: 'FIR 78/2024 PS Civil Lines',
      date: '28 Aug 2026',
      agency: 'Cyber Crime Unit, Delhi Police',
      status: 'MONITORING',
      importance: 'MEDIUM',
      importanceLabel: 'Medium Importance',
      importanceColor: '#d97706',
      risk: 'MEDIUM',
      summary: 'Rapid UPI layering across mule accounts originating from Karol Bagh & Civil Lines accounts.',
      entitiesCount: 14,
      evidenceCount: 49,
      matchRate: '88.5%'
    }
  ],
  UP: [
    {
      id: 'UP-2026-1102',
      title: 'Inter-State Illegal Arms & Smuggling Syndicate',
      fir: 'FIR 214/2026 PS Cantt Varanasi',
      date: '29 Aug 2026',
      agency: 'STF, Uttar Pradesh Police',
      status: 'ACTIVE_INVESTIGATION',
      importance: 'HIGH',
      importanceLabel: 'High Importance / Critical',
      importanceColor: '#dc2626',
      risk: 'HIGH',
      summary: 'Interception of arms supply chain along National Highway 19 with encrypted communication links to border distributors.',
      entitiesCount: 22,
      evidenceCount: 104,
      matchRate: '96.4%'
    },
    {
      id: 'UP-2026-0945',
      title: 'Land Record Forgery & Revenue Document Alteration',
      fir: 'FIR 145/2026 PS Gomti Nagar Lucknow',
      date: '15 Aug 2026',
      agency: 'EOW, Uttar Pradesh Police',
      status: 'MONITORING',
      importance: 'MEDIUM',
      importanceLabel: 'Medium Importance',
      importanceColor: '#d97706',
      risk: 'MEDIUM',
      summary: 'Synthetic mutation documents created to usurp commercial parcels in Lucknow development area.',
      entitiesCount: 9,
      evidenceCount: 38,
      matchRate: '85.2%'
    }
  ],
  MH: [
    {
      id: 'MH-2026-0881',
      title: 'Organized Hawala Network & Multi-City Layering',
      fir: 'FIR 402/2026 PS Azad Maidan Mumbai',
      date: '01 Sep 2026',
      agency: 'Crime Branch Mumbai / ED Liaison',
      status: 'ACTIVE_INVESTIGATION',
      importance: 'HIGH',
      importanceLabel: 'High Importance / Critical',
      importanceColor: '#dc2626',
      risk: 'HIGH',
      summary: 'Cross-border illicit remittance pipeline mapped through diamond bourses and crypto liquidity pools.',
      entitiesCount: 28,
      evidenceCount: 130,
      matchRate: '95.8%'
    }
  ],
  PB: [
    {
      id: 'PB-2026-0519',
      title: 'Cross-Border Drone Contraband Transit Network',
      fir: 'FIR 88/2026 PS Sadar Amritsar',
      date: '26 Aug 2026',
      agency: 'SSOC, Punjab Police',
      status: 'ACTIVE_INVESTIGATION',
      importance: 'HIGH',
      importanceLabel: 'High Importance / Critical',
      importanceColor: '#dc2626',
      risk: 'HIGH',
      summary: 'Automated waypoint drone payloads intercepted near border villages with geo-fence coordinate correlation.',
      entitiesCount: 15,
      evidenceCount: 72,
      matchRate: '93.1%'
    }
  ],
  RJ: [
    {
      id: 'RJ-2026-0440',
      title: 'Impersonation & Fake Government Recruitment Scam',
      fir: 'FIR 182/2026 PS Vidhyadhar Nagar Jaipur',
      date: '19 Aug 2026',
      agency: 'SOG, Rajasthan Police',
      status: 'UNDER_INQUIRY',
      importance: 'MEDIUM',
      importanceLabel: 'Medium Importance',
      importanceColor: '#d97706',
      risk: 'MEDIUM',
      summary: 'Fraudulent examination portals issuing bogus appointment orders for state administrative positions.',
      entitiesCount: 11,
      evidenceCount: 52,
      matchRate: '87.3%'
    }
  ],
  WB: [
    {
      id: 'WB-2026-0612',
      title: 'Counterfeit Note Circulation & Printing Nexus',
      fir: 'FIR 99/2026 PS Malda Town',
      date: '14 Aug 2026',
      agency: 'CID, West Bengal Police',
      status: 'MONITORING',
      importance: 'MEDIUM',
      importanceLabel: 'Medium Importance',
      importanceColor: '#d97706',
      risk: 'MEDIUM',
      summary: 'High-quality synthetic paper currency distribution tracked through border market hubs.',
      entitiesCount: 13,
      evidenceCount: 46,
      matchRate: '89.0%'
    }
  ],
  HR: [
    {
      id: 'HR-2026-0721',
      title: 'Chassis Number Tampering & Luxury Car Racket',
      fir: 'FIR 310/2026 PS DLF Phase 2 Gurugram',
      date: '22 Aug 2026',
      agency: 'Crime Branch Gurugram, Haryana Police',
      status: 'UNDER_INQUIRY',
      importance: 'MEDIUM',
      importanceLabel: 'Medium Importance',
      importanceColor: '#d97706',
      risk: 'MEDIUM',
      summary: 'Re-registration of total-loss vehicles using duplicate forged engine embossings.',
      entitiesCount: 10,
      evidenceCount: 39,
      matchRate: '86.7%'
    }
  ],
  GJ: [
    {
      id: 'GJ-2026-0210',
      title: 'Routine Port Container Clearance Audit',
      fir: 'Verification 45/2026 PS Mundra Port',
      date: '10 Aug 2026',
      agency: 'Marine Police & Port Security',
      status: 'ROUTINE_CHECK',
      importance: 'LOW',
      importanceLabel: 'Low Importance / Minor',
      importanceColor: '#16a34a',
      risk: 'LOW',
      summary: 'Discrepancy in manifest weights resolved as logistical labeling mismatch without contraband findings.',
      entitiesCount: 5,
      evidenceCount: 18,
      matchRate: '76.0%'
    }
  ],
  OR: [
    {
      id: 'OR-2026-0118',
      title: 'Local Commercial Trademark Dispute',
      fir: 'Complaint 22/2026 PS Saheed Nagar Bhubaneswar',
      date: '05 Aug 2026',
      agency: 'Bhubaneswar Commissionerate',
      status: 'ROUTINE_CHECK',
      importance: 'LOW',
      importanceLabel: 'Low Importance / Minor',
      importanceColor: '#16a34a',
      risk: 'LOW',
      summary: 'Minor packaging copyright dispute between retail hardware distributors.',
      entitiesCount: 4,
      evidenceCount: 12,
      matchRate: '72.5%'
    }
  ],
  KA: [
    {
      id: 'KA-2026-0091',
      title: 'SIM Box Gateway & Cross-Border Routing',
      fir: 'FIR 91/2026 PS Cyber Crime Bengaluru',
      date: '12 Aug 2026',
      agency: 'CID Cyber Unit, Karnataka Police',
      status: 'CLOSED_CHARGESHEETED',
      importance: 'CLOSED',
      importanceLabel: 'Closed Case / Chargesheeted',
      importanceColor: '#2563eb',
      risk: 'CLOSED',
      summary: 'Illegal telecom VoIP exchange dismantled following synthetic packet inspection and CDR triangulation. Final chargesheet filed in Special Court.',
      entitiesCount: 12,
      evidenceCount: 41,
      matchRate: '91.0%'
    }
  ],
  TN: [
    {
      id: 'TN-2026-0054',
      title: 'Spurious Drug Manufacturing & Counterfeit Labeling',
      fir: 'FIR 54/2026 PS Teynampet Chennai',
      date: '28 Jul 2026',
      agency: 'CB-CID, Tamil Nadu Police',
      status: 'RESOLVED_CONVICTION',
      importance: 'CLOSED',
      importanceLabel: 'Closed Case / Resolved',
      importanceColor: '#2563eb',
      risk: 'CLOSED',
      summary: 'Illicit formulation unit seized in industrial estate. All 4 main accused chargesheeted and convicted.',
      entitiesCount: 16,
      evidenceCount: 65,
      matchRate: '97.2%'
    }
  ]
};

// Exact nodes and connections matching Image 1
export const CASE_PROTOTYPE_DATA = {
  metadata: {
    case_id: 'DL-2026-0412',
    title: 'Missing Woman — Suspected Trafficking Network',
    state_code: 'DL',
    state_name: 'Delhi NCR',
    incident_date: '02 Sep 2026, 22:30 IST',
    lead_agency: 'Special Cell / Crime Branch, Delhi Police',
    fir_number: 'FIR 104/2026 PS Maurice Nagar',
    status: 'ACTIVE_INVESTIGATION',
    priority: 'HIGH',
    summary: 'Investigation tracking victim Pooja Sharma, transit vehicle DL 01 AX 4492, connected bank accounts, and primary person of interest Rakesh Kumar.',
    overall_match_rate: 91,
    primary_subject: {
      initials: 'RK',
      name: 'Rakesh Kumar',
      age: 34,
      location: 'North Delhi',
      status: 'Primary Network Entity',
      badge: 'PRIMARY INVESTIGATIVE LEAD',
      match_confidence: 91,
      summary: 'Multiple independent synthetic records connect this person to phone numbers, vehicles, financial accounts, locations and previous case records. Cross-domain correlation establishes co-location during the victim\'s disappearance window.',
      metrics: {
        phones: '2 CDR records',
        vehicles: '1 White Sedan',
        banking: '₹50,000 IMPS',
        locations: '3 Overlaps',
        prior_fir: '1 (PS Civil Lines)',
        cctv: '2 Confirmed'
      }
    },
    key_associates: [
      {
        name: "Vikram 'Vicky' Sharma",
        role: "Logistics Coordinator • 14 CDR calls, co-accused in historical FIR 78/2024",
        node_id: 'person-vikram',
        match_pct: 84
      },
      {
        name: 'Sunil Mehta',
        role: 'Driver / Transport Custodian • Owner of Swift Dzire DL 01 AX 4492, received ₹50k IMPS',
        node_id: 'person-sunil',
        match_pct: 78
      },
      {
        name: '+91 98765 43210',
        role: 'Primary Mobile Handset • Active during Kashmere Gate transit window',
        node_id: 'phone-rakesh-primary',
        match_pct: 94
      },
      {
        name: 'DL 01 AX 4492 (White Sedan)',
        role: 'Transit Vehicle • Optical CCTV match & Murthal FASTag toll pass',
        node_id: 'vehicle-dl01-ax',
        match_pct: 92
      }
    ]
  },

  graph: {
    nodes: [
      // Top-Left Cluster (Victim & Transit Corridor)
      {
        id: 'fir-104-maurice',
        label: 'FIR 104/2026 PS Maurice Nagar',
        type: 'FIR_CASE',
        match_pct: 100,
        sub_type: 'FIR / Case (100%)',
        group: 'legal',
        details: {
          police_station: 'PS Maurice Nagar',
          sections: 'BNS 2023 Sec 137(2), Sec 143',
          complainant: 'Family Missing Report'
        },
        evidence_correlation: '100% Case Origin Anchor'
      },
      {
        id: 'person-pooja',
        label: 'Pooja Sharma',
        type: 'PERSON',
        match_pct: 100,
        sub_type: 'Person (100%)',
        group: 'victim',
        details: {
          age: 21,
          status: 'Subject of Search (Victim)',
          last_seen: 'North Campus, Delhi University'
        },
        evidence_correlation: '100% Primary Complaint Correlation'
      },
      {
        id: 'loc-north-campus',
        label: 'North Campus, Delhi Univ',
        type: 'LOCATION',
        match_pct: 98,
        sub_type: 'Location (98%)',
        group: 'location',
        details: {
          area: 'Arts Faculty / Maurice Nagar Junction',
          tower_id: 'TOW-DU-CAMPUS-09'
        },
        evidence_correlation: '98% Cell Tower & Witness Match'
      },
      {
        id: 'cctv-du-exit',
        label: 'CCTV-DU-019 (Campus Exit)',
        type: 'CCTV_EVENT',
        match_pct: 94,
        sub_type: 'CCTV Event (94%)',
        group: 'surveillance',
        details: {
          camera_id: 'CAM-DU-019',
          timestamp: '02 Sep 2026, 21:18 IST',
          optical_match: '94% Frame Confidence'
        },
        evidence_correlation: '94% Optical Facial Recognition Match'
      },
      {
        id: 'vehicle-dl01-ax',
        label: 'DL 01 AX 4492',
        type: 'VEHICLE',
        match_pct: 92,
        sub_type: 'Vehicle (92%)',
        group: 'conveyance',
        details: {
          make: 'White Maruti Swift Sedan',
          registered_to: 'Sunil Mehta',
          fastag_id: 'FASTAG-DEL-4492'
        },
        evidence_correlation: '92% ANPR Toll & Video Feed Correlation'
      },
      {
        id: 'cctv-isbt-gate3',
        label: 'CCTV-KG-084 (ISBT Gate 3)',
        type: 'CCTV_EVENT',
        match_pct: 89,
        sub_type: 'CCTV Event (89%)',
        group: 'surveillance',
        details: {
          camera_id: 'CAM-ISBT-084',
          timestamp: '02 Sep 2026, 21:40 IST'
        },
        evidence_correlation: '89% Visual ANPR Vehicle Capture Match'
      },
      {
        id: 'vehicle-hr26-dq',
        label: 'HR 26 DQ 8810',
        type: 'VEHICLE',
        match_pct: 75,
        sub_type: 'Vehicle (75%)',
        group: 'conveyance',
        details: {
          make: 'Grey Hatchback',
          role: 'Convoy Escort Vehicle'
        },
        evidence_correlation: '75% Convoy Co-Travel Probability'
      },
      {
        id: 'loc-murthal-toll',
        label: 'NH-44 Murthal Toll Plaza',
        type: 'LOCATION',
        match_pct: 94,
        sub_type: 'Location (94%)',
        group: 'location',
        details: {
          highway: 'NH-44 Northbound Corridor',
          lane: 'Lane 02 Fastag Gateway'
        },
        evidence_correlation: '94% Automated Toll Timestamp Match'
      },
      {
        id: 'loc-safehouse-kundli',
        label: 'Safehouse Warehouse, Kundli',
        type: 'LOCATION',
        match_pct: 80,
        sub_type: 'Location (80%)',
        group: 'location',
        details: {
          area: 'Kundli Industrial Area Phase 2',
          role: 'Suspected Transit Staging Point'
        },
        evidence_correlation: '80% Geofence & GPS Trace Match'
      },
      {
        id: 'loc-kashmere-isbt',
        label: 'Kashmere Gate ISBT',
        type: 'LOCATION',
        match_pct: 92,
        sub_type: 'Location (92%)',
        group: 'location',
        details: {
          tower: 'TOW-DEL-KASHMERE-482',
          jurisdiction: 'North District'
        },
        evidence_correlation: '92% Multi-Device Triangulation Match'
      },

      // Middle-Right Cluster (Associates, Banking & Historical FIR)
      {
        id: 'person-sunil',
        label: 'Sunil Mehta',
        type: 'PERSON',
        match_pct: 78,
        sub_type: 'Person (78%)',
        group: 'associate',
        details: {
          role: 'Driver / Transport Custodian',
          vehicle: 'DL 01 AX 4492'
        },
        evidence_correlation: '78% VAHAN Registry & Bank IMPS Correlation'
      },
      {
        id: 'bank-icici',
        label: 'ICICI A/c ****8820',
        type: 'BANK_ACCOUNT',
        match_pct: 89,
        sub_type: 'Bank Account (89%)',
        group: 'financial',
        details: {
          holder: 'Sunil Mehta',
          branch: 'Model Town, Delhi'
        },
        evidence_correlation: '89% Banking Transaction Log Match'
      },
      {
        id: 'txn-upi-50k',
        label: 'TXN-UPI-88301 (₹50,000)',
        type: 'TRANSACTION',
        match_pct: 99,
        sub_type: 'Transaction (99%)',
        group: 'financial',
        details: {
          amount: '₹50,000 INR',
          timestamp: '02 Sep 2026, 17:15 IST',
          mode: 'UPI IMPS'
        },
        evidence_correlation: '99% NPCI Gateway Audit Match'
      },
      {
        id: 'bank-hdfc',
        label: 'HDFC A/c ****4491',
        type: 'BANK_ACCOUNT',
        match_pct: 96,
        sub_type: 'Bank Account (96%)',
        group: 'financial',
        details: {
          holder: 'R.K. Logistics / Vicky Sharma',
          branch: 'Civil Lines, Delhi'
        },
        evidence_correlation: '96% Direct Beneficiary Audit Match'
      },
      {
        id: 'person-vikram',
        label: "Vikram 'Vicky' Sharma",
        type: 'PERSON',
        match_pct: 84,
        sub_type: 'Person (84%)',
        group: 'associate',
        details: {
          role: 'Logistics Coordinator / Co-Accused',
          alias: 'Vicky'
        },
        evidence_correlation: '84% CDR Call Frequency & Prior FIR Match'
      },
      {
        id: 'fir-78-civil-lines',
        label: 'FIR 78/2024 PS Civil Lines',
        type: 'FIR_CASE',
        match_pct: 96,
        sub_type: 'FIR / Case (96%)',
        group: 'legal',
        details: {
          police_station: 'PS Civil Lines',
          case_type: 'Interstate Transport Fraud / Syndicate Syndicate'
        },
        evidence_correlation: '96% Historical Police CCTNS Record Match'
      },
      {
        id: 'person-rakesh',
        label: 'Rakesh Kumar',
        type: 'PERSON',
        match_pct: 91,
        sub_type: 'Person (91%)',
        group: 'central_entity',
        details: {
          age: 34,
          role: 'Primary Person of Interest',
          known_locations: ['North Delhi', 'Majnu Ka Tilla']
        },
        evidence_correlation: '91% Cross-Domain Graph Centrality Correlation'
      },
      {
        id: 'phone-rakesh-primary',
        label: '+91 98765 43210',
        type: 'PHONE',
        match_pct: 94,
        sub_type: 'Phone (94%)',
        group: 'telecom',
        details: {
          carrier: 'Vi Delhi',
          imei: '358912091823901'
        },
        evidence_correlation: '94% CDR Handset & Tower Sighting Match'
      },
      {
        id: 'phone-fir-linked',
        label: '+91 98710 99881',
        type: 'PHONE',
        match_pct: 88,
        sub_type: 'Phone (88%)',
        group: 'telecom',
        details: {
          carrier: 'Airtel Delhi',
          note: 'Recorded in historical FIR 78/2024'
        },
        evidence_correlation: '88% Historical Telecom Registry Match'
      },
      {
        id: 'phone-associate-contact',
        label: '+91 98112 33445',
        type: 'PHONE',
        match_pct: 82,
        sub_type: 'Phone (82%)',
        group: 'telecom',
        details: {
          carrier: 'Jio Delhi',
          calls_exchanged: '9 Calls'
        },
        evidence_correlation: '82% Direct CDR Interchange Match'
      }
    ],

    edges: [
      {
        id: 'e1',
        source: 'fir-104-maurice',
        target: 'person-pooja',
        label: 'MENTIONED_IN',
        match_pct: 100
      },
      {
        id: 'e2',
        source: 'person-pooja',
        target: 'loc-north-campus',
        label: 'LAST_SEEN_NEAR',
        match_pct: 98
      },
      {
        id: 'e3',
        source: 'person-pooja',
        target: 'cctv-du-exit',
        label: 'SEEN_AT',
        match_pct: 94
      },
      {
        id: 'e4',
        source: 'loc-north-campus',
        target: 'cctv-du-exit',
        label: 'CAPTURED_BY',
        match_pct: 94
      },
      {
        id: 'e5',
        source: 'cctv-du-exit',
        target: 'vehicle-dl01-ax',
        label: 'CAPTURED_BY',
        match_pct: 92
      },
      {
        id: 'e6',
        source: 'vehicle-dl01-ax',
        target: 'cctv-isbt-gate3',
        label: 'CAPTURED_BY',
        match_pct: 89
      },
      {
        id: 'e7',
        source: 'vehicle-dl01-ax',
        target: 'loc-safehouse-kundli',
        label: 'DESTINATION',
        match_pct: 80
      },
      {
        id: 'e8',
        source: 'vehicle-dl01-ax',
        target: 'loc-kashmere-isbt',
        label: 'SEEN_AT',
        match_pct: 92
      },
      {
        id: 'e9',
        source: 'vehicle-dl01-ax',
        target: 'vehicle-hr26-dq',
        label: 'SEEN_CONVOY_WITH',
        match_pct: 75
      },
      {
        id: 'e10',
        source: 'vehicle-hr26-dq',
        target: 'loc-murthal-toll',
        label: 'TRANSITED',
        match_pct: 94
      },
      {
        id: 'e11',
        source: 'vehicle-dl01-ax',
        target: 'person-sunil',
        label: 'OWNS',
        match_pct: 92
      },
      {
        id: 'e12',
        source: 'person-sunil',
        target: 'bank-icici',
        label: 'OWNS',
        match_pct: 89
      },
      {
        id: 'e13',
        source: 'person-sunil',
        target: 'person-vikram',
        label: 'ASSOCIATED_WITH',
        match_pct: 78
      },
      {
        id: 'e14',
        source: 'bank-icici',
        target: 'txn-upi-50k',
        label: 'CREDITED_TO',
        match_pct: 99
      },
      {
        id: 'e15',
        source: 'txn-upi-50k',
        target: 'bank-hdfc',
        label: 'DEBITED_FROM',
        match_pct: 99
      },
      {
        id: 'e16',
        source: 'person-vikram',
        target: 'bank-hdfc',
        label: 'USES',
        match_pct: 96
      },
      {
        id: 'e17',
        source: 'person-vikram',
        target: 'fir-78-civil-lines',
        label: 'MENTIONED_IN',
        match_pct: 96
      },
      {
        id: 'e18',
        source: 'person-rakesh',
        target: 'fir-78-civil-lines',
        label: 'MENTIONED_IN',
        match_pct: 96
      },
      {
        id: 'e19',
        source: 'person-rakesh',
        target: 'person-vikram',
        label: 'ASSOCIATED_WITH',
        match_pct: 88
      },
      {
        id: 'e20',
        source: 'person-rakesh',
        target: 'loc-kashmere-isbt',
        label: 'SEEN_AT',
        match_pct: 92
      },
      {
        id: 'e21',
        source: 'person-rakesh',
        target: 'phone-rakesh-primary',
        label: 'USES',
        match_pct: 94
      },
      {
        id: 'e22',
        source: 'fir-78-civil-lines',
        target: 'phone-fir-linked',
        label: 'USES',
        match_pct: 88
      },
      {
        id: 'e23',
        source: 'phone-rakesh-primary',
        target: 'phone-associate-contact',
        label: 'CALLED',
        match_pct: 82
      },
      {
        id: 'e24',
        source: 'phone-fir-linked',
        target: 'phone-rakesh-primary',
        label: 'CALLED',
        match_pct: 88
      }
    ]
  },

  timeline: [
    {
      id: 't1',
      time: '17:15 IST',
      date: '02 Sep 2026',
      title: '₹50,000 IMPS Transfer from HDFC to ICICI Mule Account',
      category: 'FINANCIAL',
      match_pct: 99,
      location: 'Civil Lines Banking Gateway',
      source: 'NPCI IMPS Switch Log #88301',
      description: '₹50,000 transferred from account linked to Vicky Sharma to Sunil Mehta.'
    },
    {
      id: 't2',
      time: '21:18 IST',
      date: '02 Sep 2026',
      title: 'Pooja Sharma Sighted at DU North Campus Exit',
      category: 'SURVEILLANCE',
      match_pct: 94,
      location: 'Arts Faculty Junction, North Campus',
      source: 'CCTV Feed CAM-DU-019',
      description: 'Victim recorded walking past campus exit camera wearing light attire.'
    },
    {
      id: 't3',
      time: '21:30 IST',
      date: '02 Sep 2026',
      title: 'Vehicle DL 01 AX 4492 Sighted Near Kashmere Gate',
      category: 'CONVEYANCE',
      match_pct: 92,
      location: 'ISBT Kashmere Gate Corridor',
      source: 'ANPR Feed CAM-ISBT-084',
      description: 'White Swift Sedan captured on camera heading towards ISBT transit area.'
    },
    {
      id: 't4',
      time: '21:45 IST',
      date: '02 Sep 2026',
      title: 'Phone +91 98765 43210 Cell Tower Activity at ISBT',
      category: 'TELECOM',
      match_pct: 94,
      location: 'ISBT Kashmere Gate Tower #482',
      source: 'CDR Tower Triangulation Dump',
      description: 'Device linked to Rakesh Kumar connected to tower sector during vehicle transit window.'
    },
    {
      id: 't5',
      time: '22:15 IST',
      date: '02 Sep 2026',
      title: 'Convoy Vehicles Pass NH-44 Murthal Toll Plaza',
      category: 'CONVEYANCE',
      match_pct: 94,
      location: 'NH-44 Toll Plaza Lane 2',
      source: 'FASTag Transaction FASTAG-DEL-4492',
      description: 'Vehicles DL 01 AX 4492 and escort HR 26 DQ 8810 recorded crossing toll northbound.'
    }
  ],

  evidence_ledger: [
    {
      block: 1,
      record_id: 'FIR-104-MAURICE-2026',
      type: 'FIRST_INFORMATION_REPORT',
      timestamp: '02 Sep 2026, 23:05 IST',
      match_pct: 100,
      sha256: '4b227777d4dd1fc61c6f884f48641d02b4d121d3fd328cb08b5531fcacdabf8a',
      status: '99.9% Authenticated'
    },
    {
      block: 2,
      record_id: 'CCTV-DU-019-OPTICAL',
      type: 'SURVEILLANCE_OPTICAL_FEED',
      timestamp: '02 Sep 2026, 23:14 IST',
      match_pct: 94,
      sha256: 'a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e',
      status: '94.0% Evidence Correlation'
    },
    {
      block: 3,
      record_id: 'ANPR-MURTHAL-FASTAG-TX',
      type: 'TOLL_ANPR_GATEWAY',
      timestamp: '02 Sep 2026, 23:28 IST',
      match_pct: 94,
      sha256: 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
      status: '94.2% Evidence Correlation'
    },
    {
      block: 4,
      record_id: 'NPCI-UPI-88301-AUDIT',
      type: 'BANKING_API_IMPS',
      timestamp: '02 Sep 2026, 23:40 IST',
      match_pct: 99,
      sha256: '8f4e2c1b9a8d7e6f5c4b3a210987654321fedcba0987654321abcdef01234567',
      status: '99.1% Cryptographic Match'
    }
  ]
};

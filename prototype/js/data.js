/**
 * CRIMENET-AI — SIH 2026 PROTOTYPE
 * Synthetic Local Knowledge Base & Investigation Dataset
 * NOTE: All data herein is strictly fabricated and synthetic for demonstration purposes.
 */

const SYNTHETIC_DATA = {
  // 1. National Cases
  cases: [
    {
      id: "DL-2026-0412",
      title: "Missing Woman — Suspected Trafficking Network",
      stateCode: "DL",
      stateName: "Delhi NCR",
      location: "North Campus / Kashmere Gate, Delhi",
      date: "12 Aug 2026",
      status: "Investigation Ongoing",
      risk: "high",
      summary: "Investigation into the sudden disappearance of a 22-year-old student from North Campus. Multi-source synthetic records connect suspicious CDR logs, unregistered sedan sightings, rapid digital IMPS banking transfers, and cross-state transit.",
      officer: "Insp. A. Verma",
      metrics: {
        entitiesCount: 18,
        linksCount: 22,
        primarySubject: "Rakesh Kumar",
        confidence: "91%"
      }
    },
    {
      id: "MH-2026-0189",
      title: "Financial Smurfing & Shell Company Nexus",
      stateCode: "MH",
      stateName: "Maharashtra",
      location: "Bandra-Kurla Complex, Mumbai",
      date: "04 Aug 2026",
      status: "Under Monitoring",
      risk: "medium",
      summary: "High-frequency multi-layered micro-deposits across 14 dummy current accounts flagged by synthetic FIU switch logs.",
      officer: "Insp. S. Kulkarni",
      metrics: { entitiesCount: 12, linksCount: 15, primarySubject: "Alok Narang", confidence: "86%" }
    },
    {
      id: "WB-2026-0304",
      title: "Cross-Border Document Forgery Ring",
      stateCode: "WB",
      stateName: "West Bengal",
      location: "Petrapole / Bongaon, West Bengal",
      date: "28 Jul 2026",
      status: "Investigation Ongoing",
      risk: "high",
      summary: "Cloned biometric cards and counterfeit travel visas identified through synchronized border checkpoint logs.",
      officer: "Insp. D. Banerjee",
      metrics: { entitiesCount: 14, linksCount: 18, primarySubject: "B. Roy", confidence: "89%" }
    },
    {
      id: "KA-2026-0091",
      title: "Cyber Extortion & SIM Box Gateway",
      stateCode: "KA",
      stateName: "Karnataka",
      location: "Electronic City, Bengaluru",
      date: "15 Jun 2026",
      status: "Closed / Chargesheeted",
      risk: "low",
      summary: "Illegal VoIP GSM gateway setup dismantled following synthetic telecom packet inspections and tower mapping.",
      officer: "Insp. R. Rao",
      metrics: { entitiesCount: 9, linksCount: 11, primarySubject: "M. Nambiar", confidence: "98%" }
    },
    {
      id: "PB-2026-0215",
      title: "Highway Cargo Diversion & Contraband",
      stateCode: "PB",
      stateName: "Punjab",
      location: "GT Road, Amritsar",
      date: "19 Jul 2026",
      status: "Under Monitoring",
      risk: "medium",
      summary: "Anomalous GPS transponder blackouts on freight trailers correlated with localized burner phone activations.",
      officer: "Insp. G. Singh",
      metrics: { entitiesCount: 11, linksCount: 13, primarySubject: "H. Dhillon", confidence: "82%" }
    },
    {
      id: "RJ-2026-0112",
      title: "Illicit Antiquities Smuggling Hub",
      stateCode: "RJ",
      stateName: "Rajasthan",
      location: "Amer Road, Jaipur",
      date: "02 May 2026",
      status: "Closed",
      risk: "low",
      summary: "Recovered stolen 12th-century terracotta idols traced through synthetic courier manifests and locker registries.",
      officer: "Insp. V. Rathore",
      metrics: { entitiesCount: 8, linksCount: 9, primarySubject: "K. Shekhawat", confidence: "95%" }
    },
    {
      id: "TS-2026-0402",
      title: "Synthetic Identity Theft & Loan Fraud",
      stateCode: "TS",
      stateName: "Telangana",
      location: "HITEC City, Hyderabad",
      date: "22 Aug 2026",
      status: "Under Monitoring",
      risk: "medium",
      summary: "Compromised Aadhaar/PAN synthetic composite profiles exploited for instant digital loan disbursements.",
      officer: "Insp. C. Reddy",
      metrics: { entitiesCount: 10, linksCount: 12, primarySubject: "T. Naidu", confidence: "87%" }
    },
    {
      id: "AS-2026-0177",
      title: "Timber Smuggling & Riverine Transit",
      stateCode: "AS",
      stateName: "Assam",
      location: "Brahmaputra Basin, Guwahati",
      date: "10 Aug 2026",
      status: "Investigation Ongoing",
      risk: "high",
      summary: "Illegal teak extraction syndicate operating via river barges using falsified forestry transit permits.",
      officer: "Insp. P. Saikia",
      metrics: { entitiesCount: 13, linksCount: 16, primarySubject: "A. Baruah", confidence: "88%" }
    }
  ],

  // 2. Primary Case Graph Data (DL-2026-0412)
  primaryCase: {
    id: "DL-2026-0412",
    nodes: [
      // Persons
      {
        id: "person-1",
        label: "Rakesh Kumar",
        type: "Person",
        category: "person",
        isCentral: true,
        risk: "high",
        confidence: 91,
        details: {
          role: "Possible Central Network Entity / Lead Subject",
          age: "34 years",
          residence: "Civil Lines / Azadpur, Delhi",
          status: "Under Active Surveillance",
          whyConnected: [
            "Subscriber of primary CDR number (+91 98765 43210)",
            "Initiated ₹50,000 IMPS transaction to courier account shortly before incident",
            "Mentioned as co-accused in historical FIR 78/2024",
            "Cell tower co-location with vehicle movements toward Kundli staging belt"
          ],
          dates: "12 Aug 2026 (16:30 - 23:45)",
          locations: "Civil Lines, Kashmere Gate ISBT, Kundli",
          source: "Multi-source Synthetic Fusion (CDR + NPCI + CCTNS)",
          aiExplanation: "Rakesh Kumar appears as the central operational node linking telecom coordination, financial disbursement to logistics drivers, and historical case associations. Co-location with victim's transit timeline indicates strong investigative relevance."
        }
      },
      {
        id: "person-2",
        label: "Vikram 'Vicky' Sharma",
        type: "Person",
        category: "person",
        risk: "high",
        confidence: 84,
        details: {
          role: "Logistics Coordinator / Key Associate",
          age: "38 years",
          residence: "Rohini Sector 7, Delhi",
          status: "Investigative Subject",
          whyConnected: [
            "High-frequency call exchange with Rakesh (14 calls in 48 hours)",
            "Common bail guarantor in historical CCTNS records",
            "Cell tower dump overlap near Civil Lines"
          ],
          dates: "12 Aug 2026, 16:30",
          locations: "Rohini, Civil Lines",
          source: "Telecom CDR & CCTNS Linked Index",
          aiExplanation: "Vicky Sharma acts as the inter-state logistics coordinator. Rapid call bursts occurred immediately prior to vehicle dispatch."
        }
      },
      {
        id: "person-3",
        label: "Sunil Mehta",
        type: "Person",
        category: "person",
        risk: "medium",
        confidence: 78,
        details: {
          role: "Driver / Vehicle Custodian",
          age: "29 years",
          residence: "Narela, Delhi",
          status: "Persons of Interest",
          whyConnected: [
            "Registered owner of White Swift Sedan (DL 01 AX 4492)",
            "Beneficiary of ₹50,000 IMPS transfer to ICICI account",
            "FastTag transponder linked to his mobile number"
          ],
          dates: "12 Aug 2026, 17:15 - 19:40",
          locations: "North Campus, Kashmere Gate, Murthal Toll",
          source: "VAHAN Registry & NPCI Banking Switch",
          aiExplanation: "Sunil Mehta operated the transport vehicle identified on highway CCTV cameras and received immediate pre-transit financial compensation."
        }
      },
      {
        id: "person-4",
        label: "Pooja Sharma",
        type: "Person",
        category: "person",
        risk: "high",
        confidence: 100,
        details: {
          role: "Victim / Missing Subject",
          age: "22 years",
          residence: "North Campus Hostel, Delhi Univ.",
          status: "Missing Person",
          whyConnected: [
            "Subject of FIR 104/2026 PS Maurice Nagar",
            "Last seen near Arts Faculty at 15:30 on 12 Aug 2026",
            "CCTV footage CCTV-DU-019 shows her boarding the suspect sedan"
          ],
          dates: "12 Aug 2026, 15:30 - 16:15",
          locations: "North Campus, Delhi",
          source: "FIR 104/2026 & CCTV-DU-019",
          aiExplanation: "Victim of sudden disappearance. Route tracking correlates exactly with the movement trajectory of vehicle DL 01 AX 4492."
        }
      },

      // Phones
      {
        id: "phone-1",
        label: "+91 98765 43210",
        type: "Phone",
        category: "phone",
        confidence: 94,
        details: {
          role: "Primary Mobile Line (Rakesh Kumar)",
          recordType: "CDR / Cell Tower Dump",
          associatedPerson: "Rakesh Kumar",
          whyConnected: [
            "Same subscriber KYC record",
            "Appears in 14 calls to associate Vicky Sharma",
            "Location overlap with Kashmere Gate cell tower at 18:20",
            "Call duration 142s to burner SIM at 18:20"
          ],
          dates: "12 Aug 2026 (16:00 - 22:00)",
          locations: "Civil Lines, Kashmere Gate Cell Tower 42-B",
          source: "Synthetic Telecom CDR Record CDR-00142",
          aiExplanation: "High-confidence anchor telecom node. Activity bursts directly correspond to milestone events in the abduction timeline."
        }
      },
      {
        id: "phone-2",
        label: "+91 98112 33445",
        type: "Phone",
        category: "phone",
        confidence: 82,
        details: {
          role: "Burner SIM / Transit Handset",
          recordType: "Prepaid CDR (Fictitious KYC)",
          associatedPerson: "Unidentified Transit Courier",
          whyConnected: [
            "Activated only 6 hours prior to the incident",
            "Received inbound coordination call from Rakesh at 18:20",
            "Co-located with vehicle transit along NH-44 highway corridor"
          ],
          dates: "12 Aug 2026, 18:20",
          locations: "NH-44 Highway Corridor",
          source: "Cell Tower Dump TD-DEL-9912",
          aiExplanation: "Temporary burner SIM utilized exclusively for in-transit communication and switched off post-Murthal toll crossing."
        }
      },
      {
        id: "phone-3",
        label: "+91 97110 99881",
        type: "Phone",
        category: "phone",
        confidence: 88,
        details: {
          role: "Associate Phone (Vicky Sharma)",
          recordType: "CDR Record",
          associatedPerson: "Vikram 'Vicky' Sharma",
          whyConnected: [
            "Subscribed to Vikram Sharma",
            "Frequent night-time calls prior to incident date",
            "Exchanged coordinates prior to vehicle pickup"
          ],
          dates: "10-12 Aug 2026",
          locations: "Rohini / Outer Delhi",
          source: "CDR Record CDR-00189",
          aiExplanation: "Used for upstream syndicate coordination and logistics scheduling."
        }
      },

      // Vehicles
      {
        id: "veh-1",
        label: "DL 01 AX 4492",
        type: "Vehicle",
        category: "vehicle",
        confidence: 92,
        details: {
          role: "White Swift Sedan (Suspect Transit Vehicle)",
          model: "Maruti Swift Dzire (White, 2022)",
          registeredOwner: "Sunil Mehta",
          whyConnected: [
            "Captured on CCTV-DU-019 at 16:15 outside Arts Faculty",
            "Identified on CCTV-KG-084 near Kashmere Gate at 18:42",
            "FastTag transaction logged at NH-44 Murthal Toll Plaza at 19:40"
          ],
          dates: "12 Aug 2026 (16:15 - 19:40)",
          locations: "North Campus → Kashmere Gate → NH-44 Murthal Toll",
          source: "VAHAN Registry & NETC FASTag Switch Log",
          aiExplanation: "Primary transport vehicle confirmed across 3 continuous physical checkpoint sensors across North Delhi into Haryana."
        }
      },
      {
        id: "veh-2",
        label: "HR 26 DQ 8810",
        type: "Vehicle",
        category: "vehicle",
        confidence: 75,
        details: {
          role: "Dark SUV (Shadow Escort Vehicle)",
          model: "Mahindra Scorpio (Black)",
          registeredOwner: "Commercial Fleet Leasing Ltd.",
          whyConnected: [
            "Spotted in convoy formation behind DL 01 AX 4492 near Kashmere Gate ISBT",
            "FastTag passed Murthal Toll 3 minutes after the white sedan"
          ],
          dates: "12 Aug 2026, 19:43",
          locations: "Kashmere Gate ISBT / Murthal",
          source: "NETC FASTag & NHAI Highway Surveillance",
          aiExplanation: "Secondary convoy vehicle likely providing inter-state escort."
        }
      },

      // Bank Accounts
      {
        id: "bank-1",
        label: "HDFC A/c ****4491",
        type: "Bank Account",
        category: "bank",
        confidence: 95,
        details: {
          role: "Source Operating Account",
          bankName: "HDFC Bank (Civil Lines Branch)",
          accountHolder: "Rakesh Kumar",
          whyConnected: [
            "Origin of ₹50,000 IMPS payout (TXN-UPI-88301) at 17:15",
            "Regular cash deposits followed by immediate IMPS transfers"
          ],
          dates: "12 Aug 2026, 17:15",
          locations: "Civil Lines, Delhi",
          source: "NPCI Banking Switch & FIU Suspicious Transaction Report",
          aiExplanation: "Acts as the operational disbursement account for network enablers."
        }
      },
      {
        id: "bank-2",
        label: "ICICI A/c ****8820",
        type: "Bank Account",
        category: "bank",
        confidence: 89,
        details: {
          role: "Receiver Account (Driver Logistics)",
          bankName: "ICICI Bank (Narela Branch)",
          accountHolder: "Sunil Mehta",
          whyConnected: [
            "Received ₹50,000 IMPS transfer minutes before highway transit commenced",
            "ATM withdrawal of ₹20,000 at Kundli border ATM at 20:30"
          ],
          dates: "12 Aug 2026, 17:15 - 20:30",
          locations: "Narela / Kundli",
          source: "NPCI IMPS Switch Log",
          aiExplanation: "Immediate financial incentive linked directly to execution of the transit leg."
        }
      },

      // Locations
      {
        id: "loc-1",
        label: "North Campus, Delhi Univ.",
        type: "Location",
        category: "location",
        confidence: 98,
        details: {
          role: "Point of Initial Incident / Disappearance",
          coordinates: "28.6900° N, 77.2085° E",
          whyConnected: [
            "Victim's last verified physical location at 15:30",
            "Sedan DL 01 AX 4492 entered university ring road at 15:45"
          ],
          dates: "12 Aug 2026, 15:30 - 16:15",
          locations: "Maurice Nagar / Mall Road",
          source: "Incident Report FIR 104/2026",
          aiExplanation: "Origin node of the investigation timeline."
        }
      },
      {
        id: "loc-2",
        label: "Kashmere Gate ISBT",
        type: "Location",
        category: "location",
        confidence: 92,
        details: {
          role: "Transit Hub & Rendezvous Point",
          coordinates: "28.6675° N, 77.2280° E",
          whyConnected: [
            "Rakesh Kumar's cell tower ping at 18:20",
            "CCTV sighting CCTV-KG-084 at 18:42",
            "Burner phone call termination point"
          ],
          dates: "12 Aug 2026, 18:20 - 18:50",
          locations: "ISBT Ring Road Junction",
          source: "Delhi Police Smart City Surveillance",
          aiExplanation: "Key staging area where convoy realignment and telephonic instructions occurred."
        }
      },
      {
        id: "loc-3",
        label: "NH-44 Murthal Toll Plaza",
        type: "Location",
        category: "location",
        confidence: 94,
        details: {
          role: "Inter-state Highway Checkpoint",
          coordinates: "29.0250° N, 77.0850° E",
          whyConnected: [
            "Automated FastTag read for sedan DL 01 AX 4492 at 19:40",
            "Escort vehicle HR 26 DQ 8810 passed at 19:43"
          ],
          dates: "12 Aug 2026, 19:40",
          locations: "Sonipat / Murthal Toll, Haryana",
          source: "NETC FASTag Gateway",
          aiExplanation: "Hard physical electronic verification of vehicle exiting Delhi jurisdiction into Haryana."
        }
      },
      {
        id: "loc-4",
        label: "Safehouse Warehouse, Kundli",
        type: "Location",
        category: "location",
        confidence: 80,
        details: {
          role: "Suspected Staging / Transfer Point",
          coordinates: "28.9800° N, 77.1200° E",
          whyConnected: [
            "Driver's ATM withdrawal at 20:30 nearby",
            "Tower dump shows handset ping cessation in this industrial cluster"
          ],
          dates: "12-13 Aug 2026",
          locations: "Kundli Industrial Area, Haryana",
          source: "Cell Tower Triangulation & ATM Log",
          aiExplanation: "Suspected secondary holding facility or inter-state transfer hub."
        }
      },

      // CCTV Events
      {
        id: "cctv-1",
        label: "CCTV-DU-019 (Campus Exit)",
        type: "CCTV Event",
        category: "cctv",
        confidence: 94,
        details: {
          role: "Direct Visual Sighting (Point of Contact)",
          cameraLocation: "North Campus Metro Exit Gate 2",
          timestamp: "12 Aug 2026, 16:15",
          whyConnected: [
            "High-resolution capture of White Sedan DL 01 AX 4492",
            "Subject Pooja Sharma seen entering vehicle rear door"
          ],
          dates: "12 Aug 2026, 16:15",
          locations: "Maurice Nagar, Delhi",
          source: "Delhi Metro DMRC CCTV Feed",
          aiExplanation: "Direct optical evidence establishing victim presence inside the suspect vehicle."
        }
      },
      {
        id: "cctv-2",
        label: "CCTV-KG-084 (ISBT Gate 3)",
        type: "CCTV Event",
        category: "cctv",
        confidence: 89,
        details: {
          role: "Transit Route Confirmation",
          cameraLocation: "Kashmere Gate ISBT Outer Ring Road Flyover",
          timestamp: "12 Aug 2026, 18:42",
          whyConnected: [
            "Vehicle DL 01 AX 4492 moving north at 58 km/h",
            "Escort vehicle visible 40m behind"
          ],
          dates: "12 Aug 2026, 18:42",
          locations: "Kashmere Gate, Delhi",
          source: "Delhi Traffic Police Integrated Command Center",
          aiExplanation: "Confirms vehicle trajectory heading toward GT Karnal Road / NH-44."
        }
      },

      // FIR / Case Records
      {
        id: "fir-1",
        label: "FIR 104/2026 PS Maurice Nagar",
        type: "FIR / Case",
        category: "fir",
        confidence: 100,
        details: {
          role: "Primary Complaint & Investigation Trigger",
          sections: "Sec 365, 370 BNS (Kidnapping / Trafficking)",
          complainant: "Hostel Warden / Family",
          whyConnected: [
            "Official missing person complaint filed at 19:00 on 12 Aug 2026",
            "Primary legal anchor for digital data warrants"
          ],
          dates: "12 Aug 2026",
          locations: "PS Maurice Nagar, Delhi",
          source: "CCTNS National Crime Records Portal",
          aiExplanation: "Foundational legal document initiating the cross-jurisdictional investigation."
        }
      },
      {
        id: "fir-2",
        label: "FIR 78/2024 PS Civil Lines",
        type: "FIR / Case",
        category: "fir",
        confidence: 96,
        details: {
          role: "Historical Modus Operandi Link",
          sections: "Sec 384, 120B IPC (Extortion & Criminal Conspiracy)",
          status: "Under Trial (Bail Granted)",
          whyConnected: [
            "Names Rakesh Kumar as primary conspirator",
            "Names Vikram Sharma as bail surety provider",
            "Identifies identical vehicle rental patterns"
          ],
          dates: "14 Mar 2024",
          locations: "PS Civil Lines, Delhi",
          source: "CCTNS Historical Repository",
          aiExplanation: "Crucial intelligence link proving pre-existing operational ties between Rakesh Kumar and Vikram Sharma."
        }
      },

      // Transactions
      {
        id: "txn-1",
        label: "TXN-UPI-88301 (₹50,000)",
        type: "Transaction",
        category: "txn",
        confidence: 99,
        details: {
          role: "Financial Coordination Payment",
          amount: "₹50,000 (Fifty Thousand INR)",
          method: "IMPS Banking Switch",
          timestamp: "12 Aug 2026, 17:15",
          whyConnected: [
            "Sender: Rakesh Kumar (HDFC ****4491)",
            "Receiver: Sunil Mehta (ICICI ****8820)",
            "Executed exactly 60 minutes after campus disappearance"
          ],
          dates: "12 Aug 2026, 17:15",
          locations: "Digital IMPS Network",
          source: "NPCI Central Switch Log",
          aiExplanation: "Temporal alignment between abduction event and driver financial payment confirms coordinated syndicate action."
        }
      }
    ],

    links: [
      { source: "person-1", target: "phone-1", label: "USES", confidence: "94%" },
      { source: "person-1", target: "person-2", label: "ASSOCIATED_WITH", confidence: "84%" },
      { source: "person-1", target: "bank-1", label: "OWNS", confidence: "95%" },
      { source: "person-1", target: "fir-2", label: "MENTIONED_IN", confidence: "96%" },
      { source: "person-1", target: "loc-2", label: "SEEN_AT", confidence: "87%" },

      { source: "person-2", target: "phone-3", label: "USES", confidence: "88%" },
      { source: "person-2", target: "person-3", label: "ASSOCIATED_WITH", confidence: "80%" },
      { source: "person-2", target: "fir-2", label: "MENTIONED_IN", confidence: "92%" },

      { source: "phone-1", target: "phone-3", label: "CALLED", confidence: "99%" },
      { source: "phone-1", target: "phone-2", label: "CALLED", confidence: "95%" },

      { source: "person-3", target: "veh-1", label: "OWNS", confidence: "98%" },
      { source: "person-3", target: "bank-2", label: "OWNS", confidence: "89%" },

      { source: "person-4", target: "fir-1", label: "MENTIONED_IN", confidence: "100%" },
      { source: "person-4", target: "loc-1", label: "LAST_SEEN_NEAR", confidence: "98%" },
      { source: "person-4", target: "cctv-1", label: "SEEN_AT", confidence: "94%" },

      { source: "veh-1", target: "loc-1", label: "SEEN_AT", confidence: "94%" },
      { source: "veh-1", target: "cctv-1", label: "CAPTURED_BY", confidence: "94%" },
      { source: "veh-1", target: "loc-2", label: "SEEN_AT", confidence: "89%" },
      { source: "veh-1", target: "cctv-2", label: "CAPTURED_BY", confidence: "89%" },
      { source: "veh-1", target: "loc-3", label: "TRANSITED", confidence: "94%" },
      { source: "veh-1", target: "loc-4", label: "DESTINATION_LEAD", confidence: "80%" },
      { source: "veh-1", target: "veh-2", label: "CONVOY_WITH", confidence: "75%" },

      { source: "bank-1", target: "txn-1", label: "DEBITED_FROM", confidence: "99%" },
      { source: "txn-1", target: "bank-2", label: "CREDITED_TO", confidence: "99%" }
    ]
  },

  // 3. Chronological Timeline Events
  timeline: [
    {
      time: "12 Aug, 15:30",
      category: "incident",
      title: "Initial Disappearance Reported",
      desc: "Victim Pooja Sharma reported missing from North Campus hostel area.",
      entityId: "person-4",
      source: "FIR 104/2026",
      tags: ["Incident", "High Priority"]
    },
    {
      time: "12 Aug, 16:15",
      category: "cctv",
      title: "CCTV Sighting at Metro Exit (CCTV-DU-019)",
      desc: "White Sedan DL 01 AX 4492 recorded near Arts Faculty. Victim seen entering rear passenger seat.",
      entityId: "cctv-1",
      source: "DMRC Optical Camera Feed",
      tags: ["CCTV", "Physical Link"]
    },
    {
      time: "12 Aug, 16:30",
      category: "telecom",
      title: "Logistics Coordination Activation",
      desc: "Vicky Sharma activates burner device in Rohini and contacts central associate.",
      entityId: "person-2",
      source: "CDR-00189",
      tags: ["Telecom", "Associate"]
    },
    {
      time: "12 Aug, 17:15",
      category: "financial",
      title: "₹50,000 IMPS Payout (TXN-UPI-88301)",
      desc: "Rakesh Kumar's HDFC account transfers ₹50,000 to driver Sunil Mehta's ICICI account.",
      entityId: "txn-1",
      source: "NPCI Switch Log",
      tags: ["Financial", "Immediate Payout"]
    },
    {
      time: "12 Aug, 18:20",
      category: "telecom",
      title: "Phone Call (142s Duration)",
      desc: "Rakesh (+91 98765 43210) connects with Burner (+91 98112 33445) while co-located at Kashmere Gate tower.",
      entityId: "phone-1",
      source: "CDR-00142",
      tags: ["Telecom", "Kashmere Gate"]
    },
    {
      time: "12 Aug, 18:42",
      category: "cctv",
      title: "CCTV Flyover Sighting (CCTV-KG-084)",
      desc: "Sedan DL 01 AX 4492 and escort SUV HR 26 DQ 8810 captured passing Kashmere Gate ISBT toward outer Ring Road.",
      entityId: "cctv-2",
      source: "Delhi Traffic Command",
      tags: ["CCTV", "Convoy Transit"]
    },
    {
      time: "12 Aug, 19:40",
      category: "transit",
      title: "FASTag Toll Crossing at Murthal",
      desc: "Vehicle DL 01 AX 4492 clears NH-44 Murthal Toll Plaza northbound lane 4 into Haryana.",
      entityId: "loc-3",
      source: "NETC FASTag Gateway",
      tags: ["Transit", "Inter-State"]
    },
    {
      time: "13 Aug, 02:10",
      category: "telecom",
      title: "Cell Tower Ping in Kundli Industrial Belt",
      desc: "Handset ping registered in Kundli sector before shutting down. Suspected staging safehouse area.",
      entityId: "loc-4",
      source: "Haryana Telecom Tower Dump",
      tags: ["Location", "Active Lead"]
    }
  ],

  // 4. Raw Ingested Evidence Logs
  evidenceLogs: [
    {
      id: "EV-CDR-00142",
      agency: "Department of Telecommunications / Telecom Gateway",
      timestamp: "12 Aug 2026, 18:20:14",
      entity: "Rakesh Kumar (+91 98765 43210)",
      metadata: "Call to +91 98112 33445 (142 sec). Tower ID: DEL-KG-042B.",
      confidence: "94%",
      entityId: "phone-1"
    },
    {
      id: "EV-NPCI-88301",
      agency: "NPCI National Financial Switch (IMPS)",
      timestamp: "12 Aug 2026, 17:15:33",
      entity: "HDFC ****4491 → ICICI ****8820",
      metadata: "Amount: ₹50,000. Narration: Logistics advance.",
      confidence: "99%",
      entityId: "txn-1"
    },
    {
      id: "EV-CCTV-DU-019",
      agency: "DMRC Integrated Optical Surveillance",
      timestamp: "12 Aug 2026, 16:15:02",
      entity: "White Sedan DL 01 AX 4492",
      metadata: "License plate OCR match: 96.2%. Passenger boarding detected.",
      confidence: "94%",
      entityId: "cctv-1"
    },
    {
      id: "EV-FASTAG-9910",
      agency: "IHMCL / NETC Toll Gateway",
      timestamp: "12 Aug 2026, 19:40:22",
      entity: "DL 01 AX 4492 (Toll: Murthal)",
      metadata: "Lane 04 Northbound. Tag EPC: E2003412019948.",
      confidence: "98%",
      entityId: "loc-3"
    },
    {
      id: "EV-VAHAN-4492",
      agency: "MoRTH VAHAN Central Registry",
      timestamp: "12 Aug 2026, 16:20:00",
      entity: "Maruti Dzire DL 01 AX 4492",
      metadata: "Registered Owner: Sunil Mehta. RTO: Delhi North (DL-01).",
      confidence: "98%",
      entityId: "veh-1"
    },
    {
      id: "EV-CCTNS-104",
      agency: "CCTNS National Crime Repository",
      timestamp: "12 Aug 2026, 19:00:00",
      entity: "FIR 104/2026 PS Maurice Nagar",
      metadata: "Sections: 365, 370 BNS. Status: Active Investigation.",
      confidence: "100%",
      entityId: "fir-1"
    }
  ],

  // 5. AI Assistant Rule & Knowledge Engine
  aiResponses: {
    "rakesh": "Rakesh Kumar is connected through three independent synthetic evidence paths: (1) his personal phone number (+91 98765 43210) appearing in the victim's proximity CDR dump, (2) an IMPS digital financial transfer of ₹50,000 to the driver shortly before departure, and (3) historical co-accused records with Vicky Sharma in FIR 78/2024. Overall association confidence: 91%. (Note: Investigative lead based on multi-source data correlation; does not constitute legal proof of guilt).",
    
    "phone": "The phone number +91 98765 43210 is linked because: (1) KYC registration matches Rakesh Kumar, (2) 14 calls were logged with logistics associate Vicky Sharma in 48 hours, and (3) a 142-second call was placed to a burner phone (+91 98112 33445) from the Kashmere Gate cell tower at 18:20 on 12 Aug 2026.",
    
    "disappearance": "Reconstruction of events prior to the disappearance:\n• 15:30 — Victim last seen near Arts Faculty, North Campus\n• 15:45 — White Sedan DL 01 AX 4492 enters university road\n• 16:15 — CCTV-DU-019 records victim entering vehicle\n• 16:30 — Associate Vicky Sharma activates burner line\n• 17:15 — ₹50,000 IMPS transaction executed to driver Sunil Mehta.",
    
    "strongest": "The strongest direct connection is the physical and optical confirmation of vehicle DL 01 AX 4492 (Confidence: 94%), which links directly from the point of disappearance (CCTV-DU-019 at 16:15) through Kashmere Gate (CCTV-KG-084 at 18:42) to the inter-state highway toll at Murthal (FASTag at 19:40). Registered owner Sunil Mehta received ₹50,000 from Rakesh Kumar at 17:15.",
    
    "people": "The local knowledge graph identifies 4 primary persons:\n1. Rakesh Kumar (Central investigative lead, 91% confidence)\n2. Vikram 'Vicky' Sharma (Logistics coordinator, 84% confidence)\n3. Sunil Mehta (Driver / vehicle owner, 78% confidence)\n4. Pooja Sharma (Missing subject / victim, 100% confidence)\nThese individuals are interconnected across 22 multi-modal graph links.",
    
    "vehicle": "Vehicle DL 01 AX 4492 (White Maruti Dzire) is registered to Sunil Mehta. Optical cameras (CCTV-DU-019 and CCTV-KG-084) and NETC FASTag records place this vehicle moving continuously from North Campus (16:15) to Kashmere Gate (18:42) and crossing into Haryana at Murthal Toll (19:40).",

    "money": "Financial intelligence flags transaction TXN-UPI-88301: A ₹50,000 IMPS transfer from Rakesh Kumar's HDFC Account (****4491) to Sunil Mehta's ICICI Account (****8820) at 17:15 on 12 Aug 2026, exactly between the campus pickup and highway departure.",

    "default": "Based on the case knowledge graph for DL-2026-0412, multi-source records establish cross-modal correlations across CDR telecom pings, NPCI banking transfers, NETC FASTag toll events, and DMRC CCTV footage. You can inspect specific entities in the Network Graph tab or ask about Rakesh Kumar, vehicle DL 01 AX 4492, timeline events, or financial payouts."
  }
};

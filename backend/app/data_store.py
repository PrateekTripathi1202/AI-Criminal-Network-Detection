"""
Seed Dataset for AI-Powered Criminal Network Analysis System
Aligned with CCTNS, ICJS, Digital Police Portal standards
Covers: People, Documents/FIRs, Vehicles, Locations, Organizations, Communications, Financial, CCTV
"""

INITIAL_NODES = [
    # People (Suspects, associates, kingpins, frontmen)
    {
        "id": "P-101",
        "label": "Vikram 'Vicky' Malhotra",
        "type": "person",
        "risk_score": 96.5,
        "syndicate": "Shadow Syndicate (D-Nexus)",
        "metadata": {
            "alias": "Vicky Bhai",
            "role": "Syndicate Kingpin / Mastermind",
            "status": "Wanted (Red Corner Notice Pending)",
            "cctns_id": "CCTNS-2024-MH-9921",
            "age": 44,
            "bns_sections": "BNS 111 (Organized Crime), 316 (Cheating), 61 (Criminal Conspiracy)",
            "last_known_city": "Dubai / Mumbai",
            "avatar": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150"
        }
    },
    {
        "id": "P-102",
        "label": "Rajesh 'Munna' Sharma",
        "type": "person",
        "risk_score": 88.0,
        "syndicate": "Shadow Syndicate (D-Nexus)",
        "metadata": {
            "alias": "Munna Delhi",
            "role": "Hawala Operator & Logistics Chief",
            "status": "Under Surveillance",
            "cctns_id": "CCTNS-2025-DL-4102",
            "age": 39,
            "bns_sections": "BNS 318, PMLA Sec 3",
            "last_known_city": "New Delhi",
            "avatar": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150"
        }
    },
    {
        "id": "P-103",
        "label": "Sameer 'Sam' Khan",
        "type": "person",
        "risk_score": 79.5,
        "syndicate": "Cyber-Cartel 09",
        "metadata": {
            "alias": "Ghost_Operator",
            "role": "Cyber Operative & SIM Mule Handler",
            "status": "Bail Granted (Violating Conditions)",
            "cctns_id": "CCTNS-2025-KA-8012",
            "age": 28,
            "bns_sections": "IT Act 66D, BNS 319",
            "last_known_city": "Bengaluru",
            "avatar": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150"
        }
    },
    {
        "id": "P-104",
        "label": "Amit 'Rana' Tyagi",
        "type": "person",
        "risk_score": 84.0,
        "syndicate": "Shadow Syndicate (D-Nexus)",
        "metadata": {
            "alias": "Rana Shooter",
            "role": "Enforcer & Weapons Courier",
            "status": "Arrested in FIR-2026-DEL-102",
            "cctns_id": "CCTNS-2026-DL-1109",
            "age": 32,
            "bns_sections": "Arms Act Sec 25, BNS 109",
            "last_known_city": "Ghaziabad / Delhi",
            "avatar": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=150"
        }
    },
    {
        "id": "P-105",
        "label": "Pooja 'Maya' Deshmukh",
        "type": "person",
        "risk_score": 71.0,
        "syndicate": "Hawala Nexus",
        "metadata": {
            "alias": "Maya D",
            "role": "Shell Entity Director & Money Launderer",
            "status": "Absconding",
            "cctns_id": "CCTNS-2025-MH-7734",
            "age": 35,
            "bns_sections": "Companies Act Fraud, BNS 318",
            "last_known_city": "Navi Mumbai",
            "avatar": "https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=150"
        }
    },
    {
        "id": "P-106",
        "label": "Karan 'KB' Bansal",
        "type": "person",
        "risk_score": 62.0,
        "syndicate": "Cyber-Cartel 09",
        "metadata": {
            "alias": "CryptoKB",
            "role": "Cryptocurrency Off-ramper",
            "status": "Questioned",
            "cctns_id": "CCTNS-2026-HR-3011",
            "age": 26,
            "bns_sections": "IT Act 43/66",
            "last_known_city": "Gurugram",
            "avatar": "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=150"
        }
    },

    # Phone numbers / SIMs (CDR)
    {
        "id": "PH-98110",
        "label": "+91 98110-XXXX1 (Burner)",
        "type": "phone",
        "risk_score": 91.0,
        "syndicate": "Shadow Syndicate (D-Nexus)",
        "metadata": {
            "subscriber_fake": "Ramesh Kumar (Aadhaar clone)",
            "imei": "864291040182910",
            "tower_circle": "Delhi NCR / Rohini",
            "call_volume_30d": 412,
            "international_calls": 38
        }
    },
    {
        "id": "PH-99200",
        "label": "+91 99200-XXXX8 (Encrypted VoIP)",
        "type": "phone",
        "risk_score": 87.5,
        "syndicate": "Shadow Syndicate (D-Nexus)",
        "metadata": {
            "subscriber_fake": "Foreign eSIM",
            "imei": "358912059102830",
            "tower_circle": "Mumbai / Bandra Kurla",
            "call_volume_30d": 184,
            "international_calls": 92
        }
    },
    {
        "id": "PH-97421",
        "label": "+91 97421-XXXX3 (Mule SIM)",
        "type": "phone",
        "risk_score": 75.0,
        "syndicate": "Cyber-Cartel 09",
        "metadata": {
            "subscriber_fake": "Student ID Mule",
            "imei": "860192849182741",
            "tower_circle": "Bengaluru / Koramangala",
            "call_volume_30d": 620,
            "international_calls": 12
        }
    },

    # Vehicles (ANPR tracked)
    {
        "id": "VH-DL01",
        "label": "DL-01-AB-9821 (Black Fortuner)",
        "type": "vehicle",
        "risk_score": 85.0,
        "syndicate": "Shadow Syndicate (D-Nexus)",
        "metadata": {
            "make": "Toyota Fortuner 4x4",
            "chassis": "MB1294819X",
            "registered_owner": "Apex Impex Front Co.",
            "anpr_sightings_7d": 19,
            "tint_violation": True,
            "tint_flag": "100% Black Film"
        }
    },
    {
        "id": "VH-MH04",
        "label": "MH-04-EK-4402 (Grey Creta)",
        "type": "vehicle",
        "risk_score": 72.0,
        "syndicate": "Hawala Nexus",
        "metadata": {
            "make": "Hyundai Creta",
            "chassis": "MAL4819281A",
            "registered_owner": "Pooja Deshmukh",
            "anpr_sightings_7d": 8
        }
    },
    {
        "id": "VH-KA03",
        "label": "KA-03-MM-1029 (White Swift)",
        "type": "vehicle",
        "risk_score": 64.0,
        "syndicate": "Cyber-Cartel 09",
        "metadata": {
            "make": "Maruti Swift",
            "chassis": "MA34918272Z",
            "registered_owner": "Rental Fleet Mule",
            "anpr_sightings_7d": 14
        }
    },

    # Bank Accounts & Financial Entities
    {
        "id": "ACC-HDFC-8819",
        "label": "HDFC #...8819 (Shell Mule)",
        "type": "account",
        "risk_score": 93.0,
        "syndicate": "Hawala Nexus",
        "metadata": {
            "bank": "HDFC Bank, Fort Branch Mumbai",
            "holder": "BlueOcean Logistics Pvt Ltd",
            "balance_inr": "₹ 4,82,50,000",
            "layering_score": "High (PMLA alert 409)",
            "flagged_tx_count": 48
        }
    },
    {
        "id": "ACC-ICICI-1102",
        "label": "ICICI #...1102 (Cash Pooling)",
        "type": "account",
        "risk_score": 89.0,
        "syndicate": "Shadow Syndicate (D-Nexus)",
        "metadata": {
            "bank": "ICICI Bank, Connaught Place New Delhi",
            "holder": "Northern Trader Corp",
            "balance_inr": "₹ 1,94,20,000",
            "layering_score": "Severe Smurfing",
            "flagged_tx_count": 72
        }
    },
    {
        "id": "ACC-USDT-WAL",
        "label": "TRC-20: 0x9fA2...39eB",
        "type": "account",
        "risk_score": 95.0,
        "syndicate": "Cyber-Cartel 09",
        "metadata": {
            "network": "Tron TRC-20 (USDT)",
            "cumulative_volume": "$1,450,000 USDT",
            "destination": "Offshore Mixer / Tornado Equivalent",
            "flagged_tx_count": 110
        }
    },

    # Organizations (Front companies / Shells / Syndicates)
    {
        "id": "ORG-APEX",
        "label": "Apex Global Impex (Shell)",
        "type": "organization",
        "risk_score": 92.0,
        "syndicate": "Shadow Syndicate (D-Nexus)",
        "metadata": {
            "cin": "U51909MH2021PTC368291",
            "directors": "Pooja Deshmukh, Dummy Peon",
            "nature": "Fake Trade Invoicing / Hawala Pipe",
            "turnover_declared": "₹ 42.5 Cr"
        }
    },
    {
        "id": "ORG-CYBERP",
        "label": "BytePay Fintech Solutions",
        "type": "organization",
        "risk_score": 78.0,
        "syndicate": "Cyber-Cartel 09",
        "metadata": {
            "cin": "U72200KA2023PTC172819",
            "nature": "Payment Gateway Aggregator for Phishing",
            "complaints_cybercrime": 312
        }
    },

    # Locations (Crime hotspots, meet points, safehouses)
    {
        "id": "LOC-CONNAUGHT",
        "label": "Connaught Place Block-B, New Delhi",
        "type": "location",
        "risk_score": 74.0,
        "syndicate": "Shadow Syndicate (D-Nexus)",
        "metadata": {
            "lat": 28.6328,
            "lng": 77.2197,
            "city": "New Delhi",
            "police_station": "Connaught Place PS",
            "significance": "Cash Handover Meeting Point"
        }
    },
    {
        "id": "LOC-BKC",
        "label": "Bandra Kurla Complex, Mumbai",
        "type": "location",
        "risk_score": 68.0,
        "syndicate": "Hawala Nexus",
        "metadata": {
            "lat": 19.0657,
            "lng": 72.8687,
            "city": "Mumbai",
            "police_station": "BKC Cyber Police",
            "significance": "Shell Corp Registered Address"
        }
    },
    {
        "id": "LOC-KORAMANGALA",
        "label": "Koramangala 5th Block, Bengaluru",
        "type": "location",
        "risk_score": 70.0,
        "syndicate": "Cyber-Cartel 09",
        "metadata": {
            "lat": 12.9352,
            "lng": 77.6245,
            "city": "Bengaluru",
            "police_station": "Koramangala PS",
            "significance": "Call-Center Boiler Room Raid Location"
        }
    },
    {
        "id": "LOC-AEROCITY",
        "label": "Aerocity Hospitality District, Delhi",
        "type": "location",
        "risk_score": 81.0,
        "syndicate": "Shadow Syndicate (D-Nexus)",
        "metadata": {
            "lat": 28.5528,
            "lng": 77.1219,
            "city": "New Delhi",
            "police_station": "IGI Airport PS",
            "significance": "Luxury Hotel Syndicate Secret Conclave"
        }
    },

    # CCTV Cameras
    {
        "id": "CAM-DEL-041",
        "label": "CCTV #DEL-CP-041 (PTZ Dome)",
        "type": "cctv",
        "risk_score": 65.0,
        "syndicate": "Surveillance Grid",
        "metadata": {
            "resolution": "4K Ultra-HD 60FPS",
            "anpr_enabled": True,
            "face_recognition": True,
            "location_name": "Outer Circle Outer Exit, CP Delhi",
            "detections_logged": 1420
        }
    },
    {
        "id": "CAM-MUM-119",
        "label": "CCTV #MUM-BKC-119 (Toll ANPR)",
        "type": "cctv",
        "risk_score": 60.0,
        "syndicate": "Surveillance Grid",
        "metadata": {
            "resolution": "1080p ANPR Optimized",
            "anpr_enabled": True,
            "face_recognition": False,
            "location_name": "BKC Connector Toll Plaza",
            "detections_logged": 980
        }
    },
    {
        "id": "CAM-AERO-012",
        "label": "CCTV #DEL-AERO-012 (Hotel Lobby)",
        "type": "cctv",
        "risk_score": 72.0,
        "syndicate": "Surveillance Grid",
        "metadata": {
            "resolution": "4K Biometric Facial Capture",
            "anpr_enabled": False,
            "face_recognition": True,
            "location_name": "Grand Hyatt Valet Entry, Aerocity",
            "detections_logged": 430
        }
    }
]

INITIAL_EDGES = [
    # Chain 1: Kingpin Vicky -> Munna Sharma -> Burner Phone -> Vehicle -> Account -> Location -> CCTV
    {
        "id": "E-01",
        "source": "P-101",
        "target": "P-102",
        "type": "commands",
        "weight": 3.8,
        "frequency": 85,
        "evidence_count": 4,
        "label": "Controls & Instructs",
        "metadata": {"intercept_ref": "CDR-INT-2026-09", "relation": "Boss to Hawala Chief"}
    },
    {
        "id": "E-02",
        "source": "P-102",
        "target": "PH-98110",
        "type": "uses_phone",
        "weight": 3.5,
        "frequency": 140,
        "evidence_count": 3,
        "label": "Operates Burner",
        "metadata": {"imsi_grabber_match": True, "imei_correlation": "99.4%"}
    },
    {
        "id": "E-03",
        "source": "PH-98110",
        "target": "VH-DL01",
        "type": "paired_with_vehicle",
        "weight": 2.9,
        "frequency": 24,
        "evidence_count": 2,
        "label": "Bluetooth Pairing / GPS Match",
        "metadata": {"infotainment_dump": "BT_MAC_00:1B:44:11:3A:B9"}
    },
    {
        "id": "E-04",
        "source": "VH-DL01",
        "target": "LOC-CONNAUGHT",
        "type": "spotted_at",
        "weight": 3.0,
        "frequency": 16,
        "evidence_count": 3,
        "label": "Parked at Spot",
        "metadata": {"timestamp": "2026-09-18 21:14:00", "duration_mins": 45}
    },
    {
        "id": "E-05",
        "source": "LOC-CONNAUGHT",
        "target": "CAM-DEL-041",
        "type": "covered_by",
        "weight": 3.2,
        "frequency": 30,
        "evidence_count": 1,
        "label": "Under CCTV Field of View",
        "metadata": {"fov_angle": "Angle 3, North-East"}
    },
    {
        "id": "E-06",
        "source": "CAM-DEL-041",
        "target": "P-104",
        "type": "facial_match",
        "weight": 3.7,
        "frequency": 6,
        "evidence_count": 2,
        "label": "Face Captured 94.8% Match",
        "metadata": {"face_confidence": 0.948, "weapon_detected": True}
    },

    # Financial links
    {
        "id": "E-07",
        "source": "P-102",
        "target": "ACC-ICICI-1102",
        "type": "controls_account",
        "weight": 3.6,
        "frequency": 90,
        "evidence_count": 5,
        "label": "Signatory & NetBanking IP",
        "metadata": {"ip_address": "103.21.58.12", "device": "iPhone 15 Pro"}
    },
    {
        "id": "E-08",
        "source": "ACC-ICICI-1102",
        "target": "ACC-HDFC-8819",
        "type": "transfers_money",
        "weight": 4.0,
        "frequency": 34,
        "evidence_count": 6,
        "label": "Hawala Layering (₹ 3.4 Cr)",
        "metadata": {"avg_tx": "₹ 10,00,000", "pattern": "Structured Smurfing"}
    },
    {
        "id": "E-09",
        "source": "ACC-HDFC-8819",
        "target": "ORG-APEX",
        "type": "owned_by_entity",
        "weight": 3.5,
        "frequency": 1,
        "evidence_count": 3,
        "label": "Corporate Account",
        "metadata": {"mca_roc_reg": "RoC Mumbai"}
    },
    {
        "id": "E-10",
        "source": "P-105",
        "target": "ORG-APEX",
        "type": "director_of",
        "weight": 3.2,
        "frequency": 1,
        "evidence_count": 4,
        "label": "Managing Director",
        "metadata": {"din": "09182741"}
    },
    {
        "id": "E-11",
        "source": "P-105",
        "target": "VH-MH04",
        "type": "owns_vehicle",
        "weight": 2.8,
        "frequency": 1,
        "evidence_count": 2,
        "label": "RC Book Registered Owner",
        "metadata": {"rto": "MH-04 Thane"}
    },
    {
        "id": "E-12",
        "source": "VH-MH04",
        "target": "LOC-BKC",
        "type": "spotted_at",
        "weight": 2.5,
        "frequency": 12,
        "evidence_count": 2,
        "label": "Daily Office Commute",
        "metadata": {"toll_tag": "FASTag-910283"}
    },
    {
        "id": "E-13",
        "source": "LOC-BKC",
        "target": "CAM-MUM-119",
        "type": "covered_by",
        "weight": 3.0,
        "frequency": 1,
        "evidence_count": 1,
        "label": "ANPR Toll Gate",
        "metadata": {"direction": "Inbound South"}
    },

    # Cyber Cartel & Crypto trail
    {
        "id": "E-14",
        "source": "P-103",
        "target": "PH-97421",
        "type": "uses_phone",
        "weight": 3.4,
        "frequency": 220,
        "evidence_count": 4,
        "label": "Primary Device SIM",
        "metadata": {"imei": "860192849182741"}
    },
    {
        "id": "E-15",
        "source": "P-103",
        "target": "ORG-CYBERP",
        "type": "operates_tech",
        "weight": 3.1,
        "frequency": 1,
        "evidence_count": 3,
        "label": "CTO / Lead Architect",
        "metadata": {"github_repo_trace": "dark_gateway_core"}
    },
    {
        "id": "E-16",
        "source": "ORG-CYBERP",
        "target": "ACC-USDT-WAL",
        "type": "crypto_drain",
        "weight": 4.2,
        "frequency": 58,
        "evidence_count": 5,
        "label": "Launders via USDT (1.45M $)",
        "metadata": {"blockchain_explorer": "Tronscan TX Cluster"}
    },
    {
        "id": "E-17",
        "source": "P-106",
        "target": "ACC-USDT-WAL",
        "type": "cash_out_crypto",
        "weight": 3.8,
        "frequency": 42,
        "evidence_count": 4,
        "label": "P2P Crypto-to-Cash Offramp",
        "metadata": {"localbitcoins_telegram": "@CryptoFastCash_IN"}
    },

    # Cross-Case Connections
    {
        "id": "E-18",
        "source": "P-104",
        "target": "P-102",
        "type": "co_accused",
        "weight": 3.9,
        "frequency": 15,
        "evidence_count": 4,
        "label": "Co-Accused in FIR-2026-DEL-102",
        "metadata": {"fir": "FIR-2026-DEL-102", "crime": "Extortion & Armed Threat"}
    },
    {
        "id": "E-19",
        "source": "P-101",
        "target": "PH-99200",
        "type": "uses_phone",
        "weight": 3.7,
        "frequency": 45,
        "evidence_count": 3,
        "label": "Encrypted Satellite/VoIP Line",
        "metadata": {"signal_contact_token": "verified_key_0x8b"}
    },
    {
        "id": "E-20",
        "source": "PH-99200",
        "target": "PH-98110",
        "type": "calls",
        "weight": 4.1,
        "frequency": 78,
        "evidence_count": 5,
        "label": "Frequent Inter-State Calls (78 calls)",
        "metadata": {"duration_total_mins": 340, "peak_hours": "01:00 AM - 04:00 AM"}
    },
    {
        "id": "E-21",
        "source": "P-104",
        "target": "VH-DL01",
        "type": "driver_of",
        "weight": 3.6,
        "frequency": 18,
        "evidence_count": 3,
        "label": "Observed Driving Fortuner",
        "metadata": {"fuel_receipt_signature": "Amit Tyagi"}
    },
    {
        "id": "E-22",
        "source": "LOC-AEROCITY",
        "target": "CAM-AERO-012",
        "type": "covered_by",
        "weight": 3.0,
        "frequency": 1,
        "evidence_count": 1,
        "label": "Lobby Security Matrix",
        "metadata": {"ai_alert": "VIP Floor Breach"}
    },
    {
        "id": "E-23",
        "source": "CAM-AERO-012",
        "target": "P-102",
        "type": "facial_match",
        "weight": 3.5,
        "frequency": 3,
        "evidence_count": 2,
        "label": "Face Sighting (96.1% match)",
        "metadata": {"timestamp": "2026-09-20 19:40:12"}
    }
]

# Registered FIRs across Delhi, Mumbai, Bengaluru for Cross-case correlation
FIRS_DATA = [
    {
        "fir_number": "FIR-2026-DEL-102",
        "police_station": "Connaught Place PS, New Delhi",
        "date_registered": "2026-08-14",
        "bns_sections": ["BNS 111", "BNS 308(2)", "Arms Act 25"],
        "complainant": "Shri Ashok Khurana (Jeweller)",
        "summary": "Extortion call demanding ₹ 2 Crore ransom. Armed suspects fled in black SUV DL-01-AB-9821. Intercepted calls originated from burner +91 98110-XXXX1.",
        "accused_named": ["Amit 'Rana' Tyagi", "Unidentified Caller 'Munna'"],
        "seized_evidence": ["CCTV Clip CAM-DEL-041", "Spent 9mm Cartridge", "ANPR snapshot DL-01-AB-9821"],
        "status": "Under Trial / Chargesheet Filed"
    },
    {
        "fir_number": "FIR-2025-MUM-844",
        "police_station": "Bandra Kurla Complex Cyber Police, Mumbai",
        "date_registered": "2025-11-20",
        "bns_sections": ["BNS 318(4)", "BNS 336", "PMLA 3"],
        "complainant": "Enforcement Directorate / FIU-IND",
        "summary": "Illegal remittances exceeding ₹ 45 Crore layered through shell company Apex Global Impex into HDFC Account #...8819 and routed offshore.",
        "accused_named": ["Pooja Deshmukh", "Vikram 'Vicky' Malhotra"],
        "seized_evidence": ["Bogus Invoices", "Bank Statements HDFC/ICICI", "Hard Drive Dumps"],
        "status": "Investigation Active / Lookout Notice Issued"
    },
    {
        "fir_number": "FIR-2026-BLR-390",
        "police_station": "Koramangala Cyber Crime PS, Bengaluru",
        "date_registered": "2026-04-10",
        "bns_sections": ["IT Act 66C/66D", "BNS 319"],
        "complainant": "Multiple Victims / State Cyber Cell",
        "summary": "Online investment fraud racket operating fake trading apps. Funds drained through BytePay Fintech into Tron USDT wallet 0x9fA2...39eB.",
        "accused_named": ["Sameer Khan", "Karan Bansal"],
        "seized_evidence": ["240 Mule SIM Cards", "Laptops with API Keys", "Hardware Wallet"],
        "status": "Partial Recovery / Key Server Forensics Ongoing"
    }
]

# Simulated CCTV detections feed
CCTV_SIMULATED_FEEDS = [
    {
        "camera_id": "CAM-DEL-041",
        "camera_name": "Connaught Place Radial-2 ANPR",
        "location": "Connaught Place, New Delhi",
        "timestamp": "2026-09-23 21:12:44",
        "detected_entities": [
            {
                "type": "face",
                "matched_person_id": "P-104",
                "matched_name": "Amit 'Rana' Tyagi",
                "confidence": 0.948,
                "bbox": [120, 85, 210, 195],
                "threat_level": "CRITICAL",
                "notes": "Red alert match with CCTNS wanted database"
            },
            {
                "type": "vehicle",
                "matched_vehicle_id": "VH-DL01",
                "plate_number": "DL-01-AB-9821",
                "confidence": 0.982,
                "bbox": [280, 140, 520, 360],
                "threat_level": "HIGH",
                "notes": "Vehicle flagged in FIR-2026-DEL-102"
            }
        ]
    },
    {
        "camera_id": "CAM-AERO-012",
        "camera_name": "Aerocity VIP Entrance Cam 4",
        "location": "Aerocity, New Delhi",
        "timestamp": "2026-09-23 21:40:19",
        "detected_entities": [
            {
                "type": "face",
                "matched_person_id": "P-102",
                "matched_name": "Rajesh 'Munna' Sharma",
                "confidence": 0.961,
                "bbox": [180, 95, 270, 210],
                "threat_level": "CRITICAL",
                "notes": "Hawala syndicate lieutenant sighted carrying duffel bag"
            }
        ]
    }
]

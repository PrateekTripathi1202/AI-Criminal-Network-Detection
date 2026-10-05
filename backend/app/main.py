from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any, List, Optional
import time
import uuid

from .models import IngestionRequest, CopilotQuery
from .graph_engine import graph_engine
from .ai_intelligence import ai_intelligence
from .vision_engine import vision_engine
from .data_store import FIRS_DATA

app = FastAPI(
    title="NATIONAL CRIMINAL INTELLIGENCE SYSTEM (NCIS)",
    description="Central Intelligence Command & Surveillance Grid - Crime & Criminal Tracking Network Systems (CCTNS 4.0)",
    version="4.2.0"
)

# Enable CORS for local Vite frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "system": "NATIONAL CRIMINAL INTELLIGENCE SYSTEM (NCIS)",
        "agency": "Ministry of Home Affairs / Central Intelligence Directorate",
        "clearance_level": "TOP SECRET // LAW ENFORCEMENT SENSITIVE",
        "cctns_grid_status": "ONLINE",
        "icjs_integration": "ACTIVE",
        "encryption": "AES-256-GCM / SHA-512"
    }

@app.get("/api/health")
def health():
    return {"status": "ok", "timestamp": time.time()}

# ----------------- GRAPH & NETWORK ENDPOINTS -----------------

@app.get("/api/network/graph")
def get_graph():
    """Returns the full knowledge graph with computed centralities and community clusters."""
    return graph_engine.get_full_graph_data()

@app.get("/api/network/node/{node_id}")
def get_node_details(node_id: str):
    node = graph_engine.get_node_by_id(node_id)
    if not node:
        raise HTTPException(status_code=404, detail="Entity node not found")
    # Also find all connected neighbors
    neighbors = []
    for edge in graph_engine.edges:
        if edge["source"] == node_id:
            target_node = graph_engine.get_node_by_id(edge["target"])
            if target_node:
                neighbors.append({"relation": edge["type"], "label": edge.get("label"), "entity": target_node})
        elif edge["target"] == node_id:
            source_node = graph_engine.get_node_by_id(edge["source"])
            if source_node:
                neighbors.append({"relation": f"reverse_{edge['type']}", "label": edge.get("label"), "entity": source_node})
    return {"node": node, "connections": neighbors}

@app.get("/api/network/shortest-path")
def get_shortest_path(source: str, target: str):
    """Traces the direct or multi-hop criminal pathway connecting two nodes."""
    return graph_engine.find_shortest_path(source, target)

# ----------------- AI & INTELLIGENCE ENDPOINTS -----------------

@app.get("/api/intelligence/predict-links")
def get_predicted_links():
    """Returns XAI link predictions with confidence scores and feature explanations."""
    return ai_intelligence.predict_hidden_links()

@app.get("/api/intelligence/cross-case")
def get_cross_case():
    """Returns cross-case correlation linkages between multiple police FIRs."""
    return ai_intelligence.get_cross_case_correlations()

@app.get("/api/intelligence/memory")
def get_investigation_memory():
    """Returns stored syndicate intelligence memory and historical modus operandi."""
    return ai_intelligence.investigation_memory

@app.post("/api/copilot/query")
def copilot_query(req: CopilotQuery):
    """Natural Language AI Case Assistant (RAG)."""
    return ai_intelligence.answer_copilot_query(req.question, req.case_context or "")

# ----------------- SURVEILLANCE & COMPUTER VISION -----------------

@app.get("/api/surveillance/feeds")
def get_surveillance_feeds():
    """Returns live CCTV feeds, ANPR detections, and face matching telemetry."""
    return vision_engine.get_live_surveillance_telemetry()

@app.get("/api/surveillance/analyze/{camera_id}")
def analyze_camera(camera_id: str):
    return vision_engine.analyze_frame_simulation(camera_id)

@app.get("/api/surveillance/audio-intercepts")
def get_audio_intercepts():
    """Returns intercepted telecom wiretaps, live waveform metadata, and bilingual transcripts."""
    return [
        {
            "intercept_id": "WIRE-2026-INT-409",
            "date_time": "2026-09-23 20:41:12 IST",
            "source_phone": "+91 98110-XXXX1 (Burner SIM)",
            "source_speaker": "Rajesh 'Munna' Sharma",
            "target_phone": "+91 99200-XXXX8 (Encrypted Satellite VoIP)",
            "target_speaker": "Vikram 'Vicky' Malhotra (Mastermind)",
            "duration_sec": 48,
            "cell_tower": "Rohini Sector 14, New Delhi (Tower ID: DEL-ROH-918)",
            "threat_level": "CRITICAL",
            "transcript_original": "भाई, गाड़ी पहुंच गई है सीपी ब्लॉक बी में। अमित खुद ड्राइव कर रहा है फॉर्च्यूनर। ज्वेलर को बोल दिया है दो करोड़ तैयार रखने। अगर आनाकानी की तो गोली चलेगी। हवाला रूट मुंबई वाला क्लियर है ना?",
            "transcript_english": "Bhai, vehicle has reached CP Block B. Amit himself is driving the Fortuner. Have told the jeweller to keep 2 Crores ready. If he hesitates, bullets will fly. The Mumbai Hawala route is clear, right?",
            "keywords_detected": ["गाड़ी", "Fortuner", "अमित", "दो करोड़", "गोली", "हवाला", "मुंबई"],
            "legal_warrant_ref": "MHA Wiretap Auth Order #CR-8812/2026"
        },
        {
            "intercept_id": "WIRE-2026-INT-410",
            "date_time": "2026-09-23 21:05:30 IST",
            "source_phone": "+91 97421-XXXX3 (Mule SIM)",
            "source_speaker": "Sameer 'Sam' Khan",
            "target_phone": "+91 98110-XXXX1 (Burner SIM)",
            "target_speaker": "Rajesh 'Munna' Sharma",
            "duration_sec": 32,
            "cell_tower": "Koramangala 5th Block, Bengaluru",
            "threat_level": "HIGH",
            "transcript_original": "नया बैच तैयार है। पचास फ्रेश आधार क्लोन्ड सिम कार्ड्स दिल्ली भेज दिए हैं कोरियर से। यूएसडीटी का पेमेंट उसी टीआरसी ट्वेंटी वॉलेट में डाल देना।",
            "transcript_english": "New batch is ready. Fifty fresh Aadhaar-cloned SIM cards dispatched to Delhi via courier. Deposit the USDT payment into the same TRC-20 wallet.",
            "keywords_detected": ["आधार क्लोन्ड", "SIM cards", "USDT", "TRC-20"],
            "legal_warrant_ref": "Cyber Crime Intercept Auth #KA-CC-119"
        }
    ]

# ----------------- CASES & INGESTION -----------------

@app.get("/api/cases")
def list_cases():
    return FIRS_DATA

@app.post("/api/ingestion/process")
def process_ingestion(req: IngestionRequest):
    """
    Simulates Multi-Source Ingestion & Automated Entity Extraction:
    Extracts Suspects, Phone numbers, Vehicles, Accounts, Locations from unstructured FIR text or CDR CSV.
    """
    raw = req.raw_text or ""
    extracted_entities = []
    
    # Simple simulated NER logic for demo
    if "fir" in req.source_type.lower() or "fir" in raw.lower():
        extracted_entities = [
            {"type": "person", "label": "Ravi 'Kalia' Yadav", "id": f"P-{uuid.uuid4().hex[:4].upper()}", "role": "Suspect"},
            {"type": "phone", "label": "+91 97118-XXXX4", "id": f"PH-{uuid.uuid4().hex[:4].upper()}", "role": "Burner Device"},
            {"type": "vehicle", "label": "DL-04-CA-7711", "id": f"VH-{uuid.uuid4().hex[:4].upper()}", "role": "Fleeing Vehicle"}
        ]
        # Dynamically add to graph
        for ent in extracted_entities:
            graph_engine.add_node({
                "id": ent["id"],
                "label": ent["label"],
                "type": ent["type"],
                "risk_score": 75.0,
                "syndicate": "Shadow Syndicate (D-Nexus)",
                "metadata": {"ingested_from": req.file_name or "Direct Upload", "role": ent["role"]}
            })
        # Add edge linking to Munna Sharma
        new_edge = {
            "id": f"E-INGEST-{uuid.uuid4().hex[:4].upper()}",
            "source": extracted_entities[0]["id"],
            "target": "P-102",
            "type": "co_accused",
            "weight": 3.0,
            "frequency": 5,
            "label": "Extracted from Ingested FIR",
            "metadata": {"source_doc": req.file_name or "Uploaded FIR"}
        }
        graph_engine.add_edge(new_edge)

    return {
        "status": "INGESTION_SUCCESS",
        "entities_extracted_count": len(extracted_entities),
        "entities": extracted_entities,
        "knowledge_graph_updated": True
    }

# ----------------- HUMAN-IN-THE-LOOP VALIDATION -----------------

@app.post("/api/investigation/validate-link")
def validate_link(payload: Dict[str, Any]):
    """
    Allows investigators to approve or reject AI-predicted linkages
    and add judicial audit comments.
    """
    source = payload.get("source")
    target = payload.get("target")
    approved = payload.get("approved", True)
    officer_badge = payload.get("officer_badge", "INSP-DL-4902")
    notes = payload.get("notes", "Verified with witness statements")

    if approved:
        new_edge = {
            "id": f"E-VAL-{uuid.uuid4().hex[:4].upper()}",
            "source": source,
            "target": target,
            "type": "investigator_verified",
            "weight": 4.5,
            "frequency": 1,
            "label": f"Verified Link ({officer_badge})",
            "metadata": {"officer": officer_badge, "notes": notes, "validated_at": time.strftime("%Y-%m-%d %H:%M:%S")}
        }
        graph_engine.add_edge(new_edge)

    return {
        "status": "VALIDATED" if approved else "REJECTED",
        "officer": officer_badge,
        "source": source,
        "target": target,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="127.0.0.1", port=8000, reload=True)

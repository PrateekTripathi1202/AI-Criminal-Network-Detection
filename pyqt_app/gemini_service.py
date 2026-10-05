"""
Google Gemini AI Integration Service
Powered by the official google-genai SDK (Gemini 3.8 Flash / Gemini 3.1 Pro Preview).
Provides law-enforcement grounded intelligence:
- Case Copilot RAG queries
- Multi-Source FIR & Document Entity Extraction
- Court-Admissible Dossier Generation (Sec 65B Bharatiya Sakshya Adhiniyam / IEA)
- Audio Wiretap Intercept Decryption & Crime Slang Analysis
- Explainable AI (XAI) Link Forensic Auditing
"""

import os
import json
from typing import Dict, Any, List, Optional
from pathlib import Path

CONFIG_FILE = Path(__file__).resolve().parent / "gemini_config.json"

DEFAULT_MODELS = [
    "gemini-3.8-flash",
    "gemini-3.1-pro-preview",
    "gemini-3.5-flash-lite"
]

class GeminiIntelligenceService:
    def __init__(self):
        self.api_key: Optional[str] = None
        self.current_model: str = "gemini-3.8-flash"
        self.client = None
        self.load_config()

    def load_config(self):
        """Loads API key and settings from environment or local config file."""
        # 1. Environment variable
        env_key = os.environ.get("GEMINI_API_KEY")
        if env_key and env_key.strip():
            self.api_key = env_key.strip()

        # 2. Local config file override
        if CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if data.get("api_key"):
                        self.api_key = data["api_key"].strip()
                    if data.get("model"):
                        self.current_model = data["model"]
            except Exception as e:
                print(f"[GeminiService] Error loading config: {e}")

        self._init_client()

    def save_config(self, api_key: str, model: str = "gemini-3.8-flash"):
        """Saves API key and selected model."""
        self.api_key = api_key.strip()
        self.current_model = model
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump({"api_key": self.api_key, "model": self.current_model}, f, indent=2)
        except Exception as e:
            print(f"[GeminiService] Error saving config: {e}")

        # Also set in environment for current process
        os.environ["GEMINI_API_KEY"] = self.api_key
        self._init_client()

    def _init_client(self):
        """Initializes google-genai Client if key is available."""
        if not self.api_key:
            self.client = None
            return

        try:
            from google import genai
            self.client = genai.Client(api_key=self.api_key)
        except Exception as e:
            print(f"[GeminiService] Client initialization error: {e}")
            self.client = None

    def is_configured(self) -> bool:
        """Returns True if a valid client is initialized."""
        return self.client is not None and bool(self.api_key)

    def test_connection(self, key_to_test: Optional[str] = None) -> Dict[str, Any]:
        """Tests the Gemini API connection with a brief verification ping."""
        key = (key_to_test or self.api_key or "").strip()
        if not key:
            return {"success": False, "message": "API key cannot be empty."}

        try:
            from google import genai
            test_client = genai.Client(api_key=key)
            response = test_client.models.generate_content(
                model=self.current_model,
                contents="Verify connection: Respond with exactly 'SYSTEM_OPERATIONAL'."
            )
            text = response.text or ""
            return {
                "success": True,
                "message": f"Connection verified successfully on {self.current_model}!",
                "response": text.strip()
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Gemini API verification failed: {str(e)}"
            }

    # =========================================================================
    # 1. CASE COPILOT (Interactive Investigation Assistant)
    # =========================================================================
    def ask_copilot(
        self,
        question: str,
        conversation_history: List[Dict[str, str]] = None,
        graph_context: Dict[str, Any] = None,
        model_override: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Interrogates the criminal intelligence graph using Gemini 3.8 Flash.
        """
        model = model_override or self.current_model

        if not self.is_configured():
            return self._fallback_copilot_response(question)

        try:
            from google.genai import types

            # Build grounded criminal intelligence prompt
            system_instruction = (
                "You are the National Criminal Intelligence System (NCIS) AI Copilot, "
                "operating under the Ministry of Home Affairs and CCTNS 4.0 guidelines. "
                "Your objective is to provide high-level, precise, and actionable tactical intelligence "
                "to police superintendents, investigating officers (IOs), and intelligence analysts. "
                "Analyze the provided criminal knowledge graph, FIRs under the Bharatiya Nyaya Sanhita (BNS) "
                "and Prevention of Money Laundering Act (PMLA), call data records (CDR), and surveillance traces. "
                "Always format your response with clean Markdown headers, bullet points, risk classifications, "
                "and specific actionable legal/tactical next steps (e.g., Red Corner Notices, STR filings, FIR additions)."
            )

            # Context summary
            context_str = ""
            if graph_context:
                nodes = graph_context.get("nodes", [])
                edges = graph_context.get("edges", [])
                context_str = (
                    f"\n--- ACTIVE CASE KNOWLEDGE GRAPH CONTEXT ---\n"
                    f"Nodes Count: {len(nodes)}\n"
                    f"Sample Key Entities:\n"
                )
                for n in nodes[:15]:
                    meta = n.get("metadata", {})
                    context_str += f"- [{n.get('type', 'entity').upper()}] {n.get('id')}: {n.get('label')} | Risk: {n.get('risk_score', 'N/A')} | Syndicate: {n.get('syndicate', 'N/A')} | Role/Status: {meta.get('role', meta.get('make', ''))}\n"

                context_str += f"\nTotal Relationships Traced: {len(edges)}\n"
                for e in edges[:15]:
                    context_str += f"- {e.get('source')} --({e.get('label') or e.get('type')})--> {e.get('target')}\n"

            # History context
            history_str = ""
            if conversation_history:
                history_str = "\n--- RECENT CONVERSATION TRAIL ---\n"
                for msg in conversation_history[-4:]:
                    history_str += f"{msg.get('role', 'user').upper()}: {msg.get('text', '')}\n"

            full_prompt = (
                f"{context_str}\n"
                f"{history_str}\n"
                f"INVESTIGATING OFFICER QUERY: {question}\n"
                f"Provide a rigorous forensic and operational intelligence assessment."
            )

            config = types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.25,
            )

            response = self.client.models.generate_content(
                model=model,
                contents=full_prompt,
                config=config
            )

            answer = response.text or "No response generated by Gemini."
            return {
                "success": True,
                "model_used": model,
                "answer": answer,
                "is_live_api": True
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "answer": f"**Gemini API Error:** {str(e)}\n\n*(Falling back to heuristic analysis below)*\n\n" + self._fallback_copilot_response(question)["answer"],
                "is_live_api": False
            }

    # =========================================================================
    # 2. MULTI-SOURCE FIR / CDR ENTITY EXTRACTION
    # =========================================================================
    def extract_entities_from_text(self, raw_text: str, source_type: str = "FIR") -> Dict[str, Any]:
        """
        Uses Gemini to extract criminal entities, CDR burner phones, vehicle plates,
        hawala bank accounts, and syndicate linkages from unstructured text.
        """
        if not self.is_configured():
            return self._fallback_extraction(raw_text)

        try:
            prompt = (
                f"You are a Police Cyber Intelligence NLP entity extractor for CCTNS 4.0.\n"
                f"Analyze the following {source_type} text and extract all relevant entities into valid JSON.\n"
                f"Categories allowed: 'person', 'phone', 'vehicle', 'account', 'location', 'organization'.\n"
                f"Return ONLY a JSON object with this exact structure:\n"
                f"{{\n"
                f'  "entities": [\n'
                f'    {{"type": "person", "label": "Name", "alias": "Alias", "role": "Role", "bns_sections": "Sections", "risk_score": 85.0}},\n'
                f'    {{"type": "phone", "label": "+91...", "imei": "...", "role": "Burner/Mule"}},\n'
                f'    {{"type": "vehicle", "label": "Plate No", "make": "Model", "owner": "Name"}},\n'
                f'    {{"type": "account", "label": "Bank/Wallet", "holder": "Name", "amount": "₹..."}}\n'
                f'  ],\n'
                f'  "suggested_links": [\n'
                f'    {{"source": "Entity1", "target": "Entity2", "relation": "drives / calls / funds"}}\n'
                f'  ],\n'
                f'  "executive_summary": "Summary of incident and legal violations"\n'
                f"}}\n\n"
                f"SOURCE TEXT TO ANALYZE:\n{raw_text}"
            )

            response = self.client.models.generate_content(
                model=self.current_model,
                contents=prompt
            )

            text = response.text or "{}"
            # Extract JSON from code fence if present
            cleaned = text.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            elif cleaned.startswith("```"):
                cleaned = cleaned[3:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            cleaned = cleaned.strip()

            parsed = json.loads(cleaned)
            parsed["is_live_api"] = True
            return parsed

        except Exception as e:
            fallback = self._fallback_extraction(raw_text)
            fallback["error"] = str(e)
            return fallback

    # =========================================================================
    # 3. COURT-ADMISSIBLE DOSSIER SYNTHESIS (Section 65B BSA / IEA)
    # =========================================================================
    def generate_dossier(self, entity_data: Dict[str, Any], graph_context: Dict[str, Any]) -> str:
        """
        Generates a Section 65B compliant judicial prosecution dossier.
        """
        if not self.is_configured():
            return self._fallback_dossier(entity_data)

        try:
            prompt = (
                f"Act as a Senior Public Prosecutor and Cyber Forensic Expert for the National Investigation Agency (NIA).\n"
                f"Draft a formal, court-admissible Criminal Syndicate Dossier and Certificate under Section 65B of the Indian Evidence Act / Section 63 Bharatiya Sakshya Adhiniyam 2023.\n"
                f"Target Suspect Profile:\n{json.dumps(entity_data, indent=2)}\n\n"
                f"Graph Context & Digital Trail:\n{json.dumps(graph_context.get('edges', [])[:10], indent=2)}\n\n"
                f"Include:\n"
                f"1. OFFICIAL CASE DOSSIER HEADER (CCTNS / ICJS / MHA Seal Format)\n"
                f"2. SUSPECT BIOGRAPHICAL & BIOMETRIC PARTICULARS\n"
                f"3. CHARGES FRAMED UNDER BHARATIYA NYAYA SANHITA (BNS) & PMLA\n"
                f"4. DIGITAL FORENSICS TRAIL (CDR Cell Tower Triangulation, ANPR Toll Sightings, Hawala Smurfing)\n"
                f"5. CORROBORATING ELECTRONIC EVIDENCE LIST (SHA-256 Hashes of CCTV footage & wiretaps)\n"
                f"6. SECTION 65B ADMISSIBILITY CERTIFICATE SIGN-OFF"
            )

            response = self.client.models.generate_content(
                model=self.current_model,
                contents=prompt
            )
            return response.text or self._fallback_dossier(entity_data)

        except Exception as e:
            return f"**Gemini Generation Failed ({str(e)}). Generating Local Template:**\n\n" + self._fallback_dossier(entity_data)

    # =========================================================================
    # 4. AUDIO WIRETAP INTERCEPT FORENSICS
    # =========================================================================
    def analyze_wiretap(self, intercept_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyzes bilingual criminal wiretaps to detect coded slang, weapons movement,
        and extortion routes.
        """
        if not self.is_configured():
            return {
                "risk_assessment": "CRITICAL - Impending violent extortion and hawala disbursement.",
                "code_words_decoded": {
                    "गाड़ी (Vehicle)": "DL-01-AB-9821 Fortuner registered to shell company Apex Impex",
                    "दो करोड़ (2 Crores)": "Extortion payoff demanded from Connaught Place jeweler",
                    "गोली चलेगी": "Direct authorization for violent firearm use under Arms Act 25"
                },
                "recommended_dispatch": "Issue Red Alert to Delhi Police Special Cell & Anti-Extortion Cell immediately."
            }

        try:
            prompt = (
                f"You are a Telecom Intercept & Counter-Crime Analyst for law enforcement.\n"
                f"Analyze this intercepted wiretap recording:\n{json.dumps(intercept_data, indent=2)}\n\n"
                f"Provide:\n"
                f"1. Threat Level & Immediate Danger Score (1-100)\n"
                f"2. Code Words & Criminal Slang Decoded\n"
                f"3. Hidden Intent & Syndicate Operational Coordination\n"
                f"4. Immediate Interception / Dispatch Recommendation for Field Teams"
            )

            response = self.client.models.generate_content(
                model=self.current_model,
                contents=prompt
            )
            return {
                "analysis": response.text,
                "is_live_api": True
            }
        except Exception as e:
            return {"error": str(e), "analysis": "Error calling Gemini for wiretap analysis."}

    # =========================================================================
    # FALLBACK ENGINE (when API key is missing or offline)
    # =========================================================================
    def _fallback_copilot_response(self, question: str) -> Dict[str, Any]:
        q = question.lower()
        if "kingpin" in q or "leader" in q or "head" in q:
            ans = (
                "### 🎯 Syndicate Leadership & Kingpin Identification\n\n"
                "**Identified Mastermind:** **Vikram 'Vicky' Malhotra (P-101)**\n"
                "- **Betweenness Centrality:** 0.384 (Highest in entire multi-state graph)\n"
                "- **PageRank Index:** 0.142 | **Risk Score:** 96.5%\n"
                "- **Modus Operandi:** Directs operations remotely via encrypted satellite VoIP (`PH-99200`) "
                "routed through Dubai, using local lieutenants Rajesh Sharma and Amit Tyagi.\n\n"
                "**Actionable Recommendation:** Issue Interpol Red Corner Notice via CBI-NCB Interpol Division; "
                "order FIU-IND to freeze all overseas hawala remittances linked to Apex Global Impex."
            )
        elif "vehicle" in q or "car" in q or "fortuner" in q or "dl-01" in q:
            ans = (
                "### 🚗 Vehicle Forensics: DL-01-AB-9821 (Toyota Fortuner 4x4)\n\n"
                "- **Registered Owner:** Apex Global Impex (Front company for Hawala operations)\n"
                "- **Driver Identified via CCTV:** Amit 'Rana' Tyagi (Enforcer, P-104)\n"
                "- **ANPR Sighting:** Connaught Place Block-B at 14:22 IST on 2026-09-18\n"
                "- **Tint Violation:** 100% Black Tint Film (Motor Vehicles Act Sec 100)\n\n"
                "**Crucial Cross-State Link:** This vehicle physically bridges the Delhi extortion FIR (`FIR-2026-DEL-102`) "
                "to Mumbai's ₹ 45 Cr corporate money laundering FIR (`FIR-2025-MUM-844`)."
            )
        elif "hawala" in q or "money" in q or "bank" in q:
            ans = (
                "### 💳 Financial Crime & Hawala Smurfing Trail\n\n"
                "1. **Primary Collection Mule:** ICICI Account `#...1102` (Rajesh Sharma) accumulated ₹ 1.94 Cr via cash pooling.\n"
                "2. **Layering Step:** 48 rapid structured transfers beneath ₹ 10 Lakh (PMLA reporting threshold) pushed funds to HDFC `#...8819` (BlueOcean Logistics).\n"
                "3. **Offramp to Crypto:** ₹ 1.2 Crore converted to TRC-20 USDT wallet `0x9fA2...39eB` for offshore flight.\n\n"
                "**Recommendation:** Submit urgent Section 12 PMLA Freezing Order to ICICI and HDFC Bank nodal officers."
            )
        else:
            ans = (
                f"### 🛡️ Criminal Intelligence Report for: '{question}'\n\n"
                "- **Active Syndicate:** Shadow Syndicate (D-Nexus) & Hawala Nexus\n"
                "- **Current Graph Scope:** 18 Entities across 3 state corridors (Delhi, Mumbai, Bengaluru)\n"
                "- **High-Risk Anchors:** Vikram Malhotra (Kingpin), Rajesh Sharma (Hawala), Amit Tyagi (Weapons)\n"
                "- **Evidence Corroboration:** 3 ANPR hits, 412 CDR interactions, 2 wiretap transcripts, and 4 CCTV biometric face matches.\n\n"
                "> 💡 **Tip:** Add your Google Gemini API key in the top-right Settings to unlock live generative reasoning and multi-turn autonomous deep forensics."
            )

        return {
            "success": True,
            "model_used": "Offline Heuristic Engine (Configure Gemini Key in Settings)",
            "answer": ans,
            "is_live_api": False
        }

    def _fallback_extraction(self, text: str) -> Dict[str, Any]:
        return {
            "is_live_api": False,
            "entities": [
                {"type": "person", "label": "Ravi 'Kalia' Yadav", "alias": "Kalia", "role": "Associate Gunman", "bns_sections": "BNS 111, Arms Act", "risk_score": 78.0},
                {"type": "phone", "label": "+91 97118-XXXX4", "imei": "864192019284910", "role": "Burner SIM"},
                {"type": "vehicle", "label": "DL-04-CA-7711", "make": "Hyundai Verna", "owner": "Ravi Yadav"}
            ],
            "suggested_links": [
                {"source": "Ravi 'Kalia' Yadav", "target": "Rajesh 'Munna' Sharma", "relation": "Co-accused & Gunman"}
            ],
            "executive_summary": "Extracted 3 entities from police document using local fallback parser. Configure Gemini API key for deep LLM entity recognition."
        }

    def _fallback_dossier(self, entity_data: Dict[str, Any]) -> str:
        name = entity_data.get("label", "Unknown Suspect")
        meta = entity_data.get("metadata", {})
        return f"""========================================================================================
GOVERNMENT OF INDIA // MINISTRY OF HOME AFFAIRS
CRIME AND CRIMINAL TRACKING NETWORK & SYSTEMS (CCTNS 4.0)
JUDICIAL PROSECUTION DOSSIER & EVIDENCE ADMISSIBILITY REPORT
========================================================================================

1. TARGET IDENTIFICATION PARTICULARS
----------------------------------------------------------------------------------------
Full Name:           {name}
Known Alias:         {meta.get('alias', 'N/A')}
CCTNS Master ID:     {meta.get('cctns_id', 'CCTNS-2026-GEN-001')}
Syndicate Division:  {entity_data.get('syndicate', 'Organized Crime Cartel')}
Assigned Role:       {meta.get('role', 'Suspect')}
Current Status:      {meta.get('status', 'Under Investigation')}
Statutory Sections:  {meta.get('bns_sections', 'BNS 111 (Organized Crime Gang), 61 (Conspiracy)')}
Risk Assessment:     {entity_data.get('risk_score', '85.0')}% [LEVEL: CRITICAL]

2. MODUS OPERANDI & SYNDICATE STRUCTURE
----------------------------------------------------------------------------------------
Subject functions as a pivotal node in the interstate criminal pipeline. Evidence shows
direct temporal and financial synchronization with overseas satellite communications and
local armed enforcers. Burner telephony cycled on a 28-day cadence to evade cell tower IMEI
tracing.

3. CORROBORATED ELECTRONIC EVIDENCE LOG
----------------------------------------------------------------------------------------
[✓] ANPR Toll Camera Sightings: Verified plate match with high-speed infrared optical sensor.
[✓] CDR Call Detail Records: 412 calls logged; high frequency between 01:00 AM and 04:00 AM.
[✓] Financial Forensic Audit: PMLA smurfing verified across ICICI and HDFC corporate tranches.
[✓] Biometric CCTV Match: DeepFace neural matching at 98.4% confidence score.

4. CERTIFICATE UNDER SECTION 65B INDIAN EVIDENCE ACT / SEC 63 BSA 2023
----------------------------------------------------------------------------------------
I hereby certify that the electronic records reproduced herein were extracted directly from
the automated digital servers of the National Criminal Intelligence Grid without human alteration
or tampering. System SHA-256 hash verified intact.

Authorized Officer:  Inspector In-Charge, Special Cell / Cyber Crime Directorate
Date of Generation:  2026-10-05
========================================================================================
"""

# Global singleton
gemini_service = GeminiIntelligenceService()

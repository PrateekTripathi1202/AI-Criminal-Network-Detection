# AI-Powered Criminal Network Analysis System
### *From Data to Justice: Uncovering hidden connections for a safer and smarter society.*

**Global Innovation Hackathon 2026 – Build for a Better Future**  
**Organized by**: Bharat Academix  
**Theme**: Blockchain & Cybersecurity | **PS Category**: Software  
**Team Name**: EliteCoders  

---

## 📌 Problem Statement

Design and develop an AI-powered system to analyze diverse and fragmented data sources (such as police records, crime reports, financial transactions, call records, social media, and other digital traces) to identify hidden criminal networks, key relationships, and emerging threats, enabling faster, data-driven investigations.

---

## 🌟 Solution Overview

The **AI-Powered Criminal Network Analysis System** connects fragmented, multi-departmental law enforcement intelligence into a unified, high-performance graph intelligence suite. Aligned with the Indian Law-Enforcement Ecosystem (**CCTNS**, **ICJS**, and the **Digital Police Portal**), the platform provides:

1. **Multiple Data Sources Integration**:
   - **People**: Suspect profiles, aliases, biometric records, and syndicate roles.
   - **Documents**: Police FIRs under BNS / IPC, court chargesheets, search seizure memos.
   - **Vehicles**: ANPR toll tracking, vehicle chassis/RC book registries, tinted window violations.
   - **Locations**: GPS traces, crime scene geofences, safehouse meeting points.
   - **Organizations**: Shell companies, bogus MCA registrations, hawala fronts.
   - **Communications (CDR)**: Telecom call detail records, burner phone detection, cell tower triangulation, VoIP traces.
   - **Financial Transactions**: Layering and smurfing analysis across bank accounts and crypto wallets (TRC-20 USDT).
   - **CCTV & Surveillance**: Real-time 4K facial biometrics and automated license plate recognition.

2. **Core Innovations & Uniqueness**:
   - **Explainable AI (XAI)**: Transparent link prediction with feature importance breakdowns and confidence scores.
   - **Cross-Case Discovery**: Automatically correlates disparate FIRs across states (e.g. connecting a Delhi extortion heist to a Mumbai hawala pipeline).
   - **Investigation Memory**: Retains gang modus operandi, syndicate structures, and cold case insights.
   - **Human-in-the-Loop Validation**: Investigators can verify, dismiss, and annotate AI-predicted connections.
   - **Relationship Example Chain (`Slide 2`)**:
     $$\text{Person } 👤 \longrightarrow \text{Phone } 📱 \longrightarrow \text{Vehicle } 🚗 \longrightarrow \text{Account } 💳 \longrightarrow \text{Location } 📍 \longrightarrow \text{CCTV } 🎥$$

---

## 🚀 Key Modules & 3D Visualizations

### 1. 3D WebGL Criminal Knowledge Graph (`Three.js`)
- Full 3D force-directed graph with interactive orbit, zoom, and pan controls.
- Dynamic particle pulses along edges indicating transaction volume and call frequency.
- Node classification by color and 3D geometry (Person, Phone, Vehicle, Account, Org, Location, CCTV).
- Centrality analysis & Kingpin detection via **PageRank** and **Betweenness Centrality**.

### 2. 3D Geospatial Surveillance Radar
- 3D Tactical Globe showing Indian crime corridors (Delhi, Mumbai, Bengaluru, Hyderabad, Kolkata).
- Real-time crime hotspot beacons, active syndicate counts, and inter-state pipeline arcs.

### 3. 3D Relationship Chain Explorer
- Interactive 3D step-through of the 6-stage evidence chain from suspect to biometric CCTV proof.

### 4. CCTV & Computer Vision Suite
- Simulated live video stream with real-time bounding boxes (YOLOv11 / ByteTrack / DeepFace / FastANPR).
- Real-time face matching against CCTNS criminal database and plate recognition.

### 5. Multi-Source Ingestion & OCR Hub
- Standardizes and parses unstructured FIRs, CDR CSV logs, and bank statements using NLP entity extraction.

### 6. AI Case Copilot (LLM / RAG)
- Natural language investigation assistant answering grounded queries with referenced graph entities.

### 7. CCTNS / ICJS Court-Admissible Case Dossier
- Generates section 65B Indian Evidence Act compliant printable dossiers.

---

## 🛠️ Technology Stack

| Layer | Technologies |
|---|---|
| **Backend & Graph Engine** | Python 3.13, FastAPI, NetworkX, Uvicorn, Pydantic |
| **Frontend & 3D Graphics** | React 19, Vite, Three.js (WebGL), Tailwind CSS, Lucide Icons |
| **Computer Vision (Simulated)** | OpenCV, YOLOv11, ByteTrack, DeepFace, FastANPR |
| **Standards & Protocols** | CCTNS, ICJS, Digital Police Portal, Section 65B BSA Compliance |

---

## ⚡ Quick Start & Running Locally

### Prerequisites
- Python 3.10+
- Node.js v18+ and npm

### 1-Click Launch (Windows)
- **PyQt6 Desktop Application (Cyber Command Interface)**: Double-click **`run_pyqt.bat`** (or run `python run_pyqt.py`).
- **Web System (FastAPI + React 3D)**: Double-click **`start_system.bat`**.

### Launching the PyQt6 Desktop Interface
```bash
# Install dependencies
pip install -r backend/requirements.txt

# Run the PyQt6 application
python run_pyqt.py
```

### 🧠 Google Gemini AI Integration
The application uses the official **`google-genai`** SDK with **`gemini-3.8-flash`** (and `gemini-3.1-pro-preview`):
1. **Interactive Case Copilot**: RAG-based criminal interrogation grounded in the active knowledge graph, FIRs, and CDR records.
2. **Multi-Source Ingestion & Evidence OCR**: Automatic entity recognition (NER) extracting suspects, burner SIMs, vehicles, and accounts from raw FIR text.
3. **Court-Admissible Dossier Synthesis**: Automatically formats Section 65B Indian Evidence Act / Section 63 BSA 2023 certified prosecution dossiers.
4. **Bilingual Audio Wiretap Decryption**: Decodes coded gang slang and impending extortion actions from intercepted wiretaps.
5. **Configuring API Key**: Set `GEMINI_API_KEY` in your environment, or click **"⚙️ Gemini Settings"** inside the PyQt interface to configure and test your key directly with 1 click.

---

## 📜 Team Information
- **Hackathon**: Global Innovation Hackathon 2026 – Bharat Academix
- **Team**: EliteCoders
- **Submission Form**: https://forms.gle/Zr6C1DbVQmjXZ1G86

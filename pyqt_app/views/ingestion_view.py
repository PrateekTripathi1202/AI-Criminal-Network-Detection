"""
Multi-Source Document Ingestion & Evidence OCR Hub
Uses Gemini AI to extract structured entities (Persons, Burners, Vehicles, Accounts)
from unstructured police FIRs and CDR logs, and injects them into the Knowledge Graph.
"""

from typing import Dict, Any, List
import uuid
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit,
    QPushButton, QFrame, QScrollArea, QTableWidget, QTableWidgetItem,
    QHeaderView, QMessageBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal

from ..gemini_service import gemini_service
from backend.app.graph_engine import graph_engine

SAMPLE_FIR = """CRIME REGISTER: FIRST INFORMATION REPORT (FIR-2026-DEL-109)
POLICE STATION: Special Cell, Lodhi Colony, New Delhi
DATE OF OCCURRENCE: 2026-09-24 21:15 IST
ACTS & SECTIONS: Bharatiya Nyaya Sanhita (BNS) 111, 308(2), Arms Act Sec 25

STATEMENT OF WITNESS / INFORMANT:
On 24th Sept at approx 21:15 hrs, a black tinted SUV bearing registration DL-04-CA-7711 (Hyundai Verna) was intercepted near Ring Road Dhaula Kuan. The driver was identified as Ravi 'Kalia' Yadav (Age 31, resident of Najafgarh), carrying an unlicensed 9mm semi-automatic pistol. 
Subsequent search revealed a burner handset (+91 97118-XXXX4) with IMEI 864192019284910. Call logs reveal repeated incoming calls from Munna Sharma (+91 98110-XXXX1) ordering delivery of cash extortion proceeds into Axis Bank account #...9921 under bogus company name 'Apex Agro Supplies'."""

SAMPLE_CDR = """CDR TRANSCRIPTION LOG: CELL TOWER DEL-ROH-918
TIMESTAMP,CALLER_MSISDN,CALLEE_MSISDN,DURATION_SEC,IMEI,CELL_TOWER_ID
2026-09-24 01:14:02,+9198110-XXXX1,+9199200-XXXX8,184,864291040182910,DEL-ROH-918
2026-09-24 02:40:19,+9198110-XXXX1,+9197118-XXXX4,55,864291040182910,DEL-ROH-918
2026-09-24 03:02:11,+9197421-XXXX3,+9198110-XXXX1,32,860192849182741,KA-BLR-402"""

class GeminiExtractionThread(QThread):
    result_ready = pyqtSignal(dict)

    def __init__(self, raw_text: str):
        super().__init__()
        self.raw_text = raw_text

    def run(self):
        res = gemini_service.extract_entities_from_text(self.raw_text)
        self.result_ready.emit(res)

class IngestionView(QWidget):
    graph_updated = pyqtSignal() # Emitted when new entities are injected

    def __init__(self, parent=None):
        super().__init__(parent)
        self.extracted_data: Dict[str, Any] = {}
        self._init_ui()

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(18, 16, 18, 16)
        main_layout.setSpacing(12)

        # Header
        header = QHBoxLayout()
        t_box = QVBoxLayout()
        lbl_t = QLabel("MULTI-SOURCE INGESTION & EVIDENCE OCR/NER HUB")
        lbl_t.setStyleSheet("color: #f8fafc; font-size: 16px; font-weight: bold; letter-spacing: 0.5px;")
        t_box.addWidget(lbl_t)

        lbl_s = QLabel("GEMINI AUTOMATED ENTITY EXTRACTION // UNSTRUCTURED POLICE FIRS // CDR LOG STANDARDIZATION")
        lbl_s.setStyleSheet("color: #38bdf8; font-size: 11px; font-weight: 600; letter-spacing: 1px;")
        t_box.addWidget(lbl_s)
        header.addLayout(t_box)

        header.addStretch()

        # Sample Load Buttons
        btn_load_fir = QPushButton("📄 Load Sample FIR")
        btn_load_fir.setProperty("class", "SecondaryButton")
        btn_load_fir.clicked.connect(lambda: self.txt_doc.setPlainText(SAMPLE_FIR))
        header.addWidget(btn_load_fir)

        btn_load_cdr = QPushButton("📱 Load Sample CDR")
        btn_load_cdr.setProperty("class", "SecondaryButton")
        btn_load_cdr.clicked.connect(lambda: self.txt_doc.setPlainText(SAMPLE_CDR))
        header.addWidget(btn_load_cdr)

        main_layout.addLayout(header)

        # Input Text Area
        lbl_in = QLabel("PASTE UNSTRUCTURED POLICE DOCUMENT, FIR, OR TELECOM LOG:")
        lbl_in.setStyleSheet("color: #94a3b8; font-size: 11px; font-weight: bold;")
        main_layout.addWidget(lbl_in)

        self.txt_doc = QTextEdit()
        self.txt_doc.setPlainText(SAMPLE_FIR)
        self.txt_doc.setMinimumHeight(150)
        self.txt_doc.setStyleSheet("background-color: #0b0f19; border: 1px solid #1e293b; color: #f8fafc; font-family: Consolas, monospace; font-size: 12px; line-height: 1.4;")
        main_layout.addWidget(self.txt_doc)

        # Action Row: Extract button
        act_row = QHBoxLayout()
        self.btn_extract = QPushButton("🧠 Extract Criminal Entities & Links with Gemini")
        self.btn_extract.setProperty("class", "PrimaryButton")
        self.btn_extract.clicked.connect(self._run_extraction)
        act_row.addWidget(self.btn_extract)

        act_row.addStretch()

        self.btn_commit = QPushButton("➕ Inject Extracted Entities into Knowledge Graph")
        self.btn_commit.setStyleSheet("background-color: #10b981; color: white; border: 1px solid #34d399; font-weight: bold; padding: 8px 16px; border-radius: 6px;")
        self.btn_commit.setEnabled(False)
        self.btn_commit.clicked.connect(self._commit_to_graph)
        act_row.addWidget(self.btn_commit)

        main_layout.addLayout(act_row)

        # Results Table
        lbl_out = QLabel("GEMINI AI EXTRACTED ENTITIES & PROPOSED RELATIONSHIPS:")
        lbl_out.setStyleSheet("color: #38bdf8; font-size: 12px; font-weight: bold;")
        main_layout.addWidget(lbl_out)

        self.table_results = QTableWidget()
        self.table_results.setColumnCount(5)
        self.table_results.setHorizontalHeaderLabels(["Entity Category", "Identified Name / Label", "Role / Status", "Statutory Sections / IMEI", "Assessed Risk"])
        self.table_results.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_results.setStyleSheet("background-color: #0d1322; border: 1px solid #1e293b; border-radius: 6px;")
        main_layout.addWidget(self.table_results, stretch=1)

    def _run_extraction(self):
        text = self.txt_doc.toPlainText().strip()
        if not text:
            return

        self.btn_extract.setEnabled(False)
        self.btn_commit.setEnabled(False)
        self.table_results.setRowCount(0)

        self.thread = GeminiExtractionThread(text)
        self.thread.result_ready.connect(self._on_extraction_ready)
        self.thread.start()

    def _on_extraction_ready(self, result: Dict[str, Any]):
        self.btn_extract.setEnabled(True)
        self.extracted_data = result
        entities = result.get("entities", [])

        self.table_results.setRowCount(len(entities))
        for row, ent in enumerate(entities):
            e_type = ent.get("type", "entity").upper()
            e_label = ent.get("label", "")
            e_role = ent.get("role", ent.get("make", ""))
            e_sec = ent.get("bns_sections", ent.get("imei", ent.get("owner", "N/A")))
            e_risk = str(ent.get("risk_score", "75.0")) + "%"

            self.table_results.setItem(row, 0, QTableWidgetItem(e_type))
            self.table_results.setItem(row, 1, QTableWidgetItem(e_label))
            self.table_results.setItem(row, 2, QTableWidgetItem(e_role))
            self.table_results.setItem(row, 3, QTableWidgetItem(e_sec))
            self.table_results.setItem(row, 4, QTableWidgetItem(e_risk))

        if entities:
            self.btn_commit.setEnabled(True)
            QMessageBox.information(
                self,
                "Extraction Successful",
                f"Gemini successfully extracted {len(entities)} criminal entities!\n"
                f"Summary: {result.get('executive_summary', 'Extracted successfully.')}"
            )

    def _commit_to_graph(self):
        entities = self.extracted_data.get("entities", [])
        if not entities:
            return

        for ent in entities:
            new_id = f"P-INGEST-{uuid.uuid4().hex[:4].upper()}" if ent.get("type") == "person" else f"ENT-{uuid.uuid4().hex[:4].upper()}"
            node_payload = {
                "id": new_id,
                "label": ent.get("label", "Ingested Entity"),
                "type": ent.get("type", "person"),
                "risk_score": float(ent.get("risk_score", 75.0)),
                "syndicate": "Shadow Syndicate (D-Nexus)",
                "metadata": {
                    "role": ent.get("role", "Extracted from Ingested Doc"),
                    "bns_sections": ent.get("bns_sections", "BNS 111"),
                    "ingested_via": "Gemini 3.8 Flash OCR/NER"
                }
            }
            graph_engine.add_node(node_payload)

            # Link to Rajesh Sharma (P-102) as associate
            edge_payload = {
                "id": f"E-INGEST-{uuid.uuid4().hex[:4].upper()}",
                "source": new_id,
                "target": "P-102",
                "type": "co_accused",
                "weight": 3.5,
                "label": "Extracted Co-Accused Link"
            }
            graph_engine.add_edge(edge_payload)

        self.btn_commit.setEnabled(False)
        self.graph_updated.emit()
        QMessageBox.information(
            self,
            "Graph Updated",
            f"Successfully injected {len(entities)} entities into the active CCTNS Knowledge Graph!\n"
            f"Switch to the 'Knowledge Graph' tab to view them."
        )

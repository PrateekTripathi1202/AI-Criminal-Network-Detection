"""
Cross-Case Discovery & Inter-State Correlation View
Connects disparate FIRs across states to uncover syndicate pipelines.
"""

from typing import Dict, Any, List
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QScrollArea, QTableWidget, QTableWidgetItem, QHeaderView, QTextEdit
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal

from backend.app.ai_intelligence import ai_intelligence
from backend.app.data_store import FIRS_DATA
from ..gemini_service import gemini_service

class GeminiCrossCaseSynthesisThread(QThread):
    result_ready = pyqtSignal(str)

    def __init__(self, correlations: List[Dict[str, Any]]):
        super().__init__()
        self.correlations = correlations

    def run(self):
        prompt = (
            f"You are the Director General of the National Inter-Agency Task Force (NIA / CBI).\n"
            f"Synthesize the following inter-state criminal FIR correlations into an urgent Joint Operation Order:\n"
            f"{self.correlations}\n\n"
            f"Include:\n"
            f"1. Executive Threat Summary & Syndicate Pipeline Architecture\n"
            f"2. Shared Physical & Digital Vectors (Vehicles, Shell Companies, SIM Batches)\n"
            f"3. Coordinated Tri-State Raid & Apprehension Directives (Delhi, Mumbai, Bengaluru)\n"
            f"4. Statutory Seizure Orders under Section 111 Bharatiya Nyaya Sanhita (BNS) & PMLA"
        )
        res = gemini_service.ask_copilot(prompt)
        self.result_ready.emit(res.get("answer", "No response from Gemini."))

class CrossCaseView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.correlations = ai_intelligence.get_cross_case_correlations()
        self._init_ui()

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(18, 16, 18, 16)
        main_layout.setSpacing(14)

        # Header
        header = QHBoxLayout()
        t_box = QVBoxLayout()
        lbl_t = QLabel("CROSS-CASE DISCOVERY & INTER-STATE SYNDICATE CORRELATIONS")
        lbl_t.setStyleSheet("color: #f8fafc; font-size: 16px; font-weight: bold; letter-spacing: 0.5px;")
        t_box.addWidget(lbl_t)

        lbl_s = QLabel("CCTNS NATIONAL REPOSITORY // CROSS-JURISDICTIONAL PATTERN RECOGNITION // ICJS LINK")
        lbl_s.setStyleSheet("color: #38bdf8; font-size: 11px; font-weight: 600; letter-spacing: 1px;")
        t_box.addWidget(lbl_s)
        header.addLayout(t_box)

        header.addStretch()

        self.btn_synthesize = QPushButton("🧠 Synthesize Tri-State Order with Gemini")
        self.btn_synthesize.setProperty("class", "PrimaryButton")
        self.btn_synthesize.clicked.connect(self._synthesize_leads)
        header.addWidget(self.btn_synthesize)

        main_layout.addLayout(header)

        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        # 1. FIR Register Matrix
        table_card = QFrame()
        table_card.setProperty("class", "CardFrame")
        tc_layout = QVBoxLayout(table_card)
        tc_layout.setContentsMargins(14, 14, 14, 14)
        tc_layout.setSpacing(10)

        tc_title = QLabel("PRIMARY POLICE FIRS UNDER ACTIVE CORRELATION")
        tc_title.setStyleSheet("color: #38bdf8; font-weight: bold; font-size: 12px;")
        tc_layout.addWidget(tc_title)

        table = QTableWidget()
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(["FIR Ref", "State / Station", "Date", "Offence Summary", "Accused Suspects"])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.setRowCount(len(FIRS_DATA))
        table.setMinimumHeight(125)

        for row, fir in enumerate(FIRS_DATA):
            table.setItem(row, 0, QTableWidgetItem(fir.get("fir_number", "")))
            table.setItem(row, 1, QTableWidgetItem(f"{fir.get('state')} / {fir.get('police_station')}"))
            table.setItem(row, 2, QTableWidgetItem(fir.get("date", "")))
            table.setItem(row, 3, QTableWidgetItem(fir.get("description", "")[:60] + "..."))
            table.setItem(row, 4, QTableWidgetItem(", ".join(fir.get("accused", []))))

        tc_layout.addWidget(table)
        layout.addWidget(table_card)

        # 2. Correlation Pipeline Cards
        for corr in self.correlations:
            card = QFrame()
            card.setStyleSheet("background-color: #111827; border: 1px solid #1f2937; border-left: 4px solid #0284c7; border-radius: 8px; padding: 14px;")
            c_layout = QVBoxLayout(card)
            c_layout.setSpacing(10)

            # Top row
            head = QHBoxLayout()
            lbl_bridge = QLabel(f"🔗 {corr.get('primary_fir')}  ⟷  {corr.get('secondary_fir')}")
            lbl_bridge.setStyleSheet("color: #f8fafc; font-size: 15px; font-weight: bold;")
            head.addWidget(lbl_bridge)

            head.addStretch()

            lbl_score = QLabel(f"CORRELATION MATCH: {corr.get('correlation_score')}%")
            lbl_score.setProperty("class", "BadgeBlue")
            head.addWidget(lbl_score)
            c_layout.addLayout(head)

            # Modus Operandi Match
            lbl_mo = QLabel(f"<b>Modus Operandi:</b> {corr.get('modus_operandi_match')}")
            lbl_mo.setWordWrap(True)
            lbl_mo.setStyleSheet("color: #cbd5e1; font-size: 12px; background-color: #0b0f19; padding: 8px; border-radius: 4px;")
            c_layout.addWidget(lbl_mo)

            # Shared Threads
            lbl_threads_t = QLabel("SHARED FORENSIC THREADS:")
            lbl_threads_t.setStyleSheet("color: #94a3b8; font-size: 11px; font-weight: bold;")
            c_layout.addWidget(lbl_threads_t)

            for thread in corr.get("shared_threads", []):
                t_lbl = QLabel(f"• <b>[{thread.get('type')}]</b> {thread.get('detail')}")
                t_lbl.setWordWrap(True)
                t_lbl.setStyleSheet("color: #38bdf8; font-size: 12px; margin-left: 6px;")
                c_layout.addWidget(t_lbl)

            # ICJS Recommendation
            rec_lbl = QLabel(f"<b>⚡ ICJS Joint Recommendation:</b> {corr.get('icjs_recommendation')}")
            rec_lbl.setWordWrap(True)
            rec_lbl.setStyleSheet("color: #34d399; font-size: 12px; background-color: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); padding: 8px; border-radius: 4px;")
            c_layout.addWidget(rec_lbl)

            layout.addWidget(card)

        # 3. Gemini Inter-Agency Synthesis Output Area
        self.synth_card = QFrame()
        self.synth_card.setStyleSheet("background-color: #0d1322; border: 1px dashed #38bdf8; border-radius: 8px; padding: 14px;")
        sc_layout = QVBoxLayout(self.synth_card)
        sc_layout.setSpacing(8)

        sc_title = QLabel("🤖 GEMINI TRI-STATE JOINT OPERATION ORDER SYNTHESIS")
        sc_title.setStyleSheet("color: #38bdf8; font-weight: bold; font-size: 12px;")
        sc_layout.addWidget(sc_title)

        self.txt_synth = QTextEdit()
        self.txt_synth.setReadOnly(True)
        self.txt_synth.setPlaceholderText("Click 'Synthesize Tri-State Order with Gemini' to generate formal joint inter-agency directives...")
        self.txt_synth.setMinimumHeight(180)
        self.txt_synth.setStyleSheet("background-color: #070b14; border: 1px solid #1e293b; color: #f1f5f9; font-size: 12px; line-height: 1.4;")
        sc_layout.addWidget(self.txt_synth)

        layout.addWidget(self.synth_card)

        scroll.setWidget(container)
        main_layout.addWidget(scroll)

    def _synthesize_leads(self):
        self.btn_synthesize.setEnabled(False)
        self.txt_synth.setPlainText("⏳ Analyzing cross-case correlations using Google Gemini 3.8 Flash...")

        self.thread = GeminiCrossCaseSynthesisThread(self.correlations)
        self.thread.result_ready.connect(self._on_synthesis_ready)
        self.thread.start()

    def _on_synthesis_ready(self, output: str):
        self.btn_synthesize.setEnabled(True)
        self.txt_synth.setPlainText(output)

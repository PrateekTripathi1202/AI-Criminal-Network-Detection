"""
Dashboard / Command Center View
Overview of active syndicates, tracked nodes, threat tickers, and quick actions.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel,
    QPushButton, QFrame, QScrollArea, QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QColor

from ..widgets.metric_card import MetricCard
from backend.app.data_store import INITIAL_NODES, INITIAL_EDGES, FIRS_DATA

class DashboardView(QWidget):
    navigate_to = pyqtSignal(str) # Emits view name (e.g. 'graph', 'copilot', etc.)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(18)

        # Header Title Banner
        header = QHBoxLayout()
        title_box = QVBoxLayout()
        title_box.setSpacing(2)

        lbl_title = QLabel("CENTRAL INTELLIGENCE COMMAND GRID")
        lbl_title.setStyleSheet("color: #f8fafc; font-size: 20px; font-weight: 800; letter-spacing: 0.5px;")
        title_box.addWidget(lbl_title)

        lbl_sub = QLabel("NATIONAL CRIME RECORDS BUREAU // CCTNS 4.0 INTEGRATION // REAL-TIME SURVEILLANCE")
        lbl_sub.setStyleSheet("color: #38bdf8; font-size: 11px; font-weight: 600; letter-spacing: 1px;")
        title_box.addWidget(lbl_sub)
        header.addLayout(title_box)

        header.addStretch()

        btn_ai_copilot = QPushButton("💬 Launch Gemini Copilot")
        btn_ai_copilot.setProperty("class", "PrimaryButton")
        btn_ai_copilot.clicked.connect(lambda: self.navigate_to.emit("copilot"))
        header.addWidget(btn_ai_copilot)

        main_layout.addLayout(header)

        # Scrollable content area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")
        
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)

        # 1. Top Metrics KPI Grid
        kpi_grid = QHBoxLayout()
        kpi_grid.setSpacing(14)

        card_nodes = MetricCard("Tracked Entities", str(len(INITIAL_NODES)), "18 Interconnected Nodes", "ONLINE", "blue", "🕸️")
        kpi_grid.addWidget(card_nodes)

        card_syndicates = MetricCard("Active Syndicates", "3", "D-Nexus, Hawala, Cyber09", "CRITICAL", "red", "☠️")
        kpi_grid.addWidget(card_syndicates)

        card_funds = MetricCard("Flagged Smurfing", "₹ 12.8 Cr", "48 Hawala Tranches + USDT", "PMLA ALERT", "amber", "💳")
        kpi_grid.addWidget(card_funds)

        card_wiretaps = MetricCard("Audio Intercepts", "2 ACTIVE", "Delhi-Mumbai-BLR Triangulation", "WIRETAP", "purple", "📡")
        kpi_grid.addWidget(card_wiretaps)

        card_threat = MetricCard("Syndicate Threat", "96.5%", "High Risk of Armed Action", "LEVEL 5", "red", "🚨")
        kpi_grid.addWidget(card_threat)

        layout.addLayout(kpi_grid)

        # 2. Middle Row: Active Syndicates & Quick Tactical Actions
        mid_row = QHBoxLayout()
        mid_row.setSpacing(16)

        # Left: Active Syndicates Box
        syndicates_frame = QFrame()
        syndicates_frame.setProperty("class", "CardFrame")
        syndicates_layout = QVBoxLayout(syndicates_frame)
        syndicates_layout.setContentsMargins(16, 16, 16, 16)
        syndicates_layout.setSpacing(12)

        syn_header = QHBoxLayout()
        syn_title = QLabel("ACTIVE CRIMINAL SYNDICATES (INTER-STATE)")
        syn_title.setStyleSheet("color: #38bdf8; font-weight: bold; font-size: 13px;")
        syn_header.addWidget(syn_title)
        syn_header.addStretch()
        syn_badge = QLabel("3 ORGANIZATIONS")
        syn_badge.setProperty("class", "BadgeRed")
        syn_header.addWidget(syn_badge)
        syndicates_layout.addLayout(syn_header)

        # Syndicate items
        syndicates = [
            ("Shadow Syndicate (D-Nexus)", "Kingpin: Vikram Malhotra | Role: Arms, Extortion, Corporate Intimidation", "Delhi - Mumbai - Dubai", "#ef4444"),
            ("Hawala Nexus", "Directors: Pooja Deshmukh, Rajesh Sharma | Role: Shell Layering & PMLA Evasion", "Mumbai (BKC) - Surat", "#f59e0b"),
            ("Cyber-Cartel 09", "Tech Leads: Sameer Khan, Karan Bansal | Role: Aadhaar Cloned SIMs & Crypto Offramps", "Bengaluru - Gurugram", "#0ea5e9")
        ]

        for s_name, s_role, s_corr, s_color in syndicates:
            item_frame = QFrame()
            item_frame.setStyleSheet(f"background-color: #0b0f19; border: 1px solid #1e293b; border-left: 3px solid {s_color}; border-radius: 6px; padding: 8px 12px;")
            i_layout = QVBoxLayout(item_frame)
            i_layout.setContentsMargins(6, 6, 6, 6)
            i_layout.setSpacing(4)

            top = QHBoxLayout()
            name_lbl = QLabel(s_name)
            name_lbl.setStyleSheet("color: #f8fafc; font-weight: bold; font-size: 13px;")
            top.addWidget(name_lbl)
            top.addStretch()
            corr_lbl = QLabel(f"📍 {s_corr}")
            corr_lbl.setStyleSheet("color: #94a3b8; font-size: 11px;")
            top.addWidget(corr_lbl)
            i_layout.addLayout(top)

            role_lbl = QLabel(s_role)
            role_lbl.setStyleSheet("color: #64748b; font-size: 11px;")
            i_layout.addWidget(role_lbl)

            syndicates_layout.addWidget(item_frame)

        mid_row.addWidget(syndicates_frame, stretch=3)

        # Right: Quick Tactical Actions & Intelligence Summary
        actions_frame = QFrame()
        actions_frame.setProperty("class", "CardFrame")
        actions_layout = QVBoxLayout(actions_frame)
        actions_layout.setContentsMargins(16, 16, 16, 16)
        actions_layout.setSpacing(10)

        act_title = QLabel("TACTICAL ACTIONS & AI MODULES")
        act_title.setStyleSheet("color: #38bdf8; font-weight: bold; font-size: 13px;")
        actions_layout.addWidget(act_title)

        # Action Buttons
        btn_graph = QPushButton("🕸️ Open Interactive Knowledge Graph")
        btn_graph.setProperty("class", "SecondaryButton")
        btn_graph.clicked.connect(lambda: self.navigate_to.emit("graph"))
        actions_layout.addWidget(btn_graph)

        btn_xai = QPushButton("🔍 Explainable AI (XAI) Link Predictions")
        btn_xai.setProperty("class", "SecondaryButton")
        btn_xai.clicked.connect(lambda: self.navigate_to.emit("xai"))
        actions_layout.addWidget(btn_xai)

        btn_cctv = QPushButton("🎥 Live CCTV & ANPR Surveillance Grid")
        btn_cctv.setProperty("class", "SecondaryButton")
        btn_cctv.clicked.connect(lambda: self.navigate_to.emit("surveillance"))
        actions_layout.addWidget(btn_cctv)

        btn_cross = QPushButton("📁 Inter-State Cross-Case Discovery")
        btn_cross.setProperty("class", "SecondaryButton")
        btn_cross.clicked.connect(lambda: self.navigate_to.emit("cross_case"))
        actions_layout.addWidget(btn_cross)

        btn_dossier = QPushButton("📄 Court-Admissible Dossier Generator")
        btn_dossier.setProperty("class", "SecondaryButton")
        btn_dossier.clicked.connect(lambda: self.navigate_to.emit("dossier"))
        actions_layout.addWidget(btn_dossier)

        mid_row.addWidget(actions_frame, stretch=2)

        layout.addLayout(mid_row)

        # 3. Bottom Table: Live Multi-State Intelligence Feed / Cases
        cases_frame = QFrame()
        cases_frame.setProperty("class", "CardFrame")
        cases_layout = QVBoxLayout(cases_frame)
        cases_layout.setContentsMargins(16, 16, 16, 16)
        cases_layout.setSpacing(10)

        c_header = QHBoxLayout()
        cases_title = QLabel("INTER-STATE CRIME REGISTER (CCTNS / ICJS LINKAGES)")
        cases_title.setStyleSheet("color: #38bdf8; font-weight: bold; font-size: 13px;")
        c_header.addWidget(cases_title)
        c_header.addStretch()
        cases_badge = QLabel("3 PRIMARY FIRS")
        cases_badge.setProperty("class", "BadgeBlue")
        c_header.addWidget(cases_badge)
        cases_layout.addLayout(c_header)

        table = QTableWidget()
        table.setColumnCount(6)
        table.setHorizontalHeaderLabels(["FIR Number", "Jurisdiction / Police Station", "Offence / Statutory Sections", "Prime Accused", "Status", "Cross-Case Match"])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.setRowCount(len(FIRS_DATA))
        table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        table.setMinimumHeight(140)

        for row, fir in enumerate(FIRS_DATA):
            table.setItem(row, 0, QTableWidgetItem(fir.get("fir_number", "")))
            table.setItem(row, 1, QTableWidgetItem(fir.get("police_station", "")))
            table.setItem(row, 2, QTableWidgetItem(fir.get("sections", "")))
            accused_list = ", ".join(fir.get("accused", []))
            table.setItem(row, 3, QTableWidgetItem(accused_list))
            table.setItem(row, 4, QTableWidgetItem(fir.get("status", "")))
            table.setItem(row, 5, QTableWidgetItem("CORRELATED (Apex Impex)" if row == 0 else "CORRELATED (Burner IMEI)"))

        cases_layout.addWidget(table)
        layout.addWidget(cases_frame)

        scroll.setWidget(container)
        main_layout.addWidget(scroll)

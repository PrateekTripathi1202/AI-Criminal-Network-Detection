"""
Master Application Window for National Criminal Intelligence System (NCIS)
PyQt6 Cyber Command Interface with Google Gemini 3.8 Flash Integration.
"""

import sys
import time
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame, QStackedWidget, QStatusBar,
    QButtonGroup
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIcon, QFont

from .theme import CYBER_THEME
from .gemini_service import gemini_service
from .dialogs.api_settings_dialog import GeminiSettingsDialog
from .views.dashboard_view import DashboardView
from .views.graph_view import GraphView
from .views.copilot_view import CopilotView
from .views.xai_view import XAIView
from .views.cross_case_view import CrossCaseView
from .views.surveillance_view import SurveillanceView
from .views.ingestion_view import IngestionView
from .views.dossier_view import DossierView

class NCISMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NATIONAL CRIMINAL INTELLIGENCE SYSTEM (NCIS) - CCTNS 4.0 // ELITECODERS")
        self.resize(1400, 880)
        self.setMinimumSize(1150, 720)

        self._init_ui()
        self._init_timer()

    def _init_ui(self):
        # Master central widget
        central = QWidget()
        self.setCentralWidget(central)
        root_layout = QHBoxLayout(central)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # 1. Left Navigation Sidebar
        sidebar = self._build_sidebar()
        root_layout.addWidget(sidebar)

        # 2. Main Content Area (Header + Stacked Views)
        content_frame = QFrame()
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # Top Header
        header = self._build_header()
        content_layout.addWidget(header)

        # Stacked Widget for Views
        self.stack = QStackedWidget()
        self.stack.setStyleSheet("background-color: #0b0f19;")

        self.view_dashboard = DashboardView()
        self.view_graph = GraphView()
        self.view_copilot = CopilotView()
        self.view_xai = XAIView()
        self.view_cross = CrossCaseView()
        self.view_surveillance = SurveillanceView()
        self.view_ingestion = IngestionView()
        self.view_dossier = DossierView()

        # Connect inter-view signals
        self.view_dashboard.navigate_to.connect(self._switch_to_view_by_name)
        self.view_graph.ask_gemini_entity.connect(self._on_graph_ask_gemini)
        self.view_ingestion.graph_updated.connect(self._on_graph_updated)

        # Add to stack
        self.stack.addWidget(self.view_dashboard)    # 0
        self.stack.addWidget(self.view_graph)        # 1
        self.stack.addWidget(self.view_copilot)      # 2
        self.stack.addWidget(self.view_xai)          # 3
        self.stack.addWidget(self.view_cross)        # 4
        self.stack.addWidget(self.view_surveillance) # 5
        self.stack.addWidget(self.view_ingestion)    # 6
        self.stack.addWidget(self.view_dossier)      # 7

        content_layout.addWidget(self.stack, stretch=1)
        root_layout.addWidget(content_frame, stretch=1)

        # Status Bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("🟢 CCTNS Grid Online | ICJS Integration: ACTIVE | Encryption: AES-256-GCM | Node Count: 18 Entities")

    def _build_sidebar(self) -> QFrame:
        sidebar = QFrame()
        sidebar.setObjectName("SidebarFrame")
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(14, 18, 14, 18)
        layout.setSpacing(8)

        # Emblem & Branding
        brand_box = QVBoxLayout()
        brand_box.setSpacing(2)

        lbl_emblem = QLabel("🛡️ CCTNS 4.0")
        lbl_emblem.setObjectName("SidebarTitle")
        brand_box.addWidget(lbl_emblem)

        lbl_sub = QLabel("CRIMINAL INTELLIGENCE GRID")
        lbl_sub.setObjectName("SidebarSubtitle")
        brand_box.addWidget(lbl_sub)

        layout.addLayout(brand_box)
        layout.addSpacing(16)

        # Nav Buttons Group
        self.nav_group = QButtonGroup(self)
        self.nav_group.setExclusive(True)

        nav_items = [
            ("📊 Dashboard & Command", 0),
            ("🕸️ Tactical Knowledge Graph", 1),
            ("🤖 Gemini Case Copilot", 2),
            ("🔍 Explainable AI (XAI)", 3),
            ("📁 Cross-Case Discovery", 4),
            ("🎥 Surveillance & Wiretaps", 5),
            ("📥 Ingestion & OCR Hub", 6),
            ("📄 Court Dossier (Sec 65B)", 7)
        ]

        self.nav_buttons = []
        for text, index in nav_items:
            btn = QPushButton(text)
            btn.setProperty("class", "NavButton")
            btn.setCheckable(True)
            if index == 0:
                btn.setChecked(True)
            btn.clicked.connect(lambda checked, idx=index: self._switch_view(idx))
            self.nav_group.addButton(btn)
            self.nav_buttons.append(btn)
            layout.addWidget(btn)

        layout.addStretch()

        # Bottom System Card
        sys_card = QFrame()
        sys_card.setStyleSheet("background-color: #0b0f19; border: 1px solid #1e293b; border-radius: 6px; padding: 10px;")
        sc_layout = QVBoxLayout(sys_card)
        sc_layout.setSpacing(4)

        lbl_sec = QLabel("CLEARANCE: LEVEL 5 TOP SECRET")
        lbl_sec.setStyleSheet("color: #ef4444; font-size: 10px; font-weight: bold;")
        sc_layout.addWidget(lbl_sec)

        self.lbl_gemini_side = QLabel(f"🧠 {gemini_service.current_model}")
        self.lbl_gemini_side.setStyleSheet("color: #38bdf8; font-size: 11px; font-weight: 600;")
        sc_layout.addWidget(self.lbl_gemini_side)

        btn_settings = QPushButton("⚙️ Gemini Settings")
        btn_settings.setProperty("class", "SecondaryButton")
        btn_settings.clicked.connect(self._open_settings)
        sc_layout.addWidget(btn_settings)

        layout.addWidget(sys_card)
        return sidebar

    def _build_header(self) -> QFrame:
        header = QFrame()
        header.setObjectName("HeaderFrame")
        layout = QHBoxLayout(header)
        layout.setContentsMargins(18, 10, 18, 10)
        layout.setSpacing(14)

        # Header Titles
        t_box = QVBoxLayout()
        t_box.setSpacing(2)

        lbl_agency = QLabel("GOVERNMENT OF INDIA // MINISTRY OF HOME AFFAIRS")
        lbl_agency.setObjectName("HeaderSubtitle")
        t_box.addWidget(lbl_agency)

        lbl_sys = QLabel("AI-POWERED CRIMINAL NETWORK ANALYSIS SYSTEM (ELITECODERS)")
        lbl_sys.setObjectName("HeaderTitle")
        t_box.addWidget(lbl_sys)

        layout.addLayout(t_box)
        layout.addStretch()

        # Live Clock
        self.lbl_clock = QLabel("")
        self.lbl_clock.setStyleSheet("color: #94a3b8; font-family: Consolas, monospace; font-size: 12px; font-weight: 600;")
        layout.addWidget(self.lbl_clock)

        # Status Pill
        self.lbl_header_status = QLabel("🟢 GEMINI ACTIVE" if gemini_service.is_configured() else "🟡 DEMO INTELLIGENCE MODE")
        self.lbl_header_status.setProperty("class", "BadgeGreen" if gemini_service.is_configured() else "BadgeAmber")
        layout.addWidget(self.lbl_header_status)

        return header

    def _init_timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_clock)
        self.timer.start(1000)
        self._update_clock()

    def _update_clock(self):
        now_str = time.strftime("%Y-%m-%d  •  %H:%M:%S IST")
        self.lbl_clock.setText(f"🕒 {now_str}")

    def _switch_view(self, index: int):
        self.stack.setCurrentIndex(index)
        if 0 <= index < len(self.nav_buttons):
            self.nav_buttons[index].setChecked(True)

    def _switch_to_view_by_name(self, name: str):
        mapping = {
            "dashboard": 0,
            "graph": 1,
            "copilot": 2,
            "xai": 3,
            "cross_case": 4,
            "surveillance": 5,
            "ingestion": 6,
            "dossier": 7
        }
        idx = mapping.get(name, 0)
        self._switch_view(idx)

    def _on_graph_ask_gemini(self, node_data: dict):
        # Switch to Copilot view and prefill inquiry
        self._switch_view(2)
        self.view_copilot.prefill_entity_query(node_data)

    def _on_graph_updated(self):
        from backend.app.data_store import INITIAL_NODES, INITIAL_EDGES
        from backend.app.graph_engine import graph_engine
        # Reload graph view canvas
        self.view_graph.canvas.populate_graph(graph_engine.nodes, graph_engine.edges)

    def _open_settings(self):
        dlg = GeminiSettingsDialog(self)
        if dlg.exec():
            # Update indicators
            is_active = gemini_service.is_configured()
            self.lbl_header_status.setText("🟢 GEMINI ACTIVE" if is_active else "🟡 DEMO INTELLIGENCE MODE")
            self.lbl_header_status.setProperty("class", "BadgeGreen" if is_active else "BadgeAmber")
            self.lbl_header_status.style().unpolish(self.lbl_header_status)
            self.lbl_header_status.style().polish(self.lbl_header_status)

            self.lbl_gemini_side.setText(f"🧠 {gemini_service.current_model}")
            self.view_copilot._update_model_status()

def run_app():
    app = QApplication(sys.argv)
    app.setStyleSheet(CYBER_THEME)
    window = NCISMainWindow()
    window.show()
    return app.exec()

if __name__ == "__main__":
    sys.exit(run_app())

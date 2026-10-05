"""
Graph Visualizer View
Interactive Knowledge Graph with filter bar and Entity Inspector panel.
"""

from typing import Dict, Any, List
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QComboBox, QPushButton, QFrame, QSplitter, QScrollArea,
    QProgressBar, QListWidget, QListWidgetItem
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from ..widgets.graph_canvas import CriminalGraphCanvas
from backend.app.data_store import INITIAL_NODES, INITIAL_EDGES
from backend.app.graph_engine import graph_engine

class GraphView(QWidget):
    ask_gemini_entity = pyqtSignal(dict) # Emits node_data to interrogate with Copilot

    def __init__(self, parent=None):
        super().__init__(parent)
        self.all_nodes = INITIAL_NODES
        self.all_edges = INITIAL_EDGES
        self.selected_node: Dict[str, Any] = None
        self._init_ui()

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(12)

        # 1. Top Filters & Search Bar
        filter_bar = QHBoxLayout()
        filter_bar.setSpacing(10)

        # Search field
        self.txt_search = QLineEdit()
        self.txt_search.setPlaceholderText("🔍 Search entity by name, ID, alias, IMEI, or plate...")
        self.txt_search.textChanged.connect(self._apply_filters)
        filter_bar.addWidget(self.txt_search, stretch=2)

        # Type filter
        lbl_type = QLabel("Type:")
        lbl_type.setStyleSheet("color: #94a3b8; font-weight: bold;")
        filter_bar.addWidget(lbl_type)

        self.cmb_type = QComboBox()
        self.cmb_type.addItems(["All Types", "Person", "Phone", "Vehicle", "Account", "Organization", "Location", "CCTV"])
        self.cmb_type.currentTextChanged.connect(self._apply_filters)
        filter_bar.addWidget(self.cmb_type)

        # Syndicate filter
        lbl_syn = QLabel("Syndicate:")
        lbl_syn.setStyleSheet("color: #94a3b8; font-weight: bold;")
        filter_bar.addWidget(lbl_syn)

        self.cmb_syndicate = QComboBox()
        self.cmb_syndicate.addItems(["All Syndicates", "Shadow Syndicate (D-Nexus)", "Hawala Nexus", "Cyber-Cartel 09"])
        self.cmb_syndicate.currentTextChanged.connect(self._apply_filters)
        filter_bar.addWidget(self.cmb_syndicate)

        # Reset button
        btn_reset = QPushButton("Reset Filters")
        btn_reset.setProperty("class", "SecondaryButton")
        btn_reset.clicked.connect(self._reset_filters)
        filter_bar.addWidget(btn_reset)

        main_layout.addLayout(filter_bar)

        # 2. Main Content Splitter: Graph Canvas on Left, Entity Inspector on Right
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setStyleSheet("""
            QSplitter::handle {
                background-color: #1e293b;
                width: 2px;
            }
        """)

        # Left: Graph Canvas
        self.canvas = CriminalGraphCanvas()
        self.canvas.node_selected.connect(self._on_node_selected)
        splitter.addWidget(self.canvas)

        # Right: Entity Inspector Panel
        self.inspector_panel = self._build_inspector_panel()
        splitter.addWidget(self.inspector_panel)
        splitter.setStretchFactor(0, 7)
        splitter.setStretchFactor(1, 3)

        main_layout.addWidget(splitter)

        # Initial graph load
        self.canvas.populate_graph(self.all_nodes, self.all_edges)

        # Default select Kingpin (Vikram Malhotra)
        kingpin = next((n for n in self.all_nodes if n.get("id") == "P-101"), None)
        if kingpin:
            self._on_node_selected(kingpin)

    def _build_inspector_panel(self) -> QFrame:
        frame = QFrame()
        frame.setStyleSheet("background-color: #0f172a; border-left: 1px solid #1e293b; border-radius: 8px;")
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(12)

        # Panel Title
        p_title = QLabel("ENTITY INTELLIGENCE DOSSIER")
        p_title.setStyleSheet("color: #38bdf8; font-weight: bold; font-size: 12px; letter-spacing: 0.5px;")
        layout.addWidget(p_title)

        # Entity Header Card
        self.header_card = QFrame()
        self.header_card.setStyleSheet("background-color: #131b2e; border: 1px solid #1e293b; border-radius: 6px; padding: 10px;")
        h_layout = QVBoxLayout(self.header_card)
        h_layout.setSpacing(4)

        self.lbl_node_name = QLabel("Select an Entity Node")
        self.lbl_node_name.setStyleSheet("color: #f8fafc; font-size: 15px; font-weight: bold;")
        h_layout.addWidget(self.lbl_node_name)

        self.lbl_node_id_type = QLabel("ID: -- | TYPE: --")
        self.lbl_node_id_type.setStyleSheet("color: #0ea5e9; font-size: 11px; font-weight: 600;")
        h_layout.addWidget(self.lbl_node_id_type)

        layout.addWidget(self.header_card)

        # Risk Score Section
        risk_box = QVBoxLayout()
        risk_box.setSpacing(4)
        r_head = QHBoxLayout()
        lbl_r_title = QLabel("CCTNS RISK SCORE:")
        lbl_r_title.setStyleSheet("color: #94a3b8; font-size: 11px; font-weight: bold;")
        r_head.addWidget(lbl_r_title)
        r_head.addStretch()
        self.lbl_risk_val = QLabel("0.0%")
        self.lbl_risk_val.setStyleSheet("color: #ef4444; font-weight: bold;")
        r_head.addWidget(self.lbl_risk_val)
        risk_box.addLayout(r_head)

        self.progress_risk = QProgressBar()
        self.progress_risk.setRange(0, 100)
        self.progress_risk.setValue(50)
        risk_box.addWidget(self.progress_risk)
        layout.addLayout(risk_box)

        # Metadata Details (Scrollable)
        lbl_meta = QLabel("FORENSIC RECORD PARTICULARS")
        lbl_meta.setStyleSheet("color: #94a3b8; font-size: 11px; font-weight: bold;")
        layout.addWidget(lbl_meta)

        scroll_meta = QScrollArea()
        scroll_meta.setWidgetResizable(True)
        scroll_meta.setStyleSheet("border: 1px solid #1e293b; background-color: #0d1322; border-radius: 6px;")
        
        self.meta_container = QWidget()
        self.meta_layout = QVBoxLayout(self.meta_container)
        self.meta_layout.setContentsMargins(10, 10, 10, 10)
        self.meta_layout.setSpacing(6)
        scroll_meta.setWidget(self.meta_container)
        layout.addWidget(scroll_meta, stretch=1)

        # Connected Neighbors List
        lbl_conn = QLabel("CONNECTED CRIMINAL RELATIONSHIPS")
        lbl_conn.setStyleSheet("color: #94a3b8; font-size: 11px; font-weight: bold;")
        layout.addWidget(lbl_conn)

        self.list_connections = QListWidget()
        self.list_connections.setStyleSheet("""
            QListWidget {
                background-color: #0d1322;
                border: 1px solid #1e293b;
                border-radius: 6px;
                color: #cbd5e1;
                font-size: 11px;
            }
            QListWidget::item {
                padding: 6px;
                border-bottom: 1px solid #162032;
            }
            QListWidget::item:hover {
                background-color: #1e293b;
            }
        """)
        layout.addWidget(self.list_connections, stretch=1)

        # Button: Gemini Interrogation
        self.btn_gemini_ask = QPushButton("🤖 Deep Interrogate with Gemini")
        self.btn_gemini_ask.setProperty("class", "PrimaryButton")
        self.btn_gemini_ask.clicked.connect(self._on_ask_gemini_clicked)
        layout.addWidget(self.btn_gemini_ask)

        return frame

    def _on_node_selected(self, node: Dict[str, Any]):
        self.selected_node = node
        name = node.get("label", node.get("id"))
        node_id = node.get("id", "")
        node_type = node.get("type", "").upper()
        risk = node.get("risk_score", 50.0)

        self.lbl_node_name.setText(name)
        self.lbl_node_id_type.setText(f"ID: {node_id}  |  CATEGORY: {node_type}")
        self.lbl_risk_val.setText(f"{risk}%")
        self.progress_risk.setValue(int(risk))

        # Color progress bar based on risk
        if risk > 80:
            self.lbl_risk_val.setStyleSheet("color: #ef4444; font-weight: bold;")
            self.progress_risk.setStyleSheet("QProgressBar::chunk { background-color: #ef4444; }")
        elif risk > 65:
            self.lbl_risk_val.setStyleSheet("color: #f59e0b; font-weight: bold;")
            self.progress_risk.setStyleSheet("QProgressBar::chunk { background-color: #f59e0b; }")
        else:
            self.lbl_risk_val.setStyleSheet("color: #10b981; font-weight: bold;")
            self.progress_risk.setStyleSheet("QProgressBar::chunk { background-color: #10b981; }")

        # Clear and repopulate metadata
        for i in reversed(range(self.meta_layout.count())): 
            widget = self.meta_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        # Add syndicate
        if node.get("syndicate"):
            self._add_meta_row("Syndicate Affiliation", node.get("syndicate"), "#38bdf8")

        metadata = node.get("metadata", {})
        for k, v in metadata.items():
            if k == "avatar":
                continue
            formatted_key = k.replace("_", " ").title()
            self._add_meta_row(formatted_key, str(v))

        # Populate connected edges
        self.list_connections.clear()
        for e in self.all_edges:
            if e.get("source") == node_id:
                target_node = next((n for n in self.all_nodes if n.get("id") == e.get("target")), None)
                tgt_name = target_node.get("label", e.get("target")) if target_node else e.get("target")
                rel = e.get("label") or e.get("type")
                self.list_connections.addItem(f"➔ {rel} ➔ {tgt_name}")
            elif e.get("target") == node_id:
                source_node = next((n for n in self.all_nodes if n.get("id") == e.get("source")), None)
                src_name = source_node.get("label", e.get("source")) if source_node else e.get("source")
                rel = e.get("label") or e.get("type")
                self.list_connections.addItem(f"⬅ (Target of: {rel}) ⬅ {src_name}")

    def _add_meta_row(self, key: str, val: str, val_color: str = "#f1f5f9"):
        row = QHBoxLayout()
        row.setSpacing(4)
        k_lbl = QLabel(f"{key}:")
        k_lbl.setStyleSheet("color: #64748b; font-size: 11px; font-weight: 600;")
        row.addWidget(k_lbl)
        
        v_lbl = QLabel(val)
        v_lbl.setWordWrap(True)
        v_lbl.setStyleSheet(f"color: {val_color}; font-size: 11px; font-weight: 500;")
        row.addWidget(v_lbl, stretch=1)
        self.meta_layout.addLayout(row)

    def _apply_filters(self):
        query = self.txt_search.text().lower().strip()
        type_filter = self.cmb_type.currentText().lower()
        syn_filter = self.cmb_syndicate.currentText()

        filtered_nodes = []
        for n in self.all_nodes:
            # 1. Type check
            if type_filter != "all types" and n.get("type") != type_filter:
                continue
            # 2. Syndicate check
            if syn_filter != "All Syndicates" and n.get("syndicate") != syn_filter:
                continue
            # 3. Text search
            if query:
                text_match = (
                    query in n.get("label", "").lower() or
                    query in n.get("id", "").lower() or
                    query in str(n.get("metadata", {})).lower()
                )
                if not text_match:
                    continue
            filtered_nodes.append(n)

        # Edges among filtered nodes
        filtered_ids = {n["id"] for n in filtered_nodes}
        filtered_edges = [
            e for e in self.all_edges
            if e.get("source") in filtered_ids and e.get("target") in filtered_ids
        ]

        self.canvas.populate_graph(filtered_nodes, filtered_edges)

    def _reset_filters(self):
        self.txt_search.clear()
        self.cmb_type.setCurrentIndex(0)
        self.cmb_syndicate.setCurrentIndex(0)
        self.canvas.populate_graph(self.all_nodes, self.all_edges)

    def _on_ask_gemini_clicked(self):
        if self.selected_node:
            self.ask_gemini_entity.emit(self.selected_node)

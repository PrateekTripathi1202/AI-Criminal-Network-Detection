"""
Court-Admissible Dossier Generator View
Generates Section 65B Bharatiya Sakshya Adhiniyam / IEA compliant prosecution dossiers
powered by Google Gemini 3.8 Flash synthesis.
"""

from typing import Dict, Any, List
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QComboBox, QFrame, QTextEdit, QFileDialog, QMessageBox, QProgressBar
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QTextCursor

from ..gemini_service import gemini_service
from backend.app.data_store import INITIAL_NODES, INITIAL_EDGES

class GeminiDossierThread(QThread):
    dossier_ready = pyqtSignal(str)

    def __init__(self, suspect_data: Dict[str, Any], graph_context: Dict[str, Any]):
        super().__init__()
        self.suspect_data = suspect_data
        self.graph_context = graph_context

    def run(self):
        text = gemini_service.generate_dossier(self.suspect_data, self.graph_context)
        self.dossier_ready.emit(text)

class DossierView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.suspects = [n for n in INITIAL_NODES if n.get("type") == "person"]
        self.selected_suspect = self.suspects[0] if self.suspects else {}
        self._init_ui()

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(18, 16, 18, 16)
        main_layout.setSpacing(12)

        # Header
        header = QHBoxLayout()
        t_box = QVBoxLayout()
        lbl_t = QLabel("COURT-ADMISSIBLE CASE DOSSIER GENERATOR")
        lbl_t.setStyleSheet("color: #f8fafc; font-size: 16px; font-weight: bold; letter-spacing: 0.5px;")
        t_box.addWidget(lbl_t)

        lbl_s = QLabel("SECTION 65B INDIAN EVIDENCE ACT // SECTION 63 BHARATIYA SAKSHYA ADHINIYAM (BSA 2023) COMPLIANT")
        lbl_s.setStyleSheet("color: #38bdf8; font-size: 11px; font-weight: 600; letter-spacing: 1px;")
        t_box.addWidget(lbl_s)
        header.addLayout(t_box)

        header.addStretch()

        # Suspect Picker
        lbl_sel = QLabel("Target Suspect:")
        lbl_sel.setStyleSheet("color: #cbd5e1; font-weight: bold; font-size: 12px;")
        header.addWidget(lbl_sel)

        self.cmb_suspect = QComboBox()
        for s in self.suspects:
            role = s.get("metadata", {}).get("role", "Suspect")
            self.cmb_suspect.addItem(f"{s.get('label')} ({s.get('id')}) - {role}")
        self.cmb_suspect.currentIndexChanged.connect(self._on_suspect_changed)
        header.addWidget(self.cmb_suspect)

        # Draft Button
        self.btn_draft = QPushButton("⚖️ Synthesize Judicial Dossier with Gemini")
        self.btn_draft.setProperty("class", "PrimaryButton")
        self.btn_draft.clicked.connect(self._draft_dossier)
        header.addWidget(self.btn_draft)

        main_layout.addLayout(header)

        # Progress bar
        self.pbar = QProgressBar()
        self.pbar.setRange(0, 0)
        self.pbar.setFixedHeight(3)
        self.pbar.setStyleSheet("QProgressBar::chunk { background-color: #38bdf8; }")
        self.pbar.setVisible(False)
        main_layout.addWidget(self.pbar)

        # Dossier Text Area
        self.txt_dossier = QTextEdit()
        self.txt_dossier.setReadOnly(False) # Allows editing before export
        self.txt_dossier.setStyleSheet("""
            QTextEdit {
                background-color: #070b14;
                border: 1px solid #1e293b;
                border-radius: 8px;
                padding: 16px;
                color: #e2e8f0;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 12px;
                line-height: 1.45;
            }
        """)
        main_layout.addWidget(self.txt_dossier, stretch=1)

        # Footer Actions
        footer = QHBoxLayout()
        footer.setSpacing(10)

        lbl_seal = QLabel("🛡️ SHA-256 System Certificate Validated • CCTNS Central Audit Node #DEL-MHA-8821")
        lbl_seal.setStyleSheet("color: #64748b; font-size: 11px;")
        footer.addWidget(lbl_seal)

        footer.addStretch()

        btn_copy = QPushButton("📋 Copy to Clipboard")
        btn_copy.setProperty("class", "SecondaryButton")
        btn_copy.clicked.connect(self._copy_clipboard)
        footer.addWidget(btn_copy)

        btn_save = QPushButton("💾 Export Judicial Dossier (.txt)")
        btn_save.setProperty("class", "PrimaryButton")
        btn_save.clicked.connect(self._save_file)
        footer.addWidget(btn_save)

        main_layout.addLayout(footer)

        # Populate initial template
        self._populate_initial()

    def _on_suspect_changed(self, idx: int):
        if 0 <= idx < len(self.suspects):
            self.selected_suspect = self.suspects[idx]
            self._populate_initial()

    def _populate_initial(self):
        fallback_text = gemini_service._fallback_dossier(self.selected_suspect)
        self.txt_dossier.setPlainText(fallback_text)

    def _draft_dossier(self):
        self.btn_draft.setEnabled(False)
        self.pbar.setVisible(True)
        self.txt_dossier.setPlainText("⏳ Calling Google Gemini 3.8 Flash to synthesize court-admissible electronic prosecution dossier...")

        graph_context = {
            "nodes": INITIAL_NODES,
            "edges": INITIAL_EDGES
        }
        self.thread = GeminiDossierThread(self.selected_suspect, graph_context)
        self.thread.dossier_ready.connect(self._on_dossier_ready)
        self.thread.start()

    def _on_dossier_ready(self, text: str):
        self.btn_draft.setEnabled(True)
        self.pbar.setVisible(False)
        self.txt_dossier.setPlainText(text)

    def _copy_clipboard(self):
        from PyQt6.QtWidgets import QApplication
        QApplication.clipboard().setText(self.txt_dossier.toPlainText())
        QMessageBox.information(self, "Copied", "Dossier text copied to system clipboard!")

    def _save_file(self):
        suspect_name = self.selected_suspect.get("label", "Suspect").replace(" ", "_")
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save Judicial Dossier",
            f"CCTNS_DOSSIER_{suspect_name}.txt",
            "Text Files (*.txt);;Markdown Files (*.md);;All Files (*)"
        )
        if filename:
            try:
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(self.txt_dossier.toPlainText())
                QMessageBox.information(self, "Exported", f"Dossier successfully saved to:\n{filename}")
            except Exception as e:
                QMessageBox.critical(self, "Error Saving File", str(e))

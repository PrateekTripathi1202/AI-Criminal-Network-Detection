"""
Google Gemini API Configuration Dialog
Allows setting and testing Google Gemini API Key and selecting model.
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QFrame, QMessageBox, QTextEdit
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont

from ..gemini_service import gemini_service, DEFAULT_MODELS

class GeminiConnectionTestThread(QThread):
    result_ready = pyqtSignal(dict)

    def __init__(self, key: str, model: str):
        super().__init__()
        self.key = key
        self.model = model

    def run(self):
        result = gemini_service.test_connection(self.key)
        self.result_ready.emit(result)

class GeminiSettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Google Gemini AI Engine Configuration")
        self.setFixedSize(540, 420)
        self.setStyleSheet("""
            QDialog {
                background-color: #0f172a;
                border: 1px solid #1e293b;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # Header
        header = QLabel("GOOGLE GEMINI API CONFIGURATION")
        header.setStyleSheet("color: #38bdf8; font-size: 16px; font-weight: bold; letter-spacing: 0.5px;")
        layout.addWidget(header)

        desc = QLabel(
            "Configure your Gemini API Key to enable real-time Case Copilot reasoning, "
            "automated Section 65B dossier drafting, multi-source FIR entity extraction, "
            "and wiretap interrogation using Gemini 3.8 Flash."
        )
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #94a3b8; font-size: 12px; line-height: 1.4;")
        layout.addWidget(desc)

        # Form Card
        card = QFrame()
        card.setStyleSheet("background-color: #131b2e; border: 1px solid #1e293b; border-radius: 8px; padding: 16px;")
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(12)

        # Model Selector
        lbl_model = QLabel("Select Model:")
        lbl_model.setStyleSheet("color: #cbd5e1; font-weight: bold; font-size: 12px;")
        card_layout.addWidget(lbl_model)

        self.cmb_model = QComboBox()
        for m in DEFAULT_MODELS:
            self.cmb_model.addItem(m)
        self.cmb_model.setCurrentText(gemini_service.current_model)
        card_layout.addWidget(self.cmb_model)

        # API Key
        lbl_key = QLabel("Gemini API Key:")
        lbl_key.setStyleSheet("color: #cbd5e1; font-weight: bold; font-size: 12px;")
        card_layout.addWidget(lbl_key)

        key_row = QHBoxLayout()
        self.txt_key = QLineEdit()
        self.txt_key.setEchoMode(QLineEdit.EchoMode.Password)
        self.txt_key.setPlaceholderText("Enter AIzaSy... or paste your Gemini API Key")
        if gemini_service.api_key:
            self.txt_key.setText(gemini_service.api_key)
        key_row.addWidget(self.txt_key)

        self.btn_toggle_echo = QPushButton("👁")
        self.btn_toggle_echo.setFixedWidth(36)
        self.btn_toggle_echo.setProperty("class", "SecondaryButton")
        self.btn_toggle_echo.clicked.connect(self._toggle_echo)
        key_row.addWidget(self.btn_toggle_echo)

        card_layout.addLayout(key_row)

        layout.addWidget(card)

        # Status text
        self.lbl_status = QLabel("")
        self.lbl_status.setWordWrap(True)
        self.lbl_status.setStyleSheet("font-size: 11px; padding: 4px;")
        layout.addWidget(self.lbl_status)

        layout.addStretch()

        # Action Buttons
        btn_row = QHBoxLayout()

        self.btn_test = QPushButton("⚡ Verify & Test Key")
        self.btn_test.setProperty("class", "SecondaryButton")
        self.btn_test.clicked.connect(self._test_connection)
        btn_row.addWidget(self.btn_test)

        btn_row.addStretch()

        self.btn_cancel = QPushButton("Cancel")
        self.btn_cancel.setProperty("class", "SecondaryButton")
        self.btn_cancel.clicked.connect(self.reject)
        btn_row.addWidget(self.btn_cancel)

        self.btn_save = QPushButton("Save & Apply")
        self.btn_save.setProperty("class", "PrimaryButton")
        self.btn_save.clicked.connect(self._save_settings)
        btn_row.addWidget(self.btn_save)

        layout.addLayout(btn_row)

    def _toggle_echo(self):
        if self.txt_key.echoMode() == QLineEdit.EchoMode.Password:
            self.txt_key.setEchoMode(QLineEdit.EchoMode.Normal)
            self.btn_toggle_echo.setText("🔒")
        else:
            self.txt_key.setEchoMode(QLineEdit.EchoMode.Password)
            self.btn_toggle_echo.setText("👁")

    def _test_connection(self):
        key = self.txt_key.text().strip()
        if not key:
            self.lbl_status.setText("❌ Please enter an API key to test.")
            self.lbl_status.setStyleSheet("color: #ef4444; font-weight: bold;")
            return

        self.btn_test.setEnabled(False)
        self.lbl_status.setText("⏳ Testing connection with Google Gemini 3.8 Flash...")
        self.lbl_status.setStyleSheet("color: #38bdf8;")

        self.thread = GeminiConnectionTestThread(key, self.cmb_model.currentText())
        self.thread.result_ready.connect(self._on_test_result)
        self.thread.start()

    def _on_test_result(self, result: dict):
        self.btn_test.setEnabled(True)
        if result.get("success"):
            self.lbl_status.setText(f"✓ {result.get('message')}")
            self.lbl_status.setStyleSheet("color: #10b981; font-weight: bold;")
        else:
            self.lbl_status.setText(f"✕ {result.get('message')}")
            self.lbl_status.setStyleSheet("color: #ef4444; font-weight: bold;")

    def _save_settings(self):
        key = self.txt_key.text().strip()
        model = self.cmb_model.currentText()
        gemini_service.save_config(key, model)
        self.accept()

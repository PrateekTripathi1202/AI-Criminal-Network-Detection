"""
Gemini AI Crime Copilot View
Interactive Law Enforcement Investigation Assistant grounded in CCTNS knowledge graph.
Powered by Google Gemini 3.8 Flash / Gemini 3.1 Pro Preview.
"""

from typing import Dict, Any, List
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit,
    QLineEdit, QPushButton, QFrame, QScrollArea, QSplitter,
    QProgressBar
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QTextCursor

from ..gemini_service import gemini_service
from ..dialogs.api_settings_dialog import GeminiSettingsDialog
from backend.app.data_store import INITIAL_NODES, INITIAL_EDGES

class GeminiQueryThread(QThread):
    response_ready = pyqtSignal(dict)

    def __init__(self, query: str, history: List[Dict[str, str]], graph_context: Dict[str, Any]):
        super().__init__()
        self.query = query
        self.history = history
        self.graph_context = graph_context

    def run(self):
        result = gemini_service.ask_copilot(
            question=self.query,
            conversation_history=self.history,
            graph_context=self.graph_context
        )
        self.response_ready.emit(result)

class CopilotView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.conversation_history: List[Dict[str, str]] = []
        self._init_ui()

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(18, 16, 18, 16)
        main_layout.setSpacing(12)

        # 1. Header Toolbar
        top_bar = QHBoxLayout()
        
        # Title and model badge
        title_box = QVBoxLayout()
        title_box.setSpacing(2)
        lbl_title = QLabel("GEMINI INVESTIGATION COPILOT")
        lbl_title.setStyleSheet("color: #f8fafc; font-size: 16px; font-weight: bold; letter-spacing: 0.5px;")
        title_box.addWidget(lbl_title)

        self.lbl_model_status = QLabel("🟢 Gemini 3.8 Flash Active" if gemini_service.is_configured() else "🟡 Local Fallback Engine (Click Settings to Add Key)")
        self.lbl_model_status.setStyleSheet("color: #38bdf8; font-size: 11px; font-weight: 600;")
        title_box.addWidget(self.lbl_model_status)
        top_bar.addLayout(title_box)

        top_bar.addStretch()

        # Context Pill
        lbl_grounding = QLabel(f"🔗 Grounded: {len(INITIAL_NODES)} Nodes / {len(INITIAL_EDGES)} Edges")
        lbl_grounding.setProperty("class", "BadgeBlue")
        top_bar.addWidget(lbl_grounding)

        # Key Settings Button
        self.btn_settings = QPushButton("⚙️ Gemini Settings")
        self.btn_settings.setProperty("class", "SecondaryButton")
        self.btn_settings.clicked.connect(self._open_settings)
        top_bar.addWidget(self.btn_settings)

        # Clear History Button
        self.btn_clear = QPushButton("🗑️ Clear Chat")
        self.btn_clear.setProperty("class", "SecondaryButton")
        self.btn_clear.clicked.connect(self._clear_chat)
        top_bar.addWidget(self.btn_clear)

        main_layout.addLayout(top_bar)

        # 2. Quick Prompt Suggestion Chips
        chips_layout = QHBoxLayout()
        chips_layout.setSpacing(8)

        chips = [
            ("👑 Identify Kingpin", "Based on graph betweenness and call records, who is the syndicate mastermind?"),
            ("🚗 Analyze Fortuner DL-01", "Forensically analyze vehicle DL-01-AB-9821 and its ownership links to Mumbai Hawala."),
            ("💳 Hawala Smurfing Trail", "Explain the structured money laundering trail from ICICI #1102 to HDFC #8819 and crypto offramps."),
            ("📁 Cross-Case Discovery", "What evidence bridges the Delhi Extortion FIR with the Mumbai Corporate Hawala FIR?")
        ]

        for label, query_text in chips:
            btn_chip = QPushButton(label)
            btn_chip.setStyleSheet("""
                QPushButton {
                    background-color: #131b2e;
                    color: #cbd5e1;
                    border: 1px solid #1e293b;
                    border-radius: 12px;
                    padding: 5px 12px;
                    font-size: 11px;
                    font-weight: 500;
                }
                QPushButton:hover {
                    background-color: #1e3a8a;
                    color: #ffffff;
                    border-color: #38bdf8;
                }
            """)
            btn_chip.clicked.connect(lambda checked, q=query_text: self._send_query_text(q))
            chips_layout.addWidget(btn_chip)

        chips_layout.addStretch()
        main_layout.addLayout(chips_layout)

        # 3. Chat History Display Area
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setStyleSheet("""
            QTextEdit {
                background-color: #0b0f19;
                border: 1px solid #1e293b;
                border-radius: 8px;
                padding: 14px;
                font-family: 'Segoe UI', 'Inter', sans-serif;
                font-size: 13px;
                line-height: 1.5;
            }
        """)
        main_layout.addWidget(self.chat_display, stretch=1)

        # Progress bar (hidden by default)
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0) # Indeterminate spinner mode
        self.progress_bar.setFixedHeight(3)
        self.progress_bar.setStyleSheet("QProgressBar::chunk { background-color: #38bdf8; }")
        self.progress_bar.setVisible(False)
        main_layout.addWidget(self.progress_bar)

        # 4. Input Bar at Bottom
        input_row = QHBoxLayout()
        input_row.setSpacing(10)

        self.txt_input = QLineEdit()
        self.txt_input.setPlaceholderText("Ask Gemini Copilot: 'Who ordered the extortion?', 'Trace crypto wallet 0x9fA2...', etc.")
        self.txt_input.returnPressed.connect(self._on_send_clicked)
        input_row.addWidget(self.txt_input, stretch=1)

        self.btn_send = QPushButton("⚡ Send Query")
        self.btn_send.setProperty("class", "PrimaryButton")
        self.btn_send.clicked.connect(self._on_send_clicked)
        input_row.addWidget(self.btn_send)

        main_layout.addLayout(input_row)

        # Initial Welcome Message
        self._append_system_message(
            "**NATIONAL CRIMINAL INTELLIGENCE SYSTEM (NCIS) AI COPILOT READY**\n\n"
            "Operating under CCTNS 4.0 & Bharatiya Nyaya Sanhita (BNS) guidelines. "
            "The active criminal knowledge graph containing **18 interconnected nodes** across Delhi, "
            "Mumbai, and Bengaluru is loaded into memory.\n\n"
            "Ask any investigative question, select a prompt chip above, or inspect an entity from the Knowledge Graph."
        )

    def _open_settings(self):
        dlg = GeminiSettingsDialog(self)
        if dlg.exec():
            self._update_model_status()

    def _update_model_status(self):
        if gemini_service.is_configured():
            self.lbl_model_status.setText(f"🟢 {gemini_service.current_model} Active")
            self.lbl_model_status.setStyleSheet("color: #10b981; font-size: 11px; font-weight: 600;")
        else:
            self.lbl_model_status.setText("🟡 Local Fallback Engine (Click Settings to Add Key)")
            self.lbl_model_status.setStyleSheet("color: #f59e0b; font-size: 11px; font-weight: 600;")

    def _clear_chat(self):
        self.conversation_history.clear()
        self.chat_display.clear()
        self._append_system_message("Chat history cleared. Active graph context remains loaded.")

    def prefill_entity_query(self, node: Dict[str, Any]):
        name = node.get("label", node.get("id"))
        node_id = node.get("id")
        q = f"Provide a complete criminal intelligence summary and risk breakdown for {name} ({node_id}). Detail their syndicate role, digital links, and recommended statutory actions."
        self._send_query_text(q)

    def _on_send_clicked(self):
        text = self.txt_input.text().strip()
        if text:
            self._send_query_text(text)

    def _send_query_text(self, query: str):
        self.txt_input.clear()
        self.btn_send.setEnabled(False)
        self.progress_bar.setVisible(True)

        # Append User Message to UI
        self._append_user_message(query)
        self.conversation_history.append({"role": "user", "text": query})

        # Launch background query thread
        graph_context = {
            "nodes": INITIAL_NODES,
            "edges": INITIAL_EDGES
        }
        self.thread = GeminiQueryThread(query, self.conversation_history, graph_context)
        self.thread.response_ready.connect(self._on_copilot_response)
        self.thread.start()

    def _on_copilot_response(self, result: Dict[str, Any]):
        self.btn_send.setEnabled(True)
        self.progress_bar.setVisible(False)

        ans = result.get("answer", "No response received.")
        model = result.get("model_used", gemini_service.current_model)
        is_live = result.get("is_live_api", False)

        badge_txt = f"⚡ {model} (Live API)" if is_live else f"🤖 {model}"
        self._append_gemini_message(ans, badge_txt)
        self.conversation_history.append({"role": "assistant", "text": ans})

    def _append_user_message(self, text: str):
        html = f"""
        <div style="margin-bottom: 14px; text-align: right;">
            <div style="display: inline-block; background-color: #1e3a8a; border: 1px solid #2563eb; color: #ffffff; padding: 10px 14px; border-radius: 10px; max-width: 80%; text-align: left;">
                <div style="font-size: 10px; font-weight: bold; color: #93c5fd; margin-bottom: 4px;">👮 INVESTIGATING OFFICER (YOU)</div>
                <div style="font-size: 13px;">{text}</div>
            </div>
        </div>
        """
        self.chat_display.append(html)
        self.chat_display.moveCursor(QTextCursor.MoveOperation.End)

    def _append_gemini_message(self, markdown_text: str, model_badge: str):
        # Convert standard markdown headers/bold to HTML
        formatted = self._markdown_to_html(markdown_text)
        html = f"""
        <div style="margin-bottom: 16px;">
            <div style="background-color: #111827; border: 1px solid #1f2937; border-left: 3px solid #38bdf8; border-radius: 8px; padding: 12px 16px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                    <span style="font-size: 11px; font-weight: bold; color: #38bdf8;">🧠 GEMINI INTELLIGENCE ASSISTANT</span>
                    <span style="font-size: 10px; background-color: #1e293b; color: #94a3b8; padding: 2px 6px; border-radius: 4px;">{model_badge}</span>
                </div>
                <div style="color: #e2e8f0; font-size: 13px; line-height: 1.5;">
                    {formatted}
                </div>
            </div>
        </div>
        """
        self.chat_display.append(html)
        self.chat_display.moveCursor(QTextCursor.MoveOperation.End)

    def _append_system_message(self, text: str):
        formatted = self._markdown_to_html(text)
        html = f"""
        <div style="margin-bottom: 14px; padding: 10px 14px; background-color: #0f172a; border: 1px dashed #334155; border-radius: 6px; color: #94a3b8; font-size: 12px;">
            {formatted}
        </div>
        """
        self.chat_display.append(html)
        self.chat_display.moveCursor(QTextCursor.MoveOperation.End)

    def _markdown_to_html(self, text: str) -> str:
        # Basic markdown to HTML renderer for clean presentation
        import re
        t = text
        t = re.sub(r'### (.*?)\n', r'<h4 style="color: #38bdf8; margin: 8px 0 4px 0;">\1</h4>', t)
        t = re.sub(r'## (.*?)\n', r'<h3 style="color: #67e8f9; margin: 10px 0 6px 0;">\1</h3>', t)
        t = re.sub(r'\*\*(.*?)\*\*', r'<strong style="color: #ffffff;">\1</strong>', t)
        t = re.sub(r'\*(.*?)\*', r'<em>\1</em>', t)
        t = re.sub(r'`(.*?)`', r'<code style="background-color: #1e293b; color: #38bdf8; padding: 1px 4px; border-radius: 3px;">\1</code>', t)
        t = t.replace("\n", "<br>")
        return t

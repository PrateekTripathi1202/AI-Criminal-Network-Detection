"""
Explainable AI (XAI) Link Prediction & Human-in-the-Loop Validation View
Transparent link predictions with feature weights, evidence chains,
and judicial investigator sign-off.
"""

from typing import Dict, Any, List
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QScrollArea, QProgressBar, QLineEdit, QTextEdit,
    QListWidget, QListWidgetItem, QMessageBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont

from backend.app.ai_intelligence import ai_intelligence
from backend.app.graph_engine import graph_engine
from ..gemini_service import gemini_service

class GeminiAuditThread(QThread):
    audit_ready = pyqtSignal(str)

    def __init__(self, link_data: Dict[str, Any]):
        super().__init__()
        self.link_data = link_data

    def run(self):
        prompt = (
            f"You are a Senior Cyber Forensic Expert and Public Prosecutor.\n"
            f"Review this Explainable AI (XAI) predicted covert link for judicial admissibility:\n"
            f"Source: {self.link_data.get('source_name')} ({self.link_data.get('source')})\n"
            f"Target: {self.link_data.get('target_name')} ({self.link_data.get('target')})\n"
            f"Predicted Relation: {self.link_data.get('predicted_relation')}\n"
            f"AI Confidence: {self.link_data.get('confidence')}%\n"
            f"Reasons: {self.link_data.get('reasons')}\n"
            f"Evidence Trail: {self.link_data.get('evidence_trail')}\n\n"
            f"Provide an objective forensic assessment: Is this evidence sufficient under Section 61/111 BNS "
            f"to issue a search warrant or wiretap order? What potential defense arguments might arise?"
        )
        res = gemini_service.ask_copilot(prompt)
        self.audit_ready.emit(res.get("answer", "No response from Gemini."))

class XAIView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.predictions = ai_intelligence.predict_hidden_links()
        self.selected_link: Dict[str, Any] = self.predictions[0] if self.predictions else None
        self._init_ui()

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(18, 16, 18, 16)
        main_layout.setSpacing(14)

        # Header
        header = QHBoxLayout()
        t_box = QVBoxLayout()
        lbl_t = QLabel("EXPLAINABLE AI (XAI) LINK PREDICTION & VALIDATION")
        lbl_t.setStyleSheet("color: #f8fafc; font-size: 16px; font-weight: bold; letter-spacing: 0.5px;")
        t_box.addWidget(lbl_t)

        lbl_s = QLabel("COVERT RELATIONSHIPS // FEATURE WEIGHTING // HUMAN-IN-THE-LOOP JUDICIAL AUDIT")
        lbl_s.setStyleSheet("color: #38bdf8; font-size: 11px; font-weight: 600; letter-spacing: 1px;")
        t_box.addWidget(lbl_s)
        header.addLayout(t_box)

        header.addStretch()

        lbl_badge = QLabel(f"{len(self.predictions)} PREDICTED COVERT LINKS")
        lbl_badge.setProperty("class", "BadgeAmber")
        header.addWidget(lbl_badge)

        main_layout.addLayout(header)

        # Content Split: Left (List of Predictions), Right (Deep Breakdown & Human Validation)
        content_layout = QHBoxLayout()
        content_layout.setSpacing(16)

        # Left: Predictions List
        left_frame = QFrame()
        left_frame.setProperty("class", "CardFrame")
        left_frame.setFixedWidth(320)
        l_layout = QVBoxLayout(left_frame)
        l_layout.setContentsMargins(12, 12, 12, 12)
        l_layout.setSpacing(10)

        lbl_list_title = QLabel("AI PREDICTIONS QUEUE")
        lbl_list_title.setStyleSheet("color: #94a3b8; font-weight: bold; font-size: 11px;")
        l_layout.addWidget(lbl_list_title)

        self.list_preds = QListWidget()
        self.list_preds.setStyleSheet("""
            QListWidget {
                background-color: #0b0f19;
                border: 1px solid #1e293b;
                border-radius: 6px;
                color: #e2e8f0;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #162032;
                border-radius: 4px;
                margin-bottom: 4px;
            }
            QListWidget::item:selected {
                background-color: #1e3a8a;
                border-left: 3px solid #38bdf8;
            }
        """)
        self.list_preds.currentRowChanged.connect(self._on_pred_selected)
        l_layout.addWidget(self.list_preds)

        for p in self.predictions:
            item = QListWidgetItem()
            src = p.get("source_name", p.get("source")).split()[0]
            tgt = p.get("target_name", p.get("target")).split()[0]
            conf = p.get("confidence", 0)
            item.setText(f"{src} ➔ {tgt}\n{p.get('predicted_relation')} ({conf}%)")
            self.list_preds.addItem(item)

        content_layout.addWidget(left_frame)

        # Right: Detail Card & Validation Form
        right_frame = QFrame()
        right_frame.setProperty("class", "CardFrame")
        r_layout = QVBoxLayout(right_frame)
        r_layout.setContentsMargins(16, 16, 16, 16)
        r_layout.setSpacing(12)

        scroll_detail = QScrollArea()
        scroll_detail.setWidgetResizable(True)
        scroll_detail.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")

        detail_container = QWidget()
        self.detail_layout = QVBoxLayout(detail_container)
        self.detail_layout.setContentsMargins(0, 0, 0, 0)
        self.detail_layout.setSpacing(12)

        # Title Card
        self.card_summary = QFrame()
        self.card_summary.setStyleSheet("background-color: #0b0f19; border: 1px solid #1e293b; border-left: 4px solid #ef4444; border-radius: 6px; padding: 12px;")
        cs_layout = QVBoxLayout(self.card_summary)
        cs_layout.setSpacing(6)

        self.lbl_link_headline = QLabel("Link Title")
        self.lbl_link_headline.setStyleSheet("color: #f8fafc; font-size: 15px; font-weight: bold;")
        cs_layout.addWidget(self.lbl_link_headline)

        self.lbl_conf_risk = QLabel("Confidence: -- | Risk: --")
        self.lbl_conf_risk.setStyleSheet("color: #38bdf8; font-size: 12px; font-weight: 600;")
        cs_layout.addWidget(self.lbl_conf_risk)

        self.detail_layout.addWidget(self.card_summary)

        # Evidence Trail
        lbl_trail_t = QLabel("⛓️ MULTI-HOP EVIDENCE TRAIL:")
        lbl_trail_t.setStyleSheet("color: #94a3b8; font-size: 11px; font-weight: bold;")
        self.detail_layout.addWidget(lbl_trail_t)

        self.lbl_trail = QLabel("")
        self.lbl_trail.setStyleSheet("background-color: #0b0f19; border: 1px solid #1e293b; border-radius: 6px; padding: 10px; color: #38bdf8; font-family: Consolas, monospace; font-size: 12px;")
        self.lbl_trail.setWordWrap(True)
        self.detail_layout.addWidget(self.lbl_trail)

        # Reasons
        lbl_reasons_t = QLabel("🔍 FORENSIC COINCIDENCE FACTORS:")
        lbl_reasons_t.setStyleSheet("color: #94a3b8; font-size: 11px; font-weight: bold;")
        self.detail_layout.addWidget(lbl_reasons_t)

        self.reasons_box = QVBoxLayout()
        self.reasons_box.setSpacing(6)
        self.detail_layout.addLayout(self.reasons_box)

        # Feature Weights Progress Bars
        lbl_weights_t = QLabel("📊 EXPLAINABLE AI (XAI) FEATURE CONTRIBUTION WEIGHTS:")
        lbl_weights_t.setStyleSheet("color: #94a3b8; font-size: 11px; font-weight: bold;")
        self.detail_layout.addWidget(lbl_weights_t)

        self.weights_box = QVBoxLayout()
        self.weights_box.setSpacing(6)
        self.detail_layout.addLayout(self.weights_box)

        # Gemini Audit Section
        self.audit_box = QFrame()
        self.audit_box.setStyleSheet("background-color: #0b0f19; border: 1px dashed #38bdf8; border-radius: 6px; padding: 10px;")
        ab_layout = QVBoxLayout(self.audit_box)
        ab_layout.setSpacing(6)

        ab_head = QHBoxLayout()
        ab_title = QLabel("🤖 GEMINI JUDICIAL AUDIT SECOND OPINION")
        ab_title.setStyleSheet("color: #38bdf8; font-weight: bold; font-size: 11px;")
        ab_head.addWidget(ab_title)
        ab_head.addStretch()

        self.btn_run_audit = QPushButton("Run Gemini Forensic Audit")
        self.btn_run_audit.setProperty("class", "PrimaryButton")
        self.btn_run_audit.clicked.connect(self._run_gemini_audit)
        ab_head.addWidget(self.btn_run_audit)
        ab_layout.addLayout(ab_head)

        self.lbl_audit_text = QLabel("Click 'Run Gemini Forensic Audit' to ask Gemini 3.8 Flash to evaluate judicial admissibility under BNS.")
        self.lbl_audit_text.setWordWrap(True)
        self.lbl_audit_text.setStyleSheet("color: #cbd5e1; font-size: 12px; line-height: 1.4;")
        ab_layout.addWidget(self.lbl_audit_text)

        self.detail_layout.addWidget(self.audit_box)

        # Human-in-the-Loop Validation Box
        val_box = QFrame()
        val_box.setStyleSheet("background-color: #131b2e; border: 1px solid #1e293b; border-radius: 8px; padding: 12px;")
        vb_layout = QVBoxLayout(val_box)
        vb_layout.setSpacing(8)

        lbl_v_title = QLabel("👮 HUMAN-IN-THE-LOOP JUDICIAL VALIDATION")
        lbl_v_title.setStyleSheet("color: #10b981; font-weight: bold; font-size: 12px;")
        vb_layout.addWidget(lbl_v_title)

        v_row = QHBoxLayout()
        lbl_badge_io = QLabel("Officer Badge ID:")
        lbl_badge_io.setStyleSheet("color: #94a3b8; font-size: 11px;")
        v_row.addWidget(lbl_badge_io)

        self.txt_badge = QLineEdit("INSP-DL-4902 (Delhi Special Cell)")
        v_row.addWidget(self.txt_badge)
        vb_layout.addLayout(v_row)

        lbl_notes = QLabel("Case Verification Notes:")
        lbl_notes.setStyleSheet("color: #94a3b8; font-size: 11px;")
        vb_layout.addWidget(lbl_notes)

        self.txt_notes = QLineEdit("Corroborated with witness statements and toll plaza CCTV records.")
        vb_layout.addWidget(self.txt_notes)

        # Buttons: Approve / Reject
        action_row = QHBoxLayout()
        action_row.setSpacing(10)

        self.btn_reject = QPushButton("✕ Reject AI Link")
        self.btn_reject.setProperty("class", "DangerButton")
        self.btn_reject.clicked.connect(self._reject_link)
        action_row.addWidget(self.btn_reject)

        action_row.addStretch()

        self.btn_approve = QPushButton("✓ Approve & Commit to Criminal Graph")
        self.btn_approve.setStyleSheet("background-color: #10b981; color: white; border: 1px solid #34d399; font-weight: bold; padding: 8px 16px; border-radius: 6px;")
        self.btn_approve.clicked.connect(self._approve_link)
        action_row.addWidget(self.btn_approve)

        vb_layout.addLayout(action_row)
        self.detail_layout.addWidget(val_box)

        scroll_detail.setWidget(detail_container)
        r_layout.addWidget(scroll_detail)

        content_layout.addWidget(right_frame, stretch=1)
        main_layout.addLayout(content_layout)

        # Select first item
        if self.predictions:
            self.list_preds.setCurrentRow(0)

    def _on_pred_selected(self, row: int):
        if row < 0 or row >= len(self.predictions):
            return
        self.selected_link = self.predictions[row]
        p = self.selected_link

        # Headline
        self.lbl_link_headline.setText(f"{p.get('source_name')} ➔ {p.get('target_name')}")
        self.lbl_conf_risk.setText(f"Predicted Relation: {p.get('predicted_relation')}  |  Confidence: {p.get('confidence')}%  |  Risk: {p.get('risk_elevation')}")

        # Trail
        trail = " ➔ ".join(p.get("evidence_trail", []))
        self.lbl_trail.setText(trail)

        # Clear old reasons
        for i in reversed(range(self.reasons_box.count())):
            w = self.reasons_box.itemAt(i).widget()
            if w:
                w.setParent(None)

        for r in p.get("reasons", []):
            lbl_r = QLabel(f"• {r}")
            lbl_r.setWordWrap(True)
            lbl_r.setStyleSheet("color: #cbd5e1; font-size: 12px; background-color: #0b0f19; padding: 6px 10px; border-radius: 4px; border-left: 2px solid #38bdf8;")
            self.reasons_box.addWidget(lbl_r)

        # Clear old weights
        for i in reversed(range(self.weights_box.count())):
            w = self.weights_box.itemAt(i).widget()
            if w:
                w.setParent(None)

        for feat, wt in p.get("xai_feature_weights", {}).items():
            w_row = QHBoxLayout()
            lbl_feat = QLabel(feat)
            lbl_feat.setStyleSheet("color: #cbd5e1; font-size: 11px;")
            w_row.addWidget(lbl_feat, stretch=1)

            pbar = QProgressBar()
            pbar.setRange(0, 100)
            pbar.setValue(int(wt))
            pbar.setFixedHeight(12)
            pbar.setStyleSheet("QProgressBar::chunk { background-color: #0284c7; }")
            w_row.addWidget(pbar, stretch=1)

            lbl_val = QLabel(f"{wt}%")
            lbl_val.setStyleSheet("color: #38bdf8; font-weight: bold; font-size: 11px;")
            w_row.addWidget(lbl_val)

            self.weights_box.addLayout(w_row)

        # Reset audit status
        self.lbl_audit_text.setText("Click 'Run Gemini Forensic Audit' to ask Gemini 3.8 Flash to evaluate judicial admissibility under BNS.")

    def _run_gemini_audit(self):
        if not self.selected_link:
            return
        self.btn_run_audit.setEnabled(False)
        self.lbl_audit_text.setText("⏳ Consulting Google Gemini 3.8 Flash for forensic evidence audit...")

        self.thread = GeminiAuditThread(self.selected_link)
        self.thread.audit_ready.connect(self._on_audit_result)
        self.thread.start()

    def _on_audit_result(self, result_text: str):
        self.btn_run_audit.setEnabled(True)
        self.lbl_audit_text.setText(result_text)

    def _approve_link(self):
        if not self.selected_link:
            return
        src = self.selected_link.get("source")
        tgt = self.selected_link.get("target")
        badge = self.txt_badge.text()

        # Add edge to graph engine
        new_edge = {
            "id": f"E-VERIFIED-{src}-{tgt}",
            "source": src,
            "target": tgt,
            "type": "investigator_verified",
            "weight": 5.0,
            "label": f"Verified Link ({badge[:12]})",
            "metadata": {"officer": badge, "notes": self.txt_notes.text()}
        }
        graph_engine.add_edge(new_edge)

        QMessageBox.information(
            self,
            "Link Committed to CCTNS",
            f"Covert link approved and recorded under Warrant Registry!\n\n"
            f"Source: {self.selected_link.get('source_name')}\n"
            f"Target: {self.selected_link.get('target_name')}\n"
            f"Authorized Officer: {badge}"
        )

    def _reject_link(self):
        if not self.selected_link:
            return
        QMessageBox.warning(
            self,
            "Link Dismissed",
            "The predicted link has been rejected by the investigating officer. "
            "Audit logs retained in National Crime Database under compliance rules."
        )

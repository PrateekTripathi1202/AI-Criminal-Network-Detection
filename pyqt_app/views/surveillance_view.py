"""
Surveillance & Computer Vision Suite + Telecom Wiretap Console
Real-time 4K simulated CCTV feeds, OpenCV Device Webcam, DeepFace matching,
ANPR, and bilingual wiretap transcript analysis via Gemini.
"""

from typing import Dict, Any, List
import winsound
import subprocess
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QComboBox, QFrame, QScrollArea, QTextEdit, QFileDialog, QMessageBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QPixmap

from ..widgets.cctv_player import SimulatedCCTVWidget
from ..gemini_service import gemini_service

CAMERAS = [
    {"id": "CAM-DEL-041", "name": "Connaught Place Block-B, New Delhi", "target": "DL-01-AB-9821 Fortuner & Amit Tyagi"},
    {"id": "CAM-MUM-108", "name": "Bandra Kurla Complex (BKC), Mumbai", "target": "Pooja Deshmukh (Apex Impex Office)"},
    {"id": "CAM-BLR-022", "name": "Electronic City Toll Plaza NH-44, Bengaluru", "target": "KA-03-MM-1029 White Swift (Mule SIM Courier)"},
    {"id": "CAM-HYD-034", "name": "Hitec City Cyber Gateway, Hyderabad", "target": "TS-09-UB-8812 Crypto Courier"},
    {"id": "CAM-KOL-012", "name": "Vidyasagar Setu Toll Plaza, Kolkata", "target": "WB-02-AK-9011 Hawala Vehicle"}
]

WIRETAPS = [
    {
        "id": "WIRE-2026-INT-409",
        "time": "2026-09-23 20:41:12 IST",
        "parties": "Rajesh 'Munna' Sharma (Burner) ➔ Vikram 'Vicky' Malhotra (Satellite VoIP)",
        "hindi": "भाई, गाड़ी पहुंच गई है सीपी ब्लॉक बी में। अमित खुद ड्राइव कर रहा है फॉर्च्यूनर। ज्वेलर को बोल दिया है दो करोड़ तैयार रखने। अगर आनाकानी की तो गोली चलेगी। हवाला रूट मुंबई वाला क्लियर है ना?",
        "english": "Bhai, vehicle has reached CP Block B. Amit himself is driving the Fortuner. Have told the jeweller to keep 2 Crores ready. If he hesitates, bullets will fly. The Mumbai Hawala route is clear, right?",
        "threat": "CRITICAL"
    },
    {
        "id": "WIRE-2026-INT-410",
        "time": "2026-09-23 21:05:30 IST",
        "parties": "Sameer 'Sam' Khan (Mule SIM) ➔ Rajesh 'Munna' Sharma (Burner)",
        "hindi": "नया बैच तैयार है। पचास फ्रेश आधार क्लोन्ड सिम कार्ड्स दिल्ली भेज दिए हैं कोरियर से। यूएसडीटी का पेमेंट उसी टीआरसी ट्वेंटी वॉलेट में डाल देना।",
        "english": "New batch is ready. Fifty fresh Aadhaar-cloned SIM cards dispatched to Delhi via courier. Deposit the USDT payment into the same TRC-20 wallet.",
        "threat": "HIGH"
    }
]

class GeminiWiretapThread(QThread):
    analysis_ready = pyqtSignal(str)

    def __init__(self, wiretap_data: Dict[str, Any]):
        super().__init__()
        self.wiretap_data = wiretap_data

    def run(self):
        prompt = (
            f"You are a Senior Counter-Terrorism & Intelligence Wiretap Intercept Analyst.\n"
            f"Interrogate this intercepted bilingual wiretap:\n"
            f"ID: {self.wiretap_data.get('id')}\n"
            f"Timestamp: {self.wiretap_data.get('time')}\n"
            f"Parties: {self.wiretap_data.get('parties')}\n"
            f"Hindi Original: {self.wiretap_data.get('hindi')}\n"
            f"English Translation: {self.wiretap_data.get('english')}\n\n"
            f"Provide:\n"
            f"1. Threat Level & Immediate Danger Score (1-100)\n"
            f"2. Coded Gang Slang & Modus Operandi Decoded\n"
            f"3. Firearm & Extortion Evidence under Arms Act Sec 25 / BNS 111\n"
            f"4. Urgent Tactical Police Dispatch Directives"
        )
        res = gemini_service.ask_copilot(prompt)
        self.analysis_ready.emit(res.get("answer", "No response from Gemini."))

class SurveillanceView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected_wiretap = WIRETAPS[0]
        self._init_ui()

    def _init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(18, 16, 18, 16)
        main_layout.setSpacing(12)

        # Header Toolbar
        header = QHBoxLayout()
        t_box = QVBoxLayout()
        lbl_t = QLabel("SURVEILLANCE & COMPUTER VISION // TELECOM WIRETAP CONSOLE")
        lbl_t.setStyleSheet("color: #f8fafc; font-size: 16px; font-weight: bold; letter-spacing: 0.5px;")
        t_box.addWidget(lbl_t)

        lbl_s = QLabel("REAL-TIME 4K OPTICAL FEED // OPENCV WEBCAM // YOLOv11 + DEEPFACE // BILINGUAL WIRETAP FORENSICS")
        lbl_s.setStyleSheet("color: #38bdf8; font-size: 11px; font-weight: 600; letter-spacing: 1px;")
        t_box.addWidget(lbl_s)
        header.addLayout(t_box)

        header.addStretch()

        # Camera Switcher Dropdown
        lbl_cam = QLabel("Switch Sector:")
        lbl_cam.setStyleSheet("color: #cbd5e1; font-weight: bold; font-size: 12px;")
        header.addWidget(lbl_cam)

        self.cmb_camera = QComboBox()
        for c in CAMERAS:
            self.cmb_camera.addItem(f"{c['id']} - {c['name']}")
        self.cmb_camera.currentIndexChanged.connect(self._on_camera_changed)
        header.addWidget(self.cmb_camera)

        # Toggle Webcam Button
        self.btn_webcam = QPushButton("📷 Enable Device Webcam")
        self.btn_webcam.setProperty("class", "SecondaryButton")
        self.btn_webcam.clicked.connect(self._toggle_webcam)
        header.addWidget(self.btn_webcam)

        # Snapshot Button
        self.btn_snap = QPushButton("💾 Capture Snapshot")
        self.btn_snap.setProperty("class", "PrimaryButton")
        self.btn_snap.clicked.connect(self._save_snapshot)
        header.addWidget(self.btn_snap)

        main_layout.addLayout(header)

        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        # 1. Live CCTV Stream Simulator Widget
        self.cctv_widget = SimulatedCCTVWidget(CAMERAS[0]["id"], CAMERAS[0]["name"])
        layout.addWidget(self.cctv_widget)

        # 2. Telecom Wiretap Intercept Console
        wiretap_frame = QFrame()
        wiretap_frame.setProperty("class", "CardFrame")
        wf_layout = QVBoxLayout(wiretap_frame)
        wf_layout.setContentsMargins(16, 16, 16, 16)
        wf_layout.setSpacing(12)

        # Wiretap Header
        wh = QHBoxLayout()
        wh_title = QLabel("TELECOM WIRETAP INTERCEPTS & AUDIO PLAYBACK (MHA WARRANT CR-8812)")
        wh_title.setStyleSheet("color: #38bdf8; font-weight: bold; font-size: 13px;")
        wh.addWidget(wh_title)
        wh.addStretch()

        self.btn_play_audio = QPushButton("🔊 Play Radio Audio Intercept")
        self.btn_play_audio.setProperty("class", "SecondaryButton")
        self.btn_play_audio.clicked.connect(self._play_intercept_audio)
        wh.addWidget(self.btn_play_audio)

        self.btn_gemini_wiretap = QPushButton("🤖 Forensic Wiretap Interrogation with Gemini")
        self.btn_gemini_wiretap.setProperty("class", "PrimaryButton")
        self.btn_gemini_wiretap.clicked.connect(self._analyze_current_wiretap)
        wh.addWidget(self.btn_gemini_wiretap)
        wf_layout.addLayout(wh)

        # Wiretap Selector buttons
        wt_btns = QHBoxLayout()
        for i, wt in enumerate(WIRETAPS):
            btn = QPushButton(f"📡 {wt['id']} ({wt['parties'].split()[0]} ➔ {wt['parties'].split('➔')[1].strip().split()[0]})")
            btn.setProperty("class", "SecondaryButton")
            btn.clicked.connect(lambda checked, idx=i: self._select_wiretap(idx))
            wt_btns.addWidget(btn)
        wt_btns.addStretch()
        wf_layout.addLayout(wt_btns)

        # Transcript Display Cards
        self.lbl_wt_parties = QLabel(f"<b>Parties:</b> {self.selected_wiretap['parties']}")
        self.lbl_wt_parties.setStyleSheet("color: #38bdf8; font-size: 12px;")
        wf_layout.addWidget(self.lbl_wt_parties)

        # Original Hindi
        lbl_h_title = QLabel("ORIGINAL AUDIO INTERCEPT (BILINGUAL HINDI / URDU):")
        lbl_h_title.setStyleSheet("color: #94a3b8; font-size: 11px; font-weight: bold;")
        wf_layout.addWidget(lbl_h_title)

        self.lbl_wt_hindi = QLabel(f'"{self.selected_wiretap["hindi"]}"')
        self.lbl_wt_hindi.setWordWrap(True)
        self.lbl_wt_hindi.setStyleSheet("background-color: #0b0f19; border: 1px solid #1e293b; border-left: 3px solid #ef4444; border-radius: 6px; padding: 10px; color: #f8fafc; font-size: 13px; font-style: italic;")
        wf_layout.addWidget(self.lbl_wt_hindi)

        # English Translation
        lbl_e_title = QLabel("VERIFIED FORENSIC ENGLISH TRANSLATION:")
        lbl_e_title.setStyleSheet("color: #94a3b8; font-size: 11px; font-weight: bold;")
        wf_layout.addWidget(lbl_e_title)

        self.lbl_wt_eng = QLabel(f'"{self.selected_wiretap["english"]}"')
        self.lbl_wt_eng.setWordWrap(True)
        self.lbl_wt_eng.setStyleSheet("background-color: #0b0f19; border: 1px solid #1e293b; border-left: 3px solid #0284c7; border-radius: 6px; padding: 10px; color: #38bdf8; font-size: 13px;")
        wf_layout.addWidget(self.lbl_wt_eng)

        # Gemini Analysis Output Box
        lbl_ga_title = QLabel("🤖 GEMINI AI THREAT FORENSICS & SLANG DECRYPTION:")
        lbl_ga_title.setStyleSheet("color: #38bdf8; font-size: 11px; font-weight: bold;")
        wf_layout.addWidget(lbl_ga_title)

        self.txt_gemini_wiretap = QTextEdit()
        self.txt_gemini_wiretap.setReadOnly(True)
        self.txt_gemini_wiretap.setPlaceholderText("Click 'Forensic Wiretap Interrogation with Gemini' to analyze coded gang slang and impending extortion...")
        self.txt_gemini_wiretap.setMinimumHeight(150)
        self.txt_gemini_wiretap.setStyleSheet("background-color: #070b14; border: 1px dashed #38bdf8; color: #f1f5f9; font-size: 12px; line-height: 1.4;")
        wf_layout.addWidget(self.txt_gemini_wiretap)

        layout.addWidget(wiretap_frame)

        scroll.setWidget(container)
        main_layout.addWidget(scroll)

    def _on_camera_changed(self, idx: int):
        if 0 <= idx < len(CAMERAS):
            cam = CAMERAS[idx]
            self.cctv_widget.set_camera(cam["id"], cam["name"])
            self.btn_webcam.setText("📷 Enable Device Webcam")

    def _toggle_webcam(self):
        active = self.cctv_widget.toggle_webcam()
        if active:
            self.btn_webcam.setText("🔴 Disconnect Webcam")
            self.btn_webcam.setStyleSheet("background-color: #dc2626; color: white; font-weight: bold;")
            try:
                winsound.Beep(1200, 100)
            except Exception:
                pass
        else:
            self.btn_webcam.setText("📷 Enable Device Webcam")
            self.btn_webcam.setStyleSheet("")
            try:
                winsound.Beep(800, 100)
            except Exception:
                pass

    def _save_snapshot(self):
        try:
            winsound.Beep(1500, 80)
        except Exception:
            pass

        pixmap = self.cctv_widget.capture_snapshot()
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save Forensic Snapshot",
            f"SURVEILLANCE_CAPTURE_{int(time.time())}.png",
            "PNG Images (*.png);;JPEG Images (*.jpg);;All Files (*)"
        )
        if filename:
            pixmap.save(filename)
            QMessageBox.information(self, "Snapshot Saved", f"Forensic image saved to:\n{filename}")

    def _select_wiretap(self, idx: int):
        if 0 <= idx < len(WIRETAPS):
            self.selected_wiretap = WIRETAPS[idx]
            self.lbl_wt_parties.setText(f"<b>Parties:</b> {self.selected_wiretap['parties']}")
            self.lbl_wt_hindi.setText(f'"{self.selected_wiretap["hindi"]}"')
            self.lbl_wt_eng.setText(f'"{self.selected_wiretap["english"]}"')
            self.txt_gemini_wiretap.clear()

    def _play_intercept_audio(self):
        # Play authentic radio beep
        try:
            winsound.Beep(1000, 120)
            winsound.Beep(700, 100)
        except Exception:
            pass
        QMessageBox.information(
            self,
            "Radio Telecom Stream",
            f"Playing encrypted intercept {self.selected_wiretap['id']}.\n\n"
            f"Party 1: {self.selected_wiretap['parties']}\n"
            f"Text: \"{self.selected_wiretap['english']}\""
        )

    def _analyze_current_wiretap(self):
        self.btn_gemini_wiretap.setEnabled(False)
        self.txt_gemini_wiretap.setPlainText("⏳ Analyzing audio intercept and gang slang via Google Gemini 3.8 Flash...")

        self.thread = GeminiWiretapThread(self.selected_wiretap)
        self.thread.analysis_ready.connect(self._on_analysis_ready)
        self.thread.start()

    def _on_analysis_ready(self, output: str):
        self.btn_gemini_wiretap.setEnabled(True)
        self.txt_gemini_wiretap.setPlainText(output)

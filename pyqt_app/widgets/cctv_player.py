"""
Enhanced Live CCTV Video & Computer Vision Telemetry Widget
Supports:
1. High-tech simulated 4K surveillance feed with YOLO bounding boxes, DeepFace HUD, FastANPR.
2. Real Device Webcam Streaming via OpenCV cv2.VideoCapture(0) with fallback.
3. Snapshot Capture & Watermarking.
"""

import time
import cv2
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox, QFrame
from PyQt6.QtCore import Qt, QTimer, QRectF, QPointF
from PyQt6.QtGui import QPainter, QPen, QBrush, QColor, QFont, QRadialGradient, QLinearGradient, QImage, QPixmap

class SimulatedCCTVWidget(QFrame):
    def __init__(self, camera_id: str = "CAM-DEL-041", location: str = "Connaught Place Block-B, New Delhi", parent=None):
        super().__init__(parent)
        self.camera_id = camera_id
        self.location = location
        self.setObjectName("CCTVFeed")
        self.setMinimumHeight(320)
        self.setStyleSheet("""
            #CCTVFeed {
                background-color: #050811;
                border: 1px solid #1e293b;
                border-radius: 8px;
            }
        """)

        self.is_webcam_active = False
        self.cap = None
        self.current_frame_pixmap = None
        self.tick = 0

        # Animation timer (30 FPS for smooth webcam & radar)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._on_tick)
        self.timer.start(33)

    def set_camera(self, camera_id: str, location: str):
        self.camera_id = camera_id
        self.location = location
        if self.is_webcam_active:
            self.stop_webcam()
        self.update()

    def toggle_webcam(self) -> bool:
        if self.is_webcam_active:
            self.stop_webcam()
            return False
        else:
            return self.start_webcam()

    def start_webcam(self) -> bool:
        try:
            self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            if not self.cap.isOpened():
                self.cap = cv2.VideoCapture(0)
            if self.cap.isOpened():
                self.is_webcam_active = True
                return True
            else:
                self.cap = None
                return False
        except Exception as e:
            print(f"[CCTV] Webcam start error: {e}")
            self.cap = None
            return False

    def stop_webcam(self):
        if self.cap:
            try:
                self.cap.release()
            except Exception:
                pass
            self.cap = None
        self.is_webcam_active = False
        self.current_frame_pixmap = None
        self.update()

    def capture_snapshot(self) -> QPixmap:
        """Grabs the current view as a high-res forensic snapshot."""
        return self.grab()

    def _on_tick(self):
        self.tick += 1

        if self.is_webcam_active and self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                # Convert BGR to RGB
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_frame.shape
                bytes_per_line = ch * w
                q_img = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
                self.current_frame_pixmap = QPixmap.fromImage(q_img)

        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        w = self.width()
        h = self.height()

        # 1. Background: Either Webcam stream or Dark Surveillance Grid
        if self.is_webcam_active and self.current_frame_pixmap:
            scaled = self.current_frame_pixmap.scaled(
                w, h, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation
            )
            # Center crop
            sx = (scaled.width() - w) // 2
            sy = (scaled.height() - h) // 2
            painter.drawPixmap(0, 0, scaled, sx, sy, w, h)

            # Tint overlay for cyber look
            painter.fillRect(0, 0, w, h, QColor(0, 242, 254, 15))
        else:
            grad = QLinearGradient(0, 0, w, h)
            grad.setColorAt(0, QColor("#09101d"))
            grad.setColorAt(1, QColor("#030712"))
            painter.fillRect(0, 0, w, h, grad)

            # Grid lines
            painter.setPen(QPen(QColor(30, 41, 59, 70), 1))
            for x in range(0, w, 40):
                painter.drawLine(x, 0, x, h)
            for y in range(0, h, 40):
                painter.drawLine(0, y, w, y)

        # 2. Scanning radar beam line
        scan_y = (self.tick * 5) % h
        scan_grad = QLinearGradient(0, scan_y - 20, 0, scan_y)
        scan_grad.setColorAt(0, QColor(6, 182, 212, 0))
        scan_grad.setColorAt(1, QColor(6, 182, 212, 45))
        painter.fillRect(0, max(0, scan_y - 20), w, 20, scan_grad)
        painter.setPen(QPen(QColor(6, 182, 212, 180), 1.5))
        painter.drawLine(0, scan_y, w, scan_y)

        # 3. Top HUD: Camera ID, Timestamp, REC indicator
        if (self.tick // 15) % 2 == 0:
            painter.setBrush(QColor("#ef4444"))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(18, 16, 10, 10)

        painter.setFont(QFont("Consolas", 10, QFont.Weight.Bold))
        painter.setPen(QColor("#f8fafc"))
        cam_label = "DEVICE WEBCAM (LOCAL OPERATOR)" if self.is_webcam_active else self.camera_id
        painter.drawText(36, 25, f"REC  [AI OPTICAL GRID]  •  {cam_label}")

        timestamp_str = time.strftime("%Y-%m-%d %H:%M:%S") + f".{(self.tick % 30):02d} IST"
        painter.setFont(QFont("Consolas", 10))
        painter.setPen(QColor("#38bdf8"))
        painter.drawText(w - 220, 25, timestamp_str)

        # Location banner
        painter.setFont(QFont("Segoe UI", 9))
        painter.setPen(QColor("#94a3b8"))
        loc_str = "Local Cyber Investigation Terminal // Auth INSP-DL-4902" if self.is_webcam_active else self.location
        painter.drawText(18, 45, f"📍 {loc_str}  |  RES: 4K UHD  |  FPS: 29.97  |  CCTNS HUD")

        # 4. Target Bounding Boxes (Simulated detections)
        if self.is_webcam_active:
            # Face scan box on operator
            cx = w * 0.5 - 110
            cy = h * 0.45 - 120
            self._draw_detection_box(
                painter,
                rect=QRectF(cx, cy, 220, 240),
                color=QColor("#10b981"),
                target_type="OPERATOR AUTHENTICATION",
                target_name="Inspector In-Charge (Authenticated)",
                extra_meta="CLEARANCE: LEVEL 5 // TERMINAL SECURE"
            )
        else:
            if "DEL" in self.camera_id:
                self._draw_detection_box(
                    painter,
                    rect=QRectF(w * 0.18, h * 0.35, w * 0.38, h * 0.48),
                    color=QColor("#ef4444"),
                    target_type="VEHICLE MATCH",
                    target_name="DL-01-AB-9821 (Toyota Fortuner)",
                    extra_meta="OWNER: Apex Global Impex | TINT: 100% Black | SPEED: 62 km/h"
                )
                self._draw_detection_box(
                    painter,
                    rect=QRectF(w * 0.62, h * 0.30, w * 0.22, h * 0.52),
                    color=QColor("#f59e0b"),
                    target_type="FACIAL RECOGNITION (98.4%)",
                    target_name="Amit 'Rana' Tyagi (P-104)",
                    extra_meta="CCTNS-2026-DL-1109 | ARMED / WANTED"
                )
            elif "MUM" in self.camera_id:
                self._draw_detection_box(
                    painter,
                    rect=QRectF(w * 0.30, h * 0.32, w * 0.28, h * 0.50),
                    color=QColor("#8b5cf6"),
                    target_type="SUBJECT SIGHTING",
                    target_name="Pooja Deshmukh (P-105)",
                    extra_meta="BlueOcean Logistics Office | HAWALA SUSPECT"
                )
            else:
                self._draw_detection_box(
                    painter,
                    rect=QRectF(w * 0.25, h * 0.30, w * 0.45, h * 0.50),
                    color=QColor("#10b981"),
                    target_type="ANPR TOLL CAPTURE",
                    target_name="KA-03-MM-1029 (White Swift)",
                    extra_meta="FASTag ID: 341689201 | TOLL PASS CONFIRMED"
                )

        # 5. Center Reticle Crosshairs
        painter.setPen(QPen(QColor(56, 189, 248, 120), 1))
        cx, cy = w / 2, h / 2
        painter.drawLine(int(cx - 20), int(cy), int(cx + 20), int(cy))
        painter.drawLine(int(cx), int(cy - 20), int(cx), int(cy + 20))

    def _draw_detection_box(self, painter: QPainter, rect: QRectF, color: QColor, target_type: str, target_name: str, extra_meta: str):
        pen = QPen(color, 2)
        painter.setPen(pen)
        painter.setBrush(QColor(color.red(), color.green(), color.blue(), 25))
        painter.drawRect(rect)

        arm = 12
        painter.setPen(QPen(color.lighter(130), 3))
        painter.drawLine(int(rect.left()), int(rect.top()), int(rect.left() + arm), int(rect.top()))
        painter.drawLine(int(rect.left()), int(rect.top()), int(rect.left()), int(rect.top() + arm))
        painter.drawLine(int(rect.right()), int(rect.top()), int(rect.right() - arm), int(rect.top()))
        painter.drawLine(int(rect.right()), int(rect.top()), int(rect.right()), int(rect.top() + arm))
        painter.drawLine(int(rect.left()), int(rect.bottom()), int(rect.left() + arm), int(rect.bottom()))
        painter.drawLine(int(rect.left()), int(rect.bottom()), int(rect.left()), int(rect.bottom() - arm))
        painter.drawLine(int(rect.right()), int(rect.bottom()), int(rect.right() - arm), int(rect.bottom()))
        painter.drawLine(int(rect.right()), int(rect.bottom()), int(rect.right()), int(rect.bottom() - arm))

        badge_rect = QRectF(rect.left(), rect.top() - 22, rect.width(), 20)
        painter.fillRect(badge_rect, color)
        painter.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        painter.setPen(QColor("#ffffff"))
        painter.drawText(badge_rect.adjusted(6, 0, -6, 0), Qt.AlignmentFlag.AlignVCenter, target_type)

        info_rect = QRectF(rect.left(), rect.bottom() + 4, rect.width(), 38)
        painter.fillRect(info_rect, QColor(15, 23, 42, 230))
        painter.setPen(QPen(color.darker(130), 1))
        painter.drawRect(info_rect)

        painter.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        painter.setPen(QColor("#f8fafc"))
        painter.drawText(info_rect.adjusted(6, 3, -6, 0), Qt.AlignmentFlag.AlignTop, target_name)

        painter.setFont(QFont("Consolas", 8))
        painter.setPen(QColor("#94a3b8"))
        painter.drawText(info_rect.adjusted(6, 20, -6, 0), Qt.AlignmentFlag.AlignTop, extra_meta)

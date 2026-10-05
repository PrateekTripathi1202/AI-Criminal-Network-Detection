"""
High-Tech Metric Card Widget for NCIS Dashboard
"""

from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt

class MetricCard(QFrame):
    def __init__(self, title: str, value: str, subtitle: str, badge_text: str = "", badge_color: str = "red", icon_symbol: str = "⚡", parent=None):
        super().__init__(parent)
        self.setObjectName("MetricCard")
        self.setStyleSheet(f"""
            #MetricCard {{
                background-color: #111827;
                border: 1px solid #1f2937;
                border-top: 3px solid {self._get_accent_hex(badge_color)};
                border-radius: 8px;
                padding: 12px;
            }}
            #MetricCard:hover {{
                border-color: #374151;
                border-top-color: {self._get_accent_hex(badge_color)};
                background-color: #141e33;
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(6)

        # Header Row: Icon + Title + Badge
        top_row = QHBoxLayout()
        top_row.setSpacing(8)

        icon_lbl = QLabel(icon_symbol)
        icon_lbl.setStyleSheet("font-size: 16px;")
        top_row.addWidget(icon_lbl)

        title_lbl = QLabel(title.upper())
        title_lbl.setStyleSheet("color: #94a3b8; font-size: 11px; font-weight: 700; letter-spacing: 0.5px;")
        top_row.addWidget(title_lbl)

        top_row.addStretch()

        if badge_text:
            badge_lbl = QLabel(badge_text)
            badge_lbl.setStyleSheet(self._get_badge_style(badge_color))
            top_row.addWidget(badge_lbl)

        layout.addLayout(top_row)

        # Main Value
        self.val_lbl = QLabel(value)
        self.val_lbl.setStyleSheet("color: #f8fafc; font-size: 24px; font-weight: 800; font-family: 'Segoe UI', sans-serif;")
        layout.addWidget(self.val_lbl)

        # Subtitle / Delta
        self.sub_lbl = QLabel(subtitle)
        self.sub_lbl.setStyleSheet("color: #64748b; font-size: 11px; font-weight: 500;")
        layout.addWidget(self.sub_lbl)

    def update_value(self, new_val: str, new_sub: str = ""):
        self.val_lbl.setText(new_val)
        if new_sub:
            self.sub_lbl.setText(new_sub)

    def _get_accent_hex(self, color: str) -> str:
        mapping = {
            "red": "#ef4444",
            "green": "#10b981",
            "blue": "#0284c7",
            "amber": "#f59e0b",
            "purple": "#8b5cf6",
            "cyan": "#06b6d4"
        }
        return mapping.get(color, "#0284c7")

    def _get_badge_style(self, color: str) -> str:
        hex_c = self._get_accent_hex(color)
        return f"""
            background-color: {hex_c}22;
            color: {hex_c};
            border: 1px solid {hex_c}55;
            border-radius: 10px;
            padding: 2px 8px;
            font-size: 10px;
            font-weight: bold;
        """

"""
High-Tech Cyber Law Enforcement Dark Theme (QSS Stylesheet)
For National Criminal Intelligence System (NCIS) CCTNS 4.0
"""

CYBER_THEME = """
/* Global Window & Typography */
QMainWindow, QDialog, QWidget {
    background-color: #0b0f19;
    color: #e2e8f0;
    font-family: "Segoe UI", "Inter", "Roboto", -apple-system, sans-serif;
    font-size: 13px;
}

/* Sidebar & Navigation */
#SidebarFrame {
    background-color: #0f172a;
    border-right: 1px solid #1e293b;
    min-width: 230px;
    max-width: 250px;
}

#SidebarTitle {
    color: #38bdf8;
    font-size: 15px;
    font-weight: bold;
    letter-spacing: 1px;
}

#SidebarSubtitle {
    color: #64748b;
    font-size: 10px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1.5px;
}

/* Navigation Buttons */
QPushButton.NavButton {
    background-color: transparent;
    color: #94a3b8;
    border: none;
    border-radius: 8px;
    padding: 10px 14px;
    text-align: left;
    font-size: 13px;
    font-weight: 500;
}

QPushButton.NavButton:hover {
    background-color: #1e293b;
    color: #38bdf8;
}

QPushButton.NavButton:checked {
    background-color: #1e3a8a;
    color: #ffffff;
    font-weight: 600;
    border-left: 3px solid #38bdf8;
}

/* Top App Header */
#HeaderFrame {
    background-color: #0f172a;
    border-bottom: 1px solid #1e293b;
    padding: 8px 16px;
}

#HeaderTitle {
    color: #f8fafc;
    font-size: 17px;
    font-weight: 700;
    letter-spacing: 0.5px;
}

#HeaderSubtitle {
    color: #0ea5e9;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 1px;
}

/* Badges & Pills */
QLabel.BadgeRed {
    background-color: rgba(239, 68, 68, 0.15);
    color: #f87171;
    border: 1px solid rgba(239, 68, 68, 0.35);
    border-radius: 12px;
    padding: 3px 10px;
    font-size: 11px;
    font-weight: bold;
}

QLabel.BadgeGreen {
    background-color: rgba(16, 185, 129, 0.15);
    color: #34d399;
    border: 1px solid rgba(16, 185, 129, 0.35);
    border-radius: 12px;
    padding: 3px 10px;
    font-size: 11px;
    font-weight: bold;
}

QLabel.BadgeBlue {
    background-color: rgba(56, 189, 248, 0.15);
    color: #38bdf8;
    border: 1px solid rgba(56, 189, 248, 0.35);
    border-radius: 12px;
    padding: 3px 10px;
    font-size: 11px;
    font-weight: bold;
}

QLabel.BadgeAmber {
    background-color: rgba(245, 158, 11, 0.15);
    color: #fbbf24;
    border: 1px solid rgba(245, 158, 11, 0.35);
    border-radius: 12px;
    padding: 3px 10px;
    font-size: 11px;
    font-weight: bold;
}

/* Card Containers */
QFrame.CardFrame {
    background-color: #131b2e;
    border: 1px solid #1e293b;
    border-radius: 10px;
}

QFrame.CardFrame:hover {
    border: 1px solid #2d3f66;
}

/* Standard Buttons */
QPushButton.PrimaryButton {
    background-color: #0284c7;
    color: #ffffff;
    border: 1px solid #38bdf8;
    border-radius: 6px;
    padding: 8px 16px;
    font-weight: 600;
    font-size: 12px;
}

QPushButton.PrimaryButton:hover {
    background-color: #0369a1;
}

QPushButton.PrimaryButton:pressed {
    background-color: #0c4a6e;
}

QPushButton.DangerButton {
    background-color: #dc2626;
    color: #ffffff;
    border: 1px solid #f87171;
    border-radius: 6px;
    padding: 8px 16px;
    font-weight: 600;
}

QPushButton.DangerButton:hover {
    background-color: #b91c1c;
}

QPushButton.SecondaryButton {
    background-color: #1e293b;
    color: #cbd5e1;
    border: 1px solid #334155;
    border-radius: 6px;
    padding: 8px 14px;
    font-weight: 500;
}

QPushButton.SecondaryButton:hover {
    background-color: #334155;
    color: #f8fafc;
}

/* Line Edits & Text Areas */
QLineEdit, QTextEdit, QPlainTextEdit {
    background-color: #0d1322;
    color: #f1f5f9;
    border: 1px solid #1e293b;
    border-radius: 6px;
    padding: 8px 10px;
    font-size: 13px;
    selection-background-color: #0284c7;
}

QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
    border: 1px solid #0284c7;
    background-color: #101728;
}

/* Combo Box */
QComboBox {
    background-color: #131b2e;
    color: #f1f5f9;
    border: 1px solid #25334d;
    border-radius: 6px;
    padding: 6px 12px;
    min-width: 140px;
}

QComboBox:hover {
    border: 1px solid #0284c7;
}

QComboBox QAbstractItemView {
    background-color: #0f172a;
    color: #f1f5f9;
    border: 1px solid #1e293b;
    selection-background-color: #1e3a8a;
    selection-color: #ffffff;
    padding: 4px;
}

/* Table Widget */
QTableWidget {
    background-color: #0d1322;
    border: 1px solid #1e293b;
    border-radius: 8px;
    gridline-color: #1a2438;
    color: #e2e8f0;
}

QTableWidget::item {
    padding: 6px 10px;
    border-bottom: 1px solid #162032;
}

QTableWidget::item:selected {
    background-color: #1e3a8a;
    color: #ffffff;
}

QHeaderView::section {
    background-color: #131b2e;
    color: #94a3b8;
    font-weight: 600;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    padding: 8px;
    border: none;
    border-bottom: 2px solid #1e293b;
}

/* Scrollbars */
QScrollBar:vertical {
    background: #0b0f19;
    width: 8px;
    margin: 0px;
    border-radius: 4px;
}

QScrollBar::handle:vertical {
    background: #25334d;
    min-height: 24px;
    border-radius: 4px;
}

QScrollBar::handle:vertical:hover {
    background: #0284c7;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    background: #0b0f19;
    height: 8px;
    margin: 0px;
    border-radius: 4px;
}

QScrollBar::handle:horizontal {
    background: #25334d;
    min-width: 24px;
    border-radius: 4px;
}

/* Tabs */
QTabWidget::pane {
    border: 1px solid #1e293b;
    background: #0f172a;
    border-radius: 8px;
}

QTabBar::tab {
    background: #0d1322;
    color: #94a3b8;
    border: 1px solid #1e293b;
    border-bottom: none;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    padding: 8px 16px;
    margin-right: 4px;
    font-weight: 500;
}

QTabBar::tab:selected {
    background: #131b2e;
    color: #38bdf8;
    border: 1px solid #0284c7;
    border-bottom: 2px solid #131b2e;
    font-weight: 600;
}

/* Status Bar */
QStatusBar {
    background-color: #0b0f19;
    border-top: 1px solid #1e293b;
    color: #64748b;
    font-size: 11px;
}

/* Sliders & Progress */
QProgressBar {
    background-color: #0d1322;
    border: 1px solid #1e293b;
    border-radius: 4px;
    text-align: center;
    color: #f8fafc;
    font-weight: bold;
    font-size: 11px;
}

QProgressBar::chunk {
    background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0284c7, stop:1 #38bdf8);
    border-radius: 4px;
}
"""

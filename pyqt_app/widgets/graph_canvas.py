"""
Interactive Criminal Knowledge Graph Canvas
Built using PyQt6 QGraphicsScene, QGraphicsView, and QPainter.
Supports drag-and-drop, zoom/pan, glowing risk rings, and node inspection.
"""

import math
from typing import Dict, Any, List, Optional
from PyQt6.QtWidgets import (
    QGraphicsView, QGraphicsScene, QGraphicsItem, QGraphicsEllipseItem,
    QGraphicsLineItem, QGraphicsTextItem, QGraphicsDropShadowEffect,
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame
)
from PyQt6.QtCore import Qt, QRectF, QPointF, pyqtSignal, QLineF
from PyQt6.QtGui import (
    QPainter, QPen, QBrush, QColor, QFont, QRadialGradient,
    QPainterPath, QCursor
)

# Color Scheme by Entity Type
TYPE_COLORS = {
    "person": QColor("#ef4444"),       # Red
    "phone": QColor("#0ea5e9"),        # Sky Blue
    "vehicle": QColor("#f59e0b"),      # Amber
    "account": QColor("#10b981"),      # Emerald Green
    "organization": QColor("#8b5cf6"), # Purple
    "location": QColor("#06b6d4"),     # Cyan
    "cctv": QColor("#ec4899")          # Pink
}

TYPE_ICONS = {
    "person": "👤",
    "phone": "📱",
    "vehicle": "🚗",
    "account": "💳",
    "organization": "🏢",
    "location": "📍",
    "cctv": "🎥"
}

class GraphEdgeItem(QGraphicsLineItem):
    def __init__(self, source_item, target_item, edge_data: Dict[str, Any]):
        super().__init__()
        self.source_item = source_item
        self.target_item = target_item
        self.edge_data = edge_data
        
        self.setZValue(1)
        pen = QPen(QColor("#334155"), 1.8, Qt.PenStyle.DashLine if "co_accused" in edge_data.get("type", "") else Qt.PenStyle.SolidLine)
        self.setPen(pen)
        self.update_position()

    def update_position(self):
        line = QLineF(self.source_item.pos(), self.target_item.pos())
        self.setLine(line)

    def paint(self, painter: QPainter, option, widget=None):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw base line
        super().paint(painter, option, widget)
        
        # Draw label midpoint
        line = self.line()
        if line.length() > 60:
            mid = line.pointAt(0.5)
            label = self.edge_data.get("label", "")
            if label:
                painter.setFont(QFont("Segoe UI", 8))
                painter.setPen(QColor("#94a3b8"))
                
                # Background pill
                metrics = painter.fontMetrics()
                rect = metrics.boundingRect(label)
                rect.moveCenter(mid.toPoint())
                rect.adjust(-4, -2, 4, 2)
                
                painter.fillRect(rect, QColor("#0f172a"))
                painter.drawRoundedRect(rect, 3, 3)
                painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, label)

class GraphNodeItem(QGraphicsItem):
    def __init__(self, node_data: Dict[str, Any], canvas):
        super().__init__()
        self.node_data = node_data
        self.canvas = canvas
        self.edges: List[GraphEdgeItem] = []
        
        self.radius = 26 if node_data.get("id") == "P-101" else 22
        self.is_kingpin = node_data.get("id") == "P-101" or node_data.get("metadata", {}).get("role") == "Syndicate Kingpin / Mastermind"
        
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges)
        self.setAcceptHoverEvents(True)
        self.setZValue(10)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.is_hovered = False

    def boundingRect(self) -> QRectF:
        r = self.radius + 14
        return QRectF(-r, -r, r * 2, r * 2 + 18)

    def shape(self) -> QPainterPath:
        path = QPainterPath()
        path.addEllipse(-self.radius, -self.radius, self.radius * 2, self.radius * 2)
        return path

    def paint(self, painter: QPainter, option, widget=None):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        node_type = self.node_data.get("type", "person").lower()
        color = TYPE_COLORS.get(node_type, QColor("#3b82f6"))
        
        # 1. Kingpin or Hover Outer Aura
        if self.is_kingpin or self.is_hovered or self.isSelected():
            glow_color = QColor("#f59e0b") if self.is_kingpin else color
            painter.setPen(QPen(glow_color, 2.5, Qt.PenStyle.SolidLine))
            painter.setBrush(QColor(glow_color.red(), glow_color.green(), glow_color.blue(), 45))
            aura_r = self.radius + 6
            painter.drawEllipse(-aura_r, -aura_r, aura_r * 2, aura_r * 2)

        # 2. Main Node Circle Gradient
        grad = QRadialGradient(-self.radius * 0.3, -self.radius * 0.3, self.radius * 1.5)
        grad.setColorAt(0, color.lighter(130))
        grad.setColorAt(0.7, color)
        grad.setColorAt(1, color.darker(150))
        
        painter.setPen(QPen(QColor("#ffffff") if self.isSelected() else color.darker(140), 2))
        painter.setBrush(QBrush(grad))
        painter.drawEllipse(-self.radius, -self.radius, self.radius * 2, self.radius * 2)

        # 3. Center Icon
        icon = "👑" if self.is_kingpin else TYPE_ICONS.get(node_type, "•")
        painter.setFont(QFont("Segoe UI Emoji", 12 if not self.is_kingpin else 14, QFont.Weight.Bold))
        painter.setPen(QColor("#ffffff"))
        painter.drawText(QRectF(-self.radius, -self.radius, self.radius * 2, self.radius * 2), Qt.AlignmentFlag.AlignCenter, icon)

        # 4. Bottom Node Label
        label = self.node_data.get("label", self.node_data.get("id"))
        if len(label) > 16:
            label = label[:14] + ".."
            
        painter.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        metrics = painter.fontMetrics()
        lbl_rect = metrics.boundingRect(label)
        lbl_rect.moveCenter(QPointF(0, self.radius + 12).toPoint())
        lbl_rect.adjust(-4, -1, 4, 1)

        # Pill background
        painter.fillRect(lbl_rect, QColor(15, 23, 42, 220))
        painter.setPen(QPen(QColor("#334155"), 1))
        painter.drawRoundedRect(lbl_rect, 3, 3)

        painter.setPen(QColor("#f8fafc"))
        painter.drawText(lbl_rect, Qt.AlignmentFlag.AlignCenter, label)

        # 5. Risk score badge top right
        risk = self.node_data.get("risk_score")
        if risk is not None:
            painter.setFont(QFont("Segoe UI", 7, QFont.Weight.Bold))
            badge_rect = QRectF(self.radius - 8, -self.radius - 4, 24, 13)
            risk_color = QColor("#ef4444") if risk > 80 else (QColor("#f59e0b") if risk > 65 else QColor("#10b981"))
            painter.fillRect(badge_rect, risk_color)
            painter.setPen(QColor("#ffffff"))
            painter.drawText(badge_rect, Qt.AlignmentFlag.AlignCenter, f"{int(risk)}")

    def itemChange(self, change, value):
        if change == QGraphicsItem.GraphicsItemChange.ItemPositionHasChanged:
            for edge in self.edges:
                edge.update_position()
        return super().itemChange(change, value)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.canvas.node_selected.emit(self.node_data)

    def hoverEnterEvent(self, event):
        self.is_hovered = True
        self.update()
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.is_hovered = False
        self.update()
        super().hoverLeaveEvent(event)


class CriminalGraphCanvas(QWidget):
    node_selected = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Controls bar at top of graph
        controls = QHBoxLayout()
        controls.setContentsMargins(12, 8, 12, 8)
        
        title = QLabel("TACTICAL KNOWLEDGE GRAPH")
        title.setStyleSheet("color: #38bdf8; font-weight: bold; font-size: 12px; letter-spacing: 1px;")
        controls.addWidget(title)

        controls.addStretch()

        self.btn_center = QPushButton("⌖ Recenter")
        self.btn_center.setProperty("class", "SecondaryButton")
        self.btn_center.clicked.connect(self.recenter_view)
        controls.addWidget(self.btn_center)

        self.btn_zoom_in = QPushButton("+ Zoom In")
        self.btn_zoom_in.setProperty("class", "SecondaryButton")
        self.btn_zoom_in.clicked.connect(lambda: self.view.scale(1.2, 1.2))
        controls.addWidget(self.btn_zoom_in)

        self.btn_zoom_out = QPushButton("- Zoom Out")
        self.btn_zoom_out.setProperty("class", "SecondaryButton")
        self.btn_zoom_out.clicked.connect(lambda: self.view.scale(0.83, 0.83))
        controls.addWidget(self.btn_zoom_out)

        layout.addLayout(controls)

        # Scene and View
        self.scene = QGraphicsScene()
        self.scene.setBackgroundBrush(QColor("#0b0f19"))
        
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.view.setRenderHint(QPainter.RenderHint.TextAntialiasing)
        self.view.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.view.setStyleSheet("border: 1px solid #1e293b; background-color: #0b0f19;")
        
        layout.addWidget(self.view)

        self.nodes_map: Dict[str, GraphNodeItem] = {}
        self.edges_list: List[GraphEdgeItem] = []

    def populate_graph(self, nodes: List[Dict[str, Any]], edges: List[Dict[str, Any]]):
        """Builds nodes and edges in dynamic concentric / clustered topology."""
        self.scene.clear()
        self.nodes_map.clear()
        self.edges_list.clear()

        # Layout algorithm:
        # Place Kingpin / core suspects in inner circle, phones/vehicles in middle ring, accounts/CCTV in outer ring
        center_x = 0
        center_y = 0

        # Separate nodes by category
        persons = [n for n in nodes if n.get("type") == "person"]
        phones = [n for n in nodes if n.get("type") == "phone"]
        vehicles = [n for n in nodes if n.get("type") == "vehicle"]
        accounts = [n for n in nodes if n.get("type") == "account"]
        others = [n for n in nodes if n.get("type") not in ("person", "phone", "vehicle", "account")]

        # Layout Persons (Inner Ring: R=130)
        p_count = max(len(persons), 1)
        for i, n in enumerate(persons):
            if n.get("id") == "P-101":
                # Kingpin placed at center top
                x, y = 0, -30
            else:
                angle = (2 * math.pi / (p_count)) * i
                x = 160 * math.cos(angle)
                y = 130 * math.sin(angle)
            item = GraphNodeItem(n, self)
            item.setPos(x, y)
            self.scene.addItem(item)
            self.nodes_map[n["id"]] = item

        # Layout Phones & Vehicles (Middle Ring: R=300)
        mid_nodes = phones + vehicles
        m_count = max(len(mid_nodes), 1)
        for i, n in enumerate(mid_nodes):
            angle = (2 * math.pi / m_count) * i + 0.3
            x = 310 * math.cos(angle)
            y = 260 * math.sin(angle)
            item = GraphNodeItem(n, self)
            item.setPos(x, y)
            self.scene.addItem(item)
            self.nodes_map[n["id"]] = item

        # Layout Accounts & Locations & CCTV (Outer Ring: R=450)
        outer_nodes = accounts + others
        o_count = max(len(outer_nodes), 1)
        for i, n in enumerate(outer_nodes):
            angle = (2 * math.pi / o_count) * i + 0.6
            x = 460 * math.cos(angle)
            y = 380 * math.sin(angle)
            item = GraphNodeItem(n, self)
            item.setPos(x, y)
            self.scene.addItem(item)
            self.nodes_map[n["id"]] = item

        # Create Edges
        for e in edges:
            src = self.nodes_map.get(e.get("source"))
            dst = self.nodes_map.get(e.get("target"))
            if src and dst:
                edge_item = GraphEdgeItem(src, dst, e)
                src.edges.append(edge_item)
                dst.edges.append(edge_item)
                self.scene.addItem(edge_item)
                self.edges_list.append(edge_item)

        self.recenter_view()

    def recenter_view(self):
        self.view.setSceneRect(self.scene.itemsBoundingRect().adjusted(-100, -100, 100, 100))
        self.view.fitInView(self.scene.itemsBoundingRect().adjusted(-60, -60, 60, 60), Qt.AspectRatioMode.KeepAspectRatio)

    def wheelEvent(self, event):
        zoom_factor = 1.15 if event.angleDelta().y() > 0 else 0.87
        self.view.scale(zoom_factor, zoom_factor)

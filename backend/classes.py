from PyQt5.QtWidgets import QLabel, QApplication, QWidget
from PyQt5.QtGui import QPainter, QPen, QPolygonF, QPixmap, QBrush, QColor
from PyQt5.QtCore import QPointF, Qt
import sys
import math


class StatsPolygon:
    def __init__(self, label, stats):
        """
        Initialize the radar chart with the QLabel passed as 'label' and the stats to plot.
        """
        self.label = label
        self.stats = stats  # Stats passed directly
        self.updatePolygon()

    def updatePolygon(self):
        pixmap = QPixmap(300, 320)
        pixmap.fill(Qt.transparent)

        # Initialize QPainter with the QPixmap
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)

        # Set the number of axes (equal to the number of stats)
        num_stats = len(self.stats)
        angle = 2 * math.pi / num_stats

        # Set the fixed radius for the chart
        radius = 100  # Radius of the chart
        center = QPointF(155, 160)  # Center of the chart in the 300x300 image

                # Draw the maximum polygon (outline for value = 1)
        max_polygon = QPolygonF()
        for i in range(num_stats):
            point = QPointF(
                center.x() + radius * math.cos(i * angle),
                center.y() - radius * math.sin(i * angle)
            )
            max_polygon.append(point)

        # Draw the outline polygon for the maximum possible values (value = 1)
        painter.setPen(QPen(QColor(200, 200, 200, 50), 2))  # White color for the outline
        painter.drawPolygon(max_polygon)

        # Apply ListView style to the polygon and axes
        painter.setPen(QPen(Qt.white, 3))  # White text color for axes lines and polygon outline

        # Create the polygon representing the stats
        polygon = QPolygonF()
        for i, (stat, value) in enumerate(self.stats.items()):
            r = value * radius
            point = QPointF(
                center.x() + r * math.cos(i * angle),
                center.y() - r * math.sin(i * angle)
            )
            polygon.append(point)

        painter.setBrush(QBrush(QColor(0, 200, 0)))  # Green fill color
        painter.setPen(Qt.NoPen)  # No outline
        painter.drawPolygon(polygon)

                # Set the font for the text labels
        painter.setPen(QColor(255, 255, 255))  # White color for the stat labels
        font_metrics = painter.fontMetrics()  # Get QFontMetrics to measure text size

        for i, stat in enumerate(self.stats.keys()):
            # Calculate the position for the text (radius + 15 to leave some space from the polygon)
            text_point = QPointF(
                center.x() + (radius + 25) * math.cos(i * angle),
                center.y() - (radius + 15) * math.sin(i * angle)
            )

            # Calculate the width and height of the text using QFontMetrics
            text_width = font_metrics.horizontalAdvance(stat)
            text_height = font_metrics.height()

            # Shift the text to center it horizontally and vertically
            shifted_point = QPointF(
                text_point.x() - text_width / 2,  # Shift left by half the text width
                text_point.y() + text_height / 4  # Shift up by half the text height
            )

            # Draw the text at the adjusted position
            painter.drawText(shifted_point, stat)

        painter.end()

        # Set the generated QPixmap on the QLabel
        self.label.setPixmap(pixmap)
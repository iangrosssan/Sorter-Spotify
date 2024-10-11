from PyQt5.QtWidgets import QLabel, QApplication, QWidget
from PyQt5.QtGui import QPainter, QPen, QPolygonF, QPixmap, QBrush, QColor
from PyQt5.QtCore import QPointF, Qt
import sys
import math


class PlaylistMetaData:
    def __init__(self):
        # Initialize cumulative sums and counts for track features
        self.total_danceability = 0
        self.total_energy = 0
        self.total_speechiness = 0
        self.total_acousticness = 0
        self.total_instrumentalness = 0
        self.total_valence = 0
        self.total_liveness = 0
        self.total_tempo = 0
        self.total_mode = 0
        self.track_count = 0
    
    def add_track(self, track_metadata):
        """Adds a track and updates cumulative sums and count."""
        self.total_danceability += track_metadata[0]
        self.total_energy += track_metadata[1]
        self.total_speechiness += track_metadata[2]
        self.total_acousticness += track_metadata[3]
        self.total_instrumentalness += track_metadata[4]
        self.total_valence += track_metadata[5]
        self.total_liveness += track_metadata[6]
        self.total_tempo += track_metadata[7]
        self.total_mode += track_metadata[8]
        self.track_count += 1
    
    def get_average_features(self):
        """Returns the average values for all the features."""
        if self.track_count == 0:
            return None
        
        avg_danceability = round(self.total_danceability / self.track_count, 2)
        avg_energy = round(self.total_energy / self.track_count, 2)
        avg_speechiness = round(self.total_speechiness / self.track_count, 2)
        avg_acousticness = round(self.total_acousticness / self.track_count, 2)
        avg_instrumentalness = round(self.total_instrumentalness / self.track_count, 2)
        avg_valence = round(self.total_valence / self.track_count, 2)
        avg_liveness = round(self.total_liveness / self.track_count, 2)
        avg_tempo = round(self.total_tempo / self.track_count, 2)
        avg_mode = round(self.total_mode / self.track_count, 2)
        
        return {
            'Dance': avg_danceability,
            'Energy': avg_energy,
            'Lyrical': avg_speechiness,
            'Acoustic': avg_acousticness,
            'Instrumental': avg_instrumentalness,
            'Valence': avg_valence
        }


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
        center = QPointF(140, 160)  # Center of the chart in the 300x300 image

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

        # Optionally draw stat names around the polygon (font color from ListView style)
        painter.setPen(QColor(255, 255, 255))  # White color for the stat labels

        for i, stat in enumerate(self.stats.keys()):
            text_point = QPointF(
                center.x() + (radius + 15) * math.cos(i * angle),
                center.y() - (radius + 15) * math.sin(i * angle)
            )
            painter.drawText(text_point, stat)

        painter.end()

        # Set the generated QPixmap on the QLabel
        self.label.setPixmap(pixmap)
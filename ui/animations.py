"""
Animation widget for displaying strike and spare celebrations.
"""

from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QGraphicsOpacityEffect
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QRect
from PyQt5.QtGui import QMovie, QFont
import os
import random


class AnimationWidget(QWidget):
    """Widget for displaying animated celebrations."""
    
    def __init__(self, parent=None):
        """Initialize the animation widget."""
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Container with background
        self.container = QWidget()
        self.container.setStyleSheet("""
            QWidget {
                background-color: rgba(44, 62, 80, 220);
                border-radius: 15px;
                border: 3px solid #27ae60;
            }
        """)
        
        container_layout = QVBoxLayout()
        container_layout.setSpacing(10)
        container_layout.setContentsMargins(20, 20, 20, 20)
        
        # Text label
        self.text_label = QLabel("")
        self.text_label.setFont(QFont("Arial", 24, QFont.Bold))
        self.text_label.setStyleSheet("color: white; background: transparent; border: none;")
        self.text_label.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(self.text_label)
        
        # GIF label (for future GIF support)
        self.gif_label = QLabel()
        self.gif_label.setAlignment(Qt.AlignCenter)
        self.gif_label.setStyleSheet("background: transparent; border: none;")
        self.gif_label.setMinimumSize(200, 200)
        container_layout.addWidget(self.gif_label)
        
        self.container.setLayout(container_layout)
        layout.addWidget(self.container)
        
        self.setLayout(layout)
        self.setFixedSize(300, 300)
        
        # Timer for auto-hide
        self.hide_timer = QTimer()
        self.hide_timer.timeout.connect(self.fade_out)
        
        # Movie object for GIF playback
        self.movie = None
        
        # Opacity effect for fade animations
        self.opacity_effect = QGraphicsOpacityEffect()
        self.container.setGraphicsEffect(self.opacity_effect)
        
        # Animation objects
        self.fade_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.scale_animation = QPropertyAnimation(self, b"geometry")
    
    def show_strike(self):
        """Display strike animation with random GIF selection."""
        self.text_label.setText("⚡ STRIKE! ⚡")
        self.container.setStyleSheet("""
            QWidget {
                background-color: rgba(231, 76, 60, 220);
                border-radius: 15px;
                border: 3px solid #c0392b;
            }
        """)
        
        # Try to load a random GIF from available strike GIFs
        gif_files = self._find_gif_files("strike")
        if gif_files:
            self._play_gif("strike")
        else:
            # Use emoji fallback
            self.gif_label.setFont(QFont("Arial", 72))
            self.gif_label.setText("💥")
        
        self._show_and_auto_hide()
    
    def show_spare(self):
        """Display spare animation with random GIF selection."""
        self.text_label.setText("✨ SPARE! ✨")
        self.container.setStyleSheet("""
            QWidget {
                background-color: rgba(52, 152, 219, 220);
                border-radius: 15px;
                border: 3px solid #2980b9;
            }
        """)
        
        # Try to load a random GIF from available spare GIFs
        gif_files = self._find_gif_files("spare")
        if gif_files:
            self._play_gif("spare")
        else:
            # Use emoji fallback
            self.gif_label.setFont(QFont("Arial", 72))
            self.gif_label.setText("🎯")
        
        self._show_and_auto_hide()
    
    def _find_gif_files(self, base_name: str) -> list:
        """
        Find all GIF files for a given base name (e.g., 'strike' finds strike.gif, strike1.gif, etc.)
        
        Args:
            base_name: Base name of the GIF (e.g., 'strike' or 'spare')
            
        Returns:
            List of found GIF file paths
        """
        gif_files = []
        assets_path = os.path.join("assets", "animations")
        
        # Check for base file (e.g., strike.gif)
        base_path = os.path.join(assets_path, f"{base_name}.gif")
        if os.path.exists(base_path):
            gif_files.append(base_path)
        
        # Check for numbered files (e.g., strike1.gif, strike2.gif, etc.)
        for i in range(1, 10):  # Support up to 9 variations
            numbered_path = os.path.join(assets_path, f"{base_name}{i}.gif")
            if os.path.exists(numbered_path):
                gif_files.append(numbered_path)
        
        return gif_files
    
    def _play_gif(self, base_name: str):
        """
        Load and play a random GIF animation from available files.
        
        Args:
            base_name: Base name of GIF files to choose from ('strike' or 'spare')
        """
        gif_files = self._find_gif_files(base_name)
        
        if gif_files:
            # Pick a random GIF from available files
            gif_path = random.choice(gif_files)
            
            if self.movie:
                self.movie.stop()
            
            self.movie = QMovie(gif_path)
            self.gif_label.setMovie(self.movie)
            self.movie.start()
            
            # Clear text from gif_label
            self.gif_label.setText("")
    
    def _show_and_auto_hide(self):
        """Show the widget and auto-hide after duration with animations."""
        # Center on parent
        if self.parent():
            parent_rect = self.parent().geometry()
            x = parent_rect.x() + (parent_rect.width() - self.width()) // 2
            y = parent_rect.y() + (parent_rect.height() - self.height()) // 2
            self.move(x, y)
        
        self.show()
        self.raise_()
        
        # Fade in animation
        self.opacity_effect.setOpacity(0)
        self.fade_animation.setDuration(300)  # 300ms
        self.fade_animation.setStartValue(0)
        self.fade_animation.setEndValue(1)
        self.fade_animation.setEasingCurve(QEasingCurve.OutCubic)
        self.fade_animation.start()
        
        # Scale in animation (pop effect)
        current_geo = self.geometry()
        start_geo = QRect(
            current_geo.x() + current_geo.width() // 4,
            current_geo.y() + current_geo.height() // 4,
            current_geo.width() // 2,
            current_geo.height() // 2
        )
        
        self.scale_animation.setDuration(300)
        self.scale_animation.setStartValue(start_geo)
        self.scale_animation.setEndValue(current_geo)
        self.scale_animation.setEasingCurve(QEasingCurve.OutBack)
        self.scale_animation.start()
        
        # Auto-hide after 2 seconds
        self.hide_timer.start(2000)
    
    def fade_out(self):
        """Fade out and then hide."""
        self.fade_animation.setDuration(300)
        self.fade_animation.setStartValue(1)
        self.fade_animation.setEndValue(0)
        self.fade_animation.setEasingCurve(QEasingCurve.InCubic)
        self.fade_animation.finished.connect(self.hide)
        self.fade_animation.start()
    
    def hide(self):
        """Override hide to stop movie and disconnect animation."""
        if self.movie:
            self.movie.stop()
        try:
            self.fade_animation.finished.disconnect(self.hide)
        except:
            pass
        super().hide()


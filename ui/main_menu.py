"""
Main menu screen for the bowling score tracker application.
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QSpacerItem, QSizePolicy)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont


class MainMenuScreen(QWidget):
    """Main menu screen with navigation buttons."""
    
    # Signals for navigation
    start_game_clicked = pyqtSignal()
    view_stats_clicked = pyqtSignal()
    manage_players_clicked = pyqtSignal()
    quit_clicked = pyqtSignal()
    
    def __init__(self):
        """Initialize the main menu screen."""
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """Set up the user interface."""
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(50, 50, 50, 50)
        
        # Title
        title = QLabel("🎳 Bowling Score Tracker")
        title_font = QFont("Arial", 32, QFont.Bold)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #2c3e50; margin: 20px;")
        layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Track Your Perfect Game")
        subtitle_font = QFont("Arial", 14)
        subtitle.setFont(subtitle_font)
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #7f8c8d; margin-bottom: 30px;")
        layout.addWidget(subtitle)
        
        # Add spacer
        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # Button container
        button_container = QVBoxLayout()
        button_container.setSpacing(15)
        
        # Create buttons
        self.start_game_btn = self._create_menu_button(
            "🎯 Start New Game",
            "#27ae60",
            "#2ecc71"
        )
        self.start_game_btn.clicked.connect(self.start_game_clicked.emit)
        
        self.view_stats_btn = self._create_menu_button(
            "📊 View Player Stats",
            "#2980b9",
            "#3498db"
        )
        self.view_stats_btn.clicked.connect(self.view_stats_clicked.emit)
        
        self.manage_players_btn = self._create_menu_button(
            "👥 Manage Players",
            "#8e44ad",
            "#9b59b6"
        )
        self.manage_players_btn.clicked.connect(self.manage_players_clicked.emit)
        
        self.quit_btn = self._create_menu_button(
            "❌ Quit",
            "#c0392b",
            "#e74c3c"
        )
        self.quit_btn.clicked.connect(self.quit_clicked.emit)
        
        # Add buttons to container
        button_container.addWidget(self.start_game_btn)
        button_container.addWidget(self.view_stats_btn)
        button_container.addWidget(self.manage_players_btn)
        button_container.addWidget(self.quit_btn)
        
        # Center the buttons
        button_layout = QHBoxLayout()
        button_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        button_layout.addLayout(button_container)
        button_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        layout.addLayout(button_layout)
        
        # Add spacer at bottom
        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # Footer
        footer = QLabel("Athlone Bowling League • v1.0")
        footer_font = QFont("Arial", 10)
        footer.setFont(footer_font)
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("color: #95a5a6;")
        layout.addWidget(footer)
        
        self.setLayout(layout)
        self.setStyleSheet("background-color: #ecf0f1;")
    
    def _create_menu_button(self, text: str, base_color: str, hover_color: str) -> QPushButton:
        """
        Create a styled menu button.
        
        Args:
            text: Button text
            base_color: Base background color
            hover_color: Hover background color
            
        Returns:
            Styled QPushButton
        """
        button = QPushButton(text)
        button.setMinimumSize(400, 70)
        button.setFont(QFont("Arial", 14, QFont.Bold))
        button.setCursor(Qt.PointingHandCursor)
        
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {base_color};
                color: white;
                border: none;
                border-radius: 10px;
                padding: 15px;
                text-align: center;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
            QPushButton:pressed {{
                background-color: {base_color};
            }}
        """)
        
        return button


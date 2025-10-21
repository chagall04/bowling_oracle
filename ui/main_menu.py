"""
main menu screen for bowling score tracker application
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QSpacerItem, QSizePolicy)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from ui.sound_manager import SoundManager


class MainMenuScreen(QWidget):
    """main menu screen with navigation buttons"""
    
    # signals for navigation
    start_game_clicked = pyqtSignal()
    view_stats_clicked = pyqtSignal()
    manage_players_clicked = pyqtSignal()
    settings_clicked = pyqtSignal()
    quit_clicked = pyqtSignal()
    
    def __init__(self):
        """initialize the main menu screen"""
        super().__init__()
        self.sound_manager = SoundManager()
        self.init_ui()
    
    def init_ui(self):
        """set up the user interface"""
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(50, 50, 50, 50)
        
        # title with decorative emojis
        title_layout = QHBoxLayout()
        
        # left decorative emojis
        left_emojis = QLabel("✨🔮🧙")
        left_emojis.setFont(QFont("Arial", 20))
        left_emojis.setStyleSheet("color: #f39c12;")
        title_layout.addWidget(left_emojis)
        
        # main title with purple banner background
        title = QLabel("🎳 Bowling Oracle 🔮")
        title_font = QFont("Arial", 36, QFont.Bold)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            color: white; 
            background-color: #9b59b6; 
            border: 3px solid #8e44ad;
            border-radius: 15px;
            padding: 20px;
            margin: 20px;
        """)
        title_layout.addWidget(title)
        
        # right decorative emojis
        right_emojis = QLabel("🧙🔮✨")
        right_emojis.setFont(QFont("Arial", 20))
        right_emojis.setStyleSheet("color: #f39c12;")
        title_layout.addWidget(right_emojis)
        
        layout.addLayout(title_layout)
        
        # add spacer
        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # button container
        button_container = QVBoxLayout()
        button_container.setSpacing(15)
        
        # create buttons
        self.start_game_btn = self._create_menu_button(
            "🔮 Start New Game 🔮",
            "#27ae60",
            "#2ecc71"
        )
        self.start_game_btn.clicked.connect(self.start_game_clicked.emit)
        
        self.view_stats_btn = self._create_menu_button(
            "✨ View Player Stats ✨",
            "#2980b9",
            "#3498db"
        )
        self.view_stats_btn.clicked.connect(self.view_stats_clicked.emit)
        
        self.manage_players_btn = self._create_menu_button(
            "🧙 Manage Players 🧙",
            "#8e44ad",
            "#9b59b6"
        )
        self.manage_players_btn.clicked.connect(self.manage_players_clicked.emit)
        
        self.settings_btn = self._create_menu_button(
            "⚙️ Settings ⚙️",
            "#34495e",
            "#2c3e50"
        )
        self.settings_btn.clicked.connect(self.settings_clicked.emit)
        
        self.quit_btn = self._create_menu_button(
            "🚪 Quit 🚪",
            "#c0392b",
            "#e74c3c"
        )
        self.quit_btn.clicked.connect(self.quit_clicked.emit)
        
        # add buttons to container
        button_container.addWidget(self.start_game_btn)
        button_container.addWidget(self.view_stats_btn)
        button_container.addWidget(self.manage_players_btn)
        button_container.addWidget(self.settings_btn)
        button_container.addWidget(self.quit_btn)
        
        # center the buttons
        button_layout = QHBoxLayout()
        button_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        button_layout.addLayout(button_container)
        button_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        layout.addLayout(button_layout)
        
        # add spacer at bottom
        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # add student info at bottom with no emojis
        student_info = QLabel("Charlie Gallagher - A00321687")
        student_info.setFont(QFont("Arial", 10))
        student_info.setAlignment(Qt.AlignCenter)
        student_info.setStyleSheet("""
            QLabel {
                color: #95a5a6;
                padding: 5px;
            }
        """)
        layout.addWidget(student_info)
        
        # set the layout on the widget
        self.setLayout(layout)
        self.setStyleSheet("background-color: #ecf0f1;")
    
    def showEvent(self, event):
        """called when the screen is shown"""
        super().showEvent(event)
        # stop any existing music first, then start menu music
        if hasattr(self, 'sound_manager'):
            self.sound_manager.stop_music()
            self.sound_manager.play_menu_music()
    
    def hideEvent(self, event):
        """called when the screen is hidden"""
        super().hideEvent(event)
        # don't stop music when leaving menu - let the next screen handle it
    
    def _create_menu_button(self, text: str, base_color: str, hover_color: str) -> QPushButton:
        """create a styled menu button"""
        button = QPushButton(text)
        button.setMinimumSize(600, 100)
        button.setFont(QFont("Arial", 20, QFont.Bold))
        button.setCursor(Qt.PointingHandCursor)
        
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {base_color};
                color: white;
                border: none;
                border-radius: 10px;
                padding: 20px;
                text-align: center;
                font-size: 22px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
            QPushButton:pressed {{
                background-color: {base_color};
                padding-top: 22px;
                padding-bottom: 18px;
            }}
        """)
        
        return button


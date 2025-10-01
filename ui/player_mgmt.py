"""
Player management screen for adding, removing, and searching players.
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QLineEdit, QListWidget, QListWidgetItem,
                             QMessageBox, QInputDialog)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from database import DatabaseHandler
import sqlite3


class PlayerManagementScreen(QWidget):
    """Screen for managing players in the database."""
    
    # Signal for navigation
    back_clicked = pyqtSignal()
    
    def __init__(self, db: DatabaseHandler):
        """
        Initialize the player management screen.
        
        Args:
            db: Database handler instance
        """
        super().__init__()
        self.db = db
        self.init_ui()
        self.load_players()
    
    def init_ui(self):
        """Set up the user interface."""
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Title
        title = QLabel("👥 Player Management")
        title_font = QFont("Arial", 24, QFont.Bold)
        title.setFont(title_font)
        title.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # Search bar
        search_layout = QHBoxLayout()
        search_label = QLabel("Search:")
        search_label.setFont(QFont("Arial", 11))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter player name...")
        self.search_input.setFont(QFont("Arial", 11))
        self.search_input.textChanged.connect(self.search_players)
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)
        
        # Player list
        self.player_list = QListWidget()
        self.player_list.setFont(QFont("Arial", 12))
        self.player_list.setStyleSheet("""
            QListWidget {
                background-color: white;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                padding: 5px;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #ecf0f1;
            }
            QListWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
        """)
        layout.addWidget(self.player_list)
        
        # Button layout
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        # Add player button
        self.add_btn = QPushButton("➕ Add Player")
        self.add_btn.setFont(QFont("Arial", 11, QFont.Bold))
        self.add_btn.setMinimumHeight(40)
        self.add_btn.setCursor(Qt.PointingHandCursor)
        self.add_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
        """)
        self.add_btn.clicked.connect(self.add_player)
        
        # Delete player button
        self.delete_btn = QPushButton("🗑️ Delete Player")
        self.delete_btn.setFont(QFont("Arial", 11, QFont.Bold))
        self.delete_btn.setMinimumHeight(40)
        self.delete_btn.setCursor(Qt.PointingHandCursor)
        self.delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #c0392b;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #e74c3c;
            }
        """)
        self.delete_btn.clicked.connect(self.delete_player)
        
        # Back button
        self.back_btn = QPushButton("⬅️ Back to Main Menu")
        self.back_btn.setFont(QFont("Arial", 11, QFont.Bold))
        self.back_btn.setMinimumHeight(40)
        self.back_btn.setCursor(Qt.PointingHandCursor)
        self.back_btn.setStyleSheet("""
            QPushButton {
                background-color: #7f8c8d;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #95a5a6;
            }
        """)
        self.back_btn.clicked.connect(self.back_clicked.emit)
        
        button_layout.addWidget(self.add_btn)
        button_layout.addWidget(self.delete_btn)
        button_layout.addWidget(self.back_btn)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        self.setStyleSheet("background-color: #ecf0f1;")
    
    def load_players(self):
        """Load all players from the database into the list."""
        self.player_list.clear()
        players = self.db.get_all_players()
        
        for player in players:
            item_text = f"{player['player_name']} (Joined: {player['date_joined'][:10]})"
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, player['player_id'])  # Store player ID
            self.player_list.addItem(item)
        
        # Update count
        count_label = f"Total Players: {len(players)}"
        self.setWindowTitle(f"Player Management - {count_label}")
    
    def search_players(self):
        """Filter players based on search input."""
        search_term = self.search_input.text().strip()
        
        if not search_term:
            self.load_players()
            return
        
        self.player_list.clear()
        players = self.db.search_players(search_term)
        
        for player in players:
            item_text = f"{player['player_name']} (Joined: {player['date_joined'][:10]})"
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, player['player_id'])
            self.player_list.addItem(item)
    
    def add_player(self):
        """Add a new player to the database."""
        name, ok = QInputDialog.getText(
            self,
            "Add New Player",
            "Enter player name:"
        )
        
        if ok and name.strip():
            try:
                self.db.add_player(name.strip())
                self.load_players()
                QMessageBox.information(
                    self,
                    "Success",
                    f"Player '{name.strip()}' added successfully!"
                )
            except sqlite3.IntegrityError:
                QMessageBox.warning(
                    self,
                    "Error",
                    f"Player '{name.strip()}' already exists!"
                )
    
    def delete_player(self):
        """Delete the selected player from the database."""
        current_item = self.player_list.currentItem()
        
        if not current_item:
            QMessageBox.warning(
                self,
                "No Selection",
                "Please select a player to delete."
            )
            return
        
        player_id = current_item.data(Qt.UserRole)
        player_name = current_item.text().split(" (")[0]
        
        # Confirm deletion
        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete '{player_name}'?\n\n"
            f"This will also delete all their game records!",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.db.delete_player(player_id)
            self.load_players()
            QMessageBox.information(
                self,
                "Success",
                f"Player '{player_name}' deleted successfully!"
            )
    
    def showEvent(self, event):
        """Reload players when screen is shown."""
        super().showEvent(event)
        self.load_players()
        self.search_input.clear()


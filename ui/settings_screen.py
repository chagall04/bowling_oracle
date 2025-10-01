"""
Settings screen for app configuration and data management.
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QMessageBox, QFileDialog, QGroupBox,
                             QRadioButton, QButtonGroup)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from database import DatabaseHandler
import csv
from datetime import datetime


class SettingsScreen(QWidget):
    """Settings screen for app configuration."""
    
    # Signals
    back_clicked = pyqtSignal()
    theme_changed = pyqtSignal(str)  # Emits 'light' or 'dark'
    
    def __init__(self, db: DatabaseHandler):
        """
        Initialize the settings screen.
        
        Args:
            db: Database handler instance
        """
        super().__init__()
        self.db = db
        self.current_theme = 'light'
        self.init_ui()
    
    def init_ui(self):
        """Set up the user interface."""
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Title
        title = QLabel("⚙️ Settings")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # Theme Settings Group
        theme_group = QGroupBox("Appearance")
        theme_group.setFont(QFont("Arial", 12, QFont.Bold))
        theme_layout = QVBoxLayout()
        
        theme_label = QLabel("Theme:")
        theme_label.setFont(QFont("Arial", 11))
        theme_layout.addWidget(theme_label)
        
        # Radio buttons for theme
        self.theme_button_group = QButtonGroup()
        
        self.light_mode_radio = QRadioButton("☀️ Light Mode")
        self.light_mode_radio.setFont(QFont("Arial", 11))
        self.light_mode_radio.setChecked(True)
        self.light_mode_radio.toggled.connect(lambda: self.on_theme_changed('light'))
        
        self.dark_mode_radio = QRadioButton("🌙 Dark Mode")
        self.dark_mode_radio.setFont(QFont("Arial", 11))
        self.dark_mode_radio.toggled.connect(lambda: self.on_theme_changed('dark'))
        
        self.theme_button_group.addButton(self.light_mode_radio)
        self.theme_button_group.addButton(self.dark_mode_radio)
        
        theme_layout.addWidget(self.light_mode_radio)
        theme_layout.addWidget(self.dark_mode_radio)
        
        theme_group.setLayout(theme_layout)
        layout.addWidget(theme_group)
        
        # Data Management Group
        data_group = QGroupBox("Data Management")
        data_group.setFont(QFont("Arial", 12, QFont.Bold))
        data_layout = QVBoxLayout()
        
        # Export buttons
        export_label = QLabel("Export Data:")
        export_label.setFont(QFont("Arial", 11))
        data_layout.addWidget(export_label)
        
        export_btn_layout = QHBoxLayout()
        
        self.export_players_btn = QPushButton("📊 Export Players to CSV")
        self.export_players_btn.setFont(QFont("Arial", 10))
        self.export_players_btn.setMinimumHeight(35)
        self.export_players_btn.setCursor(Qt.PointingHandCursor)
        self.export_players_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.export_players_btn.clicked.connect(self.export_players_csv)
        
        self.export_games_btn = QPushButton("🎳 Export Games to CSV")
        self.export_games_btn.setFont(QFont("Arial", 10))
        self.export_games_btn.setMinimumHeight(35)
        self.export_games_btn.setCursor(Qt.PointingHandCursor)
        self.export_games_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.export_games_btn.clicked.connect(self.export_games_csv)
        
        export_btn_layout.addWidget(self.export_players_btn)
        export_btn_layout.addWidget(self.export_games_btn)
        data_layout.addLayout(export_btn_layout)
        
        # Wipe data section
        wipe_label = QLabel("⚠️ Danger Zone:")
        wipe_label.setFont(QFont("Arial", 11))
        wipe_label.setStyleSheet("color: #e74c3c; margin-top: 15px;")
        data_layout.addWidget(wipe_label)
        
        self.wipe_data_btn = QPushButton("🗑️ Wipe All Data")
        self.wipe_data_btn.setFont(QFont("Arial", 10, QFont.Bold))
        self.wipe_data_btn.setMinimumHeight(35)
        self.wipe_data_btn.setCursor(Qt.PointingHandCursor)
        self.wipe_data_btn.setStyleSheet("""
            QPushButton {
                background-color: #c0392b;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #e74c3c;
            }
        """)
        self.wipe_data_btn.clicked.connect(self.wipe_all_data)
        data_layout.addWidget(self.wipe_data_btn)
        
        data_group.setLayout(data_layout)
        layout.addWidget(data_group)
        
        # Add stretch
        layout.addStretch()
        
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
            }
            QPushButton:hover {
                background-color: #95a5a6;
            }
        """)
        self.back_btn.clicked.connect(self.back_clicked.emit)
        layout.addWidget(self.back_btn)
        
        self.setLayout(layout)
        self.setStyleSheet("background-color: #ecf0f1;")
    
    def on_theme_changed(self, theme: str):
        """
        Handle theme change.
        
        Args:
            theme: 'light' or 'dark'
        """
        if self.sender().isChecked():
            self.current_theme = theme
            self.theme_changed.emit(theme)
            QMessageBox.information(
                self,
                "Theme Changed",
                f"{theme.capitalize()} mode activated!\n\n"
                f"(Theme will apply on next app restart)"
            )
    
    def export_players_csv(self):
        """Export all players to CSV file."""
        players = self.db.get_all_players()
        
        if not players:
            QMessageBox.information(
                self,
                "No Data",
                "No players to export!"
            )
            return
        
        # Get save location
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Players",
            f"bowling_players_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            "CSV Files (*.csv)"
        )
        
        if not file_path:
            return
        
        try:
            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Player ID', 'Player Name', 'Date Joined', 
                               'Total Games', 'High Score', 'Average Score', 'Strike %'])
                
                for player in players:
                    stats = self.db.get_player_stats(player['player_id'])
                    writer.writerow([
                        player['player_id'],
                        player['player_name'],
                        player['date_joined'],
                        stats['total_games'],
                        stats['high_score'],
                        stats['average_score'],
                        stats['strike_percentage']
                    ])
            
            QMessageBox.information(
                self,
                "Export Successful",
                f"Players exported to:\n{file_path}"
            )
        
        except Exception as e:
            QMessageBox.critical(
                self,
                "Export Failed",
                f"Error exporting players:\n{str(e)}"
            )
    
    def export_games_csv(self):
        """Export all games to CSV file."""
        # Get all players to get their games
        players = self.db.get_all_players()
        all_games = []
        
        for player in players:
            games = self.db.get_player_games(player['player_id'])
            for game in games:
                all_games.append({
                    'game_id': game['game_id'],
                    'player_name': player['player_name'],
                    'final_score': game['final_score'],
                    'game_date': game['game_date']
                })
        
        if not all_games:
            QMessageBox.information(
                self,
                "No Data",
                "No games to export!"
            )
            return
        
        # Get save location
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Games",
            f"bowling_games_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            "CSV Files (*.csv)"
        )
        
        if not file_path:
            return
        
        try:
            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Game ID', 'Player Name', 'Final Score', 'Game Date'])
                
                for game in all_games:
                    writer.writerow([
                        game['game_id'],
                        game['player_name'],
                        game['final_score'],
                        game['game_date']
                    ])
            
            QMessageBox.information(
                self,
                "Export Successful",
                f"Games exported to:\n{file_path}"
            )
        
        except Exception as e:
            QMessageBox.critical(
                self,
                "Export Failed",
                f"Error exporting games:\n{str(e)}"
            )
    
    def wipe_all_data(self):
        """Wipe all data from the database after confirmation."""
        reply = QMessageBox.warning(
            self,
            "⚠️ Confirm Data Wipe",
            "Are you ABSOLUTELY SURE you want to delete ALL data?\n\n"
            "This will permanently remove:\n"
            "• All players\n"
            "• All games\n"
            "• All game history\n\n"
            "THIS CANNOT BE UNDONE!",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply != QMessageBox.Yes:
            return
        
        # Second confirmation
        reply2 = QMessageBox.warning(
            self,
            "⚠️ Final Confirmation",
            "This is your last chance!\n\n"
            "Delete everything?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply2 != QMessageBox.Yes:
            return
        
        try:
            # Delete all data
            self.db.cursor.execute("DELETE FROM Frame")
            self.db.cursor.execute("DELETE FROM Game")
            self.db.cursor.execute("DELETE FROM Player")
            self.db.connection.commit()
            
            QMessageBox.information(
                self,
                "Data Wiped",
                "All data has been permanently deleted."
            )
        
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to wipe data:\n{str(e)}"
            )


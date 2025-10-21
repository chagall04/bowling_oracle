"""
settings screen for app configuration and data management
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QMessageBox, QFileDialog, QGroupBox,
                             QSpacerItem, QSizePolicy)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from database import DatabaseHandler
import csv
from datetime import datetime
from ui.sound_manager import SoundManager


class SettingsScreen(QWidget):
    """settings screen for app configuration"""
    
    # signals
    back_clicked = pyqtSignal()  # emits when back button clicked
    
    def __init__(self, db: DatabaseHandler):
        """initialize settings screen"""
        super().__init__()
        self.db = db
        self.sound_manager = SoundManager()
        self.init_ui()
    
    def init_ui(self):
        """set up user interface"""
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Title
        title = QLabel("⚙️ Settings")
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        layout.addWidget(title)
        
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
                background-color: #a93226;
            }
        """)
        self.wipe_data_btn.clicked.connect(self.wipe_all_data)
        
        data_layout.addWidget(self.wipe_data_btn)
        data_group.setLayout(data_layout)
        layout.addWidget(data_group)
        
        # Add spacer
        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        # Back button
        self.back_btn = QPushButton("← Back to Main Menu")
        self.back_btn.setFont(QFont("Arial", 12))
        self.back_btn.setMinimumHeight(40)
        self.back_btn.setCursor(Qt.PointingHandCursor)
        self.back_btn.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        self.back_btn.clicked.connect(self.back_clicked.emit)
        layout.addWidget(self.back_btn)
        
        self.setLayout(layout)
        self.setStyleSheet("background-color: #ecf0f1;")
    
    def showEvent(self, event):
        """called when screen is shown"""
        super().showEvent(event)
        if hasattr(self, 'sound_manager'):
            self.sound_manager.stop_music()
            self.sound_manager.play_menu_music()
    
    def hideEvent(self, event):
        """called when screen is hidden"""
        super().hideEvent(event)
        if hasattr(self, 'sound_manager'):
            self.sound_manager.stop_music()
    
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
        
        if file_path:
            try:
                with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(['Player ID', 'Name', 'Games Played', 'Average Score', 'High Score', 'Low Score'])
                    
                    for player in players:
                        writer.writerow([
                            player['id'],
                            player['name'],
                            player['games_played'],
                            player['average_score'],
                            player['high_score'],
                            player['low_score']
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
                    f"Failed to export players:\n{str(e)}"
                )
    
    def export_games_csv(self):
        """Export all games to CSV file."""
        games = self.db.get_all_games()
        
        if not games:
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
        
        if file_path:
            try:
                with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(['Game ID', 'Player ID', 'Player Name', 'Total Score', 'Date Played'])
                    
                    for game in games:
                        writer.writerow([
                            game['id'],
                            game['player_id'],
                            game['player_name'],
                            game['total_score'],
                            game['date_played']
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
                    f"Failed to export games:\n{str(e)}"
                )
    
    def wipe_all_data(self):
        """Wipe all data with confirmation."""
        reply = QMessageBox.question(
            self,
            "Confirm Data Wipe",
            "⚠️ WARNING: This will permanently delete ALL data!\n\n"
            "This includes:\n"
            "• All players\n"
            "• All games\n"
            "• All statistics\n\n"
            "This action cannot be undone!\n\n"
            "Are you absolutely sure?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Double confirmation
            reply2 = QMessageBox.question(
                self,
                "Final Confirmation",
                "🚨 LAST CHANCE! 🚨\n\n"
                "You are about to delete EVERYTHING!\n\n"
                "Type 'DELETE' in your mind and click Yes if you're sure.",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply2 == QMessageBox.Yes:
                try:
                    self.db.wipe_all_data()
                    QMessageBox.information(
                        self,
                        "Data Wiped",
                        "All data has been permanently deleted."
                    )
                except Exception as e:
                    QMessageBox.critical(
                        self,
                        "Wipe Failed",
                        f"Failed to wipe data:\n{str(e)}"
                    )
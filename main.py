"""
Main application entry point for Bowling Oracle.
"""

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from database import DatabaseHandler
from ui.main_menu import MainMenuScreen
from ui.scoring_screen import ScoringScreen
from ui.stats_screen import StatsScreen
from ui.player_mgmt import PlayerManagementScreen
from ui.game_over import GameOverScreen
from ui.settings_screen import SettingsScreen


class BowlingOracleApp(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        """Initialize the application."""
        super().__init__()
        
        # Initialize database
        self.db = DatabaseHandler()
        
        # Set up main window
        self.setWindowTitle("🎳 Bowling Oracle 🔮")
        self.setMinimumSize(1200, 800)
        
        # Create stacked widget for screen management
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        # Initialize screens
        self.main_menu = MainMenuScreen()
        self.scoring_screen = ScoringScreen(self.db)
        self.stats_screen = StatsScreen(self.db)
        self.player_mgmt = PlayerManagementScreen(self.db)
        self.game_over = GameOverScreen()
        self.settings_screen = SettingsScreen(self.db)
        
        # Add screens to stacked widget
        self.stacked_widget.addWidget(self.main_menu)
        self.stacked_widget.addWidget(self.scoring_screen)
        self.stacked_widget.addWidget(self.stats_screen)
        self.stacked_widget.addWidget(self.player_mgmt)
        self.stacked_widget.addWidget(self.game_over)
        self.stacked_widget.addWidget(self.settings_screen)
        
        # Connect signals
        self.connect_signals()
        
        # Show main menu
        self.stacked_widget.setCurrentIndex(0)
    
    def connect_signals(self):
        """Connect all signal-slot connections."""
        # Main menu signals
        self.main_menu.start_game_clicked.connect(self.start_game)
        self.main_menu.view_stats_clicked.connect(self.show_stats)
        self.main_menu.manage_players_clicked.connect(self.show_player_mgmt)
        self.main_menu.settings_clicked.connect(self.show_settings)
        self.main_menu.quit_clicked.connect(self.close)
        
        # Scoring screen signals
        self.scoring_screen.game_completed.connect(self.show_game_over)
        self.scoring_screen.back_clicked.connect(self.show_main_menu)
        
        # Stats screen signals
        self.stats_screen.back_clicked.connect(self.show_main_menu)
        
        # Player management signals
        self.player_mgmt.back_clicked.connect(self.show_main_menu)
        
        # Game over signals
        self.game_over.rematch_clicked.connect(self.start_game)
        self.game_over.main_menu_clicked.connect(self.show_main_menu)
        
        # Connect settings signals
        self.main_menu.settings_clicked.connect(self.show_settings)
        self.settings_screen.back_clicked.connect(self.show_main_menu)
    
    def start_game(self):
        """Start a new game."""
        players = self.db.get_all_players()
        
        if not players:
            QMessageBox.information(
                self,
                "No Players",
                "Please add players before starting a game."
            )
            return
        
        self.scoring_screen.start_new_game(players)
        self.stacked_widget.setCurrentIndex(1)
    
    def show_main_menu(self):
        """Show the main menu."""
        self.stacked_widget.setCurrentIndex(0)
    
    def show_player_mgmt(self):
        """Show the player management screen."""
        self.player_mgmt.refresh_players()
        self.stacked_widget.setCurrentIndex(3)
    
    def show_stats(self):
        """Show the statistics screen."""
        players = self.db.get_all_players()
        
        if not players:
            QMessageBox.information(
                self,
                "No Players",
                "Please add players before viewing statistics."
            )
            return
        
        self.stacked_widget.setCurrentIndex(3)
    
    def show_settings(self):
        """Show the settings screen."""
        self.stacked_widget.setCurrentIndex(5)
    
    def show_game_over(self, game_data):
        """Show the game over screen with results."""
        self.game_over.show_results(game_data)
        self.stacked_widget.setCurrentIndex(4)


def main():
    """Main entry point."""
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Bowling Oracle")
    app.setApplicationVersion("1.0")
    
    # Create and show main window
    window = BowlingOracleApp()
    window.show()
    
    # Start event loop
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
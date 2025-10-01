"""
Main application entry point for Bowling Score Tracker.
Integrates all screens and manages navigation.
"""

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from database import DatabaseHandler
from ui.main_menu import MainMenuScreen
from ui.player_mgmt import PlayerManagementScreen
from ui.scoring_screen import ScoringScreen
from ui.stats_screen import StatsScreen
from ui.game_over import GameOverScreen
from ui.animations import AnimationWidget


class BowlingTrackerApp(QMainWindow):
    """Main application window managing all screens."""
    
    def __init__(self):
        """Initialize the main application."""
        super().__init__()
        
        # Initialize database
        self.db = DatabaseHandler()
        
        # Set up main window
        self.setWindowTitle("Bowling Score Tracker")
        self.setMinimumSize(1200, 800)
        
        # Create stacked widget for screen management
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        # Initialize screens
        self.main_menu = MainMenuScreen()
        self.player_mgmt = PlayerManagementScreen(self.db)
        self.scoring_screen = ScoringScreen(self.db)
        self.stats_screen = StatsScreen(self.db)
        self.game_over_screen = GameOverScreen()
        
        # Add screens to stacked widget
        self.stacked_widget.addWidget(self.main_menu)         # Index 0
        self.stacked_widget.addWidget(self.player_mgmt)       # Index 1
        self.stacked_widget.addWidget(self.scoring_screen)    # Index 2
        self.stacked_widget.addWidget(self.stats_screen)      # Index 3
        self.stacked_widget.addWidget(self.game_over_screen)  # Index 4
        
        # Animation widget
        self.animation_widget = AnimationWidget(self)
        
        # Connect signals
        self._connect_signals()
        
        # Show main menu
        self.show_main_menu()
        
        # Center window on screen
        self.center_on_screen()
    
    def center_on_screen(self):
        """Center the window on the screen."""
        screen = QApplication.desktop().screenGeometry()
        window = self.geometry()
        x = (screen.width() - window.width()) // 2
        y = (screen.height() - window.height()) // 2
        self.move(x, y)
    
    def _connect_signals(self):
        """Connect all signal handlers for navigation."""
        # Main menu signals
        self.main_menu.start_game_clicked.connect(self.show_game_setup)
        self.main_menu.view_stats_clicked.connect(self.show_stats)
        self.main_menu.manage_players_clicked.connect(self.show_player_management)
        self.main_menu.quit_clicked.connect(self.quit_application)
        
        # Player management signals
        self.player_mgmt.back_clicked.connect(self.show_main_menu)
        
        # Scoring screen signals
        self.scoring_screen.game_complete.connect(self.show_game_over)
        self.scoring_screen.back_clicked.connect(self.show_main_menu)
        
        # Stats screen signals
        self.stats_screen.back_clicked.connect(self.show_main_menu)
        
        # Game over screen signals
        self.game_over_screen.rematch_clicked.connect(self.start_rematch)
        self.game_over_screen.main_menu_clicked.connect(self.show_main_menu)
    
    def show_main_menu(self):
        """Show the main menu screen."""
        self.stacked_widget.setCurrentIndex(0)
    
    def show_player_management(self):
        """Show the player management screen."""
        self.stacked_widget.setCurrentIndex(1)
    
    def show_game_setup(self):
        """Show game setup and start new game."""
        # Start new game (this will show player selection dialog)
        if self.scoring_screen.start_new_game():
            self.stacked_widget.setCurrentIndex(2)
            # Connect animation triggers
            self.scoring_screen.show_animation = self.show_animation
    
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
    
    def show_game_over(self, results):
        """
        Show the game over screen with results.
        
        Args:
            results: List of game results
        """
        self.game_over_screen.display_results(results)
        self.stacked_widget.setCurrentIndex(4)
    
    def start_rematch(self, player_ids):
        """
        Start a rematch with the same players.
        
        Args:
            player_ids: List of player IDs to include in rematch
        """
        # Get player data
        players = []
        for player_id in player_ids:
            player_data = self.db.get_player(player_id)
            if player_data:
                players.append(player_data)
        
        if not players:
            QMessageBox.warning(self, "Error", "Could not load player data for rematch.")
            return
        
        # Create new games for players
        from scoring import GameManager
        self.scoring_screen.game_manager = GameManager()
        
        for player_data in players:
            game_id = self.db.create_game(player_data['player_id'])
            self.scoring_screen.game_manager.add_player(
                player_data['player_id'],
                player_data['player_name'],
                game_id
            )
        
        # Build scorecard and show scoring screen
        self.scoring_screen.build_scorecard()
        self.scoring_screen.update_display()
        self.stacked_widget.setCurrentIndex(2)
    
    def show_animation(self, animation_type: str):
        """
        Show strike or spare animation.
        
        Args:
            animation_type: 'strike' or 'spare'
        """
        if animation_type == 'strike':
            self.animation_widget.show_strike()
        elif animation_type == 'spare':
            self.animation_widget.show_spare()
    
    def quit_application(self):
        """Quit the application."""
        reply = QMessageBox.question(
            self,
            "Quit Application",
            "Are you sure you want to quit?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.db.close()
            QApplication.quit()
    
    def closeEvent(self, event):
        """Handle window close event."""
        self.db.close()
        event.accept()


def main():
    """Main entry point for the application."""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Modern look
    
    # Set application metadata
    app.setApplicationName("Bowling Score Tracker")
    app.setOrganizationName("Athlone Bowling League")
    
    # Create and show main window
    window = BowlingTrackerApp()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()


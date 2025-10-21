"""
bowling oracle - main application
"""

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

# import modules
from database import DatabaseHandler
from ui.main_menu import MainMenuScreen
from ui.scoring_screen import ScoringScreen
from ui.stats_screen import StatsScreen
from ui.player_mgmt import PlayerManagementScreen
from ui.game_over import GameOverScreen
from ui.settings_screen import SettingsScreen


class BowlingOracleApp(QMainWindow):
    """main application window that manages all screens"""
    
    def __init__(self):
        super().__init__()
        
        # connect to sqlite database
        self.db = DatabaseHandler()
        
        # set up main window
        self.setWindowTitle("🎳 Bowling Oracle 🔮")
        self.setMinimumSize(1200, 800)
        
        # create stacked widget to hold all screens
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        # create all screens
        self.main_menu = MainMenuScreen()
        self.scoring_screen = ScoringScreen(self.db)
        self.stats_screen = StatsScreen(self.db)
        self.player_mgmt = PlayerManagementScreen(self.db)
        self.game_over = GameOverScreen()
        self.settings_screen = SettingsScreen(self.db)
        
        # add screens to stacked widget
        # each screen gets index number (0, 1, 2, etc.)
        self.stacked_widget.addWidget(self.main_menu)           # index 0
        self.stacked_widget.addWidget(self.scoring_screen)      # index 1
        self.stacked_widget.addWidget(self.stats_screen)        # index 2
        self.stacked_widget.addWidget(self.player_mgmt)         # index 3
        self.stacked_widget.addWidget(self.game_over)           # index 4
        self.stacked_widget.addWidget(self.settings_screen)     # index 5
        
        # connect all the button signals to methods
        self.connect_signals()
        
        # start by showing main menu
        self.stacked_widget.setCurrentIndex(0)
    
    def connect_signals(self):
        """connect all button clicks to their corresponding methods"""
        # main menu button connections
        self.main_menu.start_game_clicked.connect(self.start_game)
        self.main_menu.view_stats_clicked.connect(self.show_stats)
        self.main_menu.manage_players_clicked.connect(self.show_player_mgmt)
        self.main_menu.settings_clicked.connect(self.show_settings)
        self.main_menu.quit_clicked.connect(self.close)
        
        # scoring screen connections
        self.scoring_screen.game_complete.connect(self.show_game_over)
        self.scoring_screen.back_clicked.connect(self.show_main_menu)
        
        # stats screen connections
        self.stats_screen.back_clicked.connect(self.show_main_menu)
        
        # player management connections
        self.player_mgmt.back_clicked.connect(self.show_main_menu)
        
        # game over screen connections
        self.game_over.rematch_clicked.connect(self.start_game)
        self.game_over.main_menu_clicked.connect(self.show_main_menu)
        
        # settings screen connections
        self.settings_screen.back_clicked.connect(self.show_main_menu)
    
    def start_game(self):
        """start new bowling game"""
        # ask scoring screen to start new game
        if self.scoring_screen.start_new_game():
            # if successful, switch to scoring screen
            self.stacked_widget.setCurrentIndex(1)
    
    def show_main_menu(self):
        """switch back to main menu"""
        self.stacked_widget.setCurrentIndex(0)
    
    def show_player_mgmt(self):
        """show player management screen"""
        # refresh player list before showing
        self.player_mgmt.load_players()
        self.stacked_widget.setCurrentIndex(3)
    
    def show_stats(self):
        """show statistics screen"""
        # check if any players first
        players = self.db.get_all_players()
        
        if not players:
            # show message if no players exist
            QMessageBox.information(
                self,
                "No Players",
                "Please add players before viewing statistics."
            )
            return
        
        # switch to stats screen
        self.stacked_widget.setCurrentIndex(2)
    
    def show_settings(self):
        """show settings screen"""
        self.stacked_widget.setCurrentIndex(5)
    
    def show_game_over(self, game_data):
        """show game over screen with final results"""
        try:
            # tell game over screen to display results
            self.game_over.display_results(game_data)
            # switch to game over screen
            self.stacked_widget.setCurrentIndex(4)
        except Exception as e:
            # if something goes wrong, show an error message
            QMessageBox.critical(self, "Error", f"Failed to show game results: {e}")


def main():
    """main entry point for application"""
    # create pyqt5 application
    app = QApplication(sys.argv)
    
    # set application properties
    app.setApplicationName("Bowling Oracle")
    app.setApplicationVersion("1.0")
    
    # create and show main window
    window = BowlingOracleApp()
    window.show()
    
    # start event loop
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
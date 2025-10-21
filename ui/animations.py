"""
animation system for bowling oracle
handles wizard-themed animations for strikes, spares, and consecutive strikes
"""

import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QApplication, QDesktopWidget, QSizePolicy
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont


class AnimationWidget(QWidget):
    """widget that displays animations for bowling events"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # set up as overlay widget within parent
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(350, 250)
        self.setWindowFlags(Qt.Widget | Qt.FramelessWindowHint)
        
        # create main container
        self.container = QWidget()
        self.container.setFixedSize(350, 250)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # text label for animation message
        self.text_label = QLabel()
        self.text_label.setFont(QFont("Arial", 32, QFont.Bold))
        self.text_label.setAlignment(Qt.AlignCenter)
        self.text_label.setWordWrap(False)
        self.text_label.setMinimumHeight(100)
        self.text_label.setMaximumHeight(150)
        
        layout.addWidget(self.text_label)
        
        self.container.setLayout(layout)
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.container)
        self.setLayout(main_layout)
        
        # initially hidden
        self.hide()
        
        # set size policy to ignore layout positioning
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    
    def show_strike(self, consecutive_count: int = 1):
        """show animation for a strike"""
        self.text_label.clear()
        
        if not consecutive_count or consecutive_count < 1:
            consecutive_count = 1

        # set text based on consecutive count
        text = "STRIKE! 🎳🔮"
        if consecutive_count == 1:
            text = "STRIKE! 🎳🔮"
        elif consecutive_count == 2:
            text = "STRIKE! 🎳🔮\nDOUBLE! 🔮🔮"
        elif consecutive_count == 3:
            text = "STRIKE! 🎳🔮\nTURKEY! 🦃"
        elif consecutive_count == 4:
            text = "STRIKE! 🎳🔮\nHAMBONE! 🍖"
        elif consecutive_count == 11:
            text = f"STRIKE! 🎳🔮\n{consecutive_count}-BAGGER! 🔥"
        elif consecutive_count == 12:
            text = "STRIKE! 🎳🔮\nPERFECT GAME! 👑"
        elif consecutive_count >= 5:
            text = f"STRIKE! 🎳🔮\n{consecutive_count}-BAGGER! 🔥"
        
        self.text_label.setText(text)
        self.text_label.setVisible(True)
        self.text_label.setStyleSheet("""
            color: white;
            background: transparent;
            border: none;
            border-radius: 15px;
            font-weight: bold;
            font-size: 32px;
            padding: 15px;
            text-align: center;
        """)
        self.text_label.setMinimumHeight(100)
        self.text_label.setMaximumHeight(150)
        self.text_label.setWordWrap(False)
        self.text_label.raise_()
        
        # set background color based on consecutive count
        if consecutive_count == 1:
            color = "rgba(46, 204, 113, 255)"  # green for single strike
        elif consecutive_count == 2:
            color = "rgba(155, 89, 182, 255)"  # purple for double
        elif consecutive_count == 3:
            color = "rgba(230, 126, 34, 255)"  # orange for turkey
        elif consecutive_count == 4:
            color = "rgba(231, 76, 60, 255)"  # red for hambone
        elif consecutive_count == 11:
            color = "rgba(192, 57, 43, 255)"  # dark red for 11-bagger
        elif consecutive_count == 12:
            color = "rgba(241, 196, 15, 255)"  # gold for perfect game
        else:
            color = "rgba(192, 57, 43, 255)"  # dark red for other x-baggers
        
        self.container.setStyleSheet(f"""
            QWidget {{
                background-color: {color};
                border-radius: 20px;
                border: 4px solid black;
            }}
        """)
        
        self.container.setVisible(True)
        self.text_label.raise_()
        self.text_label.setVisible(True)
        
        # show animation with proper fade
        self._show_and_auto_hide(consecutive_count, text)
    
    def show_spare(self):
        """show animation for a spare"""
        self.text_label.clear()
        
        self.text_label.setText("SPARE! 🎯")
        self.text_label.setVisible(True)
        self.text_label.setStyleSheet("""
            color: white;
            background: transparent;
            border: none;
            border-radius: 15px;
            font-weight: bold;
            font-size: 32px;
            padding: 15px;
            text-align: center;
        """)
        self.text_label.setMinimumHeight(100)
        self.text_label.setMaximumHeight(150)
        self.text_label.setWordWrap(True)
        self.text_label.raise_()
        
        # purple theme for spares
        self.container.setStyleSheet("""
            QWidget {
                background-color: rgba(155, 89, 182, 255);
                border-radius: 20px;
                border: 4px solid black;
            }
        """)
        
        self._show_and_auto_hide(duration=2000)
    
    def show_gutter_ball(self):
        """show animation for a gutter ball"""
        self.text_label.clear()
        
        self.text_label.setText("GUTTER BALL!\n😅")
        self.text_label.setVisible(True)
        self.text_label.setStyleSheet("""
            color: white;
            background: transparent;
            border: none;
            border-radius: 15px;
            font-weight: bold;
            font-size: 28px;
            padding: 15px;
            text-align: center;
        """)
        self.text_label.setMinimumHeight(100)
        self.text_label.setMaximumHeight(150)
        self.text_label.setWordWrap(True)
        self.text_label.raise_()
        
        # grey theme for gutter balls
        self.container.setStyleSheet("""
            QWidget {
                background-color: rgba(149, 165, 166, 255);
                border-radius: 20px;
                border: 4px solid black;
            }
        """)
        
        self._show_and_auto_hide(duration=1500)
    
    def _show_and_auto_hide(self, consecutive_count: int = 1, text: str = "", duration: int = None):
        """show the animation and automatically hide it after a delay"""
        # set default duration based on animation type
        if duration is None:
            if consecutive_count == 12:  # perfect game
                duration = 4000
            else:
                duration = 3000
        
        # position the animation in the center of the parent
        if self.parent():
            parent_rect = self.parent().rect()
            x = (parent_rect.width() - self.width()) // 2
            y = (parent_rect.height() - self.height()) // 2
            self.move(x, y)
        
        # bring to front and show
        self.raise_()
        self.show()
        
        # hide after duration
        QTimer.singleShot(duration, self._fade_out_and_hide)
    
    def _fade_out_and_hide(self):
        """fade out the animation and hide it"""
        # hide the widget
        self.hide()
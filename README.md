# 🎳 Bowling Oracle 🔮

A wizard-themed bowling score tracker built with PyQt5 and SQLite for university coursework.

## ✨ Features

- **Live Scoring:** Real-time frame-by-frame score tracking with wizard animations
- **Multi-Player Support:** 2-6 players with turn management
- **Player Management:** Add, edit, and search players with statistics
- **Wizard Animations:** Strike, spare, and consecutive strike celebrations with crystal balls and magic
- **Sound Effects:** Pin knock sounds and background music
- **Purple Theme:** Consistent wizard-themed purple color scheme

## 🚀 Quick Start

1. **Install Python dependencies:**
   ```bash
   pip install PyQt5 pygame
   ```

2. **Run the application:**
   ```bash
   python main.py
   ```

3. **Start bowling:**
   - Click "Start New Game" 
   - Select 2-6 players
   - Click pin buttons (0-10) for each roll

## 🎮 How to Play

1. **Select Players:** Choose 2-6 players from your player list
2. **Enter Scores:** Click the pin buttons (0-10) for each roll
3. **View Results:** See the winner and final scores on the game over screen

## 🏗️ Project Structure

```
bowling_oracle/
├── main.py                 # Main application entry point
├── scoring.py              # Bowling game logic and scoring rules
├── database.py             # SQLite database handler
├── ui/                     # PyQt5 user interface screens
│   ├── main_menu.py        # Main menu with purple banner
│   ├── scoring_screen.py   # Live scoring interface
│   ├── player_mgmt.py      # Player management
│   ├── stats_screen.py     # Player statistics
│   ├── game_over.py        # Game over screen with purple banner
│   ├── animations.py       # Wizard-themed animations
│   └── sound_manager.py    # Audio management
├── assets/
│   └── audio/              # Sound effects and music
└── requirements.txt        # Python dependencies
```

## 🎨 Customization

### Adding Sound Effects
Place audio files in `assets/audio/`:
- **Strike Sounds:** `strike.wav`, `strike1.wav`, etc.
- **Spare Sounds:** `spare.wav`, `spare1.wav`, etc.
- **Pin Knock:** `pin.wav`, `pin1.wav`, etc.
- **Gutter Ball:** `gutterball.mp3`
- **Perfect Game:** `perfect.mp3`
- **Menu Music:** `menu.mp3`
- **Game Music:** `game.mp3`
- **Game Over Music:** `gameover.mp3`

## 🎯 Bowling Rules

- **Regular Frames (1-9):** Up to 2 rolls per frame
- **10th Frame:** Special rules for bonus rolls
  - Strike on first roll: Get 2 bonus rolls (3 total)
  - Spare on first two rolls: Get 1 bonus roll (3 total)
  - No strike/spare: Only 2 rolls total
- **Scoring:** Strikes and spares carry forward to subsequent frames

## 🧙 Wizard Theme

The application features a consistent wizard theme with:
- **Purple color scheme** throughout the interface
- **Crystal ball emojis** (🔮) for strikes and magic
- **Wizard emojis** (🧙) for decorative elements
- **Bowling ball emojis** (🎳) for bowling elements
- **Purple banners** on main menu and game over screens

## 🛠️ Technical Details

- **Framework:** PyQt5 for desktop GUI
- **Database:** SQLite for player and game data
- **Audio:** pygame for sound effects and music
- **Architecture:** MVC pattern with separate UI and logic layers

## 📝 Code Style

The codebase follows university-level standards:
- Clear, concise comments explaining functionality
- Simple, readable code structure
- Consistent naming conventions
- Modular design with separated concerns
- Error handling for robust operation

## 🎓 Educational Purpose

This project demonstrates:
- Object-oriented programming principles
- GUI development with PyQt5
- Database integration with SQLite
- Event-driven programming
- Animation and multimedia integration
- Software architecture patterns

## 📄 License

MIT License - Feel free to use for educational purposes.

---

*Built with 🧙 magic and 🔮 crystal balls for university coursework*
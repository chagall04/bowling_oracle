# 🎳 Bowling Oracle - Project Summary

## Project Overview

**Bowling Oracle** is a comprehensive, professional-grade multi-player bowling score tracking application built with Python and PyQt5. It features a modern graphical user interface, automatic score calculation following official bowling rules, player management, and advanced statistical analysis with visual charts.

---

## ✨ Key Features

### 🎯 Live Scoring System
- **Real-time scorecard** display mimicking professional bowling alleys
- **Automatic score calculation** for strikes, spares, and complex 10th frame rules
- **Multi-player support** (1-6 players per game)
- **Visual animations** for strikes and spares
- **Intuitive number pad** input system

### 👥 Player Management
- Add and remove players
- Search functionality
- Persistent player database
- Join date tracking

### 📊 Advanced Statistics
- **High score** tracking
- **Average score** calculation
- **Total games** played
- **Strike percentage** analytics
- **Performance charts** showing score trends over time (Matplotlib)
- **Complete game history** for each player

### 🏆 Game Features
- Winner announcement screen
- Rematch functionality
- Full game lifecycle management
- Automatic database persistence

---

## 🏗️ Technical Architecture

### Technology Stack
- **Language**: Python 3.8+
- **GUI Framework**: PyQt5
- **Database**: SQLite3
- **Charting**: Matplotlib
- **Image Processing**: Pillow

### Project Structure
```
bowling_oracle/
├── main.py                    # Application entry point
├── database.py                # SQLite database handler
├── scoring.py                 # Bowling game logic engine
├── requirements.txt           # Python dependencies
├── ui/                        # User interface components
│   ├── main_menu.py          # Main menu screen
│   ├── player_mgmt.py        # Player management screen
│   ├── scoring_screen.py     # Live scoring interface
│   ├── stats_screen.py       # Statistics and charts
│   ├── game_over.py          # Winner announcement
│   └── animations.py         # Strike/spare animations
├── assets/
│   └── animations/           # GIF animation files
├── README.md                 # Full documentation
├── QUICKSTART.md            # Quick start guide
├── GITHUB_SETUP.md          # GitHub deployment guide
└── LICENSE                   # MIT License
```

### Database Schema

#### Player Table
```sql
CREATE TABLE Player (
    player_id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_name TEXT NOT NULL UNIQUE,
    date_joined TEXT NOT NULL
)
```

#### Game Table
```sql
CREATE TABLE Game (
    game_id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER NOT NULL,
    final_score INTEGER NOT NULL,
    game_date TEXT NOT NULL,
    FOREIGN KEY (player_id) REFERENCES Player(player_id)
)
```

#### Frame Table
```sql
CREATE TABLE Frame (
    frame_id INTEGER PRIMARY KEY AUTOINCREMENT,
    game_id INTEGER NOT NULL,
    frame_number INTEGER NOT NULL,
    roll1_pins INTEGER,
    roll2_pins INTEGER,
    roll3_pins INTEGER,
    FOREIGN KEY (game_id) REFERENCES Game(game_id),
    CHECK (frame_number >= 1 AND frame_number <= 10)
)
```

---

## 🎨 User Interface Design

### Design Principles
- **Clean and modern**: Inspired by real bowling alley displays
- **Intuitive navigation**: Clear button hierarchy
- **Visual feedback**: Animations for special events
- **Responsive layout**: Works on various screen sizes
- **Professional color scheme**: Blue, green, and gray palette

### Screen Flow
```
Main Menu
├── Start New Game → Player Selection → Live Scoring → Game Over
├── Manage Players → Add/Remove/Search Players
└── View Stats → Player Selection → Statistics Dashboard
```

---

## 🔧 Core Components

### 1. Scoring Engine (`scoring.py`)

**BowlingGame Class**
- Manages individual player game state
- Implements official bowling scoring rules
- Handles 10th frame special cases
- Calculates cumulative scores

**GameManager Class**
- Coordinates multiple players
- Manages turn rotation
- Determines winner
- Synchronizes game state

### 2. Database Handler (`database.py`)

**Key Methods**
- Player CRUD operations
- Game creation and updating
- Frame recording
- Statistical queries
- Search functionality

### 3. UI Screens

**MainMenuScreen**
- Primary navigation hub
- Modern button design
- Signal-based navigation

**ScoringScreen**
- Digital scorecard display
- Real-time score updates
- Pin input system
- Player turn indicator

**StatsScreen**
- Player selection dropdown
- Statistical summary cards
- Matplotlib performance chart
- Game history table

**PlayerManagementScreen**
- Player list display
- Add/delete functionality
- Real-time search filtering

**GameOverScreen**
- Winner announcement
- Ranked score table
- Rematch option

---

## 📈 Scoring Logic

### Standard Frame (1-9)
```python
if strike:
    score = 10 + next_2_rolls
elif spare:
    score = 10 + next_1_roll
else:
    score = roll1 + roll2
```

### 10th Frame Special Rules
```python
if first_roll == 10:  # Strike
    get 2 bonus rolls
elif roll1 + roll2 == 10:  # Spare
    get 1 bonus roll
else:
    no bonus rolls
```

### Perfect Game
- All strikes (12 total)
- Score: 300 points

---

## 🚀 Installation & Usage

### Quick Install
```bash
# Clone repository
git clone https://github.com/yourusername/bowling_oracle.git
cd bowling_oracle

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Run application
python main.py
```

### Dependencies
```
PyQt5==5.15.10
matplotlib==3.8.2
numpy==1.26.3
Pillow==10.2.0
```

---

## 📊 Statistics & Analytics

### Calculated Metrics
- **High Score**: Maximum score achieved
- **Average Score**: Mean of all game scores
- **Total Games**: Count of completed games
- **Strike Percentage**: (Strikes / Total First Rolls) × 100

### Visualization
- **Line chart**: Score progression over time
- **Average line**: Reference benchmark
- **Interactive**: Matplotlib backend

---

## 🎯 Future Enhancement Ideas

### Planned Features
- [ ] Export game data to CSV/PDF
- [ ] Multi-language support
- [ ] Custom themes/skins
- [ ] Tournament mode (bracket system)
- [ ] Handicap system
- [ ] Lane assignment
- [ ] Team bowling support
- [ ] Cloud backup/sync
- [ ] Mobile companion app
- [ ] Advanced statistics (hooks, pocket hits, etc.)

### Technical Improvements
- [ ] Unit tests (pytest)
- [ ] Integration tests
- [ ] Performance optimization
- [ ] Database migration system
- [ ] Configuration file support
- [ ] Logging system
- [ ] Error reporting

---

## 🤝 Contributing

We welcome contributions! Here's how:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

### Contribution Areas
- Bug fixes
- New features
- Documentation improvements
- UI/UX enhancements
- Performance optimization
- Testing

---

## 📝 License

This project is licensed under the **MIT License** - see the `LICENSE` file for details.

---

## 👨‍💻 Development

### Code Style
- **PEP 8** compliant Python code
- **Type hints** for better code clarity
- **Docstrings** for all classes and methods
- **Comments** for complex logic

### Testing
Run the application in development mode:
```bash
python main.py
```

### Debugging
Enable debug mode by modifying `main.py`:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## 📚 Documentation

- **README.md**: Complete project documentation
- **QUICKSTART.md**: Fast setup guide for users
- **GITHUB_SETUP.md**: GitHub deployment instructions
- **PROJECT_SUMMARY.md**: This file - comprehensive overview

### Code Documentation
All modules include:
- Module-level docstrings
- Class docstrings
- Method docstrings with parameters and return types
- Inline comments for complex logic

---

## 🎓 Learning Resources

### Bowling Scoring
- [Official Bowling Scoring Rules](https://www.bowl.com/rules)
- Understanding strikes, spares, and the 10th frame

### Python & PyQt5
- [PyQt5 Documentation](https://www.riverbankcomputing.com/static/Docs/PyQt5/)
- [Python Official Docs](https://docs.python.org/3/)

### SQLite
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- Database design principles

---

## 🌟 Acknowledgments

- Built for the **Athlone Bowling League** community
- Inspired by professional bowling alley scoring systems
- Thanks to all contributors and testers

---

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing documentation
- Review the code (it's well-commented!)

---

## 🎉 Version History

### v1.0.0 (Initial Release)
- Complete bowling score tracking
- Multi-player support
- Player management system
- Statistical analysis
- Performance charts
- Strike/spare animations
- SQLite database persistence
- Modern PyQt5 interface

---

**Ready to track your perfect game? Let's bowl! 🎳**

*Built with ❤️ and Python*


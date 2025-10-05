# 🎳 Bowling Oracle 🧙

A mystical multi-player bowling score tracking application built with Python, PyQt5, and SQLite. Divine your perfect game with real-time scoring, player management, and performance analytics through an enchanted desktop interface.

## Features

### 🎯 Live Game Scoring

- Real-time frame-by-frame scoring for multiple players
- Automatic calculation of strikes, spares, and complex 10th frame scoring
- Visual scorecard display mimicking real bowling alley screens
- Animated celebrations for strikes and spares

### 👥 Player Management

- Add, edit, and remove players
- Track player join dates
- Search and filter player records

### 📊 Performance Analytics

- View individual player statistics (high scores, averages, totals)
- Historical game records
- Performance trends visualized with Matplotlib charts
- Strike percentage tracking

### 🏆 Game Features

- Multi-player game support
- Automatic winner declaration
- Rematch functionality
- Complete game history tracking

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repository:

```bash
git clone https://github.com/yourusername/bowling_oracle.git
cd bowling_oracle
```

2. Create a virtual environment (recommended):

```bash
python -m venv venv
```

3. Activate the virtual environment:

- Windows:
  ```bash
  venv\Scripts\activate
  ```
- macOS/Linux:
  ```bash
  source venv/bin/activate
  ```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the application:

```bash
python main.py
```

### Starting a New Game

1. From the main menu, click **Start New Game**
2. Select players from the registered player list
3. Use the number pad to enter pins knocked down for each roll
4. Watch scores update automatically!

### Viewing Statistics

1. Click **View Player Stats** from the main menu
2. Select a player from the dropdown
3. Review their performance metrics and historical data
4. Analyze trends with the interactive performance chart

### Managing Players

1. Click **Manage Players** from the main menu
2. Add new players or remove existing ones
3. Search for specific players

## Database Schema

The application uses SQLite with three relational tables:

### Player Table

- `player_id`: INTEGER (Primary Key)
- `player_name`: TEXT
- `date_joined`: TEXT

### Game Table

- `game_id`: INTEGER (Primary Key)
- `player_id`: INTEGER (Foreign Key)
- `final_score`: INTEGER
- `game_date`: TEXT

### Frame Table

- `frame_id`: INTEGER (Primary Key)
- `game_id`: INTEGER (Foreign Key)
- `frame_number`: INTEGER (1-10)
- `roll1_pins`: INTEGER
- `roll2_pins`: INTEGER
- `roll3_pins`: INTEGER (10th frame only)

## Technologies Used

- **Python 3.8+**: Core programming language
- **PyQt5**: Modern GUI framework
- **SQLite**: Lightweight database engine
- **Matplotlib**: Data visualization and charting
- **Pillow**: Image handling for animations

## Project Structure

```
bowling_oracle/
├── main.py                 # Application entry point
├── database.py             # Database handler
├── scoring.py              # Bowling scoring logic
├── ui/
│   ├── main_menu.py       # Main menu screen
│   ├── scoring_screen.py  # Live scoring interface
│   ├── stats_screen.py    # Statistics and charts
│   ├── player_mgmt.py     # Player management
│   ├── game_over.py       # Winner announcement
│   ├── animations.py      # Strike/spare animations
│   └── sound_manager.py   # Audio playback
├── assets/
│   └── animations/        # Strike/spare GIFs & sounds
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🎬 Adding GIFs and Sound Effects

Make your Bowling Oracle even more magical with custom animations and sounds!

### 🎞️ Adding GIF Animations (Optional)

1. **Download bowling GIFs** from free sources:
   - [GIPHY](https://giphy.com/search/bowling-strike)
   - [Tenor](https://tenor.com/search/bowling-gifs)
   - [Pixabay](https://pixabay.com/gifs/search/bowling/)

2. **Save them** in `assets/animations/`:
   - `strike.gif` - Plays when you get a strike
   - `spare.gif` - Plays when you get a spare

3. **Recommended specs**:
   - Size: 200x200 to 400x400 pixels
   - Duration: 1-2 seconds
   - Fun, energetic bowling theme!

**Ideas:**
- Strike: Pins exploding, "STRIKE!" text, wizard casting spell 🧙‍♂️, fireworks
- Spare: Pins falling, "SPARE!" text, crystal ball glowing 🔮, star effects

### 🔊 Adding Sound Effects (Optional)

1. **Download bowling sounds** from free sources:
   - [Freesound.org](https://freesound.org/search/?q=bowling+strike)
   - [Zapsplat](https://www.zapsplat.com/sound-effect-category/bowling/)
   - [Pixabay Sounds](https://pixabay.com/sound-effects/search/bowling/)

2. **Save them** in `assets/animations/`:
   - `strike.wav` or `strike.mp3` - Plays on strike
   - `spare.wav` or `spare.mp3` - Plays on spare

3. **Formats supported**: `.wav`, `.mp3`, `.ogg`

**Ideas:**
- Strike: Pins crashing, crowd cheering, dramatic music sting
- Spare: Lighter pin sound, satisfying "ding", mystical chime

### ✨ How It Works

Once files are in place:

1. **Strike/Spare happens** → App checks for media files
2. **GIF found** → Plays with smooth fade-in/scale animation
3. **Sound found** → Plays simultaneously  
4. **No files?** → Falls back to emoji (💥 for strike, 🎯 for spare)

The app uses **PyQt5's QPropertyAnimation** for smooth fade-in/out, scale effects, and easing curves - no CSS needed!

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Acknowledgments

✨ Powered by Ancient Bowling Wisdom ✨  
Built with 🧙 magic and Python

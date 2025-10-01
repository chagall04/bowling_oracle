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
│   └── game_over.py       # Winner announcement
├── assets/
│   └── animations/        # Strike/spare GIFs
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Acknowledgments

✨ Powered by Ancient Bowling Wisdom ✨  
Built with 🧙 magic and Python

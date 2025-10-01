# Quick Start Guide 🎳

Get your Bowling Score Tracker up and running in minutes!

## Installation

### Step 1: Install Python
Make sure you have Python 3.8 or higher installed:
```bash
python --version
```

### Step 2: Create Virtual Environment (Recommended)
```bash
python -m venv venv
```

### Step 3: Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

## Running the Application

```bash
python main.py
```

The application window should open immediately!

## First Steps

### 1. Add Players
1. Click **"👥 Manage Players"** from the main menu
2. Click **"➕ Add Player"**
3. Enter player names (e.g., "Charlie", "Alice", "Bob")
4. Click **"⬅️ Back to Main Menu"**

### 2. Start Your First Game
1. Click **"🎯 Start New Game"**
2. Select 1-6 players from the list (click to select multiple)
3. Click **"Start Game"**

### 3. Score the Game
- Use the **number pad (0-10)** to enter pins knocked down
- The app automatically:
  - Calculates strikes and spares
  - Handles the complex 10th frame rules
  - Updates cumulative scores
  - Switches between players

### 4. View Statistics
After completing some games:
1. Go to **"📊 View Player Stats"**
2. Select a player from the dropdown
3. View their:
   - High score
   - Average score
   - Total games played
   - Strike percentage
   - Performance chart over time

## Bowling Scoring Basics

### Strike (X)
- Knock down all 10 pins on the **first roll**
- Score: 10 + next 2 rolls

### Spare (/)
- Knock down all 10 pins using **both rolls**
- Score: 10 + next 1 roll

### 10th Frame Special Rules
- If you get a **strike**, you get **2 bonus rolls**
- If you get a **spare**, you get **1 bonus roll**
- Maximum score per frame: 30 (three strikes)
- Perfect game: 300 points

## Keyboard Shortcuts

While the application is focused:
- `0-9` keys work (if implemented)
- `Esc` to cancel dialogs

## Troubleshooting

### Application won't start
```bash
# Make sure all dependencies are installed
pip install --upgrade -r requirements.txt
```

### Database errors
Delete the database file and restart (this will erase all data):
```bash
# Windows
del bowling_tracker.db

# macOS/Linux  
rm bowling_tracker.db
```

### Missing animations
Animations are optional! The app uses emoji fallbacks if GIF files aren't present. To add GIFs:
1. Download bowling GIFs
2. Save as `assets/animations/strike.gif` and `assets/animations/spare.gif`

### Qt Platform Plugin Error
On some systems, you may need to install additional Qt dependencies:

**Linux:**
```bash
sudo apt-get install python3-pyqt5
```

**macOS:**
```bash
brew install pyqt5
```

## Tips & Tricks

### 💡 Scoring Strategies
- Focus on **consistency** over power
- **Spares are more valuable** than you think (they're easier than strikes!)
- The **10th frame** can make or break your score

### 📊 Using Statistics
- Track your **progress over time** with the performance chart
- Set goals based on your **average score**
- Watch your **strike percentage** improve with practice

### 🎮 Game Management
- Use **Rematch** to quickly start a new game with the same players
- **Search** in Player Management to find specific players quickly
- The database **automatically saves** all game data

## Sample Workflow

Here's a typical session:

```
1. Launch app
2. Add players: "Alice", "Bob", "Charlie"
3. Start new game, select all 3 players
4. Play the game (entering scores)
   - Alice: Frame 1 → 7, 2 (9 pins)
   - Bob: Frame 1 → 10 (Strike! 💥)
   - Charlie: Frame 1 → 8, 2 (Spare! ✨)
   - Continue through all 10 frames...
5. Game over! Bob wins with 215
6. Click "Rematch" for another round
7. After playing, view stats to see improvement
```

## Data Location

All your data is stored in:
- **Database**: `bowling_tracker.db` (in the project folder)
- **Backup tip**: Copy this file to backup your data

## Next Steps

- **Customize**: Edit the UI colors in the screen files
- **Add GIFs**: Enhance animations with custom GIFs
- **Contribute**: Fork on GitHub and add features!
- **Share**: Invite friends for a bowling tournament!

## Getting Help

- Check `README.md` for full documentation
- Review `GITHUB_SETUP.md` for deployment
- Examine the code - it's well-commented!

---

**Enjoy tracking your perfect game! 🎳✨**


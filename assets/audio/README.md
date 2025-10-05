# Audio Assets

This directory contains sound effects and music for the Bowling Oracle.

## Sound Files (Optional)

All files are optional - the app works fine without them!

### Strike Sounds
- `strike.wav` / `strike.mp3` / `strike.ogg` - Base strike sound
- `strike1.wav`, `strike2.wav`, etc. - Additional variations (up to 9)
- **Plays**: When you get a strike
- **Behavior**: Randomly picks one if multiple files exist

### Spare Sounds  
- `spare.wav` / `spare.mp3` / `spare.ogg` - Base spare sound
- `spare1.wav`, `spare2.wav`, etc. - Additional variations (up to 9)
- **Plays**: When you get a spare
- **Behavior**: Randomly picks one if multiple files exist

### Pin Knock Sound
- `pin.wav` / `pin.mp3` / `pin.ogg` - Single file
- **Plays**: Every time you click a pin button (0-10)
- **Purpose**: Tactile audio feedback

### Leaderboard Music
- `leaderboard.wav` / `leaderboard.mp3` / `leaderboard.ogg` - Single file
- **Plays**: On the game over/winner screen
- **Behavior**: Loops continuously until you exit the screen
- **Recommended**: 15-30 second upbeat victory music

## Format Support

All three formats are supported:
- `.wav` - Uncompressed, high quality, larger files
- `.mp3` - Compressed, good quality, smaller files (recommended)
- `.ogg` - Open source format, good quality

## Where to Find Free Sounds

- [Freesound.org](https://freesound.org/) - Community sound library
- [Zapsplat](https://www.zapsplat.com/) - Free sound effects
- [Pixabay Sounds](https://pixabay.com/sound-effects/) - Royalty-free audio

## Example Structure

```
assets/audio/
├── strike.mp3
├── strike1.mp3
├── strike2.mp3
├── spare.mp3
├── spare1.mp3
├── pin.wav
└── leaderboard.mp3
```

**Powered by pygame mixer** 🔊

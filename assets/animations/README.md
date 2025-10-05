# Animation Assets

This directory contains GIF animations for strikes and spares.

## GIF Files (Optional)

All files are optional - the app uses emoji fallbacks if no GIFs are present!

### Strike Animations
- `strike.gif` - Base strike GIF
- `strike1.gif`, `strike2.gif`, etc. - Additional variations (up to 9)
- **Plays**: When you get a strike
- **Behavior**: Randomly picks one if multiple files exist

### Spare Animations
- `spare.gif` - Base spare GIF  
- `spare1.gif`, `spare2.gif`, etc. - Additional variations (up to 9)
- **Plays**: When you get a spare
- **Behavior**: Randomly picks one if multiple files exist

## Specifications

- **Format**: Animated GIF only
- **Recommended size**: 200x200 to 400x400 pixels
- **Duration**: 1-2 seconds
- **Style**: Fun, energetic, mystical bowling theme

## Fallback Behavior

If no GIF files are present:
- Strike: 💥 emoji
- Spare: 🎯 emoji

## Where to Find GIFs

- [GIPHY](https://giphy.com/search/bowling-strike) - Huge GIF library
- [Tenor](https://tenor.com/search/bowling-gifs) - GIF search engine
- [Pixabay](https://pixabay.com/gifs/search/bowling/) - Free stock GIFs

## Example Structure

```
assets/animations/
├── strike.gif
├── strike1.gif
├── strike2.gif
├── spare.gif
└── spare1.gif
```

**Note**: Sound files are now in `assets/audio/` - check that folder for audio setup!


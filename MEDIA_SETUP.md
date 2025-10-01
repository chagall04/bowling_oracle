# 🎬 Adding GIFs and Sound Effects

Make your Bowling Oracle even more magical with animations and sounds!

## 📦 Install Sound Support

First, install pygame for sound effects:

```bash
pip install pygame
```

Or reinstall all requirements:
```bash
pip install -r requirements.txt
```

## 🎞️ Adding GIF Animations

1. **Download GIFs** from free sources:
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

## 🔊 Adding Sound Effects

1. **Download sounds** from free sources:
   - [Freesound.org](https://freesound.org/search/?q=bowling+strike)
   - [Zapsplat](https://www.zapsplat.com/sound-effect-category/bowling/)
   - [Pixabay Sounds](https://pixabay.com/sound-effects/search/bowling/)

2. **Save them** in `assets/animations/`:
   - `strike.wav` or `strike.mp3` - Plays on strike
   - `spare.wav` or `spare.mp3` - Plays on spare

3. **Formats supported**: .wav, .mp3, .ogg

## 🎨 Example Files

### Strike GIF Ideas:
- Bowling pins exploding
- "STRIKE!" text animation
- Wizard casting a spell 🧙‍♂️
- Fireworks/celebration

### Spare GIF Ideas:
- Pins falling smoothly
- "SPARE!" text animation
- Crystal ball glowing 🔮
- Star effects

### Sound Ideas:
- **Strike**: Pins crashing, crowd cheering, dramatic music sting
- **Spare**: Lighter pin sound, satisfying "ding", mystical chime

## ✨ How It Works

Once files are in place:

1. **Strike/Spare happens** → App checks for media files
2. **GIF found** → Plays with smooth fade-in/scale animation
3. **Sound found** → Plays simultaneously
4. **No files?** → Falls back to emoji (💥 for strike, 🎯 for spare)

## 🎭 Animations in Action

The app uses **PyQt5's QPropertyAnimation** for:
- ✨ Fade in/out effects
- 📈 Scale animations (pop effect)
- 🌊 Smooth easing curves

No CSS transitions needed - these are real Qt animations!

## 🧪 Testing

After adding files:

1. Start the app: `python main.py`
2. Start a bowling game
3. Score a strike or spare
4. Watch the magic happen! 🎉

## 📝 Notes

- Files are optional - app works fine without them
- Sound can fail silently if pygame isn't installed
- GIF files can be any size (will display at 200x200)
- Multiple sound formats supported for compatibility

---

**Happy animating! 🎳🧙✨**


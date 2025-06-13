# 🎰 Three Card Roulette

A feature-rich casino card game combining traditional roulette mechanics with real-time stock trading and an achievement system. Play in 4 languages with auto-save functionality!

## 🎮 Game Features

### 🃏 Card Game Modes
- **Color Betting**: Bet on Red or Black cards (2:1 payout)
- **Exact Suit Betting**: Bet on specific suits (3:1 payout)  
- **Multiple Bets**: Place several bets simultaneously
- **Joker Mechanic**: Jokers trigger re-draws (no win/loss)

### 📈 Stock Trading System
- **Real-time Market**: 5 companies with dynamic pricing
- **Buy & Sell Shares**: Full control over your portfolio
- **Realistic Volatility**: Each stock has different risk levels
- **Portfolio Tracking**: Monitor your investments

### 🏆 Achievement System
- **All Gamemode Achiever**: Win in every game mode
- **Triple Rare**: Get 3 Jokers in a row
- **Millionaire**: Reach $1000+ balance
- **Stock Master**: Own 100+ shares

### 🌍 Multi-Language Support
- English
- Español (Spanish)
- Français (French) 
- Deutsch (German)

## 📦 Installation

### Quick Install (Recommended)
```bash
pip install three-card-roulette
```

### From Source
```bash
git clone https://github.com/matthieu/three-card-roulette.git
cd three-card-roulette
pip install -r requirements.txt
python setup.py install
```

## 🚀 Running the Game

### Command Line
```bash
# Full name
three-card-roulette

# Short alias
tcr

# Or directly with Python
python game.py
```

## 🎯 How to Play

1. **Choose Language**: Select from 4 available languages
2. **Main Menu**: Navigate between card games, stock trading, and inventory
3. **Card Games**: Place bets and try your luck
4. **Stock Trading**: Buy/sell shares to grow your portfolio
5. **Achievements**: Unlock trophies by completing challenges

## 📊 Game Statistics

The game tracks comprehensive statistics:
- Total bets placed and win rate
- Money won/lost and net profit
- Achievement progress
- Session statistics

## 💾 Save System

- **Auto-save**: Game saves after every bet and trade
- **Persistent Data**: Your progress is preserved between sessions
- **Cross-Platform**: Save files work on Windows, Mac, and Linux

## 🔄 Auto-Updates

The game includes an automatic update system:
- Checks for new versions on startup
- One-click updates from within the game
- Automatic backup of your save data

## 🛠️ Development

### Project Structure
```
three-card-roulette/
├── game.py          # Main game controller
├── languages.py     # Multi-language translations
├── stock_market.py  # Stock trading system
├── achievements.py  # Trophy and inventory system
├── card_game.py     # Card game mechanics
├── updater.py       # Auto-update system
├── setup.py         # Package installation
└── requirements.txt # Dependencies
```

### Building from Source
```bash
# Install development dependencies
pip install -r requirements.txt

# Build package
python setup.py sdist bdist_wheel

# Install locally
pip install -e .
```

## 📋 Requirements

- Python 3.7 or higher
- Internet connection (for auto-updates and first-time setup)
- Terminal/Command Prompt

## 🎨 Credits

- **Game Design**: Matthieu
- **Programming**: Powered by Claude AI
- **Multi-language Support**: Community translations

## 📄 License

MIT License - Feel free to modify and distribute!

## 🐛 Bug Reports

Found a bug? Please report it on our [GitHub Issues](https://github.com/matthieu/three-card-roulette/issues) page.

## 🎯 Roadmap

- [ ] Online multiplayer mode
- [ ] More stock companies
- [ ] Additional achievement types
- [ ] Custom card themes
- [ ] Mobile app version

---

**Enjoy the game!** 🎮✨
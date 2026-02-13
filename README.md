# Dark Floor

A roguelike terminal game written in Python using the curses library.

## Features

- Terminal-based roguelike gameplay
- Procedurally generated dungeons
- Turn-based mechanics
- Fog of war system
- Sound/audio cues
- Sanity system for the player

## Requirements

- Python 3.7+
- curses library (included in Python on Unix/Linux/Mac; Windows users can use `windows-curses`)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/baodevbtw/Dark-Floor.git
cd Dark-Floor
```

2. (Optional) Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Game

```bash
python main.py
```

## Project Structure

```
Dark-Floor/
├── main.py           # Entry point
├── src/
│   └── darkfloor.py  # Game logic and engine
├── README.md         # This file
└── requirements.txt  # Python dependencies
```

## How to play

See [docs/HOW_TO_PLAY.md](docs/HOW_TO_PLAY.md)

## Development

This project is in early development. See [CONTRIBUTING.md](CONTRIBUTING.md) for how to help!

## License

MIT License - See [LICENSE](LICENSE) file for details

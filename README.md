# dqc - Discord Quest Completer

Discord Quest Completer for Windows, written in Python.

## Installation

```bash
git clone https://github.com/nextgencat/dqc
cd dqc

python -m venv venv
venv\Scripts\activate

pip install -r dependencies.txt
```

## Launch

```bash
python src\main.py
```

## Usage

1. Enter a game name and press Enter.
2. Click the button with the name of the target game.
3. To stop, close the created window.

## How it works

1. It fetches game names and lists of their .exe names from https://discord.com/api/v10/applications/detectable using `requests`.
2. It creates a `dummy.exe` in the `output` folder using PyInstaller.
3. It copies `dummy.exe` under the target game's .exe name and launches it.

## Note

This project was created only to learn something new.

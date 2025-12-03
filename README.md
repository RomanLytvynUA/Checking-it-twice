<div align="center">
  <img width="525" height="200" alt="title" src="https://github.com/user-attachments/assets/d0f1c3b4-6718-4622-8563-d5d06a413a30" />

  <p><b>An Arcade Management Sim developed in Python & Pygame.</b></p>

  <p>
    <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" />
    <img src="https://img.shields.io/badge/Pygame-bedc4e?style=for-the-badge&logo=pygame&logoColor=white" />
    <img src="https://img.shields.io/badge/Status-Prototype-orange?style=for-the-badge" />
  </p>
</div>

<br />

## 🎅 About
**Checking It Twice** is a fast-paced arcade game where you play as Santa on Christmas Eve. It combines flying mechanics with rapid decision-making. You must pilot the sleigh while reviewing dossiers to decide—**Present or Coal?**—before the chimney passes by.

## ⚙️ Technical Features
Built from scratch without external game engines. Key architectural highlights include:

* **State Machine Architecture:** Clean object-oriented management of game states (Menu, Game, Pause).
* **Virtual Resolution:** Renders to a fixed logical canvas and scales smoothly to any window size using `pygame.transform`.
* **Responsive Asset Loader:** Custom resource manager that adapts UI and sprite sizes based on screen percentage, ensuring cross-resolution consistency.

## 📂 Structure
```text
Checking-it-twice/
├── assets/                 # Graphics, Fonts, Audio
├── src/
│   ├── settings.py         # Global Constants & Config
│   ├── loader.py           # Responsive Asset Manager
│   ├── states.py           # State Machine Logic
│   ├── sprites.py          # Entity Classes
│   └── ui.py               # Custom UI Components
└── main.py                 # Engine Entry Point
````

## 🚀 How to Run

**1. Clone the repository**

```bash
git clone https://github.com/RomanLytvynUA/Checking-it-twice.git
cd checking-it-twice
```

**2. Set up Virtual Environment (Recommended)**

```bash
# macOS / Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

**3. Install Dependencies**

```bash
pip install pygame
```

**4. Start the Engine**

```bash
python3 main.py
```

## 🗺️ Roadmap

  - [x] Core Engine & Game Loop
  - [x] Dynamic Resolution Scaling
  - [x] Main Menu
  - [ ] Settings tab
  - [ ] Parallax Background Scrolling
  - [ ] Santa Physics & Movement
  - [ ] Randomized houses generation
  - [ ] Dossier system
  - [ ] Random events
  - [ ] Ambient events
  - [ ] Dossier System

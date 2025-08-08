# Space Invaders (Python Clone)

The classic Space Invaders game, made with Python and Pygame!

## Controls

- Left Arrow / A: Move player left
- Right Arrow / D: Move player right
- Spacebar: Shoot bullets
- Q: Exit game

## How it works

- The player moves horizontally at the bottom of the screen using the arrow keys.
- Enemies appear in rows and move left and right, dropping down each time they hit a screen edge.
- Shoot enemies to destroy them, they respawn at random positions.
- The game loop handles input, updates sprites, checks collisions, and renders everything.
- Simple and extensible code for easy customization:
    - Replace player.png and enemy.png with your own transparent PNG sprites.
    - Speeds, bullet behavior, enemy patterns, visuals can be modified in `invaders.py`.

## Requirements

- `python 3.x`
- `pygame` library: Can be installed using `pip install pygame`.

## Setup

Download the repository as-is, with the structure:

```
C:.
│   .gitattributes
│   invaders.py
│   README.md
└───assets
        enemy.png
        player.png
```

and run the game using the following command in the terminal:

```
python invaders.py
```

## Credits

Created by Soham Raut. Inspired by the original Space Invaders game. Feel free to use and modify this code for personal or educational purposes.
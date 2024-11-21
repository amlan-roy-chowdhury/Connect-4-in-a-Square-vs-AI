Connect 4 Game with AI

Overview
This program is a Connect 4 game with a user-friendly graphical interface built using Python's tkinter library. It allows you to play against an AI opponent with adjustable difficulty levels. The game is designed for two players: the human player and the AI agent.

The AI uses a minimax algorithm with alpha-beta pruning to make intelligent moves based on the game state and the selected difficulty level.

Features
Graphical Interface: Easy-to-use GUI for interacting with the game.
Adjustable AI Difficulty: Choose the AI's intelligence level (from 1 to 5).
Customizable Game Board: Select your preferred board color from various options.
Player Name Input: Personalize the game by entering your name.
Winner Announcement: Displays the winner and the duration of the game after it ends.
Move Counter: Tracks and displays the number of moves made during the game.
Agent and Player Turn Management: Automatically switches turns between the player and the AI.
How to Play
Run the program using Python 3.
Enter your name and select your preferred board color.
Choose who will start the game (Human or Agent).
Adjust the AI Intelligence Level (1 for easy, 5 for hard).
Click the Start Game button to begin.
Interact with the game by clicking on the columns where you want to drop your disc.
The AI will take its turn automatically. The game ends when there is a winner or a draw.

Requirements
Python 3.x
Libraries: math, random, time, tkinter, numpy

To install any missing libraries, run:

pip install numpy

Controls
Mouse Click: Drop a disc into a column by clicking on it.
ComboBox: Change the board color before starting the game.
Radio Buttons: Select the starting player (Human or AI).
Slider: Adjust the AI difficulty level.
Files and Directories
main.py: Main script that runs the Connect 4 game.
No additional files are required for this standalone application.

Notes
The AI difficulty level impacts the number of moves the AI looks ahead in its decision-making process. A higher difficulty results in a slower but more strategic AI.
The game board resets when the Start Game button is clicked.

License
This program is provided as-is under an open-source license. Feel free to modify and redistribute it for educational or personal use.

Developer
If you encounter any issues or have suggestions for improvements, please feel free to reach out.

Enjoy the game! 🎮

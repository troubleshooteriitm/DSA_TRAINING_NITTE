# Board Race Game using OOP in Python

## Problem Statement

You have been hired to develop a simple **Board Race Game** using **Object-Oriented Programming (OOP)** concepts in Python.

The game consists of a board with numbered cells. Multiple players take turns rolling a dice and moving forward. The first player to reach the final cell wins the game.

There is one special rule:

* If a player lands on a cell already occupied by another player, the player who was already on that cell is sent back to the starting position.

Your task is to design and implement the game using classes and objects.

---

## Requirements

### 1. Create a Class: `Player`

The class should store:

* Player Name
* Current Position (initially 0)
* Number of Dice Rolls

Add methods:

* `move(steps)` → Moves the player forward.
* `reset_position()` → Sends the player back to the start.
* `display_position()` → Displays the current position.

---

### 2. Create a Class: `Dice`

The class should simulate a dice.

Add method:

* `roll()` → Returns a random number between 1 and 6.

---

### 3. Create a Class: `Board`

The class should store:

* Board Size (customizable)

Example:

```python
board = Board(50)
```

This creates a board with positions from 0 to 50.

Add methods:

* `is_valid_position(position)` → Checks whether a move is within board limits.

---

### 4. Create a Class: `Game`

The game should manage:

* Board
* Dice
* Multiple Players

Add methods:

* `play_turn(player)`
* `check_collision(player)`
* `check_winner(player)`
* `start_game()`

Responsibilities:

* Roll the dice.
* Move players.
* Prevent movement beyond board size.
* Handle collisions.
* Track dice rolls.
* Declare the winner.

---

## Game Rules

1. Any number of players can participate.
2. All players start at position **0**.
3. Players take turns rolling the dice.
4. If a move goes beyond the board size, the move is ignored.
5. If a player lands on a position occupied by another player:

   * The player who was already on that position is sent back to position **0**.
6. The first player to reach the final board position wins.
7. The game ends immediately when a winner is found.

---

## Demonstration

Create a complete game simulation by following these steps:

1. Create a board of size 30.
2. Create a dice object.
3. Create at least 3 players.
4. Create a game object.
5. Start the game.
6. Continue turns until one player wins.
7. Display player movements and collisions.

---

## Sample Output

```text
===== Board Race Game =====

Alice rolled 4
Alice moved to 4

Bob rolled 2
Bob moved to 2

Charlie rolled 5
Charlie moved to 5

Alice rolled 3
Alice moved to 7

Bob rolled 5
Bob moved to 7

Collision!
Alice was already at position 7
Alice goes back to Start

Alice position: 0
Bob position: 7

...

Charlie rolled 4
Charlie moved to 30

Charlie wins the game!
```

---

## Bonus Challenge

* Display player rankings after every round.
* Allow different dice sizes (6-sided, 8-sided, 12-sided).
* Maintain a history of all moves.
* Save and load game progress.
* Display the total number of dice rolls made by each player at the end.

This exercise will help you practice **Classes, Objects, Composition, Game Logic, Collections, and Object Interaction** in Python.

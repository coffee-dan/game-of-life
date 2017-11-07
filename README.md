# Game Of Life
Conway's game of life, a simple implementation.

## Fundamental Rules
The game is designed around the following simple rules:
1. Any live cell with fewer than two live neighbors dies, as if caused by underpopulation.
2. Any live cell with more than three live neighbors dies, as if by overcrowding.
3. Any live cell with two or three live neighbors lives on to the next generation.
4. Any dead cell with exactly three live neighbors becomes a live cell.

> The operation of the game starts with an initial configuration on a two dimensional grid. This infinite square grid consists of cells with two possible states, alive or dead. Each cell has eight neighbors, namely the eight cells that touch it. The game operates in iterations, called ticks. Each tick applies the four rules of the game to every cell on the board simultaneously.
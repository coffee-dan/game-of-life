# Game Of Life
Conway's game of life, a simple implementation.

## Fundamental Rules
The game is designed around the following simple rules:
1. Any live cell with fewer than two live neighbors dies, as if caused by underpopulation.
2. Any live cell with more than three live neighbors dies, as if by overcrowding.
3. Any live cell with two or three live neighbors lives on to the next generation.
4. Any dead cell with exactly three live neighbors becomes a live cell.

> The operation of the game starts with an initial configuration on a two dimensional grid. This infinite square grid consists of cells with two possible states, alive or dead. Each cell has eight neighbors, namely the eight cells that touch it. The game operates in iterations, called ticks. Each tick applies the four rules of the game to every cell on the board simultaneously.

## This Repository
So far there is:
* an empty .cpp file where a C++ implementation should be
* a Python x PyGame graphical implemtation with a finite bounded grid, random initial configuration and 9 presets
  * run with ```py conway_v1.3.7x.py <preset number>``` on Windows or ```python3 conway_v1.3.7x.py <preset number>``` on Linux
  * example ```py conway_v1.3.7x.py <preset number>```
  * all other python versions in the repository are graphical
    * Not all versions run the same way, most have comments in the code explaining things
  * the number of presets available is expanding, these are kept in grid_presets.txt
* a Python command line implementation with a finite grid, random initial configuration and 1 preset
  * v1_cli and v1.1d_presets are the only Command line interface versions, both located in depreciated/
  * run with ```python3 conway_v1.1d_presets.py``` on Windows or ```python3 conway_v1.1d_presets.py```

# Game Of Life
Conway's game of life, a simple implementation.

## Fundamental Rules
The game is designed around the following simple rules:
1. Any live cell with fewer than two live neighbors dies, as if caused by underpopulation.
2. Any live cell with more than three live neighbors dies, as if by overcrowding.
3. Any live cell with two or three live neighbors lives on to the next generation.
4. Any dead cell with exactly three live neighbors becomes a live cell.

> The operation of the game starts with an initial configuration on a two dimensional grid. This infinite square grid consists of cells with two possible states, alive or dead. Each cell has eight neighbors, namely the eight cells that touch it. The game operates in iterations, called ticks. Each tick applies the four rules of the game to every cell on the board simultaneously.

# &lt;project name&gt; is an [OPEN Open Source Project](http://openopensource.org/)

-----------------------------------------

## What?

Individuals making significant and valuable contributions are given
commit-access to the project to contribute as they see fit. This project
is more like an open wiki than a standard guarded open source project.

## Rules

There are a few basic ground-rules for contributors:

1. **No `--force` pushes** or modifying the Git history in any way.
1. **Non-master branches** ought to be used for ongoing work.
1. **External API changes and significant modifications** ought to be subject to an **internal pull-request** to solicit feedback from other contributors.
1. Internal pull-requests to solicit feedback are *encouraged* for any other non-trivial contribution but left to the discretion of the contributor.
1. Contributors should attempt to adhere to the prevailing code-style.

## Releases

Declaring formal releases remains the prerogative of the project maintainer.

## Changes to this arrangement

This is an experiment and feedback is welcome! This document may also be
subject to pull-requests or changes by contributors where you believe
you have something valuable to add or change.

Get a copy of this manifesto as [markdown](https://raw.githubusercontent.com/openopensource/openopensource.github.io/master/Readme.md) and use it in your own projects.
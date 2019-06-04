# Ramirez, Daniel G.
# 2019-05-16
#--------------------------------------------------
import sys
import random
import copy
import pygame
#--------------------------------------------------
def tick( grid, n ) :
  updatedGrid = copy.deepcopy( grid )

  for y in range( 1, n+1 ) :
    for x in range( 1, n+1 ) :
      neighbors = 0

      if grid[ x-1 ][ y-1 ] == 1 :
        neighbors += 1
      if grid[  x  ][ y-1 ] == 1 : 
        neighbors += 1
      if grid[ x+1 ][ y-1 ] == 1 : 
        neighbors += 1
      if grid[ x-1 ][  y  ] == 1 : 
        neighbors += 1
      if grid[ x+1 ][  y  ] == 1 : 
        neighbors += 1
      if grid[ x-1 ][ y+1 ] == 1 : 
        neighbors += 1
      if grid[  x  ][ y+1 ] == 1 : 
        neighbors += 1
      if grid[ x+1 ][ y+1 ] == 1 : 
        neighbors += 1

      # Live cell
      if grid[x][y] == 1 :      	
        if neighbors < 2 :
          # Death by exposure ( <2 neighbors )
      	  updatedGrid[x][y] = 0
        elif neighbors > 3 :
          # Death by overcrowding ( >3 neighbors )
          updatedGrid[x][y] = 0
      # Dead cell
      elif grid[x][y] == 0 :
      	if neighbors == 3 :
      	  # New life
      	  updatedGrid[x][y] = 1

  return updatedGrid

#--------------------------------------------------
def printGrid( grid, generation ) :
  print( 'generation #' + str( generation ) )
  for y in range( 1, len( grid[0] )-1 ) :
    for x in range( 1, len( grid[0] )-1 ) :
      if grid[ x ][ y ] == 0 :
        print('░', end='')
      else :
        print('█', end='')
    print()

#--------------------------------------------------
def main() :
  size = int( sys.argv[ 1 ] )
  generations = int( sys.argv[ 2 ] )

  grid = [ [ 0 ] * ( size+2 ) for _ in range( size+2 ) ]

  for y in range( 1, size+1 ) :
    for x in range( 1, size+1 ) :
      grid[x][y] = random.randint( 0, 1 )

  for i in range( generations ) :
    printGrid( grid, i )
    grid = copy.deepcopy( tick( grid, size ) )

#--------------------------------------------------
if ( __name__ == '__main__' ) :
  main()

#--------------------------------------------------

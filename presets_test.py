# Ramirez, Daniel G.
# 2019-05-16
#--------------------------------------------------
import sys
import random
import copy
#--------------------------------------------------
GENERATIONS = 50
SIZE = 10
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
def randomGrid() :
  # Create grid of size 12
  grid = [ [ 0 ] * ( SIZE+2 ) for _ in range( SIZE+2 ) ]
  # Populate grid randomly
  for y in range( 1, SIZE+1 ) :
    for x in range( 1, SIZE+1 ) :
      grid[x][y] = random.randint( 0, 1 )
  print("randomGrid: %s" % type(grid).__name__)
  return grid
#--------------------------------------------------
# Presets
def preset1Grid() :
  grid = [ [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0],
           [0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0],
           [0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
           [0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0],
           [0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0],
           [0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
  print("preset1Grid: %s" % type(grid).__name__)
  return grid
#--------------------------------------------------
def chosePresetGrid( choice ) :
  print( choice )
  print("choice type: %s" % type(choice).__name__)
  switcher = {
    1: randomGrid,
	2: preset1Grid
  }
  # Get the function from switcher dictionary
  func = switcher.get( choice, lambda: print("Invalid choice") )
  # Execute the function
  grid = func()
  print("chosePresetGrid: %s" % type(grid).__name__)
  return grid
#--------------------------------------------------
def main() :  
  choice = int(input("Select the starting form of the grid.\n\t1. Random\n\t2. Tumbler\n"))
  grid = chosePresetGrid( choice )
  print("Result of choice: %s" % type(grid).__name__)

  # Execute 10 generations of game of life
  for i in range( GENERATIONS ) :
    printGrid( grid, i )
    grid = copy.deepcopy( tick( grid, SIZE ) )

#--------------------------------------------------
if ( __name__ == '__main__' ) :
  main()

#--------------------------------------------------

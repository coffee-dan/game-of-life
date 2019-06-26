import sys, pygame
import copy
import random
from os import path
#--------------------------------------------------
pygame.init()
GRID_SIZE = 10
size = width, height = 640, 640
screen = pygame.display.set_mode(size)

#gui grid
full_cell = pygame.image.load( path.join( '..', 'img', 'full_cell.png' ) )
empty_cell = pygame.image.load( path.join( '..', 'img', 'empty_cell.png' ) )
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
def printGrid( grid, gui_grid ):
  for i in range(10):
      for j in range(10):
        if grid[i][j] == 0:
          screen.blit(empty_cell, gui_grid[i][j])
        else:
          screen.blit(full_cell, gui_grid[i][j])
#--------------------------------------------------
def randomGrid() :
  # Create grid of size 12
  grid = [ [ 0 ] * ( GRID_SIZE+2 ) for _ in range( GRID_SIZE+2 ) ]
  # Populate grid randomly
  for y in range( 1, GRID_SIZE+1 ) :
    for x in range( 1, GRID_SIZE+1 ) :
      grid[x][y] = random.randint( 0, 1 )
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
  
  return grid
#--------------------------------------------------
def chosePresetGrid( choice ) :
  switcher = {
    1: randomGrid,
    2: preset1Grid
  }
  # Get the function from switcher dictionary
  func = switcher.get( choice, lambda: print("Invalid choice") )
  # Execute the function
  return func()
#--------------------------------------------------
def main() :  
  # Create empty grid of GRID_SIZE for display
  gui_grid = [ [ 0 ] * GRID_SIZE for _ in range( GRID_SIZE ) ]
  # Fill gui_grid with positions of each cell
  for i in range(10):
    for j in range(10):
      gui_grid[i][j] = (empty_cell.get_rect().move(i*64, j*64))
      
  choice = int( sys.argv[ 1 ] )
  grid = chosePresetGrid( choice )

  while 1:
    for event in pygame.event.get():
      if event.type == pygame.QUIT: sys.exit()

    printGrid( grid, gui_grid )

    grid = copy.deepcopy( tick( grid, GRID_SIZE ) )

    pygame.display.flip()

    pygame.time.wait(3)

#--------------------------------------------------
if ( __name__ == '__main__' ) :
  main()

#--------------------------------------------------

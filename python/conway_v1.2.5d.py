import sys, pygame
import copy
import random
import math
#--------------------------------------------------
pygame.init()
GRID_SIZE = 10
size = width, height = 640, 640
screen = pygame.display.set_mode(size)

#gui grid
full_cell = pygame.image.load("full_cell.png")
empty_cell = pygame.image.load("empty_cell.png")
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
def printGrid( grid, gui_grid ) :
  for y in range( GRID_SIZE ) :
      for x in range( GRID_SIZE ) :
        if grid[x+1][y+1] == 0 :
          screen.blit( empty_cell, gui_grid[x][y] )
        else :
          screen.blit( full_cell, gui_grid[x][y] )
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
def debugGrid() :
  # Create grid of size 12
  grid = [ [ 0 ] * ( GRID_SIZE+2 ) for _ in range( GRID_SIZE+2 ) ]
  # Populate grid randomly
  for y in range( 1, GRID_SIZE+1 ) :
    for x in range( 1, GRID_SIZE+1 ) :
      if x == 1 :
        grid[x][y] = 1
      else :
        grid[x][y] = 0
  #print( grid )
  return grid
#--------------------------------------------------
# Presets
def loadPreset( choice ) :
  presets_file = open( "grid_presets.txt" )
  for i in range(choice) :
    if i == (choice - 1) :
      preset = str( presets_file.readline() )

  preset = preset.strip( "\n" )
  preset = preset.split( "," )
  
  total_rows = GRID_SIZE - int( preset[1] )
  rows = math.ceil( total_rows / 2 ), math.floor( total_rows / 2 )

  total_cols = GRID_SIZE - int( preset[2] )
  cols = math.ceil( total_cols / 2 ), math.floor( total_cols / 2 )

  # Create a 12 by 12 grid of 0's
  grid = [ [ 0 ] * ( GRID_SIZE+2 ) for _ in range( GRID_SIZE+2 ) ]
  # Populate grid according to chosen preset
  #for y in range( 1, GRID_SIZE+1 ) :
  #  for x in range( 1, GRID_SIZE+1 ) :
      

  # process the data
  #print( preset )
  #print( str( rows ) )
  #print( str( cols ) )
  return debugGrid()
#--------------------------------------------------
def choseStartingGrid( choice ) :
  if choice == 1 :
    return randomGrid()
  elif choice < 1 or choice > 2 :
    print ("Invalid Choice")
    sys.exit(1)
  else :
    return loadPreset(choice)
#--------------------------------------------------
def main() :  
  # Create empty grid of GRID_SIZE for display
  gui_grid = [ [ 0 ] * GRID_SIZE for _ in range( GRID_SIZE ) ]
  # Fill gui_grid with positions of each cell
  for x in range( GRID_SIZE ):
    for y in range( GRID_SIZE ):
      gui_grid[x][y] = empty_cell.get_rect().move( x*64, y*64 )
      
  choice = int( sys.argv[ 1 ] )
  grid = choseStartingGrid( choice )

  while 1:
    for event in pygame.event.get():
      if event.type == pygame.QUIT: sys.exit()

    printGrid( grid, gui_grid )

    grid = copy.deepcopy( tick( grid, GRID_SIZE ) )

    pygame.display.flip()

    pygame.time.wait(20)

#--------------------------------------------------
if ( __name__ == '__main__' ) :
  main()

#--------------------------------------------------

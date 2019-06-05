import sys, pygame
import copy
import random
import math
#--------------------------------------------------
pygame.init()
GRID_SIZE = 10
NUM_OF_PRESETS = 6
size = width, height = 640, 640

#gui assets
full_cell = pygame.image.load("full_cell.png")
empty_cell = pygame.image.load("empty_cell.png")
cursor = pygame.image.load("dan_cursor.png")
random_button = pygame.image.load("random_button.png")
#window setup
pygame.display.set_icon(full_cell)
pygame.display.set_caption('game of life')
screen = pygame.display.set_mode(size,pygame.FULLSCREEN)
# pygame.display.set_mode(pygame.FULLSCREEN)
pygame.mouse.set_visible(False)
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
  #x and y coordinates are inverted 
  for y in range( GRID_SIZE ) :
      for x in range( GRID_SIZE ) :
        if grid[x+1][y+1] == 0 :
          screen.blit( empty_cell, gui_grid[y][x] )
        else :
          screen.blit( full_cell, gui_grid[y][x] )
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
def loadPreset( choice ) :
  presets_file = open( "grid_presets.txt" )
  for i in range( 1, choice ) :
    preset = str( presets_file.readline() )
      

  preset = preset.strip( "\n" )
  preset = preset.split( "," )

  total_rows = GRID_SIZE - int( preset[2] ) #4
  row_offset = math.ceil( total_rows / 2 ), math.floor( total_rows / 2 ) #2,2
  row_barrier = row_offset[0] + 1, GRID_SIZE - row_offset[1] #3,8

  total_cols = GRID_SIZE - int( preset[1] ) #3
  col_offset = math.ceil( total_cols / 2 ), math.floor( total_cols / 2 ) #2,1
  col_barrier = col_offset[0] + 1, GRID_SIZE - col_offset[1] #3,9

  # Create a 12 by 12 grid of 0's
  grid = [ [ 0 ] * ( GRID_SIZE+2 ) for _ in range( GRID_SIZE+2 ) ]
  # Populate grid according to chosen preset
  line_num = 3
  for y in range( 1, GRID_SIZE+1 ) :
    i = 0
    for x in range( 1, GRID_SIZE+1 ) :
      if y < row_barrier[0] :
        grid[x][y] = 0
      elif y > row_barrier[1] :
        grid[x][y] = 0
      elif x < col_barrier[0] :
        grid[x][y] = 0
      elif x > col_barrier[1] :
        grid[x][y] = 0
      else :
        grid[x][y] = int( preset[ line_num ][ i ] )
        i += 1
    if not (y < col_barrier[0] or y > col_barrier[1]) :
      line_num += 1
  return grid
#--------------------------------------------------
def choseStartingGrid( choice ) :
  if choice == 1 :
    return randomGrid()
  elif choice < 1 or choice > NUM_OF_PRESETS :
    print ("Invalid Choice")
    sys.exit(1)
  else :
    return loadPreset(choice)
#--------------------------------------------------
# \TODO do
def menu() :
  patternSelected = None
    # while(patternSelected == None):
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

  #get initial cursor position
  cursorPosition = cursor.get_rect()
  
  #display menu
  menu()

  while 1:
    # Make screen white
    screen.fill([255,255,255])
    # Event watchdog
    for event in pygame.event.get():
      # Watch for exit button press
      if event.type == pygame.QUIT: sys.exit()

      # Watcg for esc key press
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          sys.exit()

      # Watch for mouse movement
      if event.type == pygame.MOUSEMOTION:
        newMousePosition = pygame.mouse.get_pos()
        cursorPosition.x = newMousePosition[0]
        cursorPosition.y = newMousePosition[1]
      # Watch for mouse clicks
      if event.type == pygame.MOUSEBUTTONDOWN:
        clickedPosition = pygame.mouse.get_pos()
        #x and y coordinates are inverted 
        if((int(clickedPosition[1]/64)+1) <= GRID_SIZE and (int(clickedPosition[0]/64)+1) <= GRID_SIZE):
          if grid[int(clickedPosition[1]/64)+1][int(clickedPosition[0]/64)+1] == 1:
            grid[int(clickedPosition[1]/64)+1][int(clickedPosition[0]/64)+1] = 0
          else:
            grid[int(clickedPosition[1]/64)+1][int(clickedPosition[0]/64)+1] = 1

    #display gui grid based on grid calculation matrix
    printGrid( grid, gui_grid )
    #calculate new grid matrix based on rules
    grid = copy.deepcopy( tick( grid, GRID_SIZE ) )

    #display selection cursor
    screen.blit(cursor, newMousePosition)

    pygame.display.flip()

    pygame.time.wait(20)

#--------------------------------------------------
if ( __name__ == '__main__' ) :
  main()

#--------------------------------------------------

import sys
import pygame
import copy
import random
import math
from PIL import Image
#--------------------------------------------------
pygame.init()

NUM_OF_CELLS = 100
NUM_OF_PRESETS = 5
WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 1366, 768 # Dimensions of window

SHORT_SIDE = min( WINDOW_WIDTH, WINDOW_HEIGHT ) # Short side of window
CELL_SIZE = int( SHORT_SIDE / NUM_OF_CELLS ) # Side length of a cell
GRID_SIZE = NUM_OF_CELLS * CELL_SIZE # Side length of grid

#  Dynamic asset resizing - Open default cell design as PIL Image, 
#   resize it, save it as new .png file, load as pygame.image
# Resize full cell design
image = Image.open( 'full_cell_original.png' )
new_image = image.resize( ( CELL_SIZE, CELL_SIZE ) )
new_image.save( 'full_cell_current.png' )
# Resize empty cell design
image = Image.open( 'empty_cell_original.png' )
new_image = image.resize( ( CELL_SIZE, CELL_SIZE ) )
new_image.save( 'empty_cell_current.png' )

# Load in resized designs for use
full_cell = pygame.image.load( 'full_cell_current.png' )
empty_cell = pygame.image.load( 'empty_cell_current.png' )
cursor = pygame.image.load( 'dan_cursor.png' )
#  Random button unused
# random_button = pygame.image.load( 'random_button.png' )

#--------------------------------------------------
def generation( c_grid ) :
  n = NUM_OF_CELLS
  updated_grid = copy.deepcopy( c_grid )

  for y in range( 1, n+1 ) :
    for x in range( 1, n+1 ) :
      neighbors = 0

      if c_grid[ x-1 ][ y-1 ] == 1 :
        neighbors += 1
      if c_grid[  x  ][ y-1 ] == 1 : 
        neighbors += 1
      if c_grid[ x+1 ][ y-1 ] == 1 : 
        neighbors += 1
      if c_grid[ x-1 ][  y  ] == 1 : 
        neighbors += 1
      if c_grid[ x+1 ][  y  ] == 1 : 
        neighbors += 1
      if c_grid[ x-1 ][ y+1 ] == 1 : 
        neighbors += 1
      if c_grid[  x  ][ y+1 ] == 1 : 
        neighbors += 1
      if c_grid[ x+1 ][ y+1 ] == 1 : 
        neighbors += 1

      # Live cell
      if c_grid[ x ][ y ] == 1 :
        if neighbors < 2 :
          # Death by exposure ( <2 neighbors )
      	  updated_grid[ x ][ y ] = 0
        elif neighbors > 3 :
          # Death by overcrowding ( >3 neighbors )
          updated_grid[ x ][ y ] = 0
      # Dead cell
      else :
      	if neighbors == 3 :
      	  # New life
      	  updated_grid[ x ][ y ] = 1

  return updated_grid
#--------------------------------------------------
def printGrid( screen, c_grid, v_grid ) :
  #x and y coordinates are inverted 
  for y in range( NUM_OF_CELLS ) :
    for x in range( NUM_OF_CELLS ) :
      if c_grid[ x+1 ][ y+1 ] == 0 :
        screen.blit( empty_cell, v_grid[ y ][ x ] )
      else :
        screen.blit( full_cell, v_grid[ y ][ x ] )
#--------------------------------------------------
def randomGrid() :
  # Create empty grid full of 0's
  c_grid = [ [ 0 ] * ( NUM_OF_CELLS+2 ) for _ in range( NUM_OF_CELLS+2 ) ]

  # Populate c_grid randomly
  for y in range( 1, NUM_OF_CELLS+1 ) :
    for x in range( 1, NUM_OF_CELLS+1 ) :
      c_grid[x][y] = random.randint( 0, 1 )
  return c_grid
#--------------------------------------------------
def loadPreset( choice ) :
  # Load in all presets as list
  with open( 'grid_presets.txt' ) as presets_file :
    presets = presets_file.read().split( '\n' )	

  # Continue with only chosen preset as list of preset data
  preset = str( presets[ choice-1 ] )
  preset = preset.split( ',' )
  
  # Print name of preset to command line \TODO implement graphically
  print( preset[ 0 ] )

  # Calculate values for creating visual grid
  total_rows = NUM_OF_CELLS - int( preset[ 2 ] )
  row_offset = math.ceil( total_rows/2 ), math.floor( total_rows/2 )
  row_barrier = row_offset[ 0 ]+1, NUM_OF_CELLS - row_offset[ 1 ]

  total_cols = NUM_OF_CELLS - int( preset[ 1 ] )
  col_offset = math.ceil( total_cols/2 ), math.floor( total_cols/2 )
  col_barrier = col_offset[ 0 ]+1, NUM_OF_CELLS - col_offset[ 1 ]

  # Create a 12 by 12 grid of 0's
  c_grid = [ [ 0 ] * ( NUM_OF_CELLS+2 ) for _ in range( NUM_OF_CELLS+2 ) ]
  # Populate c_grid according to chosen preset
  line_num = 3
  for y in range( 1, NUM_OF_CELLS+1 ) :
    i = 0
    for x in range( 1, NUM_OF_CELLS+1 ) :
      if y < row_barrier[ 0 ] :
        c_grid[ x ][ y ] = 0
      elif y > row_barrier[ 1 ] :
        c_grid[ x ][ y ] = 0
      elif x < col_barrier[ 0 ] :
        c_grid[ x ][ y ] = 0
      elif x > col_barrier[ 1 ] :
        c_grid[ x ][ y ] = 0
      else :
        c_grid[ x ][ y ] = int( preset[ line_num ][ i ] )
        i += 1
    if not ( y < col_barrier[ 0 ] or y > col_barrier[ 1 ] ) :
      line_num += 1
  return c_grid
#--------------------------------------------------
def choseStartingGrid( choice ) :
  if choice == 0 :
    return randomGrid()
  elif choice < 0 or choice > NUM_OF_PRESETS :
    print ( 'Invalid Choice' )
    sys.exit( 1 )
  else :
    return loadPreset( choice )
#--------------------------------------------------
def menu() :
  pass
  # patternSelected = None
    # while(patternSelected == None):
#--------------------------------------------------
def setupWindow() :
  #window setup
  pygame.display.set_icon( full_cell )
  pygame.display.set_caption( 'game of life' )
  screen = pygame.display.set_mode( WINDOW_SIZE, pygame.FULLSCREEN )

  # Make screen white
  screen.fill( [ 255, 255, 255 ] )

  return screen
#--------------------------------------------------
def main() :
  # Create empty grid of size NUM_OF_CELLS for display
  v_grid = [ [ 0 ] * NUM_OF_CELLS for _ in range( NUM_OF_CELLS ) ]
  # Compute offsets to print grid in the center of the window
  horizontal_offset = ( WINDOW_WIDTH - GRID_SIZE )/2
  vertical_offset = ( WINDOW_HEIGHT - GRID_SIZE )/2
  # Fill v_grid with positions of each cell
  for x in range( NUM_OF_CELLS ):
    for y in range( NUM_OF_CELLS ):
      v_grid[ x ][ y ] = empty_cell.get_rect().move( ( x * CELL_SIZE ) + horizontal_offset, ( y * CELL_SIZE ) + vertical_offset )
      
  choice = int( sys.argv[ 1 ] )
  c_grid = choseStartingGrid( choice )

  # Get initial cursor position
  cursor_pos = pygame.mouse.get_pos()

  pygame.mouse.set_visible( False )

  screen = setupWindow()
  
  # Display menu - not implemented
  menu()

  # The frequency of generations per each execution of the main loop
  # Ex: if generation_frequency is exactly 7 then generations occur 1 out of every 7 loops
  generation_frequency = 2
  frequency_count = 0
  generation_flag = True

  while 1:
    # Event watchdog
    for event in pygame.event.get() :
      # Watch for exit button press
      if event.type == pygame.QUIT: sys.exit()

      # Watch for esc key press
      if event.type == pygame.KEYDOWN :
        if event.key == pygame.K_ESCAPE :
          sys.exit()
        elif event.key == pygame.K_p :
          generation_flag = not generation_flag

      # Watch for mouse movement
      if event.type == pygame.MOUSEMOTION :
        cursor_pos = pygame.mouse.get_pos()

      # Watch for mouse clicks
      if event.type == pygame.MOUSEBUTTONDOWN:
        clicked_pos = pygame.mouse.get_pos()
        # Determine which cell was clicked if one was clicked
        cell_clicked = int( clicked_pos[ 0 ] / CELL_SIZE )+1, int( clicked_pos[ 1 ] / CELL_SIZE )+1
        #x and y coordinates are inverted
        if( cell_clicked[ 1 ] <= NUM_OF_CELLS and cell_clicked[ 0 ] <= NUM_OF_CELLS ) :
          if c_grid[ cell_clicked[ 1 ] ][ cell_clicked[ 0 ] ] == 1 :
            c_grid[ cell_clicked[ 1 ] ][ cell_clicked[ 0 ] ] = 0
          else:
            c_grid[ cell_clicked[ 1 ] ][ cell_clicked[ 0 ] ] = 1
    
    # Clear screen with background grey
    screen.fill( [ 128, 128, 128 ] )

    # Display visual grid based on computational grid
    printGrid( screen, c_grid, v_grid )

    # Display selection cursor
    screen.blit( cursor, cursor_pos )

    # Only execute generation(...) 1 out of every generation_frequency times and handle pauses
    if frequency_count == generation_frequency and generation_flag :
      # Update computational grid based on game of life rules. One generation
      c_grid = copy.deepcopy( generation( c_grid ) )
      frequency_count = 1
    elif generation_flag :
      frequency_count += 1
    else :
      pass

    # Update entire window
    pygame.display.flip()

    # Control time of each generation by releasing CPU for 40ms
    # pygame.time.wait( 40 )
#--------------------------------------------------
if ( __name__ == '__main__' ) :
  main()
#--------------------------------------------------

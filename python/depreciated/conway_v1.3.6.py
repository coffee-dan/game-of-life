import pygame
import sys
import math
from random import randint
from copy import deepcopy
from PIL import Image
#--------------------------------------------------

NUM_OF_CELLS = 50

#--------------------------------------------------
def generation( c_grid ) :
  n = NUM_OF_CELLS
  updated_grid = deepcopy( c_grid )

  for y in range( 1, n+1 ) :
    for x in range( 1, n+1 ) :
      neighbors = 0

      neighbors += c_grid[ x-1 ][ y-1 ]
      neighbors += c_grid[  x  ][ y-1 ]
      neighbors += c_grid[ x+1 ][ y-1 ]
      neighbors += c_grid[ x-1 ][  y  ]
      neighbors += c_grid[ x+1 ][  y  ]
      neighbors += c_grid[ x-1 ][ y+1 ]
      neighbors += c_grid[  x  ][ y+1 ]
      neighbors += c_grid[ x+1 ][ y+1 ]

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
def printGrid( screen, c_grid, v_grid, full_cell, empty_cell ) :
  for y in range( NUM_OF_CELLS ) :
    for x in range( NUM_OF_CELLS ) :
      if c_grid[ x+1 ][ y+1 ] == 0 :
        screen.blit( empty_cell, v_grid[ x ][ y ] )
      else :
        screen.blit( full_cell, v_grid[ x ][ y ] )
#--------------------------------------------------
def randomGrid() :
  # Create empty grid full of 0's
  c_grid = [ [ 0 ] * ( NUM_OF_CELLS+2 ) for _ in range( NUM_OF_CELLS+2 ) ]

  # Populate c_grid randomly
  for y in range( 1, NUM_OF_CELLS+1 ) :
    for x in range( 1, NUM_OF_CELLS+1 ) :
      c_grid[x][y] = randint( 0, 1 )
  return c_grid
#--------------------------------------------------
def loadPreset( choice ) :
  # Load in all presets as list
  with open( 'grid_presets.txt' ) as presets_file :
    presets = presets_file.read().split( '\n' )

  # Error check
  if choice > len( presets ) :
    print ( 'Error: Choice number given does not exist' )
    sys.exit( 1 )

  # Continue with only chosen preset as list of preset data
  preset = str( presets[ choice-1 ] )
  preset = preset.split( ',' )
  name = preset[ 0 ]
  col_num = int( preset[ 1 ] )
  row_num = int( preset[ 2 ] )
  
  # Print name of preset to command line \TODO implement graphically
  # print( preset[ 0 ] )
  # Debug assistance for preset creation
  for i in range( len( preset ) ) :
    print( '%2d  %s' % ( i, preset[ i ] ) )

  # Calculate values for creating visual grid
  blank_rows = NUM_OF_CELLS - row_num
  row_offsets = math.ceil( blank_rows/2 ), math.floor( blank_rows/2 )
  row_barriers = row_offsets[ 0 ]+1, NUM_OF_CELLS - row_offsets[ 1 ]

  blank_cols = NUM_OF_CELLS - col_num
  col_offsets = math.ceil( blank_cols/2 ), math.floor( blank_cols/2 )
  col_barriers = col_offsets[ 0 ]+1, NUM_OF_CELLS - col_offsets[ 1 ]

  # Create a 12 by 12 grid of 0's
  c_grid = [ [ 0 ] * ( NUM_OF_CELLS+2 ) for _ in range( NUM_OF_CELLS+2 ) ]
  # Populate c_grid according to chosen preset
  line_num = 3
  for y in range( 1, NUM_OF_CELLS+1 ) :
    i = 0
    for x in range( 1, NUM_OF_CELLS+1 ) :
      if y < row_barriers[ 0 ] :
        c_grid[ x ][ y ] = 0
      elif y > row_barriers[ 1 ] :
        c_grid[ x ][ y ] = 0
      elif x < col_barriers[ 0 ] :
        c_grid[ x ][ y ] = 0
      elif x > col_barriers[ 1 ] :
        c_grid[ x ][ y ] = 0
      else :
        c_grid[ x ][ y ] = int( preset[ line_num ][ i ] )
        i += 1
    if ( ( y <= row_barriers[ 1 ] ) and ( y >= row_barriers[ 0 ] ) ) :
      line_num += 1
  return c_grid
#--------------------------------------------------
def choseStartingGrid( choice ) :
  if choice == 0 :
    return randomGrid()
  elif choice < 0 :
    print ( 'Error: Negative number for choice' )
    sys.exit( 1 )
  else :
    return loadPreset( choice )
#--------------------------------------------------
def menu() :
  pass
  # patternSelected = None
    # while(patternSelected == None):
#--------------------------------------------------
def setupWindow( window_size ) :
  #window setup
  icon = pygame.image.load( 'full_cell_original.png' )
  pygame.display.set_icon( icon )
  pygame.display.set_caption( 'game of life' )
  screen = pygame.display.set_mode( window_size, pygame.FULLSCREEN )

  # Make screen white
  screen.fill( [ 255, 255, 255 ] )

  # Make operating system mouse invisible
  pygame.mouse.set_visible( False )

  return screen
#--------------------------------------------------
def loadAssets( cell_size, palette ) :
  #  Dynamic asset resizing - Open default cell design as PIL Image, 
  #   resize it, save it as new .png file, load as pygame.image
  # Resize full cell design
  image = Image.open( 'full_cell_' + palette + '.png' )
  new_image = image.resize( ( cell_size, cell_size ) )
  new_image.save( 'full_cell_current.png' )
  # Resize empty cell design
  image = Image.open( 'empty_cell_' + palette + '.png' )
  new_image = image.resize( ( cell_size, cell_size ) )
  new_image.save( 'empty_cell_current.png' )

  # Load in resized designs for use
  full_cell = pygame.image.load( 'full_cell_current.png' )
  empty_cell = pygame.image.load( 'empty_cell_current.png' )
  cursor = pygame.image.load( 'dan_cursor.png' )
  #  Random button unused
  # random_button = pygame.image.load( 'random_button.png' )
  return full_cell, empty_cell, cursor
#--------------------------------------------------
def main() :
  pygame.init()

  # Dimensions of window
  window_size = window_width, window_height = 1366, 768
  screen = setupWindow( window_size )
  
  # Compute size of cell in pixels for later usage
  short_side = min( window_width, window_height )
  cell_size = int( short_side / NUM_OF_CELLS )

  # Display menu - not implemented
  menu()

  # Load assets according to specified palette
  full_cell, empty_cell, cursor = loadAssets( cell_size, 'gameboy' )

  # Create empty grid of size NUM_OF_CELLS for display
  v_grid = [ [ 0 ] * NUM_OF_CELLS for _ in range( NUM_OF_CELLS ) ]

  # Compute offsets to print grid in the center of the window
  grid_size = NUM_OF_CELLS * cell_size # Side length of grid
  horizontal_offset = ( window_width - grid_size )/2
  vertical_offset = ( window_height - grid_size )/2

  # Fill v_grid with coordinates of each cell
  for x in range( NUM_OF_CELLS ):
    for y in range( NUM_OF_CELLS ):
      v_grid[ x ][ y ] = empty_cell.get_rect().move( ( x * cell_size ) + horizontal_offset, ( y * cell_size ) + vertical_offset )
  
  # Load preset for grid based on command line input
  choice = int( sys.argv[ 1 ] )
  c_grid = choseStartingGrid( choice )

  # Get initial cursor position
  cursor_pos = pygame.mouse.get_pos()

  # The frequency of generations per each execution of the main loop
  # Ex: if generation_frequency is exactly 7 then generations occur 1 out of every 7 loops
  generation_frequency = 3
  frequency_count = 0
  generation_flag = True

  while 1:
    # Clear screen with background grey
    screen.fill( [ 15, 56, 15 ] )

    # Display visual grid based on computational grid
    printGrid( screen, c_grid, v_grid, full_cell, empty_cell )

    # Display selection cursor
    screen.blit( cursor, cursor_pos )

    # Update entire window
    pygame.display.flip()

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
      if event.type == pygame.MOUSEBUTTONDOWN :
        clicked_pos = pygame.mouse.get_pos()
        # Determine which cell was clicked if one was clicked
        cell_clicked = int( ( clicked_pos[ 0 ] - horizontal_offset ) / cell_size )+1, int( ( clicked_pos[ 1 ] - vertical_offset ) / cell_size )+1
        
        if( cell_clicked[ 1 ] <= NUM_OF_CELLS and cell_clicked[ 0 ] <= NUM_OF_CELLS ) :
          if c_grid[ cell_clicked[ 0 ] ][ cell_clicked[ 1 ] ] == 1 :
            c_grid[ cell_clicked[ 0 ] ][ cell_clicked[ 1 ] ] = 0
          else:
            c_grid[ cell_clicked[ 0 ] ][ cell_clicked[ 1 ] ] = 1

    # Only execute generation(...) 1 out of every generation_frequency times and handle pauses
    if frequency_count == generation_frequency and generation_flag :
      # Update computational grid based on game of life rules. One generation
      c_grid = deepcopy( generation( c_grid ) )
      frequency_count = 1
    elif generation_flag :
      frequency_count += 1
    else :
      pass
#--------------------------------------------------
if ( __name__ == '__main__' ) :
  main()
#--------------------------------------------------
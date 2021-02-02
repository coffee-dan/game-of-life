import pygame
import pygame.freetype
import math
from random import randint
from copy import deepcopy
from PIL import Image
from sys import exit
from os import path
#--------------------------------------------------

NUM_OF_CELLS = 50

#--------------------------------------------------
def generation( c_grid ) :
  updated_grid = deepcopy( c_grid )

  for y in range( 1, NUM_OF_CELLS+1 ) :
    for x in range( 1, NUM_OF_CELLS+1 ) :
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
      c_grid[ x ][ y ] = randint( 0, 1 )
  return c_grid
#--------------------------------------------------
def blankGrid() :
  # Create empty grid full of 0's
  c_grid = [ [ 0 ] * ( NUM_OF_CELLS+2 ) for _ in range( NUM_OF_CELLS+2 ) ]
  return c_grid
#--------------------------------------------------
def setupWindow( window_size ) :
  #window setup
  icon = pygame.image.load( path.join( 'img', 'full_cell_original.png' ) )
  pygame.display.set_icon( icon )
  pygame.display.set_caption( 'game of life' )
  screen = pygame.display.set_mode( window_size )

  # Make screen white
  screen.fill( [ 255, 255, 255 ] )

  return screen
#--------------------------------------------------
def loadAssets( cell_size, palette ) :
  #  Dynamic asset resizing - Open default cell design as PIL Image, 
  #   resize it, save it as new .png file, load as pygame.image
  # Resize full cell design
  image = Image.open( path.join( 'img', 'full_cell_' + palette + '.png' ) )
  new_image = image.resize( ( cell_size, cell_size ) )
  new_image.save( 'full_cell_current.png' )
  # Resize empty cell design
  image = Image.open( path.join( 'img', 'empty_cell_' + palette + '.png' ) )
  new_image = image.resize( ( cell_size, cell_size ) )
  new_image.save( 'empty_cell_current.png' )

  # Load in resized designs for use
  full_cell = pygame.image.load( 'full_cell_current.png' )
  empty_cell = pygame.image.load( 'empty_cell_current.png' )
  cursor = pygame.image.load( path.join( 'img', 'dan_cursor.png' ) )
  #  Random button unused
  # random_button = pygame.image.load( 'random_button.png' )

  # Load theme and select sound
  theme = pygame.mixer.music.load( path.join( 'caliope_theme.mp3' ) )
  cell_select = pygame.mixer.Sound( path.join( 'cell_select_2.ogg' ) )
  cell_select.set_volume(1)
  return full_cell, empty_cell, cursor, theme, cell_select
#--------------------------------------------------
def loadPresets( button, window_size ) :
  # Extract data from presets_file into presets_data to be further
  # split into individual presets to be added to dictionary
  with open( 'grid_presets.txt' ) as presets_file :
    presets = presets_file.read().split( '\n' )

  preset_entries = dict()

  for preset in presets :
    preset = preset.split( ',' )
    
    name = preset[ 0 ]
    col_num = int( preset[ 1 ] )
    row_num = int( preset[ 2 ] )

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
    #  Line num represents the position within the list of elements that make up a preset,
    #  it starts at 3 because that is where cell placement information starts.
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
    
    # Convert list to tuple, so it is hashable
    t = list()
    for cell in c_grid :
      t.append( tuple( cell ) )
    t = tuple( t )
    
    preset_entries.update({ name : t })
  # print(preset_entries)

  # generate ui_grid
  button_size = int( window_size[0] / (4*2) )

  ui_pages = list()
  empty_page = [
    [ '', '', ''] ,
    [ '', '', ''] ,
    [ '', '', ''] ,
  ]

  entries = list(preset_entries.keys())
  entries_transferred = 0
  while(entries_transferred < len(preset_entries.keys())):
    current_page = deepcopy(empty_page)
    for x in range(3):
      for y in range(3):
        if entries_transferred < len(preset_entries.keys()):
          current_page[x][y] = entries[entries_transferred]
          entries_transferred = entries_transferred + 1
    ui_pages.append(current_page)

  # only supports one page
  page_size = 3
  v_button_grid = [ [ None ] * page_size for _ in range( page_size ) ]
  
  button_size = button.get_rect().width
  screen_width = window_size[ 0 ]
  screen_height = window_size[ 1 ]
  b_offset = int( screen_height * 0.5 * 1/3 )
  offset = int( screen_height * 1/4 )
  h_offsets = [ 0, int( screen_width/2 - button_size*0.5 ), int( screen_width - button_size ) ]
  v_offsets = [ offset, int( screen_height*0.5 - button_size*0.5 ), int( screen_height*0.75 - button_size ) ]

  for y in range( page_size ) :
      for x in range( page_size ) :
        v_button_grid[ x ][ y ] = button.get_rect().move( h_offsets[ y ] , v_offsets[ x ] )

  return preset_entries, ui_pages, v_button_grid
#--------------------------------------------------
def printButtons( screen, v_button_grid, button, font, preset_entries, ui_pages) :
  screen_size = screen.get_size()
  title_render = pygame.freetype.Font( path.join( 'fonts', 'POLYA.otf' ), int( screen_size[0] * 1/6.45 ) )

  # title_font.underline()
  # title_name_render = title_font.render( 'GAME OF LIFE' , True, [0, 0, 0], None )
  title_size = ( int( screen_size[ 0 ]*1/10 ) , int( screen_size[ 1 ]*0.25) )
  title_position = ( ( int( screen_size[ 0 ]*0.5 ) - int( title_size[ 0 ]*3.5 ) ), 0 ) 
  title_render.render_to( screen, title_position, 'GAME OF LIFE', [ 254, 127, 156 ], None, pygame.freetype.STYLE_UNDERLINE, 0, size=title_size )

  # screen.blit( title_name_render, title_rect )
  for y in range( 3 ):
    for x in range( 3 ):
      # render button
      screen.blit( button, v_button_grid[ x ][ y ] )
      present_name = ui_pages[ 0 ][ x ][ y ]

      # render preset name
      preset_name_render = font.render( present_name , True, [ 0, 0, 0 ], None )
      screen.blit( preset_name_render, v_button_grid[ x ][ y ].move( 0, 0 ) )
      # title_font.render_to(screen, v_button_grid[x][y], present_name, [0,0,0], None, 0, size=int( 25 ) )
#--------------------------------------------------
def checkButtonClick( clicked_pos, v_button_grid, ui_pages, button_size ):
  preset_selected = ''
  for y in range( 3 ):
    for x in range( 3 ):
      if ( ( clicked_pos[ 0 ] >= v_button_grid[ x ][ y ].x ) and ( clicked_pos[ 0 ] <= v_button_grid[ x ][ y ].x + button_size ) ) :
        if ( ( clicked_pos[ 1 ] >= v_button_grid[ x ][ y ].y ) and ( clicked_pos[ 1 ]  <= v_button_grid[ x ][ y ].y + button_size ) ) :
          preset_selected = ui_pages[ 0 ][ x ][ y ]

  return preset_selected
#--------------------------------------------------
def main() :
  pygame.init()
  pygame.freetype.init()

  # Dimensions of window
  #  Emmanuel screen dimensions
  #  window_size = window_width, window_height = 1600, 800
  #  Dan screen dimensions
  window_size = window_width, window_height = 1366, 768
  screen = setupWindow( window_size )
  
  # Compute size of cell in pixels for later usage
  short_side = min( window_width, window_height )
  cell_size = int( short_side / NUM_OF_CELLS )

  # Load assets according to specified palette
  full_cell, empty_cell, cursor, theme, cell_select = loadAssets( cell_size, 'original' )

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
  
  # starting grid is blank
  c_grid = blankGrid()

  # new pause mode
  clock = pygame.time.Clock()
  paused = False

  # multiple cell selection
  cell_selection_dict = dict()
  cell_selection = False

  # set music to play
  pygame.mixer.music.set_volume(.25) 
  pygame.mixer.music.play()

  # User interface setup
  button_size = int( window_width/( 4*2 ) )
  image = Image.open( path.join( 'img' , 'full_cell_original.png' ) )
  new_image = image.resize( ( button_size , button_size ) ) 
  new_image.save( path.join( 'img' , 'button_current.png' ) )
  button =  pygame.image.load( path.join( 'img' , 'button_current.png' ) )
  # Loading in fonts
  font = pygame.font.Font( path.join( 'fonts' , 'Roboto-Regular.ttf' ), int( button_size*0.25 ) )

  preset_entries, ui_pages, v_button_grid = loadPresets( button, window_size )

  # Game starts in the menu
  in_menu = True

  # game_running boolean exists for readability
  game_running = True
  while game_running :

    # set fps
    clock.tick(30)

    # Clear screen with background grey
    if not in_menu : 
      screen.fill( [ 15, 56, 15 ] )
      # Display visual grid based on computational grid
      printGrid( screen, c_grid, v_grid, full_cell, empty_cell )
    else :
      screen.fill( [ 255, 255, 255 ] )
      printButtons( screen, v_button_grid, button, font, preset_entries, ui_pages)

    # screen.blit(s, button.get_rect())

    # Update entire window
    pygame.display.flip()
    
    # loop song every 30 seconds
    if pygame.mixer.music.get_pos() > 29999 :
      pygame.mixer.music.play()

    # Event watchdog
    for event in pygame.event.get() :
      # Watch for exit button press
      if event.type == pygame.QUIT: exit()

      # Watch for esc key press
      if event.type == pygame.KEYDOWN :
        if event.key == pygame.K_ESCAPE :
          exit()
        elif event.key == pygame.K_TAB :
          c_grid = blankGrid()
          in_menu = True

        elif event.key == pygame.K_p :
          paused = not paused
        elif event.key == pygame.K_c :
          #clear grid
          for y in range( NUM_OF_CELLS+1 ) :
            for x in range( NUM_OF_CELLS+1 ) :
              c_grid[ x ][ y ] = 0 
      
      # Watch for mouse movement
      if event.type == pygame.MOUSEMOTION :
        if not in_menu :
          if cell_selection :
            clicked_pos = pygame.mouse.get_pos()
            cell_clicked = int( ( clicked_pos[ 0 ] - horizontal_offset ) / cell_size )+1, int( ( clicked_pos[ 1 ] - vertical_offset ) / cell_size )+1
    
            # update if valid position and coordinate is not already in dictionary
            if ( cell_clicked[ 1 ] <= NUM_OF_CELLS and cell_clicked[ 0 ] <= NUM_OF_CELLS ) and ( cell_clicked not in cell_selection_dict.keys() ):
              # play sound effect when new entry is added
              cell_select.play()
              cell_selection_dict.update({ cell_clicked : c_grid[ cell_clicked[ 0 ] ][ cell_clicked[ 1 ] ] })

            # invert cell state to indicate selection
            for coordinate in cell_selection_dict.keys() :
              if c_grid[ coordinate[ 0 ] ][ coordinate[ 1 ] ] == 1 :
                c_grid[ coordinate[ 0 ] ][ coordinate[ 1 ] ] = 0
              else:
                c_grid[ coordinate[ 0 ] ][ coordinate[ 1 ] ] = 1

      # Watch for mouse clicks
      if event.type == pygame.MOUSEBUTTONDOWN :
        if not in_menu :
          cell_selection = True
          cell_select.play()
          clicked_pos = pygame.mouse.get_pos()
          # Determine which cell was clicked if one was clicked
          cell_clicked = int( ( clicked_pos[ 0 ] - horizontal_offset ) / cell_size )+1, int( ( clicked_pos[ 1 ] - vertical_offset ) / cell_size )+1
          
          if( cell_clicked[ 1 ] <= NUM_OF_CELLS and cell_clicked[ 0 ] <= NUM_OF_CELLS ) :
            if c_grid[ cell_clicked[ 0 ] ][ cell_clicked[ 1 ] ] == 1 :
              c_grid[ cell_clicked[ 0 ] ][ cell_clicked[ 1 ] ] = 0
            else:
              c_grid[ cell_clicked[ 0 ] ][ cell_clicked[ 1 ] ] = 1
        else :
            clicked_pos = pygame.mouse.get_pos()
            # check for button click
            preset_selected = checkButtonClick( clicked_pos, v_button_grid, ui_pages, button_size )
            if preset_selected != '' :
              cell_select.play()
              # convert tuple to list
              preset_selected_grid_t = preset_entries[ preset_selected ]
              preset_selected_grid_l = [ [ None ] * len( preset_selected_grid_t[ 0 ] ) for _ in range( len( preset_selected_grid_t ) ) ]
              for y in range( len( preset_selected_grid_t ) ) :
                for x in range( len( preset_selected_grid_t[ 0 ] ) ) :
                  preset_selected_grid_l[ x ][ y ] = preset_selected_grid_t[ x ][ y ]

              # set grid to preset and start simulation
              c_grid = preset_selected_grid_l
              in_menu = False

      # watch for selection end
      if event.type == pygame.MOUSEBUTTONUP :
        if not in_menu :
          for coordinate in cell_selection_dict.keys() :
            # populate cell 
            c_grid[ coordinate[ 0 ] ][ coordinate[ 1 ] ] = 1
            # invert cell state saved
            # if cell_selection_dict.get( coordinate ) == 1 :
            #   c_grid[ coordinate[ 0 ] ][ coordinate[ 1 ] ] = 0
            # else:
            #   c_grid[ coordinate[ 0 ] ][ coordinate[ 1 ] ] = 1

          cell_selection_dict.clear()
          cell_selection = False
    # End of event watchdog------------------------

    # Execute generation(...) if game is not paused
    if paused == False and not in_menu :
      c_grid = deepcopy( generation( c_grid ) )
#--------------------------------------------------
if ( __name__ == '__main__' ) :
  main()
#--------------------------------------------------

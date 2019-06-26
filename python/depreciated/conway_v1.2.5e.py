import sys, pygame
import copy
import random
from os import path
#--------------------------------------------------
pygame.init()
GRID_SIZE = 10
size = width, height = 640, 640

#gui assets
full_cell = pygame.image.load( path.join( '..', 'img', 'full_cell.png' ) )
empty_cell = pygame.image.load( path.join( '..', 'img', 'empty_cell.png' ) )
cursor = pygame.image.load( path.join( '..', 'img', 'dan_cursor.png' ) )
random_button = pygame.image.load( path.join( '..', 'img', 'random_button.png' ) )
#window setup
pygame.display.set_icon(full_cell)
pygame.display.set_caption('game of life')
screen = pygame.display.set_mode(size)
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
def printGrid( grid, gui_grid ):
  #x and y coordinates are inverted 
  for y in range(GRID_SIZE):
      for x in range(GRID_SIZE):
        if grid[x+1][y+1] == 0:
          screen.blit(empty_cell, gui_grid[y][x])
        else:
          screen.blit(full_cell, gui_grid[y][x])
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



def mainMenu():
  
    patternSelected = None
    # while(patternSelected == None):
      
#--------------------------------------------------
def main() :  
  # Create empty grid of GRID_SIZE for display
  gui_grid = [ [ 0 ] * GRID_SIZE for _ in range( GRID_SIZE ) ]
  # Fill gui_grid with positions of each cell
  for x in range(GRID_SIZE):
    for y in range(GRID_SIZE):
      gui_grid[x][y] = (empty_cell.get_rect().move(x*64, y*64))
      
  choice = int( sys.argv[ 1 ] )
  grid = chosePresetGrid( choice )


  #get initial cursor position
  cursorPosition = cursor.get_rect()
  
  #display menu
  mainMenu()


  while 1:
    screen.fill([255,255,255])

    for event in pygame.event.get():
      if event.type == pygame.QUIT: sys.exit()

      if event.type == pygame.MOUSEMOTION:
        newMousePosition = pygame.mouse.get_pos()
        cursorPosition.x = newMousePosition[0]
        cursorPosition.y = newMousePosition[1]

      if event.type == pygame.MOUSEBUTTONDOWN:
        clickedPosition = pygame.mouse.get_pos()
        #x and y coordinates are inverted 
        if grid[int(clickedPosition[1]/64)+1][int(clickedPosition[0]/64)+1] == 1:
          grid[int(clickedPosition[1]/64)+1][int(clickedPosition[0]/64)+1] = 0
        else:
          grid[int(clickedPosition[1]/64)+1][int(clickedPosition[0]/64)+1] = 1

    #display gui grid based on grid calculation matrix
    
    printGrid( grid, gui_grid )
    # screen.fill([255,255,255])

    # screen.blit(random_button,random_button.get_rect())
    #display selection cursor
    screen.blit(cursor, newMousePosition)

    #calculate new grid matrix based on rules
    grid = copy.deepcopy( tick( grid, GRID_SIZE ) )


     

    pygame.display.flip()

    pygame.time.wait(3)

#--------------------------------------------------
if ( __name__ == '__main__' ) :
  main()

#--------------------------------------------------

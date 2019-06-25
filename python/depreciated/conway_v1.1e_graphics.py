import sys, pygame
import copy
pygame.init()
import time
import random
#------------------------------------#
# how to run: python3 conway.py <size of grid> <number of iterations>
#------------------------------------#

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


size = width, height = 640, 640
speed = [20, 10]
black = 0, 0, 0

screen = pygame.display.set_mode(size)


#gui grid
full_cell = pygame.image.load("full_cell.png")
empty_cell = pygame.image.load("empty_cell.png")

gui_grid = []
for i in range(10):
    gui_grid.append([])
    for j in range(10):
        gui_grid[i].append(None)

for i in range(10):
    for j in range(10):
            gui_grid[i][j] = (full_cell.get_rect().move(i*64,j*64))



size = int( sys.argv[ 1 ] )
generations = int( sys.argv[ 2 ] )

grid = [ [ 0 ] * ( size+2 ) for _ in range( size+2 ) ]

for y in range( 1, size+1 ) :
    for x in range( 1, size+1 ) :
      grid[x][y] = random.randint( 0, 1 )



while 1:
    time.sleep(.001)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    for i in range(10):
        for j in range(10):
            if grid[i][j] == 0:
                screen.blit(empty_cell, gui_grid[i][j])
            else:
                screen.blit(full_cell, gui_grid[i][j])

    grid = copy.deepcopy( tick( grid, size ) )


    pygame.display.flip()
from util import manhattan_distance
from game import Grid
import os
import random
from functools import reduce

VISIBILITY_MATRIX_CACHE = {}

class Layout:
  """
  A Layout manages the static information about the game board.
  """
  
  def __init__(self, layoutText):
    self.width = len(layoutText[0])
    self.height= len(layoutText)
    self.walls = Grid(self.width, self.height, False)
    self.food = Grid(self.width, self.height, False)
    self.capsules = []
    self.agentPositions = []
    self.numGhosts = 0
    self.process_layout_text(layoutText)
    self.layoutText = layoutText
    # self.initialize_visibility_matrix()
    
  def get_num_ghosts(self):
    return self.numGhosts
    
  def initialize_visibility_matrix(self):
    global VISIBILITY_MATRIX_CACHE
    if reduce(str.__add__, self.layoutText) not in VISIBILITY_MATRIX_CACHE:
      from game import Directions
      vecs = [(-0.5,0), (0.5,0),(0,-0.5),(0,0.5)]
      dirs = [Directions.NORTH, Directions.SOUTH, Directions.WEST, Directions.EAST]
      vis = Grid(self.width, self.height, {Directions.NORTH:set(), Directions.SOUTH:set(), Directions.EAST:set(), Directions.WEST:set(), Directions.STOP:set()})
      for x in range(self.width):
        for y in range(self.height):
          if self.walls[x][y] == False:
            for vec, direction in zip(vecs, dirs):
              dx, dy = vec
              nextx, nexty = x + dx, y + dy
              while (nextx + nexty) != int(nextx) + int(nexty) or not self.walls[int(nextx)][int(nexty)] :
                vis[x][y][direction].add((nextx, nexty))
                nextx, nexty = x + dx, y + dy
      self.visibility = vis      
      VISIBILITY_MATRIX_CACHE[reduce(str.__add__, self.layoutText)] = vis
    else:
      self.visibility = VISIBILITY_MATRIX_CACHE[reduce(str.__add__, self.layoutText)]
      
  def is_wall(self, pos):
    x, col = pos
    return self.walls[x][col]
  
  def get_random_legal_position(self):
    x = random.choice(list(range(self.width)))
    y = random.choice(list(range(self.height)))
    while self.is_wall( (x, y) ):
      x = random.choice(list(range(self.width)))
      y = random.choice(list(range(self.height)))
    return (x,y)

  def get_random_corner(self):
    poses = [(1,1), (1, self.height - 2), (self.width - 2, 1), (self.width - 2, self.height - 2)]
    return random.choice(poses)

  def get_furthest_corner(self, pacPos):
    poses = [(1,1), (1, self.height - 2), (self.width - 2, 1), (self.width - 2, self.height - 2)]
    dist, pos = max([(manhattan_distance(p, pacPos), p) for p in poses])
    return pos
  
  def is_visible_from(self, ghostPos, pacPos, pacDirection):
    row, col = [int(x) for x in pacPos]
    return ghostPos in self.visibility[row][col][pacDirection]
  
  def __str__(self):
    return "\n".join(self.layoutText)
    
  def deep_copy(self):
    return Layout(self.layoutText[:])
    
  def process_layout_text(self, layoutText):
    """
    Coordinates are flipped from the input format to the (x,y) convention here
    
    The shape of the maze.  Each character  
    represents a different type of object.   
     % - Wall                               
     . - Food
     o - Capsule
     G - Ghost
     P - Pacman
    Other characters are ignored.
    """
    maxY = self.height - 1
    for y in range(self.height):       
      for x in range(self.width):
        layoutChar = layoutText[maxY - y][x]  
        self.process_layout_char(x, y, layoutChar)
    self.agentPositions.sort()
    self.agentPositions = [ ( i == 0, pos) for i, pos in self.agentPositions]
  
  def process_layout_char(self, x, y, layoutChar):
    if layoutChar == '%':      
      self.walls[x][y] = True
    elif layoutChar == '.':
      self.food[x][y] = True 
    elif layoutChar == 'o':    
      self.capsules.append((x, y))   
    elif layoutChar == 'P':    
      self.agentPositions.append( (0, (x, y) ) )
    elif layoutChar in ['G']:    
      self.agentPositions.append( (1, (x, y) ) )
      self.numGhosts += 1
    elif layoutChar in  ['1', '2', '3', '4']:
      self.agentPositions.append( (int(layoutChar), (x,y)))
      self.numGhosts += 1 
def get_layout(name, back = 2):
  if name.endswith('.lay'):
    layout = try_to_load('layouts/' + name)
    if layout is None: layout = try_to_load(name)
  else:
    layout = try_to_load('layouts/' + name + '.lay')
    if layout is None: layout = try_to_load(name + '.lay')
  if layout is None and back >= 0:
    curdir = os.path.abspath('.')
    os.chdir('..')
    layout = get_layout(name, back -1)
    os.chdir(curdir)
  return layout

def try_to_load(fullname):
  if(not os.path.exists(fullname)): return None
  f = open(fullname)
  try: return Layout([line.strip() for line in f])
  finally: f.close()

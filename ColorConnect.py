#Jacob Drilling
#CS5400 - Intro to AI
#Implements the game "ColorConnect"

import sys
from copy import deepcopy

#Very basic Class to hold an action in the game, wich is in essence a color
# and where to place that color
class Action:
  def __init__(self, color, coord):
    self.color = color
    self.coord = coord

class Board:
  EMPTY = 255 #All 1's for a byte.
  def __init__(self, dim = 0):
    self.dim = dim
    self.area = bytearray(self.dim**2)

  #Creates a deep copy of the board object
  #Returns: the deep copied Board object
  def copy(self):
    cp = Board(self.dim)
    cp.area = bytearray(self.area)
    return cp

  #These are the setters and getters to add some abstraction to the byte array.
  def set(self, coord, dat):
    self.area[coord[0] + self.dim*coord[1]] = dat

  def get(self, coord):
    return self.area[coord[0] + self.dim*coord[1]]

class Game:
  def __init__(self, path=None):
    self.board = None
    self.start = None
    self.head = None
    self.end = None

    if path:
      self.loadFromFile(path)

  #Desc: Loads the initial game state from the specified file.
  #Params: path - the relative path to the puzzle to be solved.
  #Post: the board, start, head and end objects are set for this puzzle 
  # instance.
  def loadFromFile(self, path):
    try:
      puzFile = open(path)
      line = puzFile.readline().rstrip('\n').split()
      rowCol = int(line[0])
      colors = int(line[1])
      self.start = [None for color in range(colors)]
      self.head = [None for color in range(colors)]
      self.end = [None for color in range(colors)]

      self.board = Board(rowCol)
      tmp = [puzFile.readline().rstrip().split() for i in range(rowCol)]

      puzFile.close()
    except IOError:
      print("Error openening puzzle file: \'{}\'\n".format(path))
      sys.exit()

    #Loops through the temp board to load it into the bytearray
    for y, row in enumerate(tmp):
      for x, dat in enumerate(row):
        if dat != 'e' and 0 <= int(dat) < colors:
          dat = int(dat)
          coord = bytearray([x,y])
          self.board.set(coord, dat)
          if self.start[dat] is None:
            self.start[dat] = coord
            self.head[dat] = coord
          elif self.end[dat] is None:
            self.end[dat] = coord
          else:
            raise Exception("Found 3rd instance of color: {}  --- Wat?".format(dat))
        elif dat == 'e':
          self.board.set([x,y], Board.EMPTY)

  #Desc: determines wich actions can be performed in this game state.
  #Returns: a list of 'Action' objects that represent valid changes to this
  # game state.
  def getAllActions(self):
    actions = []

    for color, cur in enumerate(self.head):
      if cur == self.end[color]:
        continue

      #UP
      if cur[1] + 1 < self.board.dim:
        up = bytearray(cur)
        up[1] += 1
        if self.board.get(up) == Board.EMPTY or (self.end[color] == up and cur != self.start[color]):
          act = Action(color, up)
          actions.append(act)
      
      #Down
      if cur[1] > 0:
        dn = bytearray(cur)
        dn[1] -= 1
        if self.board.get(dn) == Board.EMPTY or (self.end[color] == dn and cur != self.start[color]):
          act = Action(color, dn)
          actions.append(act)

      #Left
      if cur[0] > 0:
        lft = bytearray(cur)
        lft[0] -= 1
        if self.board.get(lft) == Board.EMPTY or (self.end[color] == lft and cur != self.start[color]):
          act = Action(color, lft)
          actions.append(act)

      #Right
      if cur[0] + 1 < self.board.dim:
        rt = bytearray(cur)
        rt[0] += 1 
        if self.board.get(rt) == Board.EMPTY or (self.end[color] == rt and cur != self.start[color]):
          act = Action(color, rt)
          actions.append(act)

    return actions

  #Determins if the current state is a goal state
  def gameOver(self):
    for color, cur in enumerate(self.head):
      if cur != self.end[color]:
        return False

    return True

  #Desc: Changes the game state to reflect the action given.
  #Param: action - an 'Action' object
  #Pre: self.board must be set as a 'Board' object. 
  #     The Action object should be a valid action in the current state.
  def perform(self, action):
    self.head[action.color] = action.coord
    self.board.set(action.coord, action.color)

  #Returns: A deep copy of this game object
  def copy(self):
    cp = Game()
    #Changed to a shallow copy because the starts don't change
    #cp.start = [bytearray(x) for x in self.start]
    cp.start = self.start
    cp.head = [bytearray(x) for x in self.head]
    #Changed to a shallow copy because the end doesn't change
    #cp.end = [bytearray(x) for x in self.end]
    cp.end = self.end
    cp.board = self.board.copy()
    return cp

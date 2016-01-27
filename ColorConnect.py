#Jacob Drilling
#CS5400 - Intro to AI
#Implements the game "ColorConnect"

import sys
from copy import deepcopy

class Action:
  def __init__(self, color, coord):
    self.color = color
    self.coord = coord

class Game:
  def __init__(self, path=None):
    self.board = None
    self.start = None
    self.end = None

    if path:
      self.loadFromFile(path)

  #Loads the initial game state from the specified file.
  def loadFromFile(self, path):
    try:
      puzFile = open(path)
      line = puzFile.readline().rstrip('\n').split()
      rowCol = int(line[0])
      colors = int(line[1])
      self.start = [None for color in range(colors)]
      self.end = [None for color in range(colors)]

      self.board = [puzFile.readline().rstrip().split() for i in range(rowCol)]

      puzFile.close()
    except IOError:
      print("Error openening puzzle file: \'{}\'\n".format(path))
      sys.exit()

    for y, row in enumerate(self.board):
      for x, dat in enumerate(row):
        if dat != 'e' and 0 <= int(dat) < colors:
          dat = int(dat)
          coord = [x,y]
          if self.start[dat] is None:
            self.start[dat] = coord
          elif self.end[dat] is None:
            self.end[dat] = coord
          else:
            raise Exception("Found 3rd instance of color: {}  --- Wat?".format(dat))

    print(self.start)
    print(self.end)

  #Returns a list of Actions that can currently be performed in this game state.
  def getAllActions(self):
    actions = []

    for color, cur in enumerate(self.start):

      if cur == self.end[color]:
        continue

      #UP
      up = list(cur)
      up[1] += 1
      if up[1] < len(self.board) and self.board[up[1]][up[0]] == 'e' or self.end[color] == up:
        act = Action(color, up)
        actions.append(act)
      
      #Down
      dn = list(cur)
      dn[1] -= 1
      if dn[1] > 0 and self.board[dn[1]][dn[0]] == 'e' or self.end[color] == dn:
        act = Action(color, dn)
        actions.append(act)

      #Left
      lft = list(cur)
      lft[0] -= 1
      if lft[0] > 0 and self.board[lft[1]][lft[0]] == 'e' or self.end[color] == lft:
        act = Action(color, lft)
        actions.append(act)

      #Right
      rt = list(cur)
      rt[0] += 1 
      if rt[0] < len(self.board) and self.board[rt[1]][rt[0]] == 'e' or self.end[color] == rt:
        act = Action(color, rt)
        actions.append(act)

    return actions

  #Determins if the current state is a goal state
  def gameOver(self):
    for color, cur in enumerate(self.start):
      if cur !=  self.end[color]:
        return False

    return True

  #Changes the game state to reflect the action given.
  def perform(self, action):
    self.start[action.color] = action.coord
    self.board[action.coord[1]][action.coord[0]] = action.color

  def copy(self):
    return deepcopy(self)

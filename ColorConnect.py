#Jacob Drilling
#CS5400 - Intro to AI
#Implements the game "ColorConnect"

import sys

class Action:
  def __init__(self, color, coord):
    self.color = color
    self.coord = coord

class Game:
  def __init__(self, path=None):
    self.board = None
    self.starts = {}
    self.ends = {}

    if path:
      self.loadFromFile(path)

  #Loads the initial game state from the specified file.
  def loadFromFile(self, path):
    try:
      puzFile = open(path)
      line = puzFile.readline().rstrip('\n').split()
      rowCol = int(line[0])
      colors = int(line[1])

      self.board = [puzFile.readline().rstrip().split() for i in range(rowCol)]

      puzFile.close()
    except IOError:
      print("Error openening puzzle file: \'{}\'\n".format(path))
      sys.exit()

    for y, row in enumerate(self.board):
      for x, dat in enumerate(row):
        if dat != 'e':
          coord = [x,y]
          if dat not in self.starts:
            self.starts[dat] = coord
          elif dat not in self.ends:
            self.ends[dat] = coord
          else:
            raise Exception("Found 3rd instance of color: {}  --- Wat?".format(dat))

  #Returns a list of Actions that can currently be performed in this game state.
  def getAllActions(self):
    actions = []

    for color in self.starts:
      cur = self.starts[color]

      #UP
      if cur[1] + 1 < len(self.board) and self.board[cur[1] + 1][cur[0]] == 'e':
        new = list(cur)
        new[1] += 1
        act = Action(color, new)
        actions.append(act)
      
      #Down
      if cur[1] - 1 > 0 and self.board[cur[1] - 1][cur[0]] == 'e':
        new = list(cur)
        new[1] -= 1
        act = Action(color, new)
        actions.append(act)

      #Left
      if cur[0] + 1 < len(self.board) and self.board[cur[1]][cur[0] + 1] == 'e':
        new = list(cur)
        new[0] += 1
        act = Action(color, new)
        actions.append(act)

      #Right
      if cur[0] - 1 >0  and self.board[cur[1]][cur[0] - 1] == 'e':
        new = list(cur)
        new[0] -= 1
        act = Action(color, new)
        actions.append(act)

    return actions

  #Determins if the current state is a goal state
  def gameOver(self):
    for color in self.starts:
      if  abs(self.starts[color][0] - self.ends[color][0]) + \
          abs(self.starts[color][1] - self.ends[color][1]) > 1:
        return False

    return True

  def perform(self, action):
    self.starts[action.color] = action.coord
    self.board[action.coord[1]][action.coord[0]] = action.color

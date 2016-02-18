#Jacob Drilling
#CS5400 - Intro to AI
#Implements the game "ColorConnect"

import sys

#Very basic Class to hold an action in the game, wich is in essence a color
# and where to place that color
class Action:
  def __init__(self, color, coord):
    self.color = color
    self.coord = coord

class Board:
  EMPTY = 255 #All 1's for a byte.
  def __init__(self, dim = 0, copy = None):
    if copy is None:
      self.dim = dim
      self.area = bytearray(self.dim**2)
      self.validMoves = None
    #Creates a deep copy of the board object
    elif copy is not None:
      self.dim = copy.dim
      self.area = copy.area[:]
      #The valid Moves will not change for a copy so shallow copy is OK.
      self.validMoves = copy.validMoves

  # Desc: Generates a dict of all possible moves at each index. this makes it
  #       so that we only have to do move math once.
  # Post: ValidMoves is set to a list of bytearrays
  def initMoveSet(self):
    self.validMoves = [[] for x in range(self.dim**2)]
    index = 0
    for y in range(self.dim):
      for x in range(self.dim):
        #Up
        if y + 1 < self.dim:
          self.validMoves[index].append(bytearray([x,y+1]))
        #Down
        if y > 0:
          self.validMoves[index].append(bytearray([x,y-1]))
        #Left
        if x > 0:
          self.validMoves[index].append(bytearray([x-1,y]))
        #Right
        if x + 1 < self.dim:
          self.validMoves[index].append(bytearray([x+1,y]))

        index += 1


  #These are the setters and getters to add some abstraction to the byte array.
  def setTile(self, coord, dat):
    self.area[coord[0] + self.dim*coord[1]] = dat

  def getTile(self, coord):
    return self.area[coord[0] + self.dim*coord[1]]

  def getValidMoves(self, coord):
    return self.validMoves[coord[0] + self.dim*coord[1]]

  # Overloding hash() and == provides a lot of abstraction so that we can use
  # sets and == (or 'in')
  def __eq__(self, other):
    if isinstance(other, Board):
      return self.area == other.area
    else:
      return False

  def __hash__(self):
    return hash(tuple(self.area))

  def printB(self):
    for y in range(self.dim):
      out = ""
      for x in range(self.dim):
        space = self.getTile((x,y))
        if space == Board.EMPTY:
          space = "e"
        out += "{} ".format(space)
      print(out)

class Game:
  def __init__(self, path=None, copy=None):
    if copy is None:
      self.board = None
      self.start = None
      self.head = None
      self.end = None

      if path:
        self.loadFromFile(path)

    elif copy is not None:
      #Changed to a shallow copy because the starts don't change
      self.start = copy.start
      self.head = list(copy.head) 
      #Changed to a shallow copy because the end doesn't change
      self.end = copy.end
      self.board = Board(copy=copy.board)

  def __eq__(self, other):
    if isinstance(other, Game):
      return self.board == other.board and self.head == other.head
    else:
      return False

  def __hash__(self):
    return hash((self.board,
            tuple(frozenset(coord) for coord in self.head)))

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
      raise Exception("Error openening puzzle file: \'{}\'\n".format(path))

    #Loops through the temp board to load it into the bytearray
    for y, row in enumerate(tmp):
      for x, dat in enumerate(row):
        if dat != 'e' and 0 <= int(dat) < colors:
          dat = int(dat)
          coord = bytearray([x,y])
          self.board.setTile(coord, dat)
          if self.start[dat] is None:
            self.start[dat] = coord
            self.head[dat] = coord
          elif self.end[dat] is None:
            self.end[dat] = coord
          else:
            raise Exception("Found 3rd instance of color: {}  --- Wat?".format(dat))
        elif dat == 'e':
          self.board.setTile([x,y], Board.EMPTY)

    self.board.initMoveSet()

  #Desc: determines wich actions can be performed in this game state.
  #Returns: a list of 'Action' objects that represent valid changes to this
  # game state.
  def getAllActions(self):
    actions = []

    for color, cur in enumerate(self.head):
      if cur == self.end[color]:
        continue

      movesOnBoard = self.board.getValidMoves(cur)
      for move in movesOnBoard:
        if self.board.getTile(move) == Board.EMPTY or \
           (self.end[color] == move and cur != self.start[color]):
          act = (move, color)
          actions.append(act)

    return actions

  #Determines if the current state is a goal state
  def gameOver(self):
    return self.head == self.end

  def allDists(self):
    dists = []
    for index in range(len(self.start)):
      dist = abs(self.head[index][0] - self.end[index][0]) +\
             abs(self.head[index][1] - self.end[index][1])

      if dist == 1 and self.head[index] == self.start[index]:
          dist = 3

      dists.append(dist)

    return dists


  def minDist(self):
    return min(self.allDists())

  def maxDist(self):
    return max(self.allDists())

  def sumDist(self):
    return sum(self.allDists())

  #Desc: Changes the game state to reflect the action given.
  #Param: action - a tuple (coord, color)
  #Pre: self.board must be set as a 'Board' object. 
  #     The Action object should be a valid action in the current state.
  def perform(self, action):
    self.head[action[1]] = action[0]
    self.board.setTile(action[0], action[1])

#Jacob Drilling
#CS5400 - Intro to AI
#Implements the game "ColorConnect"

import sys
import heapq

def manDist(p1, p2):
  return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

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
      self.curCosts = []

      if path:
        self.loadFromFile(path)

      self.curCosts = self.allDists()

    elif copy is not None:
      #Changed to a shallow copy because the starts don't change
      self.start = copy.start
      self.head = list(copy.head) 
      #Changed to a shallow copy because the end doesn't change
      self.end = copy.end
      self.board = Board(copy=copy.board)
      self.curCosts = copy.curCosts[:]

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
        if self.board.getTile(move) == Board.EMPTY or self.end[color] == move:
          act = (move, color)
          actions.append(act)

    return actions

  #Determines if the current state is a goal state
  def gameOver(self):
    return self.head == self.end


  # Astar-Ception
  # Calculates and returns the actual minimum path cost between the head 
  # and the end, using AStar.
  # Returns: the path cost if a path is found,
  #          4*manDist(head, end) if no path is found for pathcost < 2*manDist(head,end)
  #          999999 if no path is found
  def minPath(self, color):
    from SearchTree import Node
    start = self.head[color]
    end = self.end[color]

    states = 1
    frontierHeap = []
    frontierSet = set()
    exploredSet = set()

    root = Node(self.board, start, None, 0)

    heapq.heappush(frontierHeap, (manDist(start,end), states, root))
    frontierSet.add(root)

    while len(frontierHeap) > 0:
      priority, trash, node = heapq.heappop(frontierHeap)

      frontierSet.remove(node)
      exploredSet.add(node)

      if node.action == end:
        return node.cost
      elif node.cost >= 2*manDist(node.action, end):
        return 2*node.cost

      moves = node.state.getValidMoves(node.action)
      for move in moves:
        if node.state.getTile(move) == Board.EMPTY or end == move:
          newBoard = Board(copy=node.state)
          newBoard.setTile(move, color)
          newNode = Node(newBoard, move, node, node.cost + 1)

          if (newNode not in exploredSet and newNode not in frontierSet) or move == end:
            states += 1
            fn = newNode.cost + manDist(move, end)
            heapq.heappush(frontierHeap, (fn, states, newNode))
            frontierSet.add(newNode)

    return 999999
     
  # Calculates all the minPaths between colors and the end.
  # Returns:   a list of the minPaths.
  def allPaths(self):
    paths = []
    for color in range(len(self.start)):
      cost = self.minPath(color)
      paths.append(cost)
    return paths

  # Gets all manhattan distances from the current head to the end.
  # Returns:  a list of all manDist(head,end)
  def allDists(self):
    dists = []
    for index in range(len(self.start)):
      dist = manDist(self.head[index], self.end[index])
      dists.append(dist)

    return dists

  #Desc: Changes the game state to reflect the action given.
  #Param: action - a tuple (coord, color)
  #Pre: self.board must be set as a 'Board' object. 
  #     The Action object should be a valid action in the current state.
  def perform(self, action):
    self.head[action[1]] = action[0]
    self.board.setTile(action[0], action[1])

    self.curCosts[action[1]] = manDist(action[0], self.end[action[1]])

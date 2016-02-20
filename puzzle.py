#Author: Jacob Drilling
#Desc: Entry point for cs5400 puzzle assignment

import sys
import ColorConnect
import datetime
import re
import random
import heapq
from SearchTree import Node
from collections import deque, OrderedDict



#Desc: Searches a tree of ColorConnect using a breadth first search.
#Params: game - ColorConnect.Game object the the BFTS algorithm will solve
#Returns: The Last node in the solution.
def BFTS_Solve(game):
  root = Node(game)
  #Nodes to explore
  frontier = deque([root])

  states = 1
  duplicates = 0
  maxCost = 0

  #Search the frontier until we run out of nodes to explore
  while len(frontier) > 0:
    curNode = frontier.popleft()
    newActions = curNode.state.getAllActions()
    #Search through each action we can perform with the current nodes state
    for action in newActions:
      newState = ColorConnect.Game(copy=curNode.state)
      newState.perform(action)

      if newState.gameOver():
        #Debugging.
        print("Found! Searched through {} states.".format(states))
        print("\t{} are left in the frontier.".format(len(frontier)))
        return Node(newState, action, curNode, curNode.cost + 1)
      else:
        states += 1

      newNode = Node(newState, action, curNode, curNode.cost + 1)
      frontier.append(newNode)

    curNode.state = None
    
    #Debugging.
    if curNode.cost > maxCost:
      maxCost = curNode.cost
      print("Cur Depth: {}".format(maxCost))
    
  print("No solution found! Searched through {} states...".format(states))
  return None   

# Desc:     Solves the game with a depth first search. This version is not recursive
# Params:   game - a ColorConnect.Game object that has been initialized
#           it - Iterative depth. If it is None, then it will search until a 
#               solution is found or all states are searched
# Returns:  None if no solution is found,
#           A Node object if a solution is found
def DFTS_Solve(game, it=None):
  root = Node(game)
  frontier = deque([root])
  states = 1
  curDepth = 0

  # If for some reason the root is the goal.
  if root.state.gameOver():
    return root

  while len(frontier) > 0:
    curNode = frontier.pop()
    if it is not None and curNode.cost >= it:
      continue

    # Get all possible moves we can make from the curNodes state
    newActions = curNode.state.getAllActions()
    # random.shuffle(newActions)
    for action in newActions:
      # Generates a new Game object
      newState = ColorConnect.Game(copy=curNode.state)
      newState.perform(action)

      # Checks all states before putting them in the front
      if newState.gameOver():
        #Debugging.
        print("Found! Searched through {} states.".format(states))
        print("\t{} are left in the frontier stack.".format(len(frontier)))
        return Node(newState, action, curNode, curNode.cost + 1)
      else:
        states += 1

      # Add generated node to the frontier
      newNode = Node(newState, action, curNode, curNode.cost + 1)
      frontier.append(newNode)

  print("No solution found for depth of {}! Searched through {} states...".format(it, states))
  return None


# Desc: Uses DFTS with iterative Deepening to solve the game object
# Params: game - an initialized game object
# Returns: a Node object, representing the solution if one is found
#          None, if no solution is found before depth 10000
def IterDepth(game):
  it = 0

  sol = DFTS_Solve(game, it)
  while sol is None:
    it += 1
    sol = DFTS_Solve(game, it)
    if it > 10000:
      print("We got to a depth of 100 using Iterative Deepening.")
      print("\tWhile impressive that we could go that deep, something is wrong.")
      break

  return sol

# Desc: Best first solver uses a heuristic (the distance from each point to 
#       Their goal, to determine which move to make.
# Params: game - ColorConnect.Game object - initialized
#         GraphSearch - True enables graph search, false is enables tree search
#         astar - true enables astar search, otherwise it's graph search
# Returns: a Node object that represents the goal node.
#          or None if no goal is found
def BestFirst_Solve(game, graphSearch = True, astar = False):
  root = Node(game)
  explored = set()

  # I use two datastructures for my frontier pfifo. A Set for O(1) lookup, and
  # a heap for O(1) pops and O(lg(n)) insertions. Then no sorting is necessary.
  frontierSet = set()
  frontierHeap = []

  states = 1
  evaled = 0
  curF = sum(root.state.curCosts)
  unSolved = len(root.state.curCosts) - root.state.curCosts.count(0)
  minCost = min(root.state.curCosts)

  # Init both frontier data structures...
  heapq.heappush(frontierHeap, (curF, unSolved, minCost, states, root))
  frontierSet.add(root)

  while len(frontierHeap) > 0:
    priority, unSolved, minCost, stateNum, curNode = heapq.heappop(frontierHeap)
    evaled += 1

    # Large Debug Print
    # curNode.state.board.printB()
    # print("")
    
    if graphSearch:
      frontierSet.remove(curNode)
  
    # Add the node hash to the explored set, which is ignored if not graphsearch.
    explored.add(hash(curNode))

    if curNode.state.gameOver():
      print("Found! Searched through {} states.".format(evaled))
      print("\t{} states were generated.".format(states))
      print("\t{} are left in the frontier.".format(len(frontierHeap)))
      return curNode

    # Gets all the actions for the current game state, and create the nodes
    # for the resulting states.
    newActions = curNode.state.getAllActions()
    for action in newActions:
      newState = ColorConnect.Game(copy=curNode.state)
      newState.perform(action)
      newNode = Node(newState, action, curNode, curNode.cost + 1)

      # Here we select which heuristic we will use.
      # unSolved, is placed 2nd in the tuple used in the heap and is
      # therefore element considered for ordering in the pfifo if Fn is equal
      # for two nodes.
      # If the first two are equal, minCost is considered, which is the minimum
      # nonzero cost to a goal.
      if astar:
        # Gets all manhattan distances.
        pathCosts = newNode.state.allPaths()
        nonZero = [x for x in pathCosts if x != 0]
        Fn = newNode.cost + sum(nonZero)
        unSolved = len(nonZero)
        if len(nonZero) > 0:
          minCost = min(nonZero)
        else:
          minCost = 0
      # If we're not using AStar, we just set secondary Sorts to constants
      # so the heap defaults to the fourth element in the tuple, which is when
      # the node was created. I.E. for equal Fn's, the algorithem will chose
      # the node that was created first.
      else:
        Fn = sum(newNode.state.curCosts)
        minCost = unSolved = 0

      # Options for graph search and tree search.
      if graphSearch:
        if newNode not in frontierSet and hash(newNode) not in explored:
          states += 1 
          frontierSet.add(newNode)
          heapq.heappush(frontierHeap, (Fn, unSolved, minCost, states, newNode))
      else:
        states += 1 
        heapq.heappush(frontierHeap, (Fn, unSolved, minCost, states, newNode))

    # Don't need the game object after it has been evaluated, so let gc take it.
    curNode.state = None
    curNode.cost = None

  print("No solution found! Searched through {} states...".format(states))
  return None



if __name__ == "__main__":
  if len(sys.argv) > 1:
    filePath = sys.argv[1]
  else:
    raise Exception("Must provide an input file path.\n puzzle.py <Puzzle Path>")

  # Arg[2] chooses algorithm to use
  if len(sys.argv) > 2:
    algo = sys.argv[2]
  else:
    algo = "asgs"

  try:
    game = ColorConnect.Game(filePath)
  except err:
    print(err)
    sys.exit()

  #Debugging
  '''
  print("Color starting spaces are: {}".format(game.start))
  print("Color heads are at: {}".format(game.head))
  print("Color ending spaces are: {}".format(game.end))
  '''

  start = datetime.datetime.now()

  # depthfist - iterative deepening
  if algo.lower() == "dfts":
    sol = IterDepth(game)
  # breadth first tree
  elif algo.lower() == "bfts":
    sol = BFTS_Solve(game)
  # A* tree search
  elif algo.lower() == "asts":
    sol = BestFirst_Solve(game, graphSearch=False, astar=True)
  # greedy Best first tree
  elif algo.lower() == "gbfts":
    sol = BestFirst_Solve(game, graphSearch=False, astar=False)
  # greedy Best first graph
  elif algo.lower() == "gbfgs":
    sol = BestFirst_Solve(game, graphSearch=True, astar=False)
  # A* graph search
  else:
    sol = BestFirst_Solve(game, graphSearch=True, astar=True)

  end = datetime.datetime.now()
  delta = end - start
  msSpent = (delta.seconds) * 1000000 + delta.microseconds

  #Since we have the solution node and references to to parents
  #Climb back up the tree pushing each node for the solution onto a stack
  if sol is not None:
    solStack = []
    cur = sol
    while cur.parent is not None:
      solStack.append(cur.action)
      cur = cur.parent
  else:
    raise Exception("No solution found! Exiting.")


  #Outputs the solution in the specified format
  try:
    # Nice little regex to append the file with "_sol.txt"
    outPath = re.sub(r'\.(.)+$',"_sol.txt",filePath)
    print("Solution outputted to: {}".format(outPath))
    f = open(outPath, "w+")
    f.write(str(msSpent))
    f.write('\n')
    f.write(str(len(solStack)))
    f.write('\n')
    while len(solStack) > 0:
      action = solStack.pop()
      f.write("{} {} {}".format(action[1], action[0][0], action[0][1]))
      if len(solStack) != 0:
        f.write(',')
    f.write('\n')

    for i, ele in enumerate(sol.state.board.area):
      if i % sol.state.board.dim == 0 and i != 0:
        f.write('\n')
      if ele == ColorConnect.Board.EMPTY:
        f.write("e ")
      else:
        f.write(str(ele) + " ")
    f.close()
  except IOError:
    print("Could not open solution file")

  sol.state.board.printB()

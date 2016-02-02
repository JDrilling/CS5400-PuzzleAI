#Author: Jacob Drilling
#Desc: Entry point for cs5400 puzzle assignment

import sys
import ColorConnect
import datetime
import re
from SearchTree import Node
from collections import deque


#Desc: Searches a tree of ColorConnect using a breadth first search.
#Params: game - ColorConnect.Game object the the BFTS algorithm will solve
#Returns: The Last node in the solution.
def BFTS_Solve(game):
  root = Node(game)
  #Nodes to explore
  frontier = deque([root])

  states = 0
  duplicates = 0
  maxCost = 0

  #Search the frontier until we run out of nodes to explore
  while len(frontier) > 0:
    states += 1
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

      newNode = Node(newState, action, curNode, curNode.cost + 1)
      frontier.append(newNode)

    curNode.state = None
    
    #Debugging.
    if curNode.cost > maxCost:
      maxCost = curNode.cost
      print("Cur Depth: {}".format(maxCost))
    
  print("No solution found! Searched through {} states...".format(len(visited)))
  return None   


if __name__ == "__main__":
  if len(sys.argv) > 1:
    filePath = sys.argv[1]
  else:
    raise Exception("Must provide an input file path.\n puzzle.py <Puzzle Path>")

  game = ColorConnect.Game(filePath)

  #Debugging
  print("Color starting spaces are: {}".format(game.start))
  print("Color heads are at: {}".format(game.head))
  print("Color ending spaces are: {}".format(game.end))

  start = datetime.datetime.now()
  sol = BFTS_Solve(game)
  end = datetime.datetime.now()
  delta = end - start
  msSpent = (delta.seconds) * 1000000 + delta.microseconds

  #Since we have the solution node and references to to parents
  #Climb back up the tree pushing each node for the solution onto a stack
  if sol:
    solStack = []
    cur = sol
    while cur.parent is not None:
      solStack.append(cur.action)
      cur = cur.parent
  else:
    print("No solution found! :(")

  #Outputs the solution in the specified format
  try:
    outPath = re.sub(r'\.(.)+$',"_sol.txt",filePath)
    print("Solution outputted to: {}".format(outPath))
    f = open(outPath, "w+")
    f.write(str(msSpent))
    f.write('\n')
    f.write(str(len(solStack)))
    f.write('\n')
    while len(solStack) > 0:
      action = solStack.pop()
      f.write("{} {} {}".format(action.color, action.coord[0], action.coord[1]))
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

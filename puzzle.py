#Author: Jacob Drilling
#Desc: Entry point for cs5400 puzzle assignment

import sys
import ColorConnect
from SearchTree import SearchTree, Node
from collections import deque
from copy import deepcopy
    

def depthFirstSolve(game):
  root = Node(game)

  frontier = deque([root])

  while len(frontier) > 0:
    curNode = frontier.popleft()
    if curNode.state.gameOver():
      return curNode
    else:
      newActions = curNode.state.getAllActions()
      for action in newActions:
        newState = curNode.state.copy()
        newState.perform(action)
        newNode = Node(newState, action, curNode, curNode.cost + 1)
        frontier.append(newNode)

  return None   


if __name__ == "__main__":
  if len(sys.argv) > 1:
    filePath = sys.argv[1]
  else:
    raise Exception("Must provide an input file path.\n puzzle.py <Puzzle Path>")

  game = ColorConnect.Game(filePath)

  
  sol = depthFirstSolve(game)

  #Debugging
  print(game.start)
  print(game.end)
  print("Sol: {}\t Parent: {}".format(sol, sol.parent))


  #Temp Solution
  if sol:
    cur = sol
    while cur.parent is not None:
      print("Color: {}\t {}".format(cur.action.color, cur.action.coord))
      cur = cur.parent
  else:
    print("No solution found! :(")

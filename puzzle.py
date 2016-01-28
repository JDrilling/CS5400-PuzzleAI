#Author: Jacob Drilling
#Desc: Entry point for cs5400 puzzle assignment

import sys
import ColorConnect
import datetime
from SearchTree import SearchTree, Node
from collections import deque

def breadthFirstSolve(game):
  root = Node(game)

  frontier = deque([root])
  explored = set()
  states = 0
  duplicates = 0

  while len(frontier) > 0:
    states += 1
    curNode = frontier.popleft()
    if curNode.state.gameOver():
      print("Found! Searched through {} states.".format(states))
      print("\tEncountered {} duplicates along the way.".format(duplicates))
      print("\t{} are left in the frontier.".format(len(frontier)))
      return curNode
    else:
      newActions = curNode.state.getAllActions()
      for action in newActions:
        newState = curNode.state.copy()
        newState.perform(action)
        if newState in explored:
          continue
        else:
          explored.add(newState)
          newNode = Node(newState, action, curNode, curNode.cost + 1)
          frontier.append(newNode)
    
  print("No solution found! Searched through {} states...".format(len(visited)))
  return None   


if __name__ == "__main__":
  if len(sys.argv) > 1:
    filePath = sys.argv[1]
  else:
    raise Exception("Must provide an input file path.\n puzzle.py <Puzzle Path>")

  game = ColorConnect.Game(filePath)

  start = datetime.datetime.now()
  sol = breadthFirstSolve(game)
  end = datetime.datetime.now()
  msSpent = end - start
  msSpent = msSpent.microseconds

  #Debugging
  print("Color starting spaces are: {}".format(game.start))
  print("Color ending spaces are: {}".format(game.end))

  '''
  #Temp Solution
  if sol:
    cur = sol
    while cur.parent is not None:
      print("Color: {}\t {}".format(cur.action.color, cur.action.coord))
      cur = cur.parent
  else:
    print("No solution found! :(")


  '''
  if sol:
    solStack = []
    cur = sol
    while cur.parent is not None:
      solStack.append(cur.action)
      cur = cur.parent
  else:
    print("No solution found! :(")

  try:
    outPath = "{}.sol".format(filePath.rstrip(".txt"))
    print(outPath)
    f = open(outPath, "w+")
    f.write(str(msSpent))
    f.write('\n')
    f.write(str(len(solStack)))
    f.write('\n')
    while len(solStack) > 0:
      action = solStack.pop()
      f.write("{} {} {}".format(action.color, action.coord[0], action.coord[1]))
      if len(solStack) != 0:
        f.write(",")
    f.write('\n')

    for line in sol.state.board:
      for dat in line:
        f.write(str(dat) + " ")
      f.write('\n')
    f.close()
  except IOError:
    print("Could not open solution file")


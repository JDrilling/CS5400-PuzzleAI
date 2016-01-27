class Node:
  def __init__(self, state, action = None, parent = None, cost = 0):
    self.state = state
    self.parent = parent
    self.action = action
    self.cost = cost

class SearchTree:
  def __init__(self, state):
    self.root = Node(state)

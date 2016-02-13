class Node:
  def __init__(self, state, action = None, parent = None, cost = 0):
    self.state = state
    self.parent = parent
    self.action = action
    self.cost = cost

  def __eq__(self, other):
    return self.state == other.state

  def __hash__(self):
      return hash(self.state)


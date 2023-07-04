from captureAgents import CaptureAgent
import distanceCalculator
import random, time, util, sys
from game import Directions
import game
from util import nearestPoint

FIRST = 'Agent_A'
SECOND = 'Agent_D'

DEBUG = False

def createTeam(firstIndex, secondIndex, isRed, first=FIRST, second=SECOND):
  return [eval(first)(firstIndex), eval(second)(secondIndex)]
class ReflexCaptureAgent(CaptureAgent):
  def registerInitialState(self, gameState):
    self.start = gameState.getAgentPosition(self.index)
    CaptureAgent.registerInitialState(self, gameState)

  def chooseAction(self, gameState):
    actions = gameState.getLegalActions(self.index)
    values = [self.evaluate(gameState, a) for a in actions]

    maxValue = max(values)
    bestActions = [a for a, v in zip(actions, values) if v == maxValue]

    foodLeft = len(self.getFood(gameState).asList())

    if foodLeft <= 2:
      bestDist = 9999
      for action in actions:
        successor = self.getSuccessor(gameState, action)
        pos2 = successor.getAgentPosition(self.index)
        dist = self.getMazeDistance(self.start,pos2)
        if dist < bestDist:
          bestAction = action
          bestDist = dist
      return bestAction

    return random.choice(bestActions)

  def getSuccessor(self, gameState, action):
    successor = gameState.generateSuccessor(self.index, action)
    pos = successor.getAgentState(self.index).getPosition()
    if pos != nearestPoint(pos):
      return successor.generateSuccessor(self.index, action)
    else:
      return successor

  def evaluate(self, gameState, action):
    features = self.getFeatures(gameState, action)
    weights = self.getWeights(gameState, action)
    return features * weights

  def getFeatures(self, gameState, action):
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)
    features['successorScore'] = self.getScore(successor)
    return features

  def getWeights(self, gameState, action):
    return {'successorScore': 1.0}

class Agent_A(ReflexCaptureAgent):  
  def gotoTarget(self, gameState, target):
    walls = gameState.getWalls()
    pos = gameState.getAgentPosition(self.index)
    actions =  breathFirstSearch(pos, walls, lambda x, y: (x, y) == target)
    return 'Stop' if actions[0] == None else actions[0]
  
  def getHomeTarget(self, gameState):
    pos = gameState.getAgentPosition(self.index)
    width = gameState.data.layout.width
    height = gameState.data.layout.height
    nx =  width // 2 - 1 if self.red else width // 2

    minDist = float("inf")
    minIndex = (0,0)
    for ny in range(1, height-1):
      if not gameState.data.layout.isWall((nx, ny)):
        if minDist > self.getMazeDistance(pos, (nx, ny)):
          minDist = self.getMazeDistance(pos, (nx, ny))
          minIndex = (nx, ny)
    return minIndex
  ##
  def getFeatures(self, gameState, action):
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)
    foodList = self.getFood(successor).asList()    
    features['successorScore'] = -len(foodList)

    agentState = gameState.getAgentState(self.index)
    numRetured = agentState.numReturned
    scaredTimer = agentState.scaredTimer
    myPos = agentState.getPosition()
    
    if len(foodList) > 0:
      myPos = successor.getAgentState(self.index).getPosition()
      minDistance = min([self.getMazeDistance(myPos, food) for food in foodList])
      features['distanceToFood'] = minDistance

    enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
    invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]



    features['GhostDist'] = 0
    features['dontgothere'] = 0
    if len(enemies) > 0:
      ghosts = [a.getPosition() for a in enemies if a.scaredTimer == 0]
      if len(ghosts) > 0:
        minGhostDist = min([self.getMazeDistance(myPos, g) for g in ghosts])
        if minGhostDist < 4:
          features['GhostDist'] = minGhostDist*0.5
        else: features['GhostDist'] = minGhostDist

        if myPos in ghosts:
          features['dontgothere'] = -9999

    capsules = self.getCapsules(gameState)
    features['CapsuleDist'] = 0
    if len(capsules) > 0:
      if myPos in capsules:
        if DEBUG: print("Yes")
        features['CapsuleDist'] = -999
      else:
          minCapsuleDist = min([self.getMazeDistance(myPos, capsule) for capsule in capsules])
          if minCapsuleDist < 3:
            features['CapsuleDist'] = minCapsuleDist
          features['CapsuleDist'] = minCapsuleDist*2
    
    if action == Directions.STOP: features['stop'] = 1
    return features
  def getWeights(self, gameState, action):
    return {'successorScore': 100, 'distanceToFood': -1,
            'stop':-100,
            'GhostDist':1,
            'CapsuleDist':-10,
            'dontgothere':1}
  
  def chooseAction(self, gameState):
    numCarrying = gameState.getAgentState(self.index).numCarrying

    carry = 2 if self.getScore(gameState)>2 else 1
    if numCarrying < carry:
      actions = gameState.getLegalActions(self.index)

      values = [self.evaluate(gameState, a) for a in actions]
      maxValue = max(values)
      bestActions = [a for a, v in zip(actions, values) if v == maxValue]
      foodLeft = len(self.getFood(gameState).asList())

      if foodLeft <= 2:
        bestDist = 9999
        for action in actions:
          successor = self.getSuccessor(gameState, action)
          pos2 = successor.getAgentPosition(self.index)
          dist = self.getMazeDistance(self.start,pos2)
          if dist < bestDist:
            bestAction = action
            bestDist = dist
        return bestAction
      
      if DEBUG: print(values, actions)
      return random.choice(bestActions)
    else:
      self.target = self.getHomeTarget(gameState)
      action = self.gotoTarget(gameState, self.target)
      return action
    
  
class Agent_D(ReflexCaptureAgent):
    def getInvaders(self, gameState):
      enemies = [gameState.getAgentState(i) for i in self.getOpponents(gameState)]
      invaders = [e.getPosition() for e in enemies if e.isPacman and e.getPosition() != None]
      return invaders

    def getTarget(self, gameState):
      enemies = [gameState.getAgentState(i) for i in self.getOpponents(gameState)]
      enemyPositions = [e.getPosition() for e in enemies if e.getPosition() != None]
      defending = self.getFoodYouAreDefending(gameState).asList()

      target = None
      minPath = [None]*1000
      for enemy in enemyPositions:
          enemyPath = breathFirstSearch(enemy, gameState.getWalls(), lambda x, y: (x, y) in defending)
          if len(enemyPath) < len(minPath):
              minPath = enemyPath
              target = pathToPosition(enemy, enemyPath)
      return target
    
    def gotoInvader(self, gameState, invaders):
      walls = gameState.getWalls()
      pos = gameState.getAgentPosition(self.index)
      actions = breathFirstSearch(pos, walls, lambda x, y: (x, y) in invaders)
      return 'Stop' if actions[0] == None else actions[0]
    
    def gotoTarget(self, gameState, target):
      position = gameState.getAgentPosition(self.index)
      actions =  breathFirstSearch(position, gameState.getWalls(), lambda x, y: (x, y) == target)
      return 'Stop' if actions[0] == None else actions[0]

    def chooseAction(self, gameState):
      invaders = self.getInvaders(gameState)
      if invaders:
          action = self.gotoInvader(gameState, invaders)
          return action
      else: 
        self.target = self.getTarget(gameState)
        action = self.gotoTarget(gameState, self.target)
        return action
      
def breathFirstSearch(pos, walls, goalTest):
    fringe = util.Queue()
    fringe.push((pos, []))
    visited = []

    while not fringe.isEmpty():
        state, actions = fringe.pop()
        if goalTest(state[0], state[1]):
            if actions == []: actions = ['Stop']
            return actions
        if not state in visited:
            visited.append(state)
            neighbors = game.Actions.getLegalNeighbors(state, walls)
            for x, y in neighbors:
                dx, dy = x - state[0], y - state[1]
                action = game.Actions.vectorToDirection((dx, dy))
                fringe.push(((x, y), actions + [action]))
    return [None]
    

def pathToPosition(position, actions):
  for action in actions:
      dx, dy = game.Actions.directionToVector(action)
      position = (position[0] + dx, position[1] + dy)
  return position
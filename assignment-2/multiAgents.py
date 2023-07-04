from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    def getAction(self, gameState):
        legalMoves = gameState.getLegalActions()

        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        score = 0
        if action == 'Stop': 
            score -= 10

        scared = newScaredTimes[0] > 0 
        foods = newFood.asList()
        closestGhostDist, closestFoodDist = 9999, 9999

        for G in newGhostStates:
            newGhostPos = G.getPosition()
            newGhostDir = G.getDirection()
            closestGhostDist = min(closestGhostDist, manhattanDistance(newGhostPos, newPos))

        if 0<=closestGhostDist<=2:
            score -= 100

        if successorGameState.isWin():
            return 99999
        
        for food in foods:
            closestFoodDist = min(closestFoodDist, manhattanDistance(food, newPos))
        if not scared:
            score += float(1/closestFoodDist+1) - float(1/closestGhostDist+1)
        else: score += float(1/closestFoodDist+1) + float(1/closestGhostDist+1)

        return successorGameState.getScore() + score


def scoreEvaluationFunction(currentGameState):
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    def getAction(self, gameState):
        maxValue = float("-inf")

        maxAction = Directions.STOP
        for action in gameState.getLegalActions(0):
            nextState = gameState.generateSuccessor(0, action)
            nextValue = self.getValue(nextState, 0, 1)
            if nextValue > maxValue:
                maxValue = nextValue
                maxAction = action
        return maxAction

    def getValue(self, gameState, currentDepth, agentIndex):

        if agentIndex == gameState.getNumAgents():
            currentDepth+=1
            agentIndex=0

        if currentDepth == self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        
        elif agentIndex == 0:
            return self.maxValue(gameState,currentDepth, agentIndex)
        else:
            return self.minValue(gameState,currentDepth,agentIndex)

    def maxValue(self, gameState, currentDepth, agentIndex):
        maxValue = float("-inf")
        for action in gameState.getLegalActions(0):
            nextState = gameState.generateSuccessor(0, action)
            maxValue = max(maxValue, self.getValue(nextState, currentDepth, agentIndex+1))
        return maxValue

    def minValue(self, gameState, currentDepth, agentIndex):
        minValue = float("inf")
        for action in gameState.getLegalActions(agentIndex):
            nextState = gameState.generateSuccessor(agentIndex, action)
            minValue = min(minValue, self.getValue(nextState, currentDepth, agentIndex+1))
        return minValue
                
class ScoreAction: # 점수와 액션을 함께 계속 전달하기 위한 클래스 정의
    def __init__(self, score, action):
        self.score = score
        self.action = action


class AlphaBetaAgent(MultiAgentSearchAgent):
    def getAction(self, gameState):
        return self.getValue(gameState, 0, 0, float('-inf'), float('inf') ).action

    def getValue(self, gameState, currentDepth, agentIndex,  Valpha, Vbeta):

        if agentIndex == gameState.getNumAgents():
            currentDepth+=1; agentIndex=0

        if currentDepth == self.depth or gameState.isWin() or gameState.isLose():
            return ScoreAction(self.evaluationFunction(gameState), Directions.STOP)
        
        elif agentIndex == 0: # pacman's turn
            return self.maximizer(gameState, currentDepth, agentIndex, Valpha, Vbeta)
        else:
            return self.minValue(gameState, currentDepth, agentIndex, Valpha, Vbeta)
        
    def maximizer(self, state, depth, agentId, alpha, beta):
        Action = Directions.STOP
        maxValue = float("-inf") # initial value for maximizer

        for action in state.getLegalActions(0):
            nextState = state.generateSuccessor(0, action)
            
            newScoreAction = self.getValue(nextState, depth, 1, alpha, beta)
            if newScoreAction.score > maxValue:
                maxValue, Action = newScoreAction.score, action
            alpha = max(alpha, maxValue)
            if alpha>beta: return ScoreAction(maxValue, Action)
        return ScoreAction(maxValue, Action)
        
    def minValue(self, state, depth, agentId, alpha, beta): # only beta changes
        minValue = float("inf")
        Action = Directions.STOP

        for action in state.getLegalActions(agentId):
            nextState = state.generateSuccessor(agentId, action)

            newScoreAction = self.getValue(nextState, depth, agentId+1, alpha, beta)
            if newScoreAction.score < minValue:
                minValue, Action = newScoreAction.score, action
            beta = min(beta, minValue)
            if beta<alpha: return ScoreAction(minValue, Action)
        return ScoreAction(minValue, Action)

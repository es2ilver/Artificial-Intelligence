# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        "*** YOUR CODE HERE ***"

        # newGhostStates[0]를 print 하면, Ghost: (x,y)=(21.0, 1.0), South 이런식으로 반환한다.
        # getPosition, getDirection을 쓰면 된다ㅠㅠ!!

        # 팩맨이 멈추는 것을 막기 위해
        score = 0
        if action == 'Stop': 
            score -= 10

        scared = newScaredTimes[0] > 0 # 지금 고스트가 scared 상태인지 아닌지
        foods = newFood.asList()
        closestGhostDist, closestFoodDist = 9999, 9999

        for G in newGhostStates:
            newGhostPos = G.getPosition()
            newGhostDir = G.getDirection()
            closestGhostDist = min(closestGhostDist, manhattanDistance(newGhostPos, newPos))

        # 고스트와의 거리가 '매우 가까움'이면 못가도록 한다 ** 이때 Stop의 Vlaue보다 낮게되도록 하는게 좋은듯 죽을바엔 멈춰라! ㅠ
        if 0<=closestGhostDist<=2:
            score -= 100

        if successorGameState.isWin():
            return 99999
        
        for food in foods:
            closestFoodDist = min(closestFoodDist, manhattanDistance(food, newPos))
        if not scared:
            score += float(1/closestFoodDist+1) - float(1/closestGhostDist+1)
        else: score += float(1/closestFoodDist+1) + float(1/closestGhostDist+1)

        # 처음 idea: 고스트와의 거리는 멀수록, 음식과의 거리는 가까울수록 좋다.
        return successorGameState.getScore() + score


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """
    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

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
        # 한번 턴 돌때마다 다시 인덱스를 초기화하고, 깊이를 1 증가시킨다
        # 여기 주의해서 봐야 함 - grader 오답 뜬다 ㅠ

        if currentDepth == self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        
        elif agentIndex == 0: #pacman's turn
            return self.maxValue(gameState,currentDepth, agentIndex)
        else:
            return self.minValue(gameState,currentDepth,agentIndex)

    # 초기화 값이랑 함수만 다르다!
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
            # if agentIndex == gameState.getNumAgents()-1:
            #     minValue = min(minValue, self.getValue(nextState, currentDepth+1, 0))
            # else:minValue = min(minValue, self.getValue(nextState, currentDepth, agentIndex+1))
                
       

# 점수랑 액션을 함께 계속 전달하기 위해서 클래스 새롭게 정의!! ㅠㅠ
class ScoreAction:
    def __init__(self, score, action):
        self.score = score
        self.action = action


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        ### 알파베타 가지치기의 경우에 첫 맥시마이저에서도 가지치기를 해야 한다!!!
        ### 그래서 오답 나는 거였음 ㅠㅠ 근데 액션을 어떻게 킵 해놓지..??;;
        ### 결국 액션을 리턴하려면 이거 다 다시 짜야 하는걸까 ... ㅋㅋ........

        return self.getValue(gameState, 0, 0, float('-inf'), float('inf') ).action

    def getValue(self, gameState, currentDepth, agentIndex,  Valpha, Vbeta):

        # depth, index 
        if agentIndex == gameState.getNumAgents():
            currentDepth+=1; agentIndex=0

        # means leaf node # return value
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
    
       # util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

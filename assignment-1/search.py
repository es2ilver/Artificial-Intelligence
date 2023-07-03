# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):

    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"

    visited = []
    path = []
    stack = util.Stack()

    start = problem.getStartState()
    stack.push((start, path))

    while not stack.isEmpty():
        state, actions = stack.pop()

        if state in visited:
            continue
        else:
            visited.append(state) # 방문 노드 관리 -> 방문했던 노드는 다시 방문하지 않음
        
        if problem.isGoalState(state): # goal state 도달
            return actions
        
        else:
            for successor, action, stepCost in problem.getSuccessors(state):
                if successor not in visited:
                    stack.push((successor, actions+[action]))

    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    
    # 스택 대신 큐
    visited = []
    path = []
    queue = util.Queue()

    start = problem.getStartState()
    queue.push((start, path))

    while not queue.isEmpty():
        state, actions = queue.pop()

        if state in visited:
            continue
        else:
            visited.append(state) # 방문 노드 관리 -> 방문했던 노드는 다시 방문하지 않음

        if problem.isGoalState(state): # goal state 도달
            return actions
        
        else:
            for successor, action, stepCost in problem.getSuccessors(state):
                if successor not in visited:
                    queue.push((successor, actions+[action]))

    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    visited = []
    fringe = util.PriorityQueue()
    fringe.push((problem.getStartState(), [], 0), 0)

    while not fringe.isEmpty():
        state, actions, costs = fringe.pop()

        if state in visited:
            continue
        else: 
            visited.append(state)

        if problem.isGoalState(state):
            return actions
        else: 
            for successor, action, stepCost in problem.getSuccessors(state):
                if successor not in visited:
                    newCost = costs + stepCost
                    fringe.update((successor, actions+[action], newCost), newCost)
            
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    visited = []
    fringe = util.PriorityQueue()
    start = problem.getStartState()

    fringe.push((start, [], 0), 0)

    while not fringe.isEmpty():
        state, actions, costs = fringe.pop()

        if state in visited:
            continue
        else: 
            visited.append(state)

        if problem.isGoalState(state):
            return actions
        else: 
            for successor, action, stepCost in problem.getSuccessors(state):
                if successor not in visited:
                    newCost = costs + stepCost
                    fringe.update((successor, actions+[action], newCost), newCost+heuristic(successor, problem))
                    # 헤멘 이유 - 휴리스틱은 우선순위 큐 넣을때 우선순위 결정하는 값으로만 넣어야 하는 거였음 ㅠㅠ
    

    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch

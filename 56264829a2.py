from queue import PriorityQueue
import sys
import numpy as np

goalState = ["0", "1", "2", "3", "4", "5", "6", "7", "8"]  #values of puzzle
abcdefghi = [["A", "B", "C"], ["D", "E", "F"], ["G", "H",
                                                "I"]]  #predefined 2d array
xAxis = [1, 0, -1, 0]
yAxis = [0, 1, 0, -1]
n = 3  #number of column
visitedNodes = set()

initState = [int(x) for x in str((sys.argv[1]))]
for i in range(len(initState)):
    initState[i] = int(initState[i])
initState = np.array(initState).reshape(n, n)

for i in range(len(goalState)):
    goalState[i] = int(goalState[i])
goalState = np.array(goalState).reshape(n, n)


def getSeq(n, m):
    return abcdefghi[n][m]


class Search:
    def __init__(this, initState, goalState):

        this.path = []
        this.initState = initState
        this.goalState = goalState

    def findPath(this):
        nodes = PriorityQueue(1000)

        rootNode = Puzzle(this.initState.flatten().tolist(),
                          this.goalState.flatten().tolist(),
                          0,
                          parent=None)
        nodes.put(rootNode)

        targetCell = this.goalState.shape[0]

        while nodes.qsize():

            currentNode = nodes.get()
            currentState = currentNode.getState()
            visitedNodes.add(str(currentState))

            if currentState == this.goalState.flatten().tolist():

                while currentNode.getParent():
                    this.path.append(currentNode)
                    currentNode = currentNode.getParent()
                break

            emptyLabel = currentState.index(0)
            i, j = (
                emptyLabel // targetCell,
                emptyLabel % targetCell,
            )
            currentState = np.array(currentState).reshape(
                targetCell, targetCell)
            for positionX, positionY in zip(xAxis, yAxis):
                newState = np.array(currentState)
                # h = newState[i, j]
                # g = newState[i + positionX, j + positionY]
                if (i + positionX >= 0 and i + positionX < targetCell
                        and j + positionY >= 0 and j + positionY < targetCell):
                    newState[i,
                             j], newState[i + positionX, j +
                                          positionY] = (newState[i + positionX,
                                                                 j +
                                                                 positionY],
                                                        newState[i, j])
                    # (h, g) = (g, h)
                    gameState = Puzzle(newState.flatten().tolist(),
                                       this.goalState.flatten().tolist(),
                                       currentNode.getLevel() + 1, currentNode)
                    if str(gameState.getState()) not in visitedNodes:
                        nodes.put(gameState)

        return this.path

    def aStar(initState, goalState):
        search = Search(initState, goalState)
        path = search.findPath()
        output = ""

        for node in reversed(path):
            currentIndex = node.getState().index(0)
            currentI, currentJ = currentIndex // goalState.shape[
                0], currentIndex % goalState.shape[0]
            output += getSeq(currentI, currentJ)
        print(output)


class Puzzle:
    def __init__(this, state, goalState, level, parent=None):
        this.heuristicScore = level
        this.parent = parent
        this.state = state
        this.goalState = goalState
        this.level = level
        this.value = int(np.sqrt(len(this.state)))

        this.calculateF()

    def getState(this):
        return this.state

    def getLevel(this):
        return this.level

    def getParent(this):
        return this.parent

    def calculateF(this):

        for currentLabel in this.state:
            currentIndex = this.state.index(currentLabel)
            goalIndex = this.goalState.index(currentLabel)
            currentX, currentY = (
                currentIndex // this.value,
                currentIndex % this.value,
            )
            goalX, goalY = goalIndex // this.value, goalIndex % this.value
            this.heuristicScore += this.calculateM(currentX, currentY, goalX,
                                                   goalY)

    def calculateM(this, x1, y1, x2, y2):
        return abs(x1 - x2) + abs(y1 - y2)

    def __gt__(this, other):
        return this.heuristicScore > other.heuristicScore

    def __lt__(this, other):
        return this.heuristicScore < other.heuristicScore

    def __eq__(this, other):
        return this.heuristicScore == other.heuristicScore


Search.aStar(initState, goalState)
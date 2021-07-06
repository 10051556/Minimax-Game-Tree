import sys
import math

totalMoves = int(sys.argv[1])
board = []
player1Hand = []
player2Hand = []
player1 = 0
player2 = 1
pile = [0, 1, 2, 3, 4, 5, 6, 7, 8]
playerMoves = []
depth = 0
isMax = False
for i in range(totalMoves):
    if i % 2 != 0:
        player2Hand.append(int(sys.argv[i+2]))
    if i % 2 == 0:
        player1Hand.append(int(sys.argv[i+2]))
    num = pile[i]
    board.append(int(sys.argv[i+2]))
    pile.remove(int(sys.argv[i+2]))
    
playerMoves.append(player1Hand)
playerMoves.append(player2Hand)


# determine player turn
if totalMoves % 2 == 0:
    currentplayer = player1
    opponent = player2
else:
    currentplayer = player2
    opponent = player1

# check if any selected 3 num of currentplayer sum as 14


def checkSum(playerHand):
    size = len(playerHand)
    for i in range(0, size-2):
        for j in range(i+1, size-1):
            for k in range(j+1, size):
                if(playerHand[i]+playerHand[j]+playerHand[k] == 14):
                    return True
    return False


def possibleNum(numbers, target, hand=[]):

    s = sum(hand)

    if s == target:
        if len(hand) == 3:
            print(hand)

    if s >= target:
        return

    for i in range(len(numbers)):
        n = numbers[i]
        remaining = numbers[i+1:]
        possibleNum(remaining, target, hand + [n])


possibleNum([0, 1, 2, 3, 4, 5, 6, 7, 8], 14)

# determine best num to select from pile

# the minimax
# evalute the value of currentplayer

def evaluateByDepth(score, depth):
    if score > 0:
        return score - depth
    else:
        return score + depth


def evaluate(currentplayer, depth):
    score = 20
    if currentplayer == 2:
        score = -20

    if checkSum(player1Hand):
        return evaluateByDepth(score, depth)
    if checkSum(player2Hand):
        return evaluateByDepth(-score, depth)
    return 0


def gameOver(board):

    if len(board) < 8:
        return True
    return False


def minimax(pile, player, depth, isMax):

    score = evaluate(playerMoves, depth)
    if(score != 0) and len(pile) == 0:
        return score

    if (isMax):
        best = -float('inf')
        for num in pile:
            playerMoves[player].append(num)
            pile.remove(num)
            best = max(best, minimax(pile,  (player+1) % 2,  depth+1, False))
            pile.append(num)
            playerMoves[player].remove(num)
        return best
    else:
        best = float('inf')
        for num in pile:
            playerMoves[player].append(num)
            pile.remove(num)
            best = min(best, minimax(pile,  (player+1) % 2,  depth+1, True))
            pile.append(num)
            playerMoves[player].remove(num)
        return best


def bestMove(player):

    bestScore = -float('inf')
    bestMove = -float('inf')

    for num in pile:
        playerMoves[player].append(num)
        pile.remove(num)
        score = minimax(pile, (player+1)%2, depth, False)

        pile.append(num)
        playerMoves[player].remove(num)
        if(bestScore < score):
            bestMove = num
            bestScore = score
    return bestMove


# output result

while totalMoves < 9:
    player = totalMoves%2
    move = bestMove(player)
    board.append(move)
    pile.remove(move)
    totalMoves += 1
    if evaluate(0,0) != 0:
        break

output = str(totalMoves)
for i in range(totalMoves):
    output = output+" "+str(board[i])
print(output)

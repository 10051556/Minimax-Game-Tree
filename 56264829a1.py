import sys

n = int(sys.argv[1])

number_taken = [0, 0, 0, 0, 0, 0, 0, 0, 0]

move = []
for i in range(n):
    move.append(int(sys.argv[i+2]))
    number_taken[move[i]] = 1


my_move = -1
for i in range(9):
    if (number_taken[i] == 0):
        my_move = i
        break

if (my_move >= 0):
    move.append(my_move)
    n = n + 1

output = str(n)
for i in range(n):
    output = output+" "+str(move[i])
print(output)


def checkWin(state):
    return

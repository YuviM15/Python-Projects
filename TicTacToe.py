def reset():
    count=0
    board=[]
    for i in range(3):
        board.append([])
        for j in range(3):
            count+=1
            board[i].append("_")
    return board
def printBoard(board):
    count=0
    for i in range(3):
        for j in range(3):
            print(board[i][j], end=" ")
        print('    ', count+1, count+2, count+3)
        count+=3
def checkHorizontal(board,player,lastMove):
    x,y=lastMove
    for i in range(3):
        if board[x][i] != player:
            return False
    return True
def checkVertical(board,player,lastMove):
    x,y=lastMove
    for i in range(3):
        if board[i][y] != player:
            return False
    return True
def checkLDiagonal(board,player):
    for i in range(3):
        if board[i][i]!=player:
            return False
    return True
def checkRDiagonal(board,player):
    for i in range(2,-1,-1):
        if board[2-i][i]!=player:
            return False
    return True
def isWon(board,player,lastMove):
    x= checkHorizontal(board,player,lastMove) or checkVertical(board,player,lastMove) or checkLDiagonal(board,player) or checkRDiagonal(board,player)
    if x:
        print("*"*16)
        print(player," wins")
        print("*" * 16)
    return x


while True:
    h={'1': (0,0), '2': (0,1), '3': (0,2), '4': (1,0), '5': (1,1), '6': (1,2), '7': (2,0), '8':(2,1), '9':(2,2)}
    board=reset()
    printBoard(board)
    player= 1
    print("X plays first")
    print("O plays second")
    p="X"
    seen = {}
    count=0
    while True :
        if player==1:
            p="X"
        else:
            p="O"
        inp=input(f"Player {p} enter your move: ")
        while 0>int(inp) or int(inp)>9 or inp in seen:
            inp = input(f"Player {p} Enter valid move: ")
        move = h[inp]
        seen[inp]=True
        x,y=move
        board[x][y]=p
        printBoard(board)
        count+=1
        if isWon(board,p,move):
            break
        if count==9:
            print("*"*16)
            print("Tie")
            print("*" * 16)
            break
        player^=1
    choice= input("Would you like to play again? (y/n): ")
    if choice == "n":
        break
    board=reset()
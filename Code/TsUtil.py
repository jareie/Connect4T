import random
import numpy as np

#Rearrange a list such that it is easier to work with
def Rearrange(WrongList):
	output = []
	for column in range(6):
		for row in range(7):
			#index = (6*i)+(6-j)
			temp = 6-column
			index = (6*row)+temp
			#print(index)
			output.append(WrongList[index-1])
	return output

def ReshapeData(GivenList,IsConvolutiional):
    output = []
    for i in GivenList:
        NewTrainXEntry = Rearrange(i[:42]) + Rearrange(i[42:])
        if IsConvolutiional:
            temp = np.reshape(NewTrainXEntry,(7,6,2))
            output.append(temp)
        else:
            output.append(NewTrainXEntry)
    return output

def ClausePiece(nonP1,nonP2,nP1,nP2):
    fail = (nonP1 and nP1) or (nonP2 and nP2)
    piece = ""
    if fail:
        piece = "f"
    elif nP1 and nP2:
        piece = "-"
    elif nonP1 and nonP2:
        piece = "*"
    elif nonP1:
        piece = "X"
    elif nP1:
        piece = "x"
    elif nonP2:
        piece = "O"
    elif nP2:
        piece = "o"
    else:
        piece = "_"
    return piece


#Generate a more readable clause
def ReadableClause(outClause):
    output = outClause

    nonNegated = output[:int(len(output)/2)]
    negated = output[int(len(output)/2):]
    
    tPlayer1 = nonNegated[:int(len(nonNegated)/2)]
    tPlayer2 = nonNegated[int(len(nonNegated)/2):]
    
    rPlayer1 = negated[:int(len(negated)/2)]
    rPlayer2 = negated[int(len(negated)/2):]

    board = []

    for column in range(6):
        board.append([])
        for row in range(7):
            tp1 = tPlayer1[(column*7)+row]
            tp2 = tPlayer2[(column*7)+row]
            rp1 = rPlayer1[(column*7)+row]
            rp2 = rPlayer2[(column*7)+row]

            board[column].append(ClausePiece(tp1,tp2,rp1,rp2))
    return board

#Create a more readable board
def Readable(board):
    player1 = board[:int(len(board)/2)]
    player2 = board[int(len(board)/2):]
    
    rBoard = []
    for column in range(6):
        rBoard.append([])
        for row in range(7):
            index = (column*7)+row
            #print(index)
            p1 = player1[index]
            p2 = player2[index]
            if p1 == 1:
                rBoard[column].append("X")
            elif p2 == 1:
                rBoard[column].append("O")
            else:
                rBoard[column].append(" ")

    return rBoard

#Evaluate a clause for a board
def IsClauseTrue(Clause,board):
    nonNegated = Clause[:int(len(Clause)/2)]
    negated = Clause[int(len(Clause)/2):]
    
    tPlayer1 = nonNegated[:int(len(nonNegated)/2)]
    tPlayer2 = nonNegated[int(len(nonNegated)/2):]
    
    rPlayer1 = negated[:int(len(negated)/2)]
    rPlayer2 = negated[int(len(negated)/2):]

    for i in range(len(tPlayer1)):
        if tPlayer1[i] == 1 and rPlayer1[i] == 1:
            return "invalid"
        if tPlayer2[i] == 1 and rPlayer2[i] == 1:
            return "invalid"

    BoardP1 = board[:int(len(board)/2)]
    BoardP2 = board[int(len(board)/2):]
    
    for i in range(len(BoardP1)):
        if tPlayer1[i] == 1 and BoardP1[i] == 0:
            return "False"
        if rPlayer1[i] == 1 and BoardP1[i] == 1:
            return "False"
    
    for i in range(len(BoardP2)):
        if tPlayer2[i] == 1 and BoardP2[i] == 0:
            return "False"
        if rPlayer2[i] == 1 and BoardP2[i] == 1:
            return "False"
    return "True"


#Generate Boards that is to be used for evaluating clauses

def TransformBoard(board):
    player1 = [0 for i in range(42)]
    player2 = [0 for i in range(42)]
    #print(board)
    for row in range(len(board)):
        for column in range(len(board[row])):
            index = row*6 + column
            #print(index)
            if board[row][column] == "X":   
                player1[index] = 1
            elif board[row][column] == "O":
                player2[index] = 1                
    bits = Rearrange(player1) + Rearrange(player2)
    return bits

def AltRandomBoard():
    board = [[],[],[],[],[],[],[]]
    placements = random.randint(0,41)
    
    def Placement():
        bplacement = random.randint(0,6)
        while len(board[bplacement]) > 5 :
            bplacement = random.randint(0,6)
        return bplacement

    for i in range(int(placements/2)):
        board[Placement()].append("X")
        board[Placement()].append("O")

    if placements%2 > 0:
        board[Placement()].append("X")

    return TransformBoard(board)


def RandomBoard():
    player1 = [0 for i in range(42)]
    player2 = [0 for i in range(42)]
    
    number = random.randint(14,84)
    player1bits = int(number/2)
    player2bits = int(number/2)
    
    if number % 2 > 0:
        player1bits = player1bits + 1
    
    for i in range(player1bits):
        placement = 0
        while True:
            placement = random.randint(0,6)
            if player1[(6*placement)+5] == 0:
                break
        
        cloumn = player1[6*placement:(6*placement)+5]
        index = -1
        for j in range(0,len(cloumn)):
            if cloumn[j] == 0:
                index = j
                break
        if index > -1:
            player1[(6*placement)+index] = 1
    
    for i in range(player2bits):
        placement = 0
        while True:
            placement = random.randint(0,6)
            if player2[(6*placement)+5] == 1:
                continue
            break
        
        cloumn = player2[6*placement:(6*placement)+5]
        index = -1
        for j in range(len(cloumn)):
            if cloumn[j] == 0:
                index = j
                break
        if index > -1:
            player2[(6*placement)+index] = 1
    
    return player1 + player2

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
    placements = random.randint(10,41)
    
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

def GetOutput(tm,tm_class,clause):
    output = []
    for i in range(84*2):
        outputbit = tm.ta_action(tm_class,clause,i)
        output.append(outputbit)
    return output

def GetClauses(Ts,Clas,clauses):
    output = []
    for i in range(clauses):
        clause = GetOutput(Ts,Clas,i)
        action = ReadableClause(clause)
        output.append(action)
    return output

def PrintClause(clause):
    for i in clause:
        print(i)

def PrintClass(clauses):
    for i in clauses:
        PrintClause(i)

#Sjekker en caluse mot ett brett
def CheckClause(clause,board):
    result = IsClauseTrue(clause,board)
    if result == "True":
        print("-----------")
        #print(result)
        bo = Readable(board)
        for j in bo:
            print(j)
    return result

#Sjekker en clause mot flere brett
def CheckClauses(clause,boards):
    for i in range(len(boards[0])):
        result = CheckClause(clause,boards[0][i])
        #print(claus)
        if result == "True":
            boardRes = boards[1][i]
            if boardRes == 0:
                print("Loss")
            elif boardRes == 1:
                print("Win")
            elif boardRes == 2:
                print("Draw")

def ClausesTestData(ts,testx,testy,clauses):
    clas = 1
    def sortByKey(inp):
        return inp[2]

    print("Getting Boards")
    boards = []
    wins = []
    loss = []
    for i in range(len(testx)):
        if testy[i] == 1:
            wins.append((testx[i],testy[i]))
        elif testy[i] == 0:
            loss.append((testx[i],testy[i]))
    boards = wins[:len(loss)] + loss


    print("Getting clauses")
    #Get Classes and create list/tuple with score
    TotalClausesWScore = []
    for i in range(clauses):
        claus = GetOutput(ts[0],clas,i)
        
        typeOfClause = "Non"
        if i%2 > 0:
            typeOfClause = "Negated"
            continue

        TotalClausesWScore.append([claus,typeOfClause,0])

    print("Comparing clauses and boards")
    for i in TotalClausesWScore:
        #PrintClause(TsUtil.ReadableClause(i[0]))
        for board in boards:
            evaluation = IsClauseTrue(i[0],board[0])
            
            if evaluation == "True":
                if board[1] == 1:
                    i[2] += 1
                else:
                    i[2] -= 1 
        #break
        #CheckClauses(claus,testing)
        #print("---------------------------------------------")
    
    TotalClausesWScore.sort(reverse=True,key=sortByKey)
    newlist = []
    for i in TotalClausesWScore:
        if True:
            newlist.append(i)

    
    templist = TotalClausesWScore[:3]
    for i in templist:
        clss = ReadableClause(i[0])
        for j in clss:
            print(j)
        print("-----------------------------")
        
def ClausesPattern(ts,clauses):
    clas = 1
    tpye = "o"

    TotalClausesWScore = []
    for i in range(clauses):
        claus = GetOutput(ts[0],clas,i)
        
        typeOfClause = "Non"
        if i%2 > 0:
            typeOfClause = "Negated"
            continue

        clss = ReadableClause(claus)
        val = False
        
        for row in range(len(clss)):
            for column in range(len(clss[row])):
                if clss[row][column] == tpye:
                    
                    if row < 4:
                        val = val or (clss[row+1][column] == tpye and clss[row+2][column] == tpye)
                    
                    if column < 3:
                        val = val or (clss[row][column+1] == tpye and clss[row][column+2] == tpye)
                        
                    if row < 4 and column < 3:
                        val = val or (clss[row+1][column+1] == tpye and clss[row+2][column+2] == tpye)
                        
                    if row > 2 and column < 3:
                        val = val or (clss[row-1][column+1] == tpye and clss[row-2][column+2] == tpye)
                    
        if val:
            TotalClausesWScore.append(claus)
    
    for i in TotalClausesWScore:
        clss = ReadableClause(i)
        for j in clss:
            print(j)
        print("-------------")


def Clauses(clauses,ts,T,s,epochs):
    def sortByKey(inp):
        return len(inp[2])

    def sortByBit(inp):
        result = 0
        
        for i in inp:
            result += i
            
        return result


    counter = -1
    clas = 1
    
    boards = []
    for i in range(1000):
        boards.append(AltRandomBoard())

    #boards = []
    #for i in range(len(TestX)):
    #    boards.append((TestX[i],TestY[i]))

 
    
    #Get Classes and create list/tuple with score
    TotalClausesWScore = []
    for i in range(clauses):
        claus = GetOutput(ts[0],clas,i)
        
        typeOfClause = "Non"
        if i%2 > 0:
            continue
            typeOfClause = "Negated"

        TotalClausesWScore.append([claus,typeOfClause,[]])


    #print(TsUtil.Rearrange([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42]))
    for claus in TotalClausesWScore:
        for board in boards:
            evaluation = IsClauseTrue(claus[0],board)
            if evaluation == "True":
                claus[2].append(board)
    
    #TotalClausesWScore.sort(key=sortByBit)
    
    ClausesDict = [[] for i in range(85)]
    for claus in TotalClausesWScore:
        bits = sortByBit(claus[0])
        ClausesDict[bits].append(claus)

    for i in ClausesDict:
        i.sort(key=sortByKey)
    
    Directory = "Clauses/" + "Clauses: " + str(clauses) + ", Threshold:" + str(T) + ", S: " + str(s) + ", Epochs: " + str(epochs)
    import os
    if not os.path.exists(Directory):
        os.makedirs(Directory)
    
    counter = 40
    for i in ClausesDict[counter:]:
        if len(i)>0:
            SubDirectory = "Bits: " + str(counter)
            
            if not os.path.exists(Directory + "/" + SubDirectory):
                os.makedirs(Directory + "/" + SubDirectory)
            
            for bdb in i:
                String = "Type of Clause: " + bdb[1] + ", Boards: " + str(len(bdb[2]))
                
                outFile = open(Directory + "/" + SubDirectory + "/" + String,"w")
                
                clss = ReadableClause(bdb[0])
                for row in clss:
                    stt = ""
                    for index in row:
                        stt += index + " "
                    stt = stt + "\n"
                    outFile.write(stt)
                outFile.write("===================\n")
                outFile.write("Boards: \n")
                outFile.write("===================\n")
                for sc in bdb[2]:
                    aBoard = Readable(sc)
                    for row in aBoard:
                        stt = ""
                        for index in row:
                            stt += index + " "
                        stt = stt + "\n"
                        outFile.write(stt)
                    outFile.write("-----------------\n")
                outFile.close()
        counter += 1
import random

def ConvertToInt(liste):
    product = []
    for i in liste:
        product.append(int(i))
    return product

def RandomIndexes(List,amount):
    indexes = []

    while len(indexes) < amount:
        temp = len(List)
        index = random.randint(0,temp-1)
        if index in indexes:
            continue
        indexes.append(index)

    indexes.sort(reverse=True)
    #print(indexes)
    
    return indexes

def RandomChoices2L(List1,List2,amount):
    indexes = RandomIndexes(List1,amount)
    tempX = []
    tempY = []
    for i in indexes:
        tempX.append(List1.pop(i))
        tempY.append(List2.pop(i))
    return (tempX,tempY)

def KFold(number,dataset):
    CategoryW = []
    CategoryL = []
    for i in dataset:
        if i[1] == 0:
            CategoryL.append(i)
        elif i[1] == 1:
            CategoryL.append(i)
    sets = []
    for i in range(number):
        index1 = int(len(CategoryL)/number)
        index2 = int(len(CategoryW)/number)
        testList = CategoryL[index1*i:index1*(i+1)] + CategoryW[index2*i:index2*(i+1)]
        trainList = CategoryL[:index1*i] + CategoryL[index1*i:] + CategoryW[:index2*i] + CategoryW[index2*i:]
        sets.append([trainList,testList])

    return sets

def LoadCfg(FileName):
    print("Getting Config File")
    config = open("Config.cfg","r")
    rawInfo = config.readlines()
    config.close()
    Info = {}
    category = []

    for i in rawInfo:
        temp = i.replace(" ","")
        temp = temp.replace("\n","")
        if temp == "":
            continue
        if temp[0] == "-":
            ctg = temp.replace("-","")
            category.append(ctg)
            Info[ctg] = {}
        else:
            inf = temp.split("=")
            if inf[1].find('"') < 0:
                try:
                    if inf[1] == "True":
                        inf[1] = True
                    elif inf[1] == "False":
                        inf[1] = False
                    else:
                        inf[1] = float(inf[1])
                except Exception:
                    print("Failed: " + inf[1])
            else:
                inf[1] = inf[1].replace('"',"")
            Info[category[len(category)-1]][inf[0]] = inf[1]
        #print(category)

    return Info

def LoadFile(FileName,IncludeDraw=False):
    print("Processing File: " + FileName)

    testInfo = open(FileName,"r")
    data = testInfo.readlines()
    testInfo.close()

    TestX = []
    TestY = []

    for i in data:
        temp = i.replace("\n","")
        temp = temp.split(",")
        
        tempList = ConvertToInt(temp[0:len(temp)-1])
        result = int(temp[len(temp)-1])
        if not IncludeDraw and result == 2:
            #print("Including draw")
            continue
        TestX.append(tempList)
        TestY.append(result)
    return (TestX,TestY)

def GenerateKFoldSet(FileName1,FileName2):
    file1 = LoadFile(FileName1)
    file2 = LoadFile(FileName2)
    dataX = file1[0] + file2[0]
    dataY = file1[1] + file2[1]
    data = []
    for i in range(len(dataX)):
        data.append((dataX[i],dataY[i]))
    return KFold(10,data)

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

def Readable(board):
    player1 = Rearrange(board[:int(len(board)/2)])
    player2 = Rearrange(board[int(len(board)/2):])
    
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
            #column = 0-5
            #row = 0-6
            #(column*7)+row
            #temp = 6-column
			#index = (6*row)+temp
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


bd = RandomBoard()
#print(len(bd))
Rearrange(bd[:42])
print("-------------------")
print(bd)
rad = Readable(bd)
for i in rad:
    print(i)
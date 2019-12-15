from pyTsetlinMachine.tm import MultiClassTsetlinMachine
import numpy as np
#import random
import TsUtil


variables = TsUtil.LoadCfg("Config.cfg")
dataPath = variables["General"]["DataPath"]
trainPl = variables["General"]["TrainingData"]
testPl = variables["General"]["TestingData"]

#print(variables)
#------------------------------------------------------------
print("Getting Data")

#training = TsUtil.LoadFile("trainingdata.txt")
#testing = TsUtil.LoadFile("testdata.txt")

training = TsUtil.LoadFile(dataPath + trainPl)
testing = TsUtil.LoadFile(dataPath + testPl)
print(str(len(training[0])) + " entries")    

def ReshapeData(GivenList):
    output = []
    for i in GivenList:
        NewTrainXEntry = TsUtil.Rearrange(i[:42]) + TsUtil.Rearrange(i[42:])
        output.append(NewTrainXEntry)
    return output

TrainX = np.array(ReshapeData(training[0]))
TrainY = np.array(training[1])

TestX = np.array(ReshapeData(testing[0]))
TestY = np.array(testing[1])

#------------------------------------------------------------
print("Setting Up Machine")
clauses = int(variables["Connect4"]["Clause"])
T = variables["Connect4"]["T"]
s = variables["Connect4"]["S"]

epochs = int(variables["Connect4"]["epochs"])

def MakeTestlin(Clauses,t,S,Epochs):
    tm = MultiClassTsetlinMachine(Clauses,t,S,boost_true_positive_feedback=0)
    #tm = MultiClassTsetlinMachine(100,10,4.45)
    #tm.fit(TrainX,TrainY,epochs=10)
    #print("Accuracy:", 100*(tm.predict(TestX) == TestY).mean())
    result = 0
    print("Training: Clauses=" + str(Clauses) + ", T=" + str(t)+ ", S=" + str(S))
    for i in range(Epochs):
        tm.fit(TrainX, TrainY, epochs=1, incremental=True)
        result = 100*(tm.predict(TestX) == TestY).mean()
        print("Accuracy: ", result)
    return (tm,result)

def CrossValidation():
    datasets = TsUtil.GenerateKFoldSet(dataPath + trainPl,dataPath + testPl)
    results = []
    for sets in datasets:
        print("Making Tsetlin Machine for new set")
        tm = MultiClassTsetlinMachine(clauses,T,s,boost_true_positive_feedback=0)
        result = 0.0
        TrainX = []
        TrainY = []
        for i in sets[0]:
            TrainX.append(i[0])
            TrainY.append(i[1])

        TestX = []
        TestY = []
        for i in sets[1]:
            TestX.append(i[0])
            TestY.append(i[1])
        
        for i in range(epochs):
            tm.fit(np.array(TrainX),np.array(TrainY),epochs=1,incremental=True)
            result = 100*(tm.predict(np.array(TestX)) == np.array(TestY)).mean()
            print(" " + str(result))
        results.append(result)
    return results
    

#------------------------------------------------------------
#print(MakeTestlin(10000,80,27,15))
#tm.ta_action(mc_tm_class, clause, ta)
#har 84 features ta = feature
#vil trenge aa gaa over hver feature for hver clause
#for eksempel 100,10,5 med 2 klasser og 84 input/features
#2 100 84
#mc_tm_class = 1 tsetlin machine per klasse man har (win,loss,draw = 3 klasser)
#clause = clause. hvis gitt 85 clauses, kan velge fra 0-84
#ta = ukjent. Paavirker en posisjon i tsetlin automata

def GetBits(byte):
    bits = [0 for i in range(8)]
    for i in range(8):
        temp = 2**(7-i)
        if byte-temp < 0:
            continue
        else:
            byte = byte-temp
            bits[i] = 1
    return bits
#print(GetBits(130))

#non-negated
#plain
#Henter ut action for en gitt clause i en gitt klasse
def GetOutput(tm,tm_class,clause):
    output = []
    for i in range(84*2):
        outputbit = tm.ta_action(tm_class,clause,i)
        output.append(outputbit)
    return output

'''
det vi trodde:
1 2 3 4 5 6 7
8 9 10 11 12 1 2 3 4 5 6 7 8 9 10 11 12

det dataen var:
6 12
5 11
4 10
3 9
2 8
1 7
'''


def GetClauses(Ts,Clas,clauses):
    output = []
    for i in range(clauses):
        clause = GetOutput(Ts,Clas,i)
        action = TsUtil.ReadableClause(clause)
        output.append(action)
    return output

def PrintClause(clause):
    for i in clause:
        print(i)

def PrintClass(clauses):
    for i in clauses:
        PrintClause(i)
#------------------------------------------------------------
#t = MakeTestlin(5000, 35, 45,1)
#t = MakeTestlin(935, 5, 14.617627461915859,1)
#Sjekker en caluse mot ett brett
def CheckClause(clause,board):
    result = TsUtil.IsClauseTrue(clause,board)
    if result == "True":
        print("-----------")
        #print(result)
        bo = TsUtil.Readable(board)
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

def sortByKey(inp):
    return len(inp[2])

def sortByBit(inp):
    result = 0
    
    for i in inp:
        result += i
        
    return result

if __name__ == "__main__":
    ts = MakeTestlin(clauses,T,s,epochs)
    actions = GetClauses(ts[0],1,clauses)
    #print(actions[0])
    TsUtil.IsClauseTrue(GetOutput(ts[0],1,0),testing[0][0])
    #PrintClass(ts[0],1,clauses)
    #writefile = open("Clauses.txt","w)

    counter = -1
    clas = 1
    
    boards = []
    for i in range(1000):
        boards.append(TsUtil.AltRandomBoard())

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
            evaluation = TsUtil.IsClauseTrue(claus[0],board)
            if evaluation == "True":
                claus[2].append(board)
    
    #TotalClausesWScore.sort(key=sortByBit)
    
    ClausesDict = [[] for i in range(85)]
    for claus in TotalClausesWScore:
        bits = sortByBit(claus[0])
        ClausesDict[bits].append(claus)

    for i in ClausesDict:
        i.sort(key=sortByKey)
    
    Directory = "Clauses: " + str(clauses) + ", Threshold:" + str(T) + ", S: " + str(s) + ", Epochs: " + str(epochs)
    import os
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    counter = 0
    for i in ClausesDict[40:]:
        if len(i)>0:
            counter += len(i)
            directory = ""
            
            for bdb in i:
                String = "Bits Set: " + sortByBit(bdb[0]) + ", Type of Clause: " + bdb[1] + ", Boards: " + str(len(bdb[2]))
                open(Directory + "/" + String,"w")
                bord = TsUtil.ReadableClause(bdb[0])
                for row in bord:
                    print(row)
                print("-----------------------")

    print(counter)


    
    '''
    for i in TotalClausesWScore:
        counter += 1
        if counter%2 > 0:
            continue
        #PrintClause(TsUtil.ReadableClause(i[0]))
        
        for board in boards:
            evaluation = TsUtil.IsClauseTrue(i[0],board[0])
            result = -1
            
            if evaluation == "True":
                result = 1
            elif evaluation == "False":
                result = 0
            
            if result == board[1]:
                i[1] += 1
            else:
                i[1] -= 1 
        #break
        #CheckClauses(claus,testing)
        #print("---------------------------------------------")
    
    TotalClausesWScore.sort(key=sortByKey)
    print(TotalClausesWScore)
    print(len(TotalClausesWScore))
    print(counter)
    #print(TotalClausesWScore)
    '''


    #result = CrossValidation()
    #print(result)
    #print(result.mean())

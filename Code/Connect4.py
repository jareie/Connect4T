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

TrainX = np.array(training[0])
TrainY = np.array(training[1])

TestX = np.array(testing[0])
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
1 2 3 4 5 6 7 8 9 10 11 12 1 2 3 4 5 6 7 8 9 10 11 12

det dataen var:
6 12
5 11
4 10
3 9
2 8
1 7
'''


	
def ReadableClause(outClause):
    output = outClause

    nonNegated = output[:int(len(output)/2)]
    negated = output[int(len(output)/2):]
    
    tPlayer1 = TsUtil.Rearrange(nonNegated[:int(len(nonNegated)/2)])
    tPlayer2 = TsUtil.Rearrange(nonNegated[int(len(nonNegated)/2):])
    
    rPlayer1 = TsUtil.Rearrange(negated[:int(len(negated)/2)])
    rPlayer2 = TsUtil.Rearrange(negated[int(len(negated)/2):])
    
    #print(nonNegated)
    #print(negated)

    board = []

    for column in range(6):
        board.append([])
        for row in range(7):
            tp1 = tPlayer1[(column*7)+row]
            tp2 = tPlayer2[(column*7)+row]
            rp1 = rPlayer1[(column*7)+row]
            rp2 = rPlayer2[(column*7)+row]
            fail = (tp1 and rp1) or (tp2 and rp2)
            piece = ""
            if fail:
                piece = "f"
            elif rp1 and rp2:
                piece = "-"
            elif tp1 and tp2:
                piece = "*"
            elif tp1:
                piece = "X"
            elif rp1:
                piece = "x"
            elif tp2:
                piece = "O"
            elif rp2:
                piece = "o"
            else:
                piece = "_"
            board[column].append(piece)
    return board

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
#------------------------------------------------------------
#t = MakeTestlin(5000, 35, 45,1)
#t = MakeTestlin(935, 5, 14.617627461915859,1)

def CheckClauses(clause,boards):
    for i in range(len(boards[0])):
        #print(claus)
        result = TsUtil.IsClauseTrue(clause,boards[0][i])
        if result == "True":
            print(boards[1][i])
			print(result)
            bo = TsUtil.Readable(boards[0][i])
            for j in bo:
                print(j)
    
if __name__ == "__main__":
    ts = MakeTestlin(clauses,T,s,epochs)
    actions = GetClauses(ts[0],1,clauses)
    #print(actions[0])
    TsUtil.IsClauseTrue(GetOutput(ts[0],1,0),testing[0][0])
    #PrintClass(ts[0],1,clauses)
    #writefile = open("Clauses.txt","w)

    counter = 0
    clas = 1
    for i in range(clauses):
        claus = GetOutput(ts[0],clas,0)
        if counter%2 == 0:
            print("Class: " + str(clas) + ", Non-negated")
        else:
            print("Class: " + str(clas) + ", Negated")
        PrintClause(ReadableClause(claus))
        CheckClauses(claus,testing)
        print("---------------------------------------------")
            


    #result = CrossValidation()
    #print(result)
    #print(result.mean())

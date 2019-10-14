from pyTsetlinMachine.tm import MultiClassTsetlinMachine
import numpy as np
#import random
import TsUtil

dataPath = "Data/"
#------------------------------------------------------------
print("Getting Data")

#training = TsUtil.LoadFile("trainingdata.txt")
#testing = TsUtil.LoadFile("testdata.txt")

training = TsUtil.LoadFile(dataPath + "DataTraining.data")
testing = TsUtil.LoadFile(dataPath + "DataTest.data")
print(str(len(training[0])) + " entries")    

TrainX = np.array(training[0])
TrainY = np.array(training[1])

TestX = np.array(testing[0])
TestY = np.array(testing[1])

#------------------------------------------------------------
print("Setting Up Machine")
clauses = 85
T = 15
s = 3.9

epochs = 1

def MakeTestlin(Clauses,t,S,Epochs):
    tm = MultiClassTsetlinMachine(Clauses,t,S,boost_true_positive_feedback=0)
    #tm = MultiClassTsetlinMachine(100,10,4.45)
    #tm.fit(TrainX,TrainY,epochs=10)
    #print("Accuracy:", 100*(tm.predict(TestX) == TestY).mean())
    result = 0
    print("Training")
    for i in range(Epochs):
        tm.fit(TrainX, TrainY, epochs=1)
        result = 100*(tm.predict(TestX) == TestY).mean()
        print("Accuracy: ", result)
    return (tm,result)


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

def GetAction(tm,tm_class,clause):
    output = GetOutput(tm,tm_class,clause)

    nonNegated = output[:int(len(output)/2)]
    negated = output[int(len(output)/2):]
    
    tPlayer1 = nonNegated[:int(len(nonNegated)/2)]
    tPlayer2 = nonNegated[int(len(nonNegated)/2):]
    
    rPlayer1 = negated[:int(len(negated)/2)]
    rPlayer2 = negated[int(len(negated)/2):]
    
    print(nonNegated)
    print(negated)

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

#------------------------------------------------------------
#t = MakeTestlin(5000, 35, 45,1)
t = MakeTestlin(935, 5, 14.617627461915859,1)

print(t)
#action = GetAction(t[0],0,0)
#for i in action:
#    print(i)
for clause in range(935):
    action = GetAction(t[0],0,clause)
    for i in action:
        print(i)
#for i in range(935):
#    action.append(GetOutput(t[0],0,i))
#print("-----------------------------------")
#for i in action:
#    for j in i:
#        print(j)
#    print("-----------------------------------")
#print(action)

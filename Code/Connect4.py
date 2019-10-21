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
def Rearrange(WrongList):
	output = []
	for column in range(6):
		for row in range(7):
			#index = (6*i)+(6-j)
			temp = 6-column
			index = (6*row)+temp
			output.append(WrongList[index-1])
	return output

	
def ReadableClause(tm,tm_class,clause):
    output = GetOutput(tm,tm_class,clause)

    nonNegated = output[:int(len(output)/2)]
    negated = output[int(len(output)/2):]
    
    tPlayer1 = Rearrange(nonNegated[:int(len(nonNegated)/2)])
    tPlayer2 = Rearrange(nonNegated[int(len(nonNegated)/2):])
    
    rPlayer1 = Rearrange(negated[:int(len(negated)/2)])
    rPlayer2 = Rearrange(negated[int(len(negated)/2):])
    
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

def PrintClause(clause):
    for i in clause:
        print(i)

def PrintClass(Ts,Clas,clauses):
    for i in range(clauses):
        action = ReadableClause(Ts,Clas,i)
        PrintClause(action)
#------------------------------------------------------------
#t = MakeTestlin(5000, 35, 45,1)
#t = MakeTestlin(935, 5, 14.617627461915859,1)

if __name__ == "__main__":
    ts = MakeTestlin(clauses,T,s,epochs)
    PrintClass(ts[0],1,clauses)

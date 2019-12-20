
import numpy as np
#import random
import TsUtil
import GeneralUtil
import DataUtil

#regne ut antall bit for 
#forst kommer posisjon for vinduet, saa kommer vinduet som er 4,4,2 * 2
variables = GeneralUtil.LoadCfg("Config.cfg")
dataPath = variables["General"]["DataPath"]
trainPl = variables["General"]["TrainingData"]
testPl = variables["General"]["TestingData"]

convolutional = variables["Connect4"]["Convolutional"]
parallel = variables["Connect4"]["Parallel"]
CrossVal = variables["General"]["CrossEvaluation"]
FindClauses = variables["General"]["FindClauses"]

#print(variables)
#------------------------------------------------------------
print("Getting Data")

#training = TsUtil.LoadFile("trainingdata.txt")
#testing = TsUtil.LoadFile("testdata.txt")

training = DataUtil.LoadFile(dataPath + trainPl)
testing = DataUtil.LoadFile(dataPath + testPl)
print(str(len(training[0])) + " entries")    


TrainX = np.array(TsUtil.ReshapeData(training[0], convolutional))
TrainY = np.array(training[1])

TestX = np.array(TsUtil.ReshapeData(testing[0], convolutional))
TestY = np.array(testing[1])

#------------------------------------------------------------
print("Setting Up Machine")
clauses = int(variables["Connect4"]["Clause"])
T = variables["Connect4"]["T"]
s = variables["Connect4"]["S"]

epochs = int(variables["Connect4"]["epochs"])

WindowX = int(variables["Connect4"]["WindowX"])
WindowY = int(variables["Connect4"]["WindowY"])

if convolutional:
    if parallel:
        from pyTsetlinMachineParallel.tm import MultiClassConvolutionalTsetlinMachine2D as TM
    else:
        from pyTsetlinMachine.tm import MultiClassConvolutionalTsetlinMachine2D as TM
else:
    if parallel:
        from pyTsetlinMachineParallel.tm import MultiClassTsetlinMachine as TM
    else:
        from pyTsetlinMachine.tm import MultiClassTsetlinMachine as TM

def MakeTestlin(Clauses,t,S,Epochs):
    def GetMachine():
        if convolutional:
            return TM(Clauses, t, S, (WindowX, WindowY), weighted_clauses=True, boost_true_positive_feedback=0)
        else:
            return TM(Clauses, t, S, weighted_clauses=True, boost_true_positive_feedback=0)
        
    tm = GetMachine()

    #tm = MultiClassTsetlinMachine(100,10,4.45)
    #tm.fit(TrainX,TrainY,epochs=10)
    #print("Accuracy:", 100*(tm.predict(TestX) == TestY).mean())
    result = 0
    print("Training: Clauses=" + str(Clauses) + ", T=" + str(t)+ ", S=" + str(S))
    for i in range(Epochs):
        tm.fit(TrainX, TrainY, epochs=1, incremental=True)
        result = 100*(tm.predict(TestX) == TestY).mean()
        print(str(i) + " Accuracy: ", result)
    return (tm,result)

def CrossValidation():
    datasets = DataUtil.GenerateKFoldSet(dataPath + trainPl,dataPath + testPl)
    results = []
    for sets in datasets:
        print("Making Tsetlin Machine for new set")
        def GetMachine():
            if convolutional:
                return TM(clauses, T, s, (WindowX, WindowY), weighted_clauses=True, boost_true_positive_feedback=0)
            else:
                return TM(clauses, T, s, weighted_clauses=True, boost_true_positive_feedback=0)
        
        tm = GetMachine()
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
        
        inbetweenResults = []
        for i in range(epochs):
            tm.fit(np.array(TsUtil.ReshapeData(TrainX, convolutional)),np.array(TrainY),epochs=1,incremental=True)
            result = 100*(tm.predict(np.array(TsUtil.ReshapeData(TestX, convolutional))) == np.array(TestY)).mean()
            inbetweenResults.append(result)
            print(" " + str(result))
        results.append(inbetweenResults)
    return results

def RunCrossWWrite():
    resFile = open("Data/CorssvalidationResult.txt","w")
    results = CrossValidation()
    for row in results:
        string = ""
        for ind in row:
            string += str(ind) + ", "
        string += "\n"
        resFile.write(string)
    resFile.close()

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



#------------------------------------------------------------
#t = MakeTestlin(5000, 35, 45,1)
#t = MakeTestlin(935, 5, 14.617627461915859,1)

if __name__ == "__main__":
    if CrossVal:
        RunCrossWWrite()
    elif FindClauses:
        ts = MakeTestlin(clauses,T,s,epochs)
        TsUtil.Clauses(clauses,ts,T,s,epochs)
    else:
        ts = MakeTestlin(clauses,T,s,epochs)

    

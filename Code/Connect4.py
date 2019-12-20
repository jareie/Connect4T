
import numpy as np
#import random
import TsUtil
import GeneralUtil
import DataUtil

#Get config parameters
variables = GeneralUtil.LoadCfg("Config.cfg")
dataPath = variables["General"]["DataPath"]
trainPl = variables["General"]["TrainingData"]
testPl = variables["General"]["TestingData"]

#paramteres for deciding what version of the Tsetlin Machine
#and what the pro gram should do
convolutional = variables["Connect4"]["Convolutional"]
parallel = variables["Connect4"]["Parallel"]
CrossVal = variables["General"]["CrossEvaluation"]
FindClauses = variables["General"]["FindClauses"]


#------------------------------------------------------------
print("Getting Data")

#Load the data
training = DataUtil.LoadFile(dataPath + trainPl)
testing = DataUtil.LoadFile(dataPath + testPl)
print(str(len(training[0])) + " entries")    

#Transform the data to correct form
TrainX = np.array(TsUtil.ReshapeData(training[0], convolutional))
TrainY = np.array(training[1])

TestX = np.array(TsUtil.ReshapeData(testing[0], convolutional))
TestY = np.array(testing[1])

#------------------------------------------------------------
print("Setting Up Machine")
#Get parameters for Tsetlin Machine
clauses = int(variables["Connect4"]["Clause"])
T = variables["Connect4"]["T"]
s = variables["Connect4"]["S"]

epochs = int(variables["Connect4"]["epochs"])

WindowX = int(variables["Connect4"]["WindowX"])
WindowY = int(variables["Connect4"]["WindowY"])

#Set up the appropriate library
#allows easy reuse of other code
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

#Creates a Tsetlin Machine based on the hyper-parameters, version. And trains it on the data.
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

#Cross validaiont function. uses other helper functions to generate the sets it is to test the crewated machine on
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

#Runs the cross validation and writes the reults to a file
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

#Deprecated function that was supposed to help bet bits fdrom a byte of data
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



#------------------------------------------------------------

#Main
if __name__ == "__main__":
    if CrossVal:
        RunCrossWWrite()
    elif FindClauses:
        ts = MakeTestlin(clauses,T,s,epochs)
        TsUtil.ClausesTestData(ts,TestX,TestY,clauses)
        #TsUtil.Clauses(clauses,ts,T,s,epochs)
        #TsUtil.ClausesPattern(ts,clauses)
    else:
        ts = MakeTestlin(clauses,T,s,epochs)

    

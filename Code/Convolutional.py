
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
        temp = np.reshape(NewTrainXEntry,(2,6,7))
        output.append(temp)
    return output

TrainX = np.array(ReshapeData(training[0]))
TrainY = np.array(training[1])

TestX = np.array(ReshapeData(testing[0]))
TestY = np.array(testing[1])
#print(np.zeros((2,3,2)))

#TrainX[0].shape = (6,7,2)


#Rearange test
'''
print(TsUtil.Rearrange([
    1,2,3,4,5,6,7,
    8,9,10,11,12,13,14,
    15,16,17,18,19,20,21,
    22,23,24,25,26,27,28,
    29,30,31,32,33,34,35,
    36,37,38,39,40,41,42
]))'''


import sys
sys.exit(1)

#------------------------------------------------------------
from pyTsetlinMachine.tm import MultiClassConvolutionalTsetlinMachine2D
print("Setting Up Machine")
clauses = int(variables["Connect4"]["Clause"])
T = variables["Connect4"]["T"]
s = variables["Connect4"]["S"]

epochs = int(variables["Connect4"]["epochs"])


ctm = MultiClassConvolutionalTsetlinMachine2D(40, 60, 3.9, (2, 2), boost_true_positive_feedback=0)

ctm.fit(TrainX, TrainY, epochs=5000)

print("Accuracy:", 100*(ctm.predict(TestX) == TestY).mean())
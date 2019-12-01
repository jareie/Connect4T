from pyTsetlinMachine.tm import MultiClassConvolutionalTsetlinMachine2D
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


ctm = MultiClassConvolutionalTsetlinMachine2D(40, 60, 3.9, (2, 2), boost_true_positive_feedback=0)

ctm.fit(TrainX, TrainY, epochs=5000)

print("Accuracy:", 100*(ctm.predict(TestX) == TestY).mean())
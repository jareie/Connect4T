import numpy as np

import DataUtil
import TsUtil
import GeneralUtil

variables = GeneralUtil.LoadCfg("Config.cfg")
dataPath = variables["General"]["DataPath"]
trainPl = variables["General"]["TrainingData"]
testPl = variables["General"]["TestingData"]

from sklearn.naive_bayes import CategoricalNB
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import LinearSVC

def GetLearningAutomata(typeOfAutomata):
    if typeOfAutomata == "Categorical":
        return CategoricalNB()
    elif typeOfAutomata == "Gaussian":
        return GaussianNB()
    elif typeOfAutomata == "DecisionTree":
        return DecisionTreeClassifier()
    elif typeOfAutomata == "LinearSVC":
        return LinearSVC()

def CrossValidation(typeOfAutomata):
    datasets = DataUtil.GenerateKFoldSet(dataPath + trainPl,dataPath + testPl)
    results = []
    for sets in datasets:
        print("Making for new set")
        tm = GetLearningAutomata(typeOfAutomata)
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

        TrainX = np.array(TsUtil.ReshapeData(TrainX, False))
        TrainY = np.array(TrainY)

        TestX = np.array(TsUtil.ReshapeData(TestX, False))
        TestY = np.array(TestY)
        inbetweenResults = []

        tm.fit(TrainX,TrainY)
        #result = 100*(tm.predict(np.array(TsUtil.ReshapeData(TestX, False))) == np.array(TestY)).mean()
        result = tm.score(TestX,TestY)*100
        inbetweenResults.append(result)
        print(" " + str(result))
        results.append(inbetweenResults)
    return results

results = []

results.append(("Categorical",CrossValidation("Categorical")))
results.append(("Gaussian",CrossValidation("Gaussian")))
results.append(("DecisionTree",CrossValidation("DecisionTree")))
results.append(("LinearSVC",CrossValidation("LinearSVC")))

Directory = "Data/Automata"
import os
if not os.path.exists(Directory):
    os.makedirs(Directory)

String = "Results"
outFile = open(Directory + "/" + String,"w")

for sets in results:
    WriteString = sets[0] + "\n"

    Average = 0.0
    for i in sets[1]:
        WriteString += str(i[0]) + ", "
        print(i[0])
        Average += i[0]
    Average = Average/10
    WriteString += str(Average) + "\n\n"
    outFile.write(WriteString)
outFile.close()
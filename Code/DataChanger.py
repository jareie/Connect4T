import random
import GeneralUtil as gti

variables = gti.LoadCfg("Config.cfg")

TestPl = variables["General"]["TestingData"]
TrainPl = variables["General"]["TrainingData"]
DataPath = variables["General"]["DataPath"]
ratio = variables["DataChanger"]["ratio"]
shuffleData = variables["DataChanger"]["shuffledata"]
dataPt = variables["DataChanger"]["data"]


def ProccesData(UData):
    Replacement = []
    for i in UData:
        test = i.replace("\n","")
        Replacement.append(test)
    
    #print(Replacement[0:10])
    
    Final = []
    for i in Replacement:
        test = i.split(",")
        Final.append(test)

    return Final

unProccesedData = open(DataPath + dataPt).readlines()
data = ProccesData(unProccesedData)
BitsData = []

wins = []
loss = []
draws = []


for line in data:
    Player1 = [0 for i in range(42)]
    Player2 = [0 for i in range(42)]
    for i in range(len(line)-1):
        if line[i] == "x":
            Player1[i] = 1
        elif line[i] == "o":
            Player2[i] = 1
    
    temp = line[len(line)-1]
    NewFormat = Player1 + Player2

    if temp == "win":
        wins.append((NewFormat,1))
    elif temp == "loss":
        loss.append((NewFormat,0))
    else:
        draws.append((NewFormat,2))

def Hexify(Bits):
    HexString = ""
    for i in range(24):
        #AHex = 
        for j in range(4):
            print(i)
    return

if shuffleData:
    random.shuffle(wins)
    random.shuffle(loss)
    random.shuffle(draws)

training = wins[:int(len(wins)*ratio)] + loss[:int(len(loss)*ratio)] + draws[:int(len(draws)*ratio)]
testing = wins[int(len(wins)*ratio):] + loss[int(len(loss)*ratio):] + draws[int(len(draws)*ratio):]

random.seed(0)
random.shuffle(training)
random.shuffle(testing)
random.seed(None)

WriteTrFile = open(DataPath + TrainPl,"w")
WriteTeFile = open(DataPath + TestPl,"w")

for data in training:
    String = ""
    for i in data[0]:
        String += str(i) + ","
    String += str(data[1]) + "\n"
    WriteTrFile.write(String)

for data in testing:
    String = ""
    for i in data[0]:
        String += str(i) + ","
    String += str(data[1]) + "\n"
    WriteTeFile.write(String)

WriteTrFile.close()
WriteTeFile.close()
print("Files written")
#84 bits
#print(data[0:10])

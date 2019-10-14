import random

ratio = 0.9
shuffleData = True

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

unProccesedData = open("connect-4.data").readlines()
data = ProccesData(unProccesedData)
BitsData = []

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
        BitsData.append((NewFormat,1))
    elif temp == "loss":
        BitsData.append((NewFormat,0))
    else:
        BitsData.append((NewFormat,2))

def Hexify(Bits):
    HexString = ""
    for i in range(24):
        #AHex = 
        for j in range(4):
            print(i)
    return

if shuffleData:
    random.shuffle(BitsData)

training = BitsData[:int(len(BitsData)*ratio)]
testing = BitsData[int(len(BitsData)*ratio):]

WriteTrFile = open("DataTraining.data","w")
WriteTeFile = open("DataTest.data","w")

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
#84 bits
#print(data[0:10])

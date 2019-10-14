import Connect4 as Tsm
import random

sizePop = 2
epochs = 2
keepMultiplier = 0.9

heldGenes = []

def Gene():
    #Clause, T, s
    return [random.randint(1,1000),random.randint(1,100),random.uniform(1,50)]

def DNA(amount):
    if not amount % 2 == 0:
        amount = amount+1
        print("Added to the amount")
    return [Gene() for i in range(amount)]

def SameGene(gene1,gene2):
    for i in range(len(gene1)):
        if not gene1[i] == gene2[i]:
            return False
    return True

def RemoveScoring(inpList):
    output = []
    for i in inpList:
        output.append(i[0])
    return output

def RateGene(gene):
    out = Tsm.MakeTestlin(gene[0],gene[1],gene[2],1)
    machine = out[0]
    score = out[1]
    return (gene,machine,score)

def RateDNA(dna):
    scoreList = []
    for i in dna:
        rating = RateGene(i)
        scoreList.append(rating)
    return scoreList

def Mix(a,b):
    index1 = random.randint(0,len(a)-1)
    index2 = random.randint(index1,len(a)-1)
    new1 = a[0][:index1] + b[0][index1:index2] + a[0][index2:]
    new2 = b[0][:index1] + a[0][index1:index2] + b[0][index2:]
    return [new1,new2]

def Pairings(dna):
    dnaCopy = dna[:]
    random.shuffle(dnaCopy)
    list1 = dnaCopy[:int(len(dnaCopy)/2)]
    list2 = dnaCopy[int(len(dnaCopy)/2):]

    newGenes = []
    for i in range(len(list1)):
        temp = Mix(list1[i],list2[i])
        newGenes.extend(temp)
    return newGenes

def NewSort(gene):
    for i in heldGenes:
        if SameGene(gene[0],i[0]):
            return i[1]/i[2]

def SortVal(list):
    return list[2]

def HeldGeneAdd(listOfGenes):
    for i in listOfGenes:
        exists = False
        for j in heldGenes:
            if SameGene(i[0],j[0]):
                exists = True
                j[1] += i[2]
                j[2] += 1
                break
        if not exists:
            heldGenes.append([i[0],i[2],1])

def Generation(listOfGenes):
    newDNA = Pairings(listOfGenes)
    print(newDNA)
    newList = listOfGenes + RateDNA(newDNA)
    HeldGeneAdd(newList)
    newList.sort(key=NewSort)
    print(newList)
    print("--------------------------------")
    return newList[int(len(newList)/2):]


print("--------------------------------")

genes = RateDNA(DNA(sizePop))
print(genes)

for i in range(epochs):
    genes = Generation(genes)
    if SameGene(genes[0][0],genes[len(genes)-1][0]):
        print("New Pool")
        temp = RateDNA(DNA(int(len(genes)*keepMultiplier)))
        genes = genes[int(len(genes)*keepMultiplier):] + temp

fi = open("Result.txt","w")
for i in genes:
    string = ""
    for j in i[0]:
        string += str(j) + ", "
    string += "accuracy: "
    string += str(i[2])
    string += "\n"
    fi.write(string)
fi.close()


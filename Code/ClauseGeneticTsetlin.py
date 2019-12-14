import Connect4 as Tsm
import random
import TsUtil as uti

variables = uti.LoadCfg("Config.cfg")

sizePop = int(variables["GeneticTsetlin"]["sizePop"])
epochs = int(variables["GeneticTsetlin"]["epochs"])
keepMultiplier = variables["GeneticTsetlin"]["amountKeep"]

Clauses = int(variables["ClauseGeneticTsetlin"]["clauses"])

heldGenes = []

def GetTAndS(clause,bits):
    Tbits = bits[:int(len(bits)/2)]
    sbits = bits[int(len(bits)/2):]
    T = 0
    s = 0
    RangeBitsT = len(Tbits)
    for i in range(RangeBitsT):
        if Tbits[i] == 1:
            T += (2**((RangeBitsT-1)-i))

    RangeBitsS = len(sbits)    
    for i in range(RangeBitsS):
        if sbits[i] == 1:
            s += (2**((RangeBitsS-1)-i))
    return [clause,T,s]

def Gene():
    #T, s
    return [random.randint(0,1) for i in range(8*2)]

def DNA(amount):
    if not amount % 2 == 0:
        amount = amount+1
        print("Added to the amount")
    return [Gene() for i in range(amount)]

def SameGene(gene1,gene2):
    print(gene1)
    print(gene2)
    for i in range(len(gene1)):
        if not gene1[i] == gene2[i]:
            return False
    return True

def InHeldGenes(Gene):
    for i in range(len(heldGenes)):
        if SameGene(heldGenes[i][0],Gene):
            return i
    return -1

def RateGene(gene):
    index = InHeldGenes(gene)
    if index > -1:
        score = heldGenes[index][1]
        return (gene,score)
    
    temp = GetTAndS(Clauses,gene)
    out = Tsm.MakeTestlin(temp[0],temp[1],temp[2],5)
    score = out[1]
    return (gene,score)

import Proccessing as ps
def RateMulti(dna):
    scoreList = ps.MakeWorkers(RateGene,dna)
    return scoreList
    

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

def RemoveScoring(inpList):
    output = []
    for i in inpList:
        output.append(i[0])
    return output

def NewSort(gene):
    for i in heldGenes:
        if SameGene(gene[0],i[0]):
            return i[1]/i[2]

def SortVal(list):
    return list[1]

def HeldGeneAdd(listOfGenes):
    for i in listOfGenes:
        exists = False
        for j in heldGenes:
            if SameGene(i[0],j[0]):
                exists = True
                j[1] += i[1]
                j[2] += 1
                break
        if not exists:
            heldGenes.append([i[0],i[1],1])

def HeldGeneNoScoreAdd(listOfGenes):
    for i in listOfGenes:
        exists = False
        for j in heldGenes:
            if SameGene(i[0],j[0]):
                exists = True
                break
        if not exists:
            heldGenes.append([i[0],i[1],1])

def Generation(listOfGenes):
    newDNA = Pairings(listOfGenes)
    newList = listOfGenes + RateMulti(newDNA)
    HeldGeneNoScoreAdd(newList)
    newList.sort(key=SortVal)
    print(newList)
    print(len(newList))
    print("--------------------------------")
    return newList[int(len(newList)/2):]

if __name__ == "__main__":
    print("--------------------------------")
    genes = RateMulti(DNA(sizePop))
    print(genes)

    for i in range(epochs):
        print("Percent Complete: " + str(((i+1)/epochs)*100))
        genes = Generation(genes)
        if SameGene(genes[0][0],genes[len(genes)-1][0]):
            print("New Pool")
            temp = RateDNA(DNA(int(len(genes)*keepMultiplier)))
            genes = genes[int(len(genes)*keepMultiplier):] + temp


    fi = open(variables["General"]["DataPath"] + "Result.txt","w")
    for i in genes:
        string = ""
        ts = GetTAndS(i[0])
        for j in ts:
            string += str(j) + ", "
        string += "accuracy: "
        string += str(i[2])
        string += "\n"
        fi.write(string)
    fi.close()


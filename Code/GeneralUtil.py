def ConvertToInt(liste):
    product = []
    for i in liste:
        product.append(int(i))
    return product

def LoadCfg(FileName):
    print("Getting Config File")
    config = open("Config.cfg","r")
    rawInfo = config.readlines()
    config.close()
    Info = {}
    category = []

    for i in rawInfo:
        temp = i.replace(" ","")
        temp = temp.replace("\n","")
        if temp.find("#") >= 0:
            continue
        if temp == "":
            continue
        if temp[0] == "-":
            ctg = temp.replace("-","")
            category.append(ctg)
            Info[ctg] = {}
        else:
            inf = temp.split("=")
            #print(inf,inf[0])
            if inf[1].find('"') < 0:
                try:
                    if inf[1] == "True":
                        inf[1] = True
                    elif inf[1] == "False":
                        inf[1] = False
                    else:
                        inf[1] = float(inf[1])
                except Exception:
                    print("Failed: " + inf[1])
            else:
                inf[1] = inf[1].replace('"',"")
            Info[category[len(category)-1]][inf[0]] = inf[1]
        #print(category)

    return Info


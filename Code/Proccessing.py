from multiprocessing import Pool

def MakeWorkers(function,argumentList):
    pool = Pool(processes=3)
    result = pool.map(function,argumentList)
    return result

if __name__ == "__main__":
    print("Settup complete")
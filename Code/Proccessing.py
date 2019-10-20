from multiprocessing import Pool

def MakeWorkers(function,argumentList):
    pool = Pool(processes=3)
    pool.map(function,argumentList)

if __name__ == "__main__":
    print("Settup complete")
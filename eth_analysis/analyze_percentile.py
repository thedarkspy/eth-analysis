import numpy as np
import os
import json 

blocksDir = "../blocks_new"
resultsDir = "../results/"

def getBlockNum(blockFile):
    return blockFile.split('.')[0]

def getBlockTransactions(dirEntry, blockFile):
    with open(os.path.join(dirEntry, blockFile), "r") as reader:
        return json.load(reader)

def getGasPriceList(transactions):
    return list(map( lambda x : x['gasPrice'], transactions))

def getNthPercentile(gasPriceList, n):
    return np.percentile(gasPriceList, n)

def etherValue(gasValue):
    return round(gasValue/pow(10, 9), 7)

def calculateAbsoluteLoss(transactions):
    absoluteLoss = 0
    for i in range(0, len(transactions)):
        # absolute loss by summing all transction fees
        absoluteLoss = absoluteLoss + transactions[i]['gasUsed']*transactions[i]['gasPrice'] 
    
    return etherValue(absoluteLoss) 

def calculateLossAtPercentile(transactions, gasPercentile):
    gasUsed = 0
    ceilingLoss = 0
    for i in range(len(transactions) - 1, -1, -1):
        # tracking gas used up to Nth percentile                             
        gasUsed = gasUsed + transactions[i]['gasUsed']
        if transactions[i]['gasPrice']  >= gasPercentile:

            # loss at Nth percentile
            ceilingLoss = gasUsed*transactions[i]['gasPrice']
            break

    return etherValue(ceilingLoss)

def main():
    with os.scandir(blocksDir) as rootDir:
        for dirEntry in rootDir:
            if dirEntry.is_dir():
                for blockFile in os.listdir(dirEntry): 
                    if blockFile.endswith(".json"):
                        blockNum = getBlockNum(blockFile)  
                        print("Calculating loss for block: " + blockNum)
                        block_stats = {}
                        block_stats['blockNum'] = blockNum

                        transactions = getBlockTransactions(dirEntry, blockFile)
                        block_stats['absoluteLoss'] = calculateAbsoluteLoss(transactions)

                        gasPrices = getGasPriceList(transactions)
                        for i in range(1, 100):
                            nthPercentile = getNthPercentile(gasPrices, i)
                            block_stats['ceilingLossAtPercentile'] = calculateLossAtPercentile(transactions, nthPercentile)
                            with open(resultsDir + str(i) + '.json', 'a') as writer:
                                writer.write(json.dumps(block_stats) + '\n')

if __name__ == "__main__":
    main()

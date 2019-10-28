import matplotlib.pyplot as plt 
import json
import statistics
import random

resultsDir = '../results/'
blocks = {}

for i in [20,40,60,80]:
    with open(resultsDir + str(i) + '.json', 'r') as reader:
        data = []
        j = 0
        for line in reader.readlines():
            if j == 1000:
                break
            entry = json.loads(line)
            data.append((entry['blockNum'],entry['ceilingLossAtPercentile']))
            j = j + 1
        
        plt.plot([x[0] for x in data],[x[1] for x in data], label=str(i) + 'Nth Percentile')

        # data.sort(key=lambda x : x['blockNum'], reverse=True)
        # blocks = list(map(lambda x : x['blockNum'], data))
        # cost = list(map(lambda x : x['ceilingLossAtPercentile'], data)) 
    # plt.bar(i, median, align='center', width=5) 

plt.legend(loc=1)
plt.xlabel('Blocks #') 
plt.ylabel('Loss (ETH)') 
# plt.title('')
plt.xticks([])
plt.savefig('test.png')


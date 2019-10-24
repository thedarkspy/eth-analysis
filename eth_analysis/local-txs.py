import time

from web3 import Web3
from tqdm import tqdm
from json import dump, dumps,loads
from os import getcwd, mkdir, listdir
from os.path import isfile


blocks_path = "../blocks_new/"
max_files_in_dir = 5000
files_in_dir = 0
current_dir = 0

try:
    mkdir(blocks_path + str(current_dir))
except OSError:
    print('Failed to create directory %s' % blocks_path + str(current_dir))
else:
    print('Created directory %s successfully' % blocks_path + str(current_dir))

web3 = Web3(Web3.IPCProvider("~/Library/Ethereum/geth.ipc"))
start_block = 4220000
end_block = 4330000

for index in tqdm(range(start_block, end_block + 1)):
    txs = web3.eth.getBlock(index, True)['transactions']
    if len(txs) > 0:
        filtered_txs = []
        for tx in txs:
            receipt = web3.eth.getTransactionReceipt(tx['hash'])
            if receipt is not None:
                tx_item = {}
                tx_item['hash'] = tx['hash'].hex()
                tx_item['gasPrice'] = tx['gasPrice']/pow(10, 9)
                tx_item['gas'] = tx['gas']
                tx_item['gasUsed'] = receipt['gasUsed']
                filtered_txs.append(tx_item)
        filtered_txs.sort(key=lambda x: x['gasUsed'], reverse=True)

        with open(blocks_path + str(current_dir) + '/' + str(index) + '.json', 'w') as fwriter:
            dump(filtered_txs, fwriter)   

        files_in_dir = files_in_dir + 1
        if files_in_dir == max_files_in_dir:
            files_in_dir = 0
            current_dir = current_dir + 1
            try:
                mkdir(blocks_path + str(current_dir))
            except OSError:
                print('Failed to create directory %s' % blocks_path)
            else:
                print('Created directory %s successfully' % blocks_path)
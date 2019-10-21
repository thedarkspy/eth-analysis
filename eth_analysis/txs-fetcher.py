from tqdm import tqdm
from json import dump, dumps,loads
from time import sleep
from os import getcwd, mkdir, listdir
from os.path import isfile
from requests import HTTPError
from etherscan.proxies import Proxies

blocks_path = "../blocks/"
max_files_in_dir = 5000
files_in_dir = 0
current_dir = 12

sleep_time = 0.2
first_block_num = 4650000
last_block_num = 4825000

with open('api_key.json', mode='r') as key_file:
    key = loads(key_file.read())['key']
api = Proxies(api_key=key)

try:
    mkdir(blocks_path + str(current_dir))
except OSError:
    print('Failed to create directory %s' % blocks_path + str(current_dir))
else:
    print('Created directory %s successfully' % blocks_path + str(current_dir))

print("Downloading transactions for blocks: {} to {}".format(first_block_num, last_block_num))
for i in tqdm(range(4708444, last_block_num + 1)):
    try:
        block = api.get_block_by_number(i)
        minified_txs = []
        for tx in block['transactions']:
            tx_item = {}
            tx_item['hash'] = tx['hash']
            tx_item['gas'] = int(tx['gas'], 16)
            tx_item['gasPrice'] = int(tx['gasPrice'], 16)/pow(10, 9)
            minified_txs.append(tx_item)
        minified_txs.sort(key=lambda x: x['gasPrice'], reverse=True)

        with open(blocks_path + str(current_dir) + '/' + str(i) + '.json', 'w') as fwriter:
            dump(minified_txs, fwriter)  

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
        
        sleep(sleep_time)

    except HTTPError as err:
        print(err.response.text)
        print('Block nmuber %d' % i)
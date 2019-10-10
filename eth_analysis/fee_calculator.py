from web3 import Web3 

web3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/62d37c37f64a4703a8a7394e616b4166"))

block = web3.eth.getBlock('latest')

print(block)
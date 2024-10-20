from brownie import accounts, network, config, MockV3Aggregator
from web3 import Web3
from brownie.network import gas_price
from brownie.network.gas.strategies import LinearScalingStrategy

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ['development', 'ganache-local']
FORKED = ['mainnet-fork', 'mainnet-fork-dev']

#gas_strategy = LinearScalingStrategy("60 gwei", "70 gwei", 1.1)
#gas_price(gas_strategy)

DECIMALS = 18
STARTING_PRICE = 2000

def get_account():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS or network.show_active() in FORKED:
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])
    
def deploy_mocks():
    if len(MockV3Aggregator) <= 0: 
            #MockV3Aggregator.deploy(DECIMALS, Web3.to_wei(STARTING_PRICE, "ether"), {"from":get_account(), "gas_price": gas_strategy})
            MockV3Aggregator.deploy(DECIMALS, Web3.to_wei(STARTING_PRICE, "ether"), {"from":get_account()})